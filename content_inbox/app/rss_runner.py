from __future__ import annotations

import time
from datetime import datetime
from typing import Any

from app.config import settings
from app.models import ContentAnalyzeRequest, RSSAnalyzeRequest
from app.processor import build_dedupe_key, normalize_content, process_content_thread_safe
from app.profiler import profiler
from app.rss import parse_feed
from app.storage import InboxStore


def sort_entries_for_processing(
    entries: list[ContentAnalyzeRequest],
) -> list[ContentAnalyzeRequest]:
    dated_entries: list[tuple[datetime, int, ContentAnalyzeRequest]] = []
    undated_entries: list[ContentAnalyzeRequest] = []
    for index, entry in enumerate(entries):
        published_at = parse_published_at(entry.published_at)
        if published_at is None:
            undated_entries.append(entry)
            continue
        dated_entries.append((published_at, index, entry))
    dated_entries.sort(key=lambda item: (item[0], item[1]))
    return [entry for _, _, entry in dated_entries] + undated_entries


def analyze_one_rss_source(
    inbox_store: InboxStore,
    payload: RSSAnalyzeRequest,
    *,
    include_items: bool = True,
    preserve_source_entry_order: bool = True,
) -> dict[str, Any]:
    t_source = time.monotonic()
    if payload.profile:
        profiler.enable_for_request()
    profiler.reset()

    response_extra: dict[str, Any] = {}
    meta: dict[str, Any] = {}

    if payload.incremental_mode == "until_existing":
        # ---- Path A: until_existing mode ----
        meta, all_entries = parse_feed(
            payload.feed_url,
            source_name=payload.source_name,
            source_category=payload.source_category,
            limit=None,
        )

        source_identity_name = payload.source_name or meta.get("source_name", "")
        source_has_history = inbox_store.has_source_history(
            source_identity_name,
            payload.source_category,
        )

        scan_candidates: list[ContentAnalyzeRequest] = []
        anchor_found = False
        anchor_index: int | None = None

        for i, entry in enumerate(all_entries):
            if i >= payload.probe_limit:
                break
            normalized_stub = normalize_content(entry)
            dedupe_key = build_dedupe_key(normalized_stub)
            if inbox_store.get_by_dedupe_key(dedupe_key):
                anchor_found = True
                anchor_index = i
                break
            scan_candidates.append(entry)

        feed_items_seen = len(scan_candidates) + (1 if anchor_found else 0)
        warnings: list[str] = []

        if anchor_found:
            items_to_process = scan_candidates
            incremental_decision = "until_existing_anchor_found"
        elif not source_has_history:
            items_to_process = all_entries[: payload.new_source_initial_limit]
            incremental_decision = "new_source_initial_baseline"
            warnings.append(
                f"New source: processing first {len(items_to_process)} items as initial baseline "
                f"(new_source_initial_limit={payload.new_source_initial_limit})."
            )
        else:
            items_to_process = all_entries[: payload.old_source_no_anchor_limit]
            incremental_decision = "old_source_no_anchor"
            warnings.append(
                f"This source has history in DB but no existing item was found within "
                f"probe_limit={payload.probe_limit}. Processing first {len(items_to_process)} items "
                f"(old_source_no_anchor_limit={payload.old_source_no_anchor_limit}). "
                f"Possible causes: high-frequency updates, guid/url changes, RSSHub route changes, "
                f"or dedupe rule changes."
            )

        processing_entries = (
            sort_entries_for_processing(items_to_process)
            if preserve_source_entry_order
            else list(items_to_process)
        )

        response_extra = {
            "incremental_mode": "until_existing",
            "incremental_decision": incremental_decision,
            "source_has_history": source_has_history,
            "probe_limit": payload.probe_limit,
            "new_source_initial_limit": payload.new_source_initial_limit,
            "old_source_no_anchor_limit": payload.old_source_no_anchor_limit,
            "feed_items_seen": feed_items_seen,
            "anchor_found": anchor_found,
            "anchor_index": anchor_index,
            "selected_items_for_processing": len(processing_entries),
            "warnings": warnings,
        }

    else:
        # ---- Path B: fixed_limit mode (existing logic, unchanged) ----
        meta, entries = parse_feed(
            payload.feed_url,
            source_name=payload.source_name,
            source_category=payload.source_category,
            limit=payload.limit,
        )
        processing_entries = (
            sort_entries_for_processing(entries) if preserve_source_entry_order else list(entries)
        )

    # ---- Shared processing pipeline ----
    total = len(processing_entries)
    new_items = 0
    duplicate_items = 0
    screened_items = 0
    recommended_items = 0
    new_event_items = 0
    incremental_items = 0
    silent_items = 0
    failed_items = 0
    item_results: list[dict[str, Any]] = []

    for entry in processing_entries:
        try:
            entry.screen = payload.screen
            result = process_content_thread_safe(inbox_store, entry, raw=entry.model_dump())
            if include_items:
                item_results.append(result.model_dump())
            if result.is_duplicate:
                duplicate_items += 1
            else:
                new_items += 1
                if payload.screen:
                    screened_items += 1
            if result.screening.suggested_action in {"read", "save", "transcribe", "review"}:
                recommended_items += 1
            if result.cluster_relation == "new_event":
                new_event_items += 1
            if result.cluster_relation == "incremental_update":
                incremental_items += 1
            if result.notification_decision == "silent":
                silent_items += 1
        except Exception as exc:
            failed_items += 1
            if include_items:
                item_results.append({"ok": False, "error": str(exc), "title": entry.title})

    response: dict[str, Any] = {
        "ok": failed_items == 0,
        "feed_url": payload.feed_url,
        "source_name": meta["source_name"],
        "total_items": total,
        "new_items": new_items,
        "duplicate_items": duplicate_items,
        "screened_items": screened_items,
        "new_event_items": new_event_items,
        "incremental_items": incremental_items,
        "silent_items": silent_items,
        "recommended_items": recommended_items,
        "failed_items": failed_items,
    }
    response.update(response_extra)
    if include_items:
        response["items"] = item_results
    source_total = time.monotonic() - t_source
    profiler.record("source_total_seconds", source_total)
    if profiler.enabled:
        response["profile"] = profiler.collect()
    response["screening_mode"] = settings.screening.get("mode", "two_stage")
    return response


def parse_published_at(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
