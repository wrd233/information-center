from __future__ import annotations

import json
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from app.config import settings
from app.models import RSSAnalyzeRequest
from app.rss_errors import classify_exception, retryable_for
from app.rss_runner import analyze_one_rss_source
from app.storage import InboxStore
from app.utils import stable_hash, utc_now


PostProcessCallback = Callable[[InboxStore, str, list[str]], dict[str, Any]]

TERMINAL_RUN_STATUSES = {"success", "partial_success", "failed", "cancelled"}
TRUSTED_EVENT_LIMIT = 20
WEAK_SIGNAL_LIMIT = 20
AGENT_QUEUE_LIMIT = 20


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def add_run_event(
    store: InboxStore,
    run_id: str,
    event_type: str,
    *,
    source_id: str | None = None,
    item_id: str | None = None,
    object_type: str | None = None,
    object_id: str | None = None,
    level: str = "info",
    message: str = "",
    payload: dict[str, Any] | None = None,
) -> None:
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO ingest_run_events(
                run_id, event_type, source_id, item_id, object_type, object_id,
                level, message, payload_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                event_type,
                source_id,
                item_id,
                object_type,
                object_id,
                level,
                message,
                json.dumps(payload or {}, ensure_ascii=False),
                utc_now(),
            ),
        )


def build_inbox_run_id(trigger_type: str) -> str:
    return f"inbox_{trigger_type}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"


def latest_recent_full_run(store: InboxStore, *, grace_minutes: int) -> dict[str, Any] | None:
    latest = store.latest_full_ingest_run(
        trigger_types=["manual", "scheduled"],
        statuses=["success", "partial_success"],
    )
    if not latest:
        return None
    finished_at = parse_utc(latest.get("finished_at"))
    if not finished_at:
        return None
    if datetime.now(timezone.utc) - finished_at <= timedelta(minutes=grace_minutes):
        return latest
    return None


def start_inbox_run(
    store: InboxStore,
    payload: dict[str, Any] | None = None,
    *,
    trigger_type: str = "manual",
    post_process: PostProcessCallback | None = None,
) -> dict[str, Any]:
    payload = payload or {}
    force = bool(payload.get("force", False))
    run_synchronously = bool(payload.get("run_synchronously", False))
    if not settings.enable_real_runs:
        state = {
            "status": "real_runs_disabled",
            "message": "Registry-full inbox runs require CONTENT_INBOX_ENABLE_REAL_RUNS=1.",
        }
        store.set_metadata_value("inbox_loop_last_start_rejected", state)
        return {"accepted": False, "status": "real_runs_disabled", **state}

    grace_minutes = int(payload.get("recent_grace_minutes") or settings.manual_run_recent_grace_minutes)
    if trigger_type == "manual" and not force:
        recent = latest_recent_full_run(store, grace_minutes=grace_minutes)
        if recent:
            return {
                "accepted": False,
                "status": "skipped_recent",
                "recent_run": recent,
                "grace_minutes": grace_minutes,
            }

    run_id = build_inbox_run_id(trigger_type)
    acquired, lock = store.try_acquire_inbox_run_lock(run_id=run_id, owner=trigger_type)
    if not acquired:
        return {
            "accepted": False,
            "status": "locked",
            "active_lock": lock,
        }

    sources = store.list_active_rss_sources(limit=int((payload.get("limits") or {}).get("max_sources", 10000)))
    started_at = utc_now()
    request_payload = {
        **payload,
        "trigger_type": trigger_type,
        "source_mode": "registry_full",
        "source_count": len(sources),
        "screen": bool(payload.get("screen", False)),
    }
    store.create_ingest_run(
        {
            "run_id": run_id,
            "trigger_type": trigger_type,
            "source_mode": "registry_full",
            "status": "running",
            "started_at": started_at,
            "selected_source_count": len(sources),
            "request": request_payload,
        }
    )
    add_run_event(store, run_id, "run_started", message="Inbox registry-full run started.", payload=request_payload)

    if run_synchronously:
        execute_inbox_run(store, run_id, sources, request_payload, post_process=post_process)
    else:
        thread = threading.Thread(
            target=execute_inbox_run,
            args=(store, run_id, sources, request_payload),
            kwargs={"post_process": post_process},
            daemon=True,
        )
        thread.start()
    return {"accepted": True, "status": "started", "run_id": run_id, "run": store.get_ingest_run(run_id)}


def execute_inbox_run(
    store: InboxStore,
    run_id: str,
    sources: list[dict[str, Any]],
    request_payload: dict[str, Any],
    *,
    post_process: PostProcessCallback | None = None,
) -> None:
    started = time.monotonic()
    limits = request_payload.get("limits") or {}
    max_items_per_source = int(limits.get("max_items_per_source", 20) or 20)
    probe_limit = int(limits.get("probe_limit", max_items_per_source) or max_items_per_source)
    new_source_initial_limit = int(limits.get("new_source_initial_limit", min(max_items_per_source, 5)) or 5)
    old_source_no_anchor_limit = int(limits.get("old_source_no_anchor_limit", max_items_per_source) or max_items_per_source)
    screen = bool(request_payload.get("screen", False))
    linked_item_ids: list[str] = []
    success_sources = failure_sources = 0
    total_new = total_dup = total_processed = total_failed = 0
    kernel_error: tuple[str, str] | None = None

    try:
        for source in sources:
            source_started = utc_now()
            source_t0 = time.monotonic()
            add_run_event(store, run_id, "source_started", source_id=source["source_id"], message=source["source_name"])
            try:
                config = source.get("config") or {}
                request = RSSAnalyzeRequest(
                    feed_url=source["feed_url"],
                    source_id=source["source_id"],
                    source_name=source["source_name"],
                    source_category=source.get("source_category"),
                    limit=max_items_per_source,
                    screen=screen or bool(config.get("screen", False)),
                    incremental_mode="until_existing",
                    probe_limit=probe_limit,
                    new_source_initial_limit=new_source_initial_limit,
                    old_source_no_anchor_limit=old_source_no_anchor_limit,
                    stop_on_first_existing=bool(request_payload.get("stop_on_first_existing", True)),
                    process_order=request_payload.get("process_order") or "oldest_first",
                )
                analysis = analyze_one_rss_source(
                    store,
                    request,
                    include_items=True,
                    preserve_source_entry_order=True,
                    process_order=request.process_order,
                    dry_run=False,
                )
                if analysis.get("ok") is False:
                    raise RuntimeError(str(analysis.get("error") or "source analysis failed"))
                item_ids = link_run_items(store, run_id, source["source_id"], analysis.get("items") or [])
                linked_item_ids.extend(item_ids)
                new_items = int(analysis.get("new_items", 0) or 0)
                duplicate_items = int(analysis.get("duplicate_items", 0) or 0)
                failed_items = int(analysis.get("failed_items", 0) or 0)
                processed_items = new_items + duplicate_items
                success_sources += 1
                total_new += new_items
                total_dup += duplicate_items
                total_failed += failed_items
                total_processed += processed_items
                finished_at = utc_now()
                duration_ms = int((time.monotonic() - source_t0) * 1000)
                store.record_rss_source_success(
                    source["source_id"],
                    run_id=run_id,
                    finished_at=finished_at,
                    new_items=new_items,
                    duplicate_items=duplicate_items,
                    processed_items=processed_items,
                    feed_items_seen=int(analysis.get("feed_items_seen", analysis.get("total_items", 0)) or 0),
                    incremental_decision=analysis.get("incremental_decision"),
                    anchor_found=analysis.get("anchor_found"),
                    duration_ms=duration_ms,
                )
                store.create_ingest_run_source(
                    {
                        "run_id": run_id,
                        "source_id": source["source_id"],
                        "feed_url": source["feed_url"],
                        "source_name": source["source_name"],
                        "source_category": source.get("source_category"),
                        "status": "success",
                        "started_at": source_started,
                        "finished_at": finished_at,
                        "duration_ms": duration_ms,
                        "retryable": False,
                        "fetched_entries_count": int(analysis.get("feed_items_seen", analysis.get("total_items", 0)) or 0),
                        "processed_entries_count": processed_items,
                        "new_items_count": new_items,
                        "duplicate_items_count": duplicate_items,
                        "failed_items_count": failed_items,
                        "incremental_mode": analysis.get("incremental_mode"),
                        "incremental_decision": analysis.get("incremental_decision"),
                        "anchor_found": analysis.get("anchor_found"),
                        "anchor_index": analysis.get("anchor_index"),
                        "warnings": analysis.get("warnings") or [],
                        "result": summarize_source_analysis(analysis),
                    }
                )
                add_run_event(
                    store,
                    run_id,
                    "source_completed",
                    source_id=source["source_id"],
                    message="Source completed.",
                    payload={"new_items": new_items, "duplicate_items": duplicate_items, "processed_items": processed_items},
                )
            except Exception as exc:
                failure_sources += 1
                total_failed += 1
                code, message = classify_exception(exc)
                finished_at = utc_now()
                duration_ms = int((time.monotonic() - source_t0) * 1000)
                store.record_rss_source_failure(
                    source["source_id"],
                    run_id=run_id,
                    finished_at=finished_at,
                    error_code=code,
                    error_message=message,
                    retryable=retryable_for(code),
                    duration_ms=duration_ms,
                )
                store.create_ingest_run_source(
                    {
                        "run_id": run_id,
                        "source_id": source["source_id"],
                        "feed_url": source.get("feed_url"),
                        "source_name": source.get("source_name"),
                        "source_category": source.get("source_category"),
                        "status": "failed",
                        "started_at": source_started,
                        "finished_at": finished_at,
                        "duration_ms": duration_ms,
                        "error_code": code,
                        "error_message": message,
                        "retryable": retryable_for(code),
                        "failed_items_count": 1,
                        "warnings": [],
                        "result": {"error_code": code, "error_message": message},
                    }
                )
                add_run_event(
                    store,
                    run_id,
                    "source_failed",
                    source_id=source["source_id"],
                    level="error",
                    message=message,
                    payload={"error_code": code, "retryable": retryable_for(code)},
                )

        if post_process and linked_item_ids:
            add_run_event(store, run_id, "post_processing_started", message="Deterministic post-processing started.")
            try:
                result = post_process(store, run_id, sorted(set(linked_item_ids)))
                add_run_event(store, run_id, "post_processing_completed", message="Deterministic post-processing completed.", payload=result)
            except Exception as exc:
                code, message = classify_exception(exc)
                kernel_error = (code, message)
                add_run_event(store, run_id, "post_processing_failed", level="error", message=message, payload={"error_code": code})
    except Exception as exc:
        kernel_error = classify_exception(exc)
        add_run_event(store, run_id, "run_kernel_failed", level="error", message=kernel_error[1], payload={"error_code": kernel_error[0]})
    finally:
        final_status = final_run_status(success_sources, failure_sources, kernel_error, len(sources))
        duration_ms = int((time.monotonic() - started) * 1000)
        sources_result = store.list_ingest_run_sources(run_id)
        summary = build_run_summary(
            {
                "run_id": run_id,
                "trigger_type": request_payload.get("trigger_type"),
                "source_mode": "registry_full",
                "status": final_status,
                "selected_source_count": len(sources),
                "success_source_count": success_sources,
                "failure_source_count": failure_sources,
                "new_items_count": total_new,
                "duplicate_items_count": total_dup,
                "processed_items_count": total_processed,
                "failed_items_count": total_failed,
            },
            sources_result,
            kernel_error=kernel_error,
        )
        store.create_ingest_run(
            {
                "run_id": run_id,
                "trigger_type": request_payload.get("trigger_type", "manual"),
                "source_mode": "registry_full",
                "status": final_status,
                "started_at": (store.get_ingest_run(run_id) or {}).get("started_at") or utc_now(),
                "finished_at": utc_now(),
                "duration_ms": duration_ms,
                "selected_source_count": len(sources),
                "success_source_count": success_sources,
                "failure_source_count": failure_sources,
                "new_items_count": total_new,
                "duplicate_items_count": total_dup,
                "processed_items_count": total_processed,
                "failed_items_count": total_failed,
                "request": request_payload,
                "summary": summary,
                "error_code": kernel_error[0] if kernel_error else None,
                "error_message": kernel_error[1] if kernel_error else None,
            }
        )
        add_run_event(store, run_id, f"run_{final_status}", message=f"Inbox run {final_status}.", payload=summary)
        store.release_inbox_run_lock(run_id)


def link_run_items(store: InboxStore, run_id: str, source_id: str, items: list[dict[str, Any]]) -> list[str]:
    item_ids: list[str] = []
    with store.connect() as conn:
        for item in items:
            item_id = item.get("item_id")
            if not item_id:
                continue
            item_ids.append(item_id)
            status = "duplicate" if item.get("is_duplicate") else "inserted"
            conn.execute(
                """
                INSERT OR IGNORE INTO item_run_links(run_id, source_id, item_id, status, operation_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (run_id, source_id, item_id, status, None, utc_now()),
            )
    return item_ids


def summarize_source_analysis(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "total_items": analysis.get("total_items", 0),
        "new_items": analysis.get("new_items", 0),
        "duplicate_items": analysis.get("duplicate_items", 0),
        "silent_items": analysis.get("silent_items", 0),
        "recommended_items": analysis.get("recommended_items", 0),
        "incremental_mode": analysis.get("incremental_mode"),
        "incremental_decision": analysis.get("incremental_decision"),
        "anchor_found": analysis.get("anchor_found"),
        "warnings": analysis.get("warnings") or [],
    }


def final_run_status(
    success_sources: int,
    failure_sources: int,
    kernel_error: tuple[str, str] | None,
    selected_sources: int,
) -> str:
    if kernel_error and not success_sources:
        return "failed"
    if not selected_sources:
        return "failed"
    if failure_sources and success_sources:
        return "partial_success"
    if failure_sources and not success_sources:
        return "failed"
    if kernel_error:
        return "partial_success"
    return "success"


def build_run_summary(
    run: dict[str, Any],
    sources: list[dict[str, Any]],
    *,
    kernel_error: tuple[str, str] | None = None,
) -> dict[str, Any]:
    active_sources = int(run.get("selected_source_count", 0) or 0)
    succeeded = int(run.get("success_source_count", 0) or 0)
    failed = int(run.get("failure_source_count", 0) or 0)
    attempted = succeeded + failed
    coverage_rate = round((succeeded / active_sources), 4) if active_sources else 0.0
    failed_sources = [source for source in sources if source.get("status") == "failed"]
    high_priority_failures = [
        source
        for source in failed_sources
        if is_high_priority_source(source)
    ]
    confidence, confidence_reasons = confidence_for_run(
        active_sources=active_sources,
        succeeded=succeeded,
        failed=failed,
        high_priority_failures=high_priority_failures,
        kernel_error=kernel_error,
    )
    return {
        "active_sources": active_sources,
        "attempted_sources": attempted,
        "succeeded_sources": succeeded,
        "failed_sources": failed,
        "coverage_rate": coverage_rate,
        "new_items": int(run.get("new_items_count", 0) or 0),
        "duplicate_items": int(run.get("duplicate_items_count", 0) or 0),
        "processed_items": int(run.get("processed_items_count", 0) or 0),
        "failed_items": int(run.get("failed_items_count", 0) or 0),
        "failed_source_digest": [
            {
                "source_id": source.get("source_id"),
                "source_name": source.get("source_name"),
                "error_code": source.get("error_code"),
                "error_message": source.get("error_message"),
                "retryable": source.get("retryable"),
            }
            for source in failed_sources[:10]
        ],
        "critical_failures": [
            {
                "source_id": source.get("source_id"),
                "source_name": source.get("source_name"),
                "error_code": source.get("error_code"),
            }
            for source in high_priority_failures
        ],
        "confidence": confidence,
        "confidence_reasons": confidence_reasons,
        "post_processing": {
            "deterministic": "completed" if run.get("status") in {"success", "partial_success"} else "unknown",
            "llm_enrichment": "disabled_by_default",
        },
    }


def is_high_priority_source(source: dict[str, Any]) -> bool:
    priority = source.get("priority")
    tags = {str(tag).lower() for tag in source.get("tags") or []}
    config = source.get("config") or {}
    return (
        (isinstance(priority, int) and priority <= 1)
        or bool(config.get("core"))
        or bool({"core", "high_priority", "high-priority"} & tags)
    )


def confidence_for_run(
    *,
    active_sources: int,
    succeeded: int,
    failed: int,
    high_priority_failures: list[dict[str, Any]],
    kernel_error: tuple[str, str] | None,
) -> tuple[str, list[str]]:
    if kernel_error and not succeeded:
        return "failed", [f"run_kernel_failed:{kernel_error[0]}"]
    if active_sources <= 0:
        return "failed", ["no_active_sources"]
    success_rate = succeeded / active_sources
    reasons = [f"source_success_rate:{success_rate:.0%}"]
    if high_priority_failures:
        reasons.append(f"high_priority_failures:{len(high_priority_failures)}")
    if success_rate >= 0.95 and not high_priority_failures:
        return "high", reasons
    if success_rate >= 0.80:
        return "medium", reasons
    return "low", reasons


def run_summary(store: InboxStore, run_id: str) -> dict[str, Any] | None:
    run = store.get_ingest_run(run_id)
    if not run:
        return None
    sources = store.list_ingest_run_sources(run_id)
    summary = run.get("summary") or build_run_summary(run, sources)
    return {
        "run": run,
        "summary": summary,
        "pipeline": pipeline_status_for_events(store, run_id),
    }


def pipeline_status_for_events(store: InboxStore, run_id: str) -> dict[str, str]:
    with store.connect() as conn:
        rows = conn.execute("SELECT event_type FROM ingest_run_events WHERE run_id = ?", (run_id,)).fetchall()
    event_types = {row["event_type"] for row in rows}
    return {
        "ingest": "completed" if any(evt.startswith("run_") and evt != "run_started" for evt in event_types) else "running",
        "post_processing": "failed" if "post_processing_failed" in event_types else ("completed" if "post_processing_completed" in event_types else "pending"),
        "triage": "available",
        "llm_enrichment": "disabled_by_default",
    }


def run_diagnostics(store: InboxStore, run_id: str) -> dict[str, Any] | None:
    run = store.get_ingest_run(run_id)
    if not run:
        return None
    sources = store.list_ingest_run_sources(run_id)
    failures = [source for source in sources if source.get("status") == "failed"]
    return {
        "run_id": run_id,
        "source_count": len(sources),
        "failures": failures,
        "sources": sources,
    }


def scope_metadata(run_id: str | None) -> dict[str, Any]:
    return {
        "type": "selected_run" if run_id else "legacy_full",
        "run_id": run_id,
        "label": f"Selected Run {run_id}" if run_id else "Legacy / 全库",
        "data_policy": "registry_full_run_only" if run_id else "legacy_full_database",
        "includes_history": not bool(run_id),
    }


def operating_view(store: InboxStore, run_id: str | None = None) -> dict[str, Any]:
    with store.connect() as conn:
        if run_id:
            trusted_events = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT e.event_id, e.event_title, e.event_summary, e.event_type, e.status, e.confidence,
                        e.importance, e.primary_cluster_id, e.created_at
                    FROM events e
                    WHERE (e.status = 'ready' OR e.confidence >= 0.9)
                      AND EXISTS (
                        SELECT 1
                        FROM event_items ei
                        JOIN item_run_links irl ON irl.item_id = ei.item_id
                        WHERE ei.event_id = e.event_id
                          AND irl.run_id = ?
                      )
                    ORDER BY e.importance DESC, COALESCE(e.event_time, e.created_at) DESC
                    LIMIT ?
                    """,
                    (run_id, TRUSTED_EVENT_LIMIT),
                ).fetchall()
            ]
            weak_signals = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT DISTINCT i.item_id, i.title, i.source_name, i.source_id, i.published_at,
                        i.screening_json, i.clustering_json, i.created_at
                    FROM inbox_items i
                    JOIN item_run_links irl ON irl.item_id = i.item_id
                    WHERE i.deleted_at IS NULL
                      AND irl.run_id = ?
                    ORDER BY i.created_at DESC
                    LIMIT ?
                    """,
                    (run_id, WEAK_SIGNAL_LIMIT * 4),
                ).fetchall()
            ]
            agent_queue = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT rq.*
                    FROM review_queue rq
                    WHERE rq.status = 'pending'
                      AND (
                        (rq.target_type = 'item' AND EXISTS (
                          SELECT 1 FROM item_run_links irl
                          WHERE irl.item_id = rq.target_id AND irl.run_id = ?
                        ))
                        OR (rq.target_type = 'event' AND EXISTS (
                          SELECT 1
                          FROM event_items ei
                          JOIN item_run_links irl ON irl.item_id = ei.item_id
                          WHERE ei.event_id = rq.target_id AND irl.run_id = ?
                        ))
                        OR (rq.target_type = 'cluster' AND EXISTS (
                          SELECT 1
                          FROM cluster_items ci
                          JOIN item_run_links irl ON irl.item_id = ci.item_id
                          WHERE ci.cluster_id = rq.target_id AND irl.run_id = ?
                        ))
                      )
                    ORDER BY rq.created_at DESC
                    LIMIT ?
                    """,
                    (run_id, run_id, run_id, AGENT_QUEUE_LIMIT),
                ).fetchall()
            ]
            source_health_anomalies = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT s.source_id, s.source_name, s.status, s.priority, s.last_failure_at, s.last_error_code,
                        s.last_error_message, s.consecutive_failure_count, s.last_duration_ms
                    FROM rss_sources s
                    JOIN rss_ingest_run_sources rs ON rs.source_id = s.source_id
                    WHERE s.deleted_at IS NULL
                      AND rs.run_id = ?
                      AND (s.status IN ('broken', 'paused') OR s.consecutive_failure_count > 0 OR s.last_error_code IS NOT NULL OR rs.status = 'failed')
                    ORDER BY s.consecutive_failure_count DESC, s.last_failure_at DESC
                    LIMIT 20
                    """,
                    (run_id,),
                ).fetchall()
            ]
        else:
            trusted_events = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT event_id, event_title, event_summary, event_type, status, confidence, importance, primary_cluster_id, created_at
                    FROM events
                    WHERE status = 'ready' OR confidence >= 0.9
                    ORDER BY importance DESC, COALESCE(event_time, created_at) DESC
                    LIMIT ?
                    """,
                    (TRUSTED_EVENT_LIMIT,),
                ).fetchall()
            ]
            weak_signals = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT item_id, title, source_name, source_id, published_at, screening_json, clustering_json
                    FROM inbox_items
                    WHERE deleted_at IS NULL
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (WEAK_SIGNAL_LIMIT * 4,),
                ).fetchall()
            ]
            agent_queue = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT * FROM review_queue
                    WHERE status = 'pending'
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (AGENT_QUEUE_LIMIT,),
                ).fetchall()
            ]
            source_health_anomalies = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT source_id, source_name, status, priority, last_failure_at, last_error_code,
                        last_error_message, consecutive_failure_count, last_duration_ms
                    FROM rss_sources
                    WHERE deleted_at IS NULL
                      AND (status IN ('broken', 'paused') OR consecutive_failure_count > 0 OR last_error_code IS NOT NULL)
                    ORDER BY consecutive_failure_count DESC, last_failure_at DESC
                    LIMIT 20
                    """
                ).fetchall()
            ]
    weak = [weak_signal_from_item(row) for row in weak_signals]
    weak = [entry for entry in weak if entry is not None][:WEAK_SIGNAL_LIMIT]
    silent_summary = silent_summary_from_items(weak_signals)
    user_escalations = [
        review for review in agent_queue
        if "user" in (review.get("review_type") or "") or "manual" in (review.get("reason") or "")
    ]
    return {
        "run_id": run_id,
        "scope": scope_metadata(run_id),
        "trusted_events": trusted_events,
        "weak_signals": weak,
        "silent_summary": silent_summary,
        "agent_queue": [review_with_suggestion(review) for review in agent_queue],
        "user_escalations": [review_with_suggestion(review) for review in user_escalations],
        "source_health_anomalies": source_health_anomalies,
    }


def weak_signal_from_item(row: dict[str, Any]) -> dict[str, Any] | None:
    screening = safe_json(row.get("screening_json"), {})
    clustering = safe_json(row.get("clustering_json"), {})
    value = int(screening.get("value_score", 0) or 0)
    relevance = int(screening.get("personal_relevance", 0) or 0)
    topic_hits = screening.get("topic_matches") or []
    hidden = screening.get("hidden_signals") or []
    is_silent = clustering.get("notification_decision") == "silent" or screening.get("suggested_action") in {"ignore", "skim"}
    if value >= 4 or relevance >= 4 or topic_hits or hidden:
        return {
            "target_type": "item",
            "target_id": row["item_id"],
            "title": row["title"],
            "source_name": row["source_name"],
            "published_at": row["published_at"],
            "reason_codes": compact_reason_codes(screening, clustering, is_silent),
            "evidence_ids": [row["item_id"]],
            "score": max(value, relevance),
        }
    return None


def compact_reason_codes(screening: dict[str, Any], clustering: dict[str, Any], is_silent: bool) -> list[str]:
    reasons: list[str] = []
    if is_silent:
        reasons.append("silent_item_rescue_candidate")
    if screening.get("topic_matches"):
        reasons.append("watch_topic_hit")
    if screening.get("hidden_signals"):
        reasons.append("hidden_signal")
    if clustering.get("cluster_relation") == "uncertain":
        reasons.append("uncertain_merge")
    if not reasons:
        reasons.append("weak_signal")
    return reasons


def silent_summary_from_items(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = 0
    samples: list[dict[str, Any]] = []
    reasons: dict[str, int] = {}
    for row in rows:
        screening = safe_json(row.get("screening_json"), {})
        clustering = safe_json(row.get("clustering_json"), {})
        is_silent = clustering.get("notification_decision") == "silent" or screening.get("suggested_action") in {"ignore", "skim"}
        if not is_silent:
            continue
        total += 1
        reason = screening.get("suggested_action") or clustering.get("notification_decision") or "silent"
        reasons[reason] = reasons.get(reason, 0) + 1
        if len(samples) < 5:
            samples.append({"item_id": row["item_id"], "title": row["title"], "source_name": row["source_name"], "reason": reason})
    return {"silent_items_sampled": total, "reason_counts": reasons, "samples": samples}


def review_with_suggestion(review: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(review)
    enriched["suggestion"] = safe_json(review.get("suggestion_json"), {})
    return enriched


def build_triage_packets(store: InboxStore, *, run_id: str | None = None, limit: int = 10) -> dict[str, Any]:
    view = operating_view(store, run_id)
    candidates: list[dict[str, Any]] = []
    for review in view["agent_queue"]:
        candidates.append(
            {
                "target_type": review.get("target_type"),
                "target_id": review.get("target_id"),
                "candidate_source": "review_queue",
                "reason_codes": [review.get("review_type") or "pending_review"],
                "evidence_ids": [review.get("target_id")],
                "preview": review.get("reason") or review.get("review_type"),
            }
        )
    for signal in view["weak_signals"]:
        candidates.append(
            {
                "target_type": signal["target_type"],
                "target_id": signal["target_id"],
                "candidate_source": "weak_signal",
                "reason_codes": signal["reason_codes"],
                "evidence_ids": signal["evidence_ids"],
                "preview": signal["title"],
            }
        )
    packet_id = f"triage_{stable_hash((run_id or 'latest') + json.dumps(candidates[:limit], sort_keys=True, ensure_ascii=False))[:16]}"
    return {
        "packet_id": packet_id,
        "run_id": run_id,
        "limit": limit,
        "policy": {
            "network": "disabled_by_default",
            "raw_item_scope": "bounded_evidence_only",
            "allowed_decisions": ["surface", "research", "silent", "noise", "merge_suggest", "do_not_merge"],
        },
        "candidates": candidates[:limit],
        "stats": {"candidate_count": min(len(candidates), limit), "unbounded_raw_items_exposed": False},
    }


def context_pack(
    store: InboxStore,
    goal: str,
    *,
    run_id: str | None = None,
    target_type: str | None = None,
    target_id: str | None = None,
) -> dict[str, Any]:
    latest = store.latest_full_ingest_run(trigger_types=["manual", "scheduled"])
    effective_run_id = run_id or (latest or {}).get("run_id")
    summary = run_summary(store, effective_run_id) if effective_run_id else None
    view = operating_view(store, effective_run_id)
    ledger = store.decision_ledger(run_id=effective_run_id, target_type=target_type, target_id=target_id, limit=30)
    base = {
        "goal": goal,
        "run_id": effective_run_id,
        "scope": scope_metadata(effective_run_id),
        "latest_run_summary": summary,
        "trusted_events": view["trusted_events"],
        "weak_signals": view["weak_signals"],
        "silent_summary": view["silent_summary"],
        "agent_queue": view["agent_queue"],
        "user_escalations": view["user_escalations"],
        "source_health_anomalies": view["source_health_anomalies"],
        "decision_ledger": ledger,
        "policy": {"raw_items": "not_included_by_default", "network": "disabled_by_default"},
    }
    base["object_counts"] = {
        "trusted_events": len(base["trusted_events"]),
        "weak_signals": len(base["weak_signals"]),
        "agent_queue": len(base["agent_queue"]),
        "user_escalations": len(base["user_escalations"]),
        "source_health_anomalies": len(base["source_health_anomalies"]),
        "decision_ledger": len(base["decision_ledger"]),
    }
    base["budget"] = {
        "approx_tokens": max(1, len(json.dumps(base, ensure_ascii=False, default=str)) // 4),
        "raw_items_included": False,
    }
    if goal == "research_object":
        base["target"] = {"target_type": target_type, "target_id": target_id}
    return base


def safe_json(value: Any, default: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value or "")
    except Exception:
        return default
