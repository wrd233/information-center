from __future__ import annotations

import re
import time as monotonic_time
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.batch_runner import RSSBatchRunner
from app.config import settings
from app.models import ContentAnalyzeRequest, RSSAnalyzeRequest, RSSBatchAnalyzeRequest
from app.models import RSSSourceCreateRequest, RSSSourceIngestRequest, RSSSourceUpdateRequest
from app.processor import normalize_content, process_content_thread_safe
from app.rss import parse_feed
from app.rss_errors import classify_exception, error_payload, error_response, retryable_for
from app.rss_runner import analyze_one_rss_source
from app.screener import audit_screen_content, configure_llm_dump, reconfigure_llm_semaphore, reconfigure_screening_mode
from app.storage import InboxStore


app = FastAPI(title="content-inbox", version="0.1.0")
store = InboxStore(settings.database_path)


def get_store() -> InboxStore:
    return store


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "database_path": str(settings.database_path),
        "ai_configured": bool(settings.openai_api_key and settings.ai_enabled),
        "embedding_configured": bool(settings.embedding_api_key()),
        "sqlite_vec_available": store.vec_available,
        "config": {
            "llm_model": settings.llm.get("model"),
            "embedding_model": settings.embedding.get("model"),
            "prompt_version": settings.prompt_version,
            "llm_max_concurrency": int(settings.llm.get("max_concurrency", 2)),
            "screening_mode": settings.screening.get("mode", "two_stage"),
        },
    }


class LLMConcurrencyRequest(BaseModel):
    max_concurrency: int = Field(ge=1, le=32)


@app.post("/api/runtime/llm-concurrency")
def set_llm_concurrency(payload: LLMConcurrencyRequest) -> dict[str, Any]:
    try:
        new_value = reconfigure_llm_semaphore(payload.max_concurrency)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "ok": True,
        "llm_max_concurrency": new_value,
    }


class ScreeningModeRequest(BaseModel):
    mode: str


@app.post("/api/runtime/screening-mode")
def set_screening_mode(payload: ScreeningModeRequest) -> dict[str, Any]:
    try:
        new_mode = reconfigure_screening_mode(payload.mode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "ok": True,
        "screening_mode": new_mode,
    }


@app.post("/api/rss/sources")
def create_rss_source(
    payload: RSSSourceCreateRequest, inbox_store: Annotated[InboxStore, Depends(get_store)]
) -> JSONResponse:
    try:
        source, created = inbox_store.create_rss_source(payload.model_dump())
    except ValueError as exc:
        return error_response(
            "source_conflict",
            str(exc),
            status_code=409,
            source_id=payload.source_id,
            feed_url=payload.feed_url,
        )
    return JSONResponse({"ok": True, "source": source, "created": created})


@app.get("/api/rss/sources")
def list_rss_sources(
    status: str | None = None,
    category: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    inbox_store: Annotated[InboxStore, Depends(get_store)] = store,
) -> dict[str, Any]:
    sources, stats = inbox_store.list_rss_sources(
        {"status": status, "category": category, "limit": limit, "offset": offset}
    )
    return {"ok": True, "sources": sources, "stats": stats}


@app.get("/api/rss/sources/{source_id}")
def get_rss_source(
    source_id: str, inbox_store: Annotated[InboxStore, Depends(get_store)]
) -> JSONResponse:
    source = inbox_store.get_rss_source(source_id)
    if not source:
        return error_response("source_not_found", "RSS source not found", status_code=404, source_id=source_id)
    return JSONResponse({"ok": True, "source": source})


@app.patch("/api/rss/sources/{source_id}")
def update_rss_source(
    source_id: str,
    payload: RSSSourceUpdateRequest,
    inbox_store: Annotated[InboxStore, Depends(get_store)],
) -> JSONResponse:
    updates = payload.model_dump(exclude_unset=True)
    try:
        source = inbox_store.update_rss_source(source_id, updates)
    except ValueError as exc:
        return error_response("source_conflict", str(exc), status_code=409, source_id=source_id)
    if not source:
        return error_response("source_not_found", "RSS source not found", status_code=404, source_id=source_id)
    return JSONResponse({"ok": True, "source": source})


@app.delete("/api/rss/sources/{source_id}")
def delete_rss_source(
    source_id: str, inbox_store: Annotated[InboxStore, Depends(get_store)]
) -> JSONResponse:
    source = inbox_store.disable_rss_source(source_id)
    if not source:
        return error_response("source_not_found", "RSS source not found", status_code=404, source_id=source_id)
    return JSONResponse({"ok": True, "source_id": source_id, "status": "disabled"})


@app.post("/api/rss/sources/{source_id}/ingest")
def ingest_rss_source(
    source_id: str,
    payload: RSSSourceIngestRequest,
    inbox_store: Annotated[InboxStore, Depends(get_store)],
) -> JSONResponse:
    source = inbox_store.get_rss_source(source_id)
    if not source:
        return error_response("source_not_found", "RSS source not found", status_code=404, source_id=source_id)
    if source["status"] == "disabled":
        return error_response(
            "source_disabled",
            "RSS source is disabled",
            status_code=409,
            source_id=source_id,
            feed_url=source["feed_url"],
        )

    started_at = datetime.now(timezone.utc)
    t0 = monotonic_time.monotonic()
    run_id = build_rss_run_id(started_at, source_id)
    config = source.get("config") or {}
    request = RSSAnalyzeRequest(
        feed_url=source["feed_url"],
        source_id=source_id,
        source_name=source["source_name"],
        source_category=source["source_category"],
        limit=payload.limit if payload.limit is not None else int(config.get("limit", 20)),
        screen=payload.screen if payload.screen is not None else bool(config.get("screen", True)),
        incremental_mode=payload.incremental_mode or config.get("incremental_mode", "fixed_limit"),
        probe_limit=payload.probe_limit if payload.probe_limit is not None else int(config.get("probe_limit", 20)),
        new_source_initial_limit=(
            payload.new_source_initial_limit
            if payload.new_source_initial_limit is not None
            else int(config.get("new_source_initial_limit", 5))
        ),
        old_source_no_anchor_limit=(
            payload.old_source_no_anchor_limit
            if payload.old_source_no_anchor_limit is not None
            else int(config.get("old_source_no_anchor_limit", 20))
        ),
    )

    try:
        analysis = analyze_one_rss_source(
            inbox_store,
            request,
            include_items=payload.include_items,
            preserve_source_entry_order=True,
        )
        if analysis.get("ok") is False:
            raise RuntimeError("content processing failed")
        finished_at = datetime.now(timezone.utc)
        processed_items = int(analysis.get("new_items", 0)) + int(analysis.get("duplicate_items", 0))
        run = build_run_result(
            run_id,
            source_id,
            started_at,
            finished_at,
            t0,
            "success",
            analysis,
        )
        updated_source = inbox_store.record_rss_source_success(
            source_id,
            run_id=run_id,
            finished_at=finished_at.isoformat(),
            new_items=int(analysis.get("new_items", 0)),
            duplicate_items=int(analysis.get("duplicate_items", 0)),
            processed_items=processed_items,
            feed_items_seen=int(analysis.get("feed_items_seen", analysis.get("total_items", 0)) or 0),
            incremental_decision=analysis.get("incremental_decision"),
            anchor_found=analysis.get("anchor_found"),
        )
        return JSONResponse(
            {
                "ok": True,
                "run": run,
                "source": source_status_summary(updated_source or source),
                "items": analysis.get("items", []),
            }
        )
    except Exception as exc:
        error_code, message = classify_exception(exc)
        finished_at = datetime.now(timezone.utc)
        run = build_run_result(
            run_id,
            source_id,
            started_at,
            finished_at,
            t0,
            "failed",
            {},
            error_code=error_code,
            error_message=message,
        )
        updated_source = inbox_store.record_rss_source_failure(
            source_id,
            run_id=run_id,
            finished_at=finished_at.isoformat(),
            error_code=error_code,
            error_message=message,
        )
        return JSONResponse(
            status_code=400,
            content={
                **error_payload(error_code, message, source_id=source_id, feed_url=source["feed_url"]),
                "run": run,
                "source": source_status_summary(updated_source or source),
            },
        )


@app.post("/api/content/analyze")
def analyze_content(
    payload: ContentAnalyzeRequest, inbox_store: Annotated[InboxStore, Depends(get_store)]
) -> dict[str, Any]:
    if payload.audit_prompt:
        normalized = normalize_content(payload)
        audit_records = audit_screen_content(normalized)
        return {
            "ok": True,
            "audit_type": "prompt_audit",
            "audit_records": audit_records,
        }
    if payload.dump_llm_prompt:
        dump_dir = payload.dump_llm_prompt_dir or "outputs/runs/llm_prompt_dumps"
        Path(dump_dir).mkdir(parents=True, exist_ok=True)
        configure_llm_dump(enabled=True, output_dir=dump_dir)
    try:
        result = process_content_thread_safe(inbox_store, payload, raw=payload.model_dump())
        return {"ok": True, **result.model_dump()}
    finally:
        if payload.dump_llm_prompt:
            configure_llm_dump(enabled=False)


@app.post("/api/rss/analyze")
def analyze_rss(
    payload: RSSAnalyzeRequest, inbox_store: Annotated[InboxStore, Depends(get_store)]
) -> dict[str, Any]:
    if payload.audit_prompt:
        meta, entries = parse_feed(
            payload.feed_url,
            source_id=payload.source_id,
            source_name=payload.source_name,
            source_category=payload.source_category,
            limit=payload.limit,
        )
        audit_records: list[dict[str, Any]] = []
        for entry in entries:
            normalized = normalize_content(entry)
            records = audit_screen_content(normalized)
            audit_records.extend(records)
        return {
            "ok": True,
            "audit_type": "prompt_audit",
            "feed_url": payload.feed_url,
            "source_name": meta["source_name"],
            "total_items": len(entries),
            "audit_records": audit_records,
        }
    if payload.dump_llm_prompt:
        dump_dir = payload.dump_llm_prompt_dir or "outputs/runs/llm_prompt_dumps"
        Path(dump_dir).mkdir(parents=True, exist_ok=True)
        configure_llm_dump(enabled=True, output_dir=dump_dir)
    try:
        return analyze_one_rss_source(
            inbox_store,
            payload,
            include_items=True,
            preserve_source_entry_order=True,
        )
    except Exception as exc:
        error_code, message = classify_exception(exc)
        return error_response(error_code, message, status_code=400, source_id=payload.source_id, feed_url=payload.feed_url)
    finally:
        if payload.dump_llm_prompt:
            configure_llm_dump(enabled=False)

@app.post("/api/rss/analyze-batch")
def analyze_rss_batch(
    payload: RSSBatchAnalyzeRequest, inbox_store: Annotated[InboxStore, Depends(get_store)]
) -> dict[str, Any]:
    runner = RSSBatchRunner(inbox_store)
    return runner.run(payload)


@app.get("/api/inbox")
def get_inbox(
    request: Request,
    date_filter: Annotated[str | None, Query(alias="date")] = None,
    from_filter: Annotated[str | None, Query(alias="from")] = None,
    to_filter: Annotated[str | None, Query(alias="to")] = None,
    source_name: str | None = None,
    source_category: str | None = None,
    content_type: str | None = None,
    category: str | None = None,
    min_score: int | None = Query(default=None, ge=1, le=5),
    min_relevance: int | None = Query(default=None, ge=1, le=5),
    suggested_action: str | None = None,
    followup_type: str | None = None,
    cluster_id: str | None = None,
    cluster_relation: str | None = None,
    notification_decision: str | None = None,
    min_similarity: float | None = Query(default=None, ge=0.0, le=1.0),
    include_silent: bool | None = None,
    only_new_events: bool = False,
    only_incremental: bool = False,
    tag: str | None = None,
    keyword: str | None = None,
    need_id: str | None = None,
    topic_id: str | None = None,
    min_need_score: int | None = Query(default=None, ge=1, le=5),
    priority: str | None = None,
    include_maybe: bool = False,
    needs_more_context: bool | None = None,
    include_ignored: bool = False,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    inbox_store: Annotated[InboxStore, Depends(get_store)] = store,
) -> JSONResponse:
    reading_view_query = bool(need_id or topic_id)
    include_silent_value = include_silent
    if reading_view_query and "include_silent" not in request.query_params:
        include_silent_value = True

    include_ignored_value = include_ignored
    if reading_view_query and "include_ignored" not in request.query_params:
        include_ignored_value = True

    filters: dict[str, Any] = {
        "source_name": source_name,
        "source_category": source_category,
        "content_type": content_type,
        "category": category,
        "min_score": min_score,
        "min_relevance": min_relevance,
        "suggested_action": split_csv(suggested_action),
        "followup_type": followup_type,
        "cluster_id": cluster_id,
        "cluster_relation": cluster_relation,
        "notification_decision": split_csv(notification_decision),
        "min_similarity": min_similarity,
        "include_silent": include_silent_value
        if include_silent_value is not None
        else settings.notification.get("include_silent_in_default_inbox", False),
        "only_new_events": only_new_events,
        "only_incremental": only_incremental,
        "tag": tag,
        "keyword": keyword,
        "need_id": need_id,
        "topic_id": topic_id,
        "min_need_score": min_need_score,
        "priority": split_csv(priority),
        "include_maybe": include_maybe,
        "needs_more_context": needs_more_context,
        "include_ignored": include_ignored_value,
        "limit": limit,
        "offset": offset,
    }
    filters.update(resolve_date_filters(date_filter, from_filter, to_filter))
    items, total = inbox_store.query(filters)
    stats = build_stats(items)
    compact_filters = {key: value for key, value in filters.items() if value not in (None, [], "")}
    return JSONResponse(
        {
            "ok": True,
            "filters": compact_filters,
            "stats": {"total": len(items), "matched_before_screening_filters": total, **stats},
            "items": items,
        }
    )


def resolve_date_filters(
    date_filter: str | None, from_filter: str | None, to_filter: str | None
) -> dict[str, str | None]:
    if date_filter:
        if date_filter == "today":
            target = date.today()
        else:
            target = date.fromisoformat(date_filter)
        start = datetime.combine(target, time.min, tzinfo=timezone.utc).isoformat()
        end = datetime.combine(target, time.max, tzinfo=timezone.utc).isoformat()
        return {"from": start, "to": end}
    return {"from": from_filter, "to": to_filter}


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def build_stats(items: list[dict[str, Any]]) -> dict[str, int]:
    stats = {
        "ignore": 0,
        "skim": 0,
        "read": 0,
        "save": 0,
        "transcribe": 0,
        "review": 0,
        "full_push": 0,
        "incremental_push": 0,
        "silent": 0,
        "manual_review": 0,
        "new_event": 0,
        "incremental_update": 0,
        "duplicate": 0,
        "uncertain": 0,
        "embedding_failed": 0,
    }
    for item in items:
        action = item["screening"].get("suggested_action")
        if action in stats:
            stats[action] += 1
        decision = item.get("notification_decision")
        if decision in stats:
            stats[decision] += 1
        relation = item.get("cluster_relation")
        if relation in stats:
            stats[relation] += 1
    return stats


def build_rss_run_id(started_at: datetime, source_id: str) -> str:
    safe_source = re.sub(r"[^A-Za-z0-9_.-]+", "-", source_id).strip("-") or "source"
    return f"rss_{started_at.strftime('%Y%m%d_%H%M%S')}_{safe_source}"


def build_run_result(
    run_id: str,
    source_id: str,
    started_at: datetime,
    finished_at: datetime,
    monotonic_started_at: float,
    status: str,
    analysis: dict[str, Any],
    *,
    error_code: str | None = None,
    error_message: str | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "source_id": source_id,
        "status": status,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": round(monotonic_time.monotonic() - monotonic_started_at, 3),
        "error_code": error_code,
        "error_message": error_message,
        "retryable": retryable_for(error_code or ""),
        "stats": {
            "feed_items_seen": int(analysis.get("feed_items_seen", analysis.get("total_items", 0)) or 0),
            "selected_items_for_processing": int(
                analysis.get("selected_items_for_processing", analysis.get("total_items", 0)) or 0
            ),
            "processed_items": int(analysis.get("new_items", 0) or 0)
            + int(analysis.get("duplicate_items", 0) or 0),
            "new_items": int(analysis.get("new_items", 0) or 0),
            "duplicate_items": int(analysis.get("duplicate_items", 0) or 0),
            "failed_items": int(analysis.get("failed_items", 0) or 0),
        },
        "incremental": {
            "incremental_mode": analysis.get("incremental_mode", "fixed_limit"),
            "incremental_decision": analysis.get("incremental_decision"),
            "source_has_history": analysis.get("source_has_history"),
            "anchor_found": analysis.get("anchor_found"),
            "anchor_index": analysis.get("anchor_index"),
            "warnings": analysis.get("warnings", []),
        },
    }


def source_status_summary(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source["source_id"],
        "status": source["status"],
        "last_fetch_at": source.get("last_fetch_at"),
        "last_success_at": source.get("last_success_at"),
        "last_failure_at": source.get("last_failure_at"),
        "consecutive_failures": source.get("consecutive_failures", 0),
        "last_error_code": source.get("last_error_code"),
        "last_error_message": source.get("last_error_message"),
    }


def main() -> None:
    import uvicorn

    uvicorn.run("app.server:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    main()
