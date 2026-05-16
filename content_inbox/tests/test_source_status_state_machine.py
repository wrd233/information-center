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


def register(client: TestClient, source_id: str, status: str = "active", fixture: str = "rss_basic.xml") -> None:
    response = client.post(
        "/api/rss/sources",
        json={
            "source_id": source_id,
            "source_name": source_id,
            "source_category": "Fixtures",
            "feed_url": (FIXTURES / fixture).as_uri(),
            "status": status,
            "config": {"screen": False},
        },
    )
    assert response.status_code == 200


def test_paused_source_requires_force_for_manual_ingest(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    register(client, "paused-source", status="paused")

    rejected = client.post("/api/rss/sources/paused-source/ingest", json={"screen": False})
    forced = client.post("/api/rss/sources/paused-source/ingest", json={"screen": False, "force": True, "limit": 1})
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert rejected.status_code == 409
    assert rejected.json()["error"]["error_code"] == "source_paused"
    assert forced.status_code == 200
    assert total == 1


def test_active_source_becomes_broken_after_failure_threshold(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    register(client, "flaky-source", fixture="rss_malformed.xml")

    for _ in range(5):
        client.post("/api/rss/sources/flaky-source/ingest", json={"screen": False})

    source = client.get("/api/rss/sources/flaky-source").json()["source"]
    assert source["status"] == "broken"
    assert source["failure_count"] == 5
    assert source["consecutive_failure_count"] == 5


def test_broken_source_allows_test_mode_without_writing_items(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    register(client, "broken-source", status="broken")

    rejected = client.post("/api/rss/sources/broken-source/ingest", json={"screen": False})
    tested = client.post("/api/rss/sources/broken-source/ingest", json={"test": True, "screen": False, "limit": 1})
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})

    assert rejected.status_code == 409
    assert rejected.json()["error"]["error_code"] == "source_broken"
    assert tested.status_code == 200
    assert tested.json()["run"]["status"] == "success"
    assert total == 0
