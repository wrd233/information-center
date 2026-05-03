from __future__ import annotations

from datetime import datetime
from typing import Any

from app.models import ContentAnalyzeRequest, RSSAnalyzeRequest
from app.processor import process_content_thread_safe
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
    meta, entries = parse_feed(
        payload.feed_url,
        source_name=payload.source_name,
        source_category=payload.source_category,
        limit=payload.limit,
    )
    processing_entries = (
        sort_entries_for_processing(entries) if preserve_source_entry_order else list(entries)
    )

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
    if include_items:
        response["items"] = item_results
    return response


def parse_published_at(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
