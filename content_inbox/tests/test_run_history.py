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


def test_source_ingest_writes_run_history_and_run_source_rows(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "run-source",
            "source_name": "Run Source",
            "source_category": "Fixtures",
            "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
            "config": {"screen": False},
        },
    )

    ingest = client.post("/api/rss/sources/run-source/ingest", json={"screen": False, "limit": 1}).json()
    run_id = ingest["run"]["run_id"]
    listed = client.get("/api/rss/runs").json()
    detail = client.get(f"/api/rss/runs/{run_id}").json()
    sources = client.get(f"/api/rss/runs/{run_id}/sources").json()

    assert listed["ok"] is True
    assert listed["stats"]["total"] == 1
    assert detail["run"]["run_id"] == run_id
    assert detail["run"]["status"] == "success"
    assert sources["sources"][0]["source_id"] == "run-source"
    assert sources["sources"][0]["new_items_count"] == 1


def test_failed_source_ingest_writes_failed_run_history(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "bad-source",
            "source_name": "Bad Source",
            "feed_url": (FIXTURES / "rss_malformed.xml").as_uri(),
            "config": {"screen": False},
        },
    )

    failed = client.post("/api/rss/sources/bad-source/ingest", json={"screen": False}).json()
    run_id = failed["run"]["run_id"]
    detail = client.get(f"/api/rss/runs/{run_id}").json()
    sources = client.get(f"/api/rss/runs/{run_id}/sources").json()

    assert detail["run"]["status"] == "failed"
    assert detail["run"]["error_code"] == "rss_parse_error"
    assert sources["sources"][0]["status"] == "failed"
    assert sources["sources"][0]["error_code"] == "rss_parse_error"
