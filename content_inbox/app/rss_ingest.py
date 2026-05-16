from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from typing import Any

from app.models import RSSAnalyzeRequest, RSSSourceIngestRequest
from app.rss_errors import classify_exception, error_payload, retryable_for
from app.rss_runner import analyze_one_rss_source
from app.storage import InboxStore


def build_rss_run_id(started_at: datetime, source_id: str) -> str:
    safe_source = re.sub(r"[^A-Za-z0-9_.-]+", "-", source_id).strip("-") or "source"
    return f"rss_{started_at.strftime('%Y%m%d_%H%M%S_%f')}_{safe_source}"


def duration_ms(start_monotonic: float) -> int:
    return int(round((time.monotonic() - start_monotonic) * 1000))


def run_result(
    run_id: str,
    source_id: str,
    started_at: datetime,
    finished_at: datetime,
    duration: int,
    status: str,
    analysis: dict[str, Any],
    *,
    error_code: str | None = None,
    error_message: str | None = None,
) -> dict[str, Any]:
    stats = {
        "fetched_entries": int(analysis.get("feed_items_seen", analysis.get("total_items", 0)) or 0),
        "processed_entries": int(analysis.get("new_items", 0) or 0)
        + int(analysis.get("duplicate_items", 0) or 0),
        "new_items": int(analysis.get("new_items", 0) or 0),
        "duplicate_items": int(analysis.get("duplicate_items", 0) or 0),
        "failed_items": int(analysis.get("failed_items", 0) or 0),
        # Backwards-compatible names used by existing callers.
        "feed_items_seen": int(analysis.get("feed_items_seen", analysis.get("total_items", 0)) or 0),
        "selected_items_for_processing": int(
            analysis.get("selected_items_for_processing", analysis.get("total_items", 0)) or 0
        ),
        "processed_items": int(analysis.get("new_items", 0) or 0)
        + int(analysis.get("duplicate_items", 0) or 0),
    }
    error = None
    if error_code:
        error = {
            "error_code": error_code,
            "message": error_message or "",
            "retryable": retryable_for(error_code),
        }
    return {
        "run_id": run_id,
        "source_id": source_id,
        "status": status,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_ms": duration,
        "duration_seconds": round(duration / 1000, 3),
        "error_code": error_code,
        "error_message": error_message,
        "retryable": retryable_for(error_code or ""),
        "stats": stats,
        "incremental": {
            "mode": analysis.get("incremental_mode", "fixed_limit"),
            "decision": analysis.get("incremental_decision"),
            "anchor_found": analysis.get("anchor_found"),
            "anchor_index": analysis.get("anchor_index"),
            "warnings": analysis.get("warnings", []),
            # Backwards-compatible aliases.
            "incremental_mode": analysis.get("incremental_mode", "fixed_limit"),
            "incremental_decision": analysis.get("incremental_decision"),
            "source_has_history": analysis.get("source_has_history"),
        },
        "error": error,
    }


def source_status_summary(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source["source_id"],
        "status": source["status"],
        "last_fetch_at": source.get("last_fetch_at"),
        "last_ingest_at": source.get("last_ingest_at"),
        "last_success_at": source.get("last_success_at"),
        "last_failure_at": source.get("last_failure_at"),
        "consecutive_failures": source.get("consecutive_failures", 0),
        "consecutive_failure_count": source.get("consecutive_failure_count", 0),
        "failure_count": source.get("failure_count", 0),
        "last_error_code": source.get("last_error_code"),
        "last_error_message": source.get("last_error_message"),
    }


def _request_from_source(source: dict[str, Any], payload: RSSSourceIngestRequest) -> RSSAnalyzeRequest:
    config = source.get("config") or {}
    return RSSAnalyzeRequest(
        feed_url=source["feed_url"],
        source_id=source["source_id"],
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
        stop_on_first_existing=(
            payload.stop_on_first_existing
            if payload.stop_on_first_existing is not None
            else bool(config.get("stop_on_first_existing", True))
        ),
        process_order=payload.process_order,
    )


def ingest_registered_source(
    store: InboxStore,
    source_id: str,
    payload: RSSSourceIngestRequest,
    *,
    trigger_type: str = "api",
) -> tuple[int, dict[str, Any]]:
    source = store.get_rss_source(source_id)
    if not source:
        return 404, error_payload("source_not_found", "RSS source not found", source_id=source_id)
    if source["status"] == "disabled":
        return 409, error_payload("source_disabled", "RSS source is disabled", source_id=source_id, feed_url=source["feed_url"])
    if source["status"] == "paused" and not payload.force:
        return 409, error_payload("source_paused", "RSS source is paused", source_id=source_id, feed_url=source["feed_url"])
    if source["status"] == "broken" and not (payload.force or payload.test):
        return 409, error_payload("source_broken", "RSS source is broken", source_id=source_id, feed_url=source["feed_url"])

    started_at = datetime.now(timezone.utc)
    t0 = time.monotonic()
    run_id = build_rss_run_id(started_at, source_id)
    request = _request_from_source(source, payload)
    request_payload = payload.model_dump()
    store.create_ingest_run(
        {
            "run_id": run_id,
            "trigger_type": "test" if payload.test else trigger_type,
            "source_mode": "source",
            "status": "running",
            "started_at": started_at.isoformat(),
            "selected_source_count": 1,
            "request": request_payload,
        }
    )
    try:
        analysis = analyze_one_rss_source(
            store,
            request,
            include_items=payload.include_items,
            preserve_source_entry_order=True,
            process_order=payload.process_order,
            dry_run=payload.dry_run or payload.test,
        )
        if analysis.get("ok") is False:
            raise RuntimeError("content processing failed")
        finished_at = datetime.now(timezone.utc)
        duration = duration_ms(t0)
        run = run_result(run_id, source_id, started_at, finished_at, duration, "success", analysis)
        processed = run["stats"]["processed_entries"]
        updated_source = source
        if not payload.dry_run and not payload.test:
            updated_source = store.record_rss_source_success(
                source_id,
                run_id=run_id,
                finished_at=finished_at.isoformat(),
                new_items=run["stats"]["new_items"],
                duplicate_items=run["stats"]["duplicate_items"],
                processed_items=processed,
                feed_items_seen=run["stats"]["fetched_entries"],
                incremental_decision=run["incremental"].get("decision"),
                anchor_found=run["incremental"].get("anchor_found"),
                duration_ms=duration,
            ) or source
        store.create_ingest_run(
            {
                "run_id": run_id,
                "trigger_type": "test" if payload.test else trigger_type,
                "source_mode": "source",
                "status": "success",
                "started_at": started_at.isoformat(),
                "finished_at": finished_at.isoformat(),
                "duration_ms": duration,
                "selected_source_count": 1,
                "success_source_count": 1,
                "new_items_count": run["stats"]["new_items"],
                "duplicate_items_count": run["stats"]["duplicate_items"],
                "processed_items_count": processed,
                "failed_items_count": run["stats"]["failed_items"],
                "request": request_payload,
                "summary": run,
            }
        )
        store.create_ingest_run_source(
            {
                "run_id": run_id,
                "source_id": source_id,
                "feed_url": source["feed_url"],
                "source_name": source["source_name"],
                "source_category": source["source_category"],
                "status": "success",
                "started_at": started_at.isoformat(),
                "finished_at": finished_at.isoformat(),
                "duration_ms": duration,
                "retryable": False,
                "fetched_entries_count": run["stats"]["fetched_entries"],
                "processed_entries_count": processed,
                "new_items_count": run["stats"]["new_items"],
                "duplicate_items_count": run["stats"]["duplicate_items"],
                "failed_items_count": run["stats"]["failed_items"],
                "incremental_mode": run["incremental"].get("mode"),
                "incremental_decision": run["incremental"].get("decision"),
                "anchor_found": run["incremental"].get("anchor_found"),
                "anchor_index": run["incremental"].get("anchor_index"),
                "warnings": run["incremental"].get("warnings", []),
                "result": run,
            }
        )
        return 200, {"ok": True, "run": run, "source": source_status_summary(updated_source), "items": analysis.get("items", [])}
    except Exception as exc:
        error_code, message = classify_exception(exc)
        finished_at = datetime.now(timezone.utc)
        duration = duration_ms(t0)
        run = run_result(
            run_id,
            source_id,
            started_at,
            finished_at,
            duration,
            "failed",
            {},
            error_code=error_code,
            error_message=message,
        )
        updated_source = store.record_rss_source_failure(
            source_id,
            run_id=run_id,
            finished_at=finished_at.isoformat(),
            error_code=error_code,
            error_message=message,
            retryable=run["retryable"],
            duration_ms=duration,
        ) or source
        store.create_ingest_run(
            {
                "run_id": run_id,
                "trigger_type": "test" if payload.test else trigger_type,
                "source_mode": "source",
                "status": "failed",
                "started_at": started_at.isoformat(),
                "finished_at": finished_at.isoformat(),
                "duration_ms": duration,
                "selected_source_count": 1,
                "failure_source_count": 1,
                "request": request_payload,
                "summary": run,
                "error_code": error_code,
                "error_message": message,
            }
        )
        store.create_ingest_run_source(
            {
                "run_id": run_id,
                "source_id": source_id,
                "feed_url": source["feed_url"],
                "source_name": source["source_name"],
                "source_category": source["source_category"],
                "status": "failed",
                "started_at": started_at.isoformat(),
                "finished_at": finished_at.isoformat(),
                "duration_ms": duration,
                "error_code": error_code,
                "error_message": message,
                "retryable": run["retryable"],
                "result": run,
            }
        )
        return 400, {
            **error_payload(error_code, message, source_id=source_id, feed_url=source["feed_url"]),
            "run": run,
            "source": source_status_summary(updated_source),
        }
