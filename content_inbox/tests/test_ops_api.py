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


def test_reset_preview_and_commit_keep_sources(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"}).json()
    source_id = client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]}).json()["data"]["created"][0]["source_id"]
    run = client.post(
        "/api/runs",
        json={"mode": "real_write", "source_scope": {"type": "selected", "source_ids": [source_id]}, "limits": {"max_items_per_source": 1}, "time_filter": {}, "run_synchronously": True},
    ).json()

    reset_preview = client.post("/api/environment/reset/preview", json={"level": "clear_runs_items_keep_sources"}).json()
    reset = client.post("/api/environment/reset/commit", json={"level": "clear_runs_items_keep_sources", "operation_id": reset_preview["data"]["operation_id"], "confirmation": "RESET"}).json()
    sources = client.get("/api/sources").json()
    items = client.get("/api/items").json()

    assert run["ok"] is True
    assert reset["ok"] is True
    assert sources["data"]["stats"]["total"] == 1
    assert items["data"]["stats"]["returned"] == 0


def test_reset_clear_all_sources_and_content_and_audit(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"}).json()
    client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]})

    reset_preview = client.post("/api/environment/reset/preview", json={"level": "clear_all_sources_and_content"}).json()
    reset = client.post("/api/environment/reset/commit", json={"level": "clear_all_sources_and_content", "operation_id": reset_preview["data"]["operation_id"], "confirmation": "RESET"}).json()
    sources = client.get("/api/sources").json()
    env = client.get("/api/environment").json()

    assert reset["data"]["legacy_db_affected"] is False
    assert sources["data"]["stats"]["total"] == 0
    assert env["data"]["environment"]["last_reset_at"]


def test_reset_disabled_on_non_fresh_database(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    client.get("/api/environment")
    with store.connect() as conn:
        conn.execute("UPDATE system_metadata SET value = 'false' WHERE key = 'is_fresh_database'")

    response = client.post("/api/environment/reset/preview", json={"level": "clear_runs_items_keep_sources"})

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "FRESH_DB_REQUIRED"


def test_source_check_archive_restore_and_bulk_preview_commit(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    check = client.post("/api/sources/check", json={"feed_url": feed_uri, "source_name": "Fixture"}).json()
    source = client.post("/api/sources", json={"source_name": "Fixture", "feed_url": feed_uri, "source_category": "Tests"}).json()["data"]["source"]
    archived = client.post(f"/api/sources/{source['source_id']}/archive", json={}).json()
    restored = client.post(f"/api/sources/{source['source_id']}/restore", json={}).json()
    bulk_preview = client.post("/api/sources/bulk/preview", json={"action": "disable", "source_ids": [source["source_id"]]}).json()
    bulk = client.post("/api/sources/bulk/commit", json={"operation_id": bulk_preview["data"]["operation_id"]}).json()

    assert check["data"]["parse_ok"] is True
    assert archived["data"]["status"] == "archived"
    assert restored["data"]["source"]["status"] == "active"
    assert bulk["data"]["count"] == 1


def test_pipeline_stage_briefing_and_report(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"}).json()
    source_id = client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]}).json()["data"]["created"][0]["source_id"]
    run_id = client.post(
        "/api/runs",
        json={"mode": "real_write", "source_scope": {"type": "selected", "source_ids": [source_id]}, "limits": {"max_items_per_source": 2}, "time_filter": {}, "run_synchronously": True},
    ).json()["data"]["run_id"]

    dedupe = client.post(f"/api/runs/{run_id}/pipeline/dedupe", json={}).json()
    semantic = client.post(f"/api/runs/{run_id}/pipeline/semantic", json={}).json()
    briefing = client.post(f"/api/runs/{run_id}/briefing", json={}).json()
    report = client.post(f"/api/runs/{run_id}/report", json={}).json()

    assert dedupe["data"]["pipeline"]["dedupe"] == "completed"
    assert semantic["data"]["pipeline"]["semantic"] == "completed"
    assert briefing["data"]["pipeline"]["briefing"] == "completed"
    assert report["data"]["pipeline"]["report"] == "completed"


def test_reset_clear_pipeline_outputs_keeps_items_and_runs(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"}).json()
    source_id = client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]}).json()["data"]["created"][0]["source_id"]
    run_id = client.post(
        "/api/runs",
        json={"mode": "real_write", "source_scope": {"type": "selected", "source_ids": [source_id]}, "limits": {"max_items_per_source": 2}, "time_filter": {}, "run_synchronously": True},
    ).json()["data"]["run_id"]
    client.post(f"/api/runs/{run_id}/pipeline/dedupe", json={})
    before_items = client.get("/api/items").json()["data"]["stats"]["returned"]
    assert client.get("/api/events").json()["data"]["events"]

    reset_preview = client.post("/api/environment/reset/preview", json={"level": "clear_pipeline_outputs_keep_items"}).json()
    reset = client.post("/api/environment/reset/commit", json={"level": "clear_pipeline_outputs_keep_items", "operation_id": reset_preview["data"]["operation_id"], "confirmation": "RESET"}).json()

    assert reset["ok"] is True
    assert client.get("/api/items").json()["data"]["stats"]["returned"] == before_items
    assert client.get("/api/runs").json()["data"]["stats"]["total"] == 1
    assert client.get("/api/events").json()["data"]["events"] == []
    assert reset["data"]["legacy_db_affected"] is False


def test_reset_clear_outputs_keeps_events(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"}).json()
    source_id = client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]}).json()["data"]["created"][0]["source_id"]
    run_id = client.post(
        "/api/runs",
        json={"mode": "real_write", "source_scope": {"type": "selected", "source_ids": [source_id]}, "limits": {"max_items_per_source": 1}, "time_filter": {}, "run_synchronously": True},
    ).json()["data"]["run_id"]
    client.post(f"/api/runs/{run_id}/briefing", json={})
    client.post(f"/api/runs/{run_id}/report", json={})
    events_before = client.get("/api/events").json()["data"]["events"]
    assert events_before
    assert client.get("/api/reports").json()["data"]["reports"]

    reset_preview = client.post("/api/environment/reset/preview", json={"level": "clear_outputs_keep_events"}).json()
    reset = client.post("/api/environment/reset/commit", json={"level": "clear_outputs_keep_events", "operation_id": reset_preview["data"]["operation_id"], "confirmation": "RESET"}).json()

    assert reset["ok"] is True
    assert client.get("/api/events").json()["data"]["events"]
    assert client.get("/api/reports").json()["data"]["reports"] == []
    assert client.get("/api/briefings/daily").json()["data"]["briefings"] == []


def test_reset_clear_by_run_id_preserves_shared_items(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_uri = (FIXTURES / "rss_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_uri}, Fixture Source, Tests"}).json()
    source_id = client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]}).json()["data"]["created"][0]["source_id"]
    payload = {"mode": "real_write", "source_scope": {"type": "selected", "source_ids": [source_id]}, "limits": {"max_items_per_source": 1}, "time_filter": {}, "run_synchronously": True}
    run_1 = client.post("/api/runs", json=payload).json()["data"]["run_id"]
    run_2 = client.post("/api/runs", json=payload).json()["data"]["run_id"]
    assert client.get(f"/api/runs/{run_2}/items").json()["data"]["stats"]["returned"] == 1

    reset_preview = client.post("/api/environment/reset/preview", json={"level": "clear_by_run_id", "run_id": run_2}).json()
    reset = client.post("/api/environment/reset/commit", json={"level": "clear_by_run_id", "run_id": run_2, "operation_id": reset_preview["data"]["operation_id"], "confirmation": f"RESET {run_2}"}).json()

    assert reset["ok"] is True
    assert client.get(f"/api/runs/{run_1}/items").json()["data"]["stats"]["returned"] == 1
    assert client.get(f"/api/runs/{run_2}").status_code == 404
    assert client.get("/api/items").json()["data"]["stats"]["returned"] == 1


def test_reset_clear_by_source_id_does_not_delete_other_source_items(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    feed_a = (FIXTURES / "rss_basic.xml").as_uri()
    feed_b = (FIXTURES / "atom_basic.xml").as_uri()
    preview = client.post("/api/sources/import/preview", json={"format": "urls", "content": f"{feed_a}, RSS Source, Tests\n{feed_b}, Atom Source, Tests"}).json()
    created = client.post("/api/sources/import/commit", json={"operation_id": preview["data"]["operation_id"]}).json()["data"]["created"]
    source_a, source_b = created[0]["source_id"], created[1]["source_id"]
    for source_id in [source_a, source_b]:
        client.post(
            "/api/runs",
            json={"mode": "real_write", "source_scope": {"type": "selected", "source_ids": [source_id]}, "limits": {"max_items_per_source": 1}, "time_filter": {}, "run_synchronously": True},
        )
    assert client.get("/api/items").json()["data"]["stats"]["returned"] == 2

    reset_preview = client.post("/api/environment/reset/preview", json={"level": "clear_by_source_id", "source_ids": [source_a], "archive_sources": True}).json()
    reset = client.post("/api/environment/reset/commit", json={"level": "clear_by_source_id", "source_ids": [source_a], "archive_sources": True, "operation_id": reset_preview["data"]["operation_id"], "confirmation": f"RESET {source_a}"}).json()

    assert reset["ok"] is True
    remaining = client.get("/api/items").json()["data"]["items"]
    assert len(remaining) == 1
    assert remaining[0]["source_id"] == source_b
    source_a_detail = client.get(f"/api/sources/{source_a}").json()["data"]["source"]
    assert source_a_detail["status"] == "archived"
