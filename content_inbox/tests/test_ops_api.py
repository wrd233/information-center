from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.server import app
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    db_path = tmp_path / "content_inbox.db"
    store = InboxStore(db_path)
    app.state.store = store
    settings.database_path = db_path
    settings.enable_real_runs = True
    return TestClient(app), store


def test_environment_reports_fresh_database_and_legacy_proof(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    body = client.get("/api/environment").json()

    assert body["ok"] is True
    assert body["data"]["environment"]["is_fresh_database"] is True
    assert body["data"]["environment"]["database_path"].endswith("content_inbox.db")
    assert "legacy_database" in body["data"]


def test_source_import_preview_and_commit(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()

    preview = client.post(
        "/api/sources/import/preview",
        json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"},
    ).json()
    commit = client.post(
        "/api/sources/import/commit",
        json={"operation_id": preview["data"]["operation_id"]},
    ).json()
    listed = client.get("/api/sources").json()

    assert preview["data"]["stats"]["new"] == 1
    assert commit["data"]["stats"] == {"created": 1, "skipped": 0}
    assert listed["data"]["stats"]["total"] == 1


def test_dry_run_does_not_write_items_and_real_run_links_items(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post(
        "/api/sources/import/preview",
        json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"},
    ).json()
    created = client.post(
        "/api/sources/import/commit",
        json={"operation_id": preview["data"]["operation_id"]},
    ).json()["data"]["created"][0]
    source_id = created["source_id"]
    payload = {
        "mode": "dry_run",
        "source_scope": {"type": "selected", "source_ids": [source_id]},
        "limits": {"max_items_per_source": 2, "max_total_items": 10},
        "time_filter": {},
        "run_synchronously": True,
    }

    dry = client.post("/api/runs", json=payload).json()
    _items, dry_total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})
    payload["mode"] = "real_write"
    real = client.post("/api/runs", json=payload).json()
    run_id = real["data"]["run_id"]
    run_items = client.get(f"/api/runs/{run_id}/items").json()
    events = client.get(f"/api/runs/{run_id}/events").json()
    generated_events = client.get("/api/events").json()

    assert dry["ok"] is True
    assert dry_total == 0
    assert real["ok"] is True
    assert run_items["data"]["stats"]["returned"] == 2
    assert any(event["event_type"] == "item_inserted" for event in events["data"]["events"])
    assert generated_events["data"]["events"]


def test_published_time_filter_excludes_out_of_range_items(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post(
        "/api/sources/import/preview",
        json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"},
    ).json()
    source_id = client.post(
        "/api/sources/import/commit",
        json={"operation_id": preview["data"]["operation_id"]},
    ).json()["data"]["created"][0]["source_id"]

    response = client.post(
        "/api/runs",
        json={
            "mode": "real_write",
            "source_scope": {"type": "selected", "source_ids": [source_id]},
            "limits": {"max_items_per_source": 5, "max_total_items": 10},
            "time_filter": {"published_from": "2999-01-01T00:00:00+00:00"},
            "run_synchronously": True,
        },
    ).json()
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 10})
    events = client.get(f"/api/runs/{response['data']['run_id']}/events").json()["data"]["events"]

    assert total == 0
    assert any(event["event_type"] == "item_filtered_by_time" for event in events)
