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


def register_source(client: TestClient, fixture: str = "rss_basic.xml", **overrides) -> dict:
    payload = {
        "source_id": "fixture-source",
        "source_name": "Fixture Source",
        "source_category": "Fixtures",
        "feed_url": (FIXTURES / fixture).as_uri(),
        "status": "active",
        "priority": 3,
        "tags": ["fixture"],
        "config": {"screen": False, "incremental_mode": "fixed_limit", "limit": 2},
    }
    payload.update(overrides)
    response = client.post("/api/rss/sources", json=payload)
    assert response.status_code == 200
    return response.json()["source"]


def test_registered_source_ingest_success_updates_status_and_items(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    register_source(client)

    response = client.post("/api/rss/sources/fixture-source/ingest", json={"screen": False, "limit": 2, "include_items": True})

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["run"]["source_id"] == "fixture-source"
    assert body["run"]["status"] == "success"
    assert body["run"]["error_code"] is None
    assert body["run"]["stats"]["new_items"] == 2
    assert body["run"]["stats"]["processed_items"] == 2
    assert body["source"]["last_success_at"] is not None
    assert body["source"]["consecutive_failures"] == 0
    items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})
    assert total == 2
    assert {item["source_id"] for item in items} == {"fixture-source"}
    assert {item["feed_url"] for item in items} == {(FIXTURES / "rss_basic.xml").as_uri()}


def test_registered_source_ingest_failure_updates_error_state(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    register_source(client, fixture="rss_malformed.xml")

    response = client.post("/api/rss/sources/fixture-source/ingest", json={"screen": False})
    source = client.get("/api/rss/sources/fixture-source").json()["source"]

    body = response.json()
    assert response.status_code == 400
    assert body["ok"] is False
    assert body["error"]["error_code"] == "rss_parse_error"
    assert body["run"]["status"] == "failed"
    assert body["run"]["error_code"] == "rss_parse_error"
    assert body["run"]["retryable"] is False
    assert source["last_failure_at"] is not None
    assert source["last_error_code"] == "rss_parse_error"
    assert source["consecutive_failures"] == 1


def test_disabled_source_ingest_returns_source_disabled(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    register_source(client, status="disabled")

    response = client.post("/api/rss/sources/fixture-source/ingest", json={"screen": False})

    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "source_disabled"


def test_missing_source_ingest_returns_source_not_found(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post("/api/rss/sources/missing/ingest", json={"screen": False})

    assert response.status_code == 404
    assert response.json()["error"]["error_code"] == "source_not_found"
