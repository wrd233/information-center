from __future__ import annotations

import sqlite3
from pathlib import Path

from app.models import ContentAnalyzeRequest
from app.processor import build_dedupe_key, normalize_content, process_content_thread_safe
from app.storage import InboxStore
from app.utils import normalize_url


def process(store: InboxStore, **overrides):
    payload = ContentAnalyzeRequest(
        title=overrides.pop("title", "Dedupe Title"),
        url=overrides.pop("url", "https://example.com/article"),
        guid=overrides.pop("guid", None),
        source_name=overrides.pop("source_name", "Dedupe Source"),
        summary=overrides.pop("summary", "Dedupe summary"),
        screen=False,
        **overrides,
    )
    return process_content_thread_safe(store, payload, raw=payload.model_dump())


def row_count_for_key(path: Path, dedupe_key: str) -> int:
    with sqlite3.connect(path) as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM inbox_items WHERE dedupe_key = ?", (dedupe_key,)
        ).fetchone()[0]


def test_same_url_dedupes_and_marks_seen_without_overwriting_created_at(tmp_path: Path) -> None:
    db_path = tmp_path / "inbox.sqlite3"
    store = InboxStore(db_path)

    first = process(store, url="https://example.com/post?utm_source=a#frag", title="Original")
    before = store.get_by_dedupe_key(build_dedupe_key(first.normalized))
    second = process(
        store,
        url="https://example.com/post/",
        title="Updated title that should not overwrite original",
        summary="Updated summary",
    )
    after = store.get_by_dedupe_key(build_dedupe_key(first.normalized))

    assert first.is_duplicate is False
    assert second.is_duplicate is True
    assert second.item_id == first.item_id
    assert after["seen_count"] == before["seen_count"] + 1
    assert after["created_at"] == before["created_at"]
    assert after["title"] == "Original"
    assert row_count_for_key(db_path, build_dedupe_key(first.normalized)) == 1


def test_url_normalization_boundaries_are_stable() -> None:
    assert normalize_url("HTTPS://Example.COM/a/?utm_source=x&b=2#section") == "https://example.com/a?b=2"
    assert normalize_url("https://example.com/a?b=2&a=1") == "https://example.com/a?a=1&b=2"
    assert normalize_url("http://example.com/a") != normalize_url("https://example.com/a")


def test_guid_dedupes_within_same_source_when_url_missing(tmp_path: Path) -> None:
    store = InboxStore(tmp_path / "inbox.sqlite3")

    first = process(store, url=None, guid="shared-guid", source_name="Source A", title="A")
    second = process(store, url=None, guid="shared-guid", source_name="Source A", title="B")

    assert first.is_duplicate is False
    assert second.is_duplicate is True
    assert second.item_id == first.item_id


def test_same_guid_different_source_does_not_merge_without_url(tmp_path: Path) -> None:
    store = InboxStore(tmp_path / "inbox.sqlite3")

    first = process(store, url=None, guid="shared-guid", source_name="Source A")
    second = process(store, url=None, guid="shared-guid", source_name="Source B")

    assert first.is_duplicate is False
    assert second.is_duplicate is False
    assert second.item_id != first.item_id


def test_source_title_fallback_dedupes_only_within_same_source(tmp_path: Path) -> None:
    store = InboxStore(tmp_path / "inbox.sqlite3")

    first = process(store, url=None, guid=None, source_name="Source A", title="Same Title")
    second = process(store, url=None, guid=None, source_name="Source A", title="same title")
    third = process(store, url=None, guid=None, source_name="Source B", title="Same Title")

    assert first.is_duplicate is False
    assert second.is_duplicate is True
    assert third.is_duplicate is False
    assert third.item_id != first.item_id


def test_persistent_dedupe_survives_store_recreation(tmp_path: Path) -> None:
    db_path = tmp_path / "inbox.sqlite3"
    first_store = InboxStore(db_path)
    first = process(first_store, url="https://example.com/persist")

    restarted_store = InboxStore(db_path)
    second = process(restarted_store, url="https://example.com/persist#fragment")

    assert first.is_duplicate is False
    assert second.is_duplicate is True
    assert second.item_id == first.item_id


def test_build_dedupe_key_priority_prefers_url_over_guid() -> None:
    with_url_a = normalize_content(
        ContentAnalyzeRequest(
            url="https://example.com/same",
            guid="guid-a",
            title="A",
            source_name="Source",
            summary="summary",
            screen=False,
        )
    )
    with_url_b = normalize_content(
        ContentAnalyzeRequest(
            url="https://example.com/same#x",
            guid="guid-b",
            title="B",
            source_name="Other",
            summary="summary",
            screen=False,
        )
    )

    assert build_dedupe_key(with_url_a) == build_dedupe_key(with_url_b)
