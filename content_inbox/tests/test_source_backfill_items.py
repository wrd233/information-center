from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.models import ContentAnalyzeRequest
from app.processor import process_content_thread_safe
from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def test_backfill_items_dry_run_and_apply_match_by_feed_url(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "source-a",
            "source_name": "Source A",
            "feed_url": "https://example.com/a.xml",
        },
    )
    process_content_thread_safe(
        store,
        ContentAnalyzeRequest(
            title="Needs Backfill",
            url="https://example.com/item",
            feed_url="https://example.com/a.xml#fragment",
            source_name="Source A",
            screen=False,
        ),
    )
    with store.connect() as conn:
        conn.execute("UPDATE inbox_items SET source_id = NULL WHERE title = ?", ("Needs Backfill",))

    dry = client.post("/api/rss/backfill-items?apply=false").json()
    applied = client.post("/api/rss/backfill-items?apply=true").json()
    items, _total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert dry["stats"]["matched"] == 1
    assert dry["stats"]["updated"] == 0
    assert applied["stats"]["updated"] == 1
    assert items[0]["source_id"] == "source-a"


def test_backfill_ambiguous_name_category_does_not_write(tmp_path: Path) -> None:
    _client, store = make_client(tmp_path)
    for source_id, feed_url in [("a", "https://example.com/a.xml"), ("b", "https://example.com/b.xml")]:
        store.create_rss_source(
            {
                "source_id": source_id,
                "source_name": "Same",
                "source_category": "SameCat",
                "feed_url": feed_url,
            }
        )
    process_content_thread_safe(
        store,
        ContentAnalyzeRequest(title="Ambiguous", url="https://example.com/item", source_name="Same", source_category="SameCat", screen=False),
    )

    from app.source_backfill import backfill_items

    result = backfill_items(store, apply=True)
    items, _total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert result["stats"]["ambiguous"] == 1
    assert items[0]["source_id"] is None
