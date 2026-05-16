from __future__ import annotations

from app.models import ContentAnalyzeRequest
from app.rss_runner import sort_entries_for_processing


def entry(title: str, published_at: str | None) -> ContentAnalyzeRequest:
    return ContentAnalyzeRequest(title=title, source_name="Order", published_at=published_at, screen=False)


def test_process_order_feed_preserves_source_order() -> None:
    entries = [entry("new", "2026-05-16T00:00:00Z"), entry("old", "2026-05-15T00:00:00Z"), entry("none", None)]

    assert [item.title for item in sort_entries_for_processing(entries, process_order="feed")] == ["new", "old", "none"]


def test_process_order_oldest_first_places_undated_last() -> None:
    entries = [entry("new", "2026-05-16T00:00:00Z"), entry("none", None), entry("old", "2026-05-15T00:00:00Z")]

    assert [item.title for item in sort_entries_for_processing(entries, process_order="oldest_first")] == ["old", "new", "none"]


def test_process_order_newest_first_places_undated_last() -> None:
    entries = [entry("old", "2026-05-15T00:00:00Z"), entry("none", None), entry("new", "2026-05-16T00:00:00Z")]

    assert [item.title for item in sort_entries_for_processing(entries, process_order="newest_first")] == ["new", "old", "none"]
