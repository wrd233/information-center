from __future__ import annotations

from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse

from app.batch_runner import RSSBatchRunner
from app.config import settings
from app.models import ContentAnalyzeRequest, RSSAnalyzeRequest, RSSBatchAnalyzeRequest
from app.processor import normalize_content, process_content_thread_safe
from app.rss import parse_feed
from app.rss_runner import analyze_one_rss_source
from app.screener import audit_screen_content, configure_llm_dump
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
        },
    }


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
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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


def main() -> None:
    import uvicorn

    uvicorn.run("app.server:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    main()
