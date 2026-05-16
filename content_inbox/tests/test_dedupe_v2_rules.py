from __future__ import annotations

from app.dedupe import build_dedupe_key
from app.models import ContentAnalyzeRequest
from app.processor import normalize_content, process_content_thread_safe
from app.storage import InboxStore


def key(payload: ContentAnalyzeRequest) -> str:
    return build_dedupe_key(normalize_content(payload))


def test_missing_link_guid_uses_guid_not_url_dedupe() -> None:
    payload_a = ContentAnalyzeRequest(
        title="No Link",
        source_id="source-a",
        source_name="Source A",
        guid="guid-only",
        screen=False,
    )
    payload_b = ContentAnalyzeRequest(
        title="Changed Title",
        source_id="source-a",
        source_name="Source A",
        guid="guid-only",
        screen=False,
    )
    other_source = ContentAnalyzeRequest(
        title="No Link",
        source_id="source-b",
        source_name="Source B",
        guid="guid-only",
        screen=False,
    )

    assert key(payload_a) == key(payload_b)
    assert key(payload_a) != key(other_source)


def test_same_title_different_published_dates_do_not_merge() -> None:
    base = {
        "title": "Daily Brief",
        "source_id": "source-a",
        "source_name": "Source A",
        "summary": "same title different day",
        "screen": False,
    }

    first = key(ContentAnalyzeRequest(**base, published_at="2026-05-15T08:00:00Z"))
    second = key(ContentAnalyzeRequest(**base, published_at="2026-05-16T08:00:00Z"))

    assert first != second


def test_http_https_are_not_canonicalized_by_default() -> None:
    http_key = key(
        ContentAnalyzeRequest(
            title="URL",
            url="http://example.com/path?utm_source=x#frag",
            source_name="Source",
            screen=False,
        )
    )
    https_key = key(
        ContentAnalyzeRequest(
            title="URL",
            url="https://example.com/path",
            source_name="Source",
            screen=False,
        )
    )

    assert http_key != https_key
    assert "#frag" not in http_key
    assert "utm_source" not in http_key


def test_duplicate_updates_latest_fields_without_overwriting_first_content(tmp_path) -> None:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    first = ContentAnalyzeRequest(
        title="Stable Title",
        url="https://example.com/stable",
        source_name="Source",
        summary="first summary",
        screen=False,
    )
    second = ContentAnalyzeRequest(
        title="Stable Title Changed",
        url="https://example.com/stable",
        source_name="Source",
        summary="latest summary",
        screen=False,
    )

    process_content_thread_safe(store, first, raw={"version": 1})
    duplicate = process_content_thread_safe(store, second, raw={"version": 2})
    items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert duplicate.is_duplicate is True
    assert total == 1
    assert items[0]["summary"] == "first summary"
    assert items[0]["latest_seen_summary"] == "latest summary"
    assert '"version": 2' in items[0]["latest_raw_json"]
