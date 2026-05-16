from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.models import RSSAnalyzeRequest, RSSBatchAnalyzeRequest
from app.rss_runner import analyze_one_rss_source
from app.storage import InboxStore


class RSSBatchRunner:
    def __init__(self, inbox_store: InboxStore):
        self.inbox_store = inbox_store

    def run(self, payload: RSSBatchAnalyzeRequest) -> dict[str, Any]:
        source_results: list[dict[str, Any] | None] = [None] * len(payload.sources)
        with ThreadPoolExecutor(max_workers=payload.max_concurrent_sources) as executor:
            futures = {
                executor.submit(self._run_one_source, index, payload): index
                for index in range(len(payload.sources))
            }
            for future in as_completed(futures):
                index = futures[future]
                source_results[index] = future.result()

        ordered_results = [result for result in source_results if result is not None]
        summary = summarize_batch_results(
            ordered_results,
            max_concurrent_sources=payload.max_concurrent_sources,
        )
        summary["source_results"] = ordered_results
        return summary

    def _run_one_source(self, index: int, payload: RSSBatchAnalyzeRequest) -> dict[str, Any]:
        source = payload.sources[index]
        source_payload = RSSAnalyzeRequest(
            feed_url=source.feed_url,
            source_id=source.source_id,
            source_name=source.source_name,
            source_category=source.source_category,
            limit=source.limit if source.limit is not None else payload.limit_per_source,
            screen=source.screen if source.screen is not None else payload.screen,
            incremental_mode=(
                source.incremental_mode
                if source.incremental_mode is not None
                else payload.incremental_mode
            ),
            probe_limit=(
                source.probe_limit
                if source.probe_limit is not None
                else payload.probe_limit
            ),
            new_source_initial_limit=(
                source.new_source_initial_limit
                if source.new_source_initial_limit is not None
                else payload.new_source_initial_limit
            ),
            old_source_no_anchor_limit=(
                source.old_source_no_anchor_limit
                if source.old_source_no_anchor_limit is not None
                else payload.old_source_no_anchor_limit
            ),
            stop_on_first_existing=(
                source.stop_on_first_existing
                if source.stop_on_first_existing is not None
                else payload.stop_on_first_existing
            ),
        )
        try:
            result = analyze_one_rss_source(
                self.inbox_store,
                source_payload,
                include_items=payload.include_items,
                preserve_source_entry_order=payload.preserve_source_entry_order,
            )
            return {
                "source_id": source.source_id,
                "source_index": index,
                "source_category": source.source_category,
                **result,
            }
        except Exception as exc:
            failed_result: dict[str, Any] = {
                "ok": False,
                "source_id": source.source_id,
                "source_index": index,
                "feed_url": source.feed_url,
                "source_name": source.source_name,
                "source_category": source.source_category,
                "error": str(exc),
                "total_items": 0,
                "new_items": 0,
                "duplicate_items": 0,
                "screened_items": 0,
                "new_event_items": 0,
                "incremental_items": 0,
                "silent_items": 0,
                "recommended_items": 0,
                "failed_items": 0,
            }
            if payload.include_items:
                failed_result["items"] = []
            return failed_result


def summarize_batch_results(
    source_results: list[dict[str, Any]],
    *,
    max_concurrent_sources: int,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "ok": True,
        "total_sources": len(source_results),
        "successful_sources": 0,
        "failed_sources": 0,
        "partial_failed_sources": 0,
        "total_items": 0,
        "new_items": 0,
        "duplicate_items": 0,
        "screened_items": 0,
        "recommended_items": 0,
        "new_event_items": 0,
        "incremental_items": 0,
        "silent_items": 0,
        "failed_items": 0,
        "max_concurrent_sources": max_concurrent_sources,
    }
    for result in source_results:
        failed_by_source = int(result.get("failed_items", 0))
        total_items = int(result.get("total_items", 0))
        if "error" in result:
            summary["failed_sources"] += 1
        elif failed_by_source > 0 and failed_by_source < total_items:
            summary["partial_failed_sources"] += 1
        elif failed_by_source > 0 and failed_by_source == total_items:
            summary["failed_sources"] += 1
        else:
            summary["successful_sources"] += 1

        for key in (
            "total_items",
            "new_items",
            "duplicate_items",
            "screened_items",
            "recommended_items",
            "new_event_items",
            "incremental_items",
            "silent_items",
            "failed_items",
        ):
            summary[key] += int(result.get(key, 0))

    summary["ok"] = summary["failed_sources"] == 0 and summary["partial_failed_sources"] == 0
    return summary
