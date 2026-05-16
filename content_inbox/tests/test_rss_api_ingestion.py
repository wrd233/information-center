from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.server import app, get_store
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def fixture_uri(name: str) -> str:
    return (FIXTURES / name).as_uri()


def test_rss_analyze_screen_false_ingests_fixture_without_llm(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_basic.xml"),
            "source_category": "Fixtures/Core",
            "limit": 2,
            "screen": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["feed_url"] == fixture_uri("rss_basic.xml")
    assert body["source_name"] == "Fixture Basic RSS"
    assert body["total_items"] == 2
    assert body["new_items"] == 2
    assert body["duplicate_items"] == 0
    assert body["failed_items"] == 0
    assert len(body["items"]) == 2
    assert body["items"][0]["screening"]["screening_method"] == "none"


def test_rss_analyze_repeated_feed_returns_duplicates(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    payload = {"feed_url": fixture_uri("rss_basic.xml"), "limit": 2, "screen": False}

    first = client.post("/api/rss/analyze", json=payload).json()
    second = client.post("/api/rss/analyze", json=payload).json()

    assert first["new_items"] == 2
    assert second["new_items"] == 0
    assert second["duplicate_items"] == 2
    items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})
    assert total == 2
    assert sorted(item["seen_count"] for item in items) == [2, 2]


def test_rss_analyze_feed_internal_duplicate_is_counted_not_failed(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze",
        json={"feed_url": fixture_uri("rss_duplicate_items.xml"), "limit": 5, "screen": False},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["new_items"] == 1
    assert body["duplicate_items"] == 1
    assert body["failed_items"] == 0
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})
    assert total == 1


def test_rss_analyze_malformed_feed_returns_400_with_detail(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze",
        json={"feed_url": fixture_uri("rss_malformed.xml"), "screen": False},
    )

    assert response.status_code == 400
    assert response.json()["error"]["error_code"] == "rss_parse_error"
