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


def test_dry_run_returns_run_without_writing_items_or_source_success(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "dry-source",
            "source_name": "Dry Source",
            "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
            "config": {"screen": False},
        },
    )

    response = client.post(
        "/api/rss/sources/dry-source/ingest",
        json={"dry_run": True, "screen": False, "limit": 2, "include_items": True},
    )
    source = client.get("/api/rss/sources/dry-source").json()["source"]
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert response.status_code == 200
    assert response.json()["run"]["stats"]["new_items"] == 2
    assert total == 0
    assert source["last_success_at"] is None


def test_test_mode_writes_run_history_but_not_items(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "test-source",
            "source_name": "Test Source",
            "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
            "config": {"screen": False},
        },
    )

    response = client.post("/api/rss/sources/test-source/ingest", json={"test": True, "screen": False, "limit": 1})
    run_id = response.json()["run"]["run_id"]
    run = client.get(f"/api/rss/runs/{run_id}").json()["run"]
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert response.status_code == 200
    assert run["trigger_type"] == "test"
    assert total == 0


def test_force_allows_broken_source_normal_ingest(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "force-source",
            "source_name": "Force Source",
            "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
            "status": "broken",
            "config": {"screen": False},
        },
    )

    response = client.post("/api/rss/sources/force-source/ingest", json={"force": True, "screen": False, "limit": 1})
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert response.status_code == 200
    assert response.json()["source"]["consecutive_failure_count"] == 0
    assert total == 1
