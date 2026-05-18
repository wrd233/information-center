from __future__ import annotations

from fastapi.testclient import TestClient

from app.backend_client import BackendClient
from app.main import create_app


def fake_response(path: str) -> dict:
    data = {
        "/api/environment": {
            "environment": {
                "database_label": "fresh_test",
                "database_path": "/tmp/fresh/content_inbox.db",
                "database_id": "db_test",
                "schema_version": "operational_v1",
                "is_fresh_database": True,
                "source_count": 1,
                "item_count": 2,
                "run_count": 1,
                "real_runs_enabled": True,
            },
            "legacy_database": {"path": "/legacy/content_inbox.sqlite3", "exists": True, "size": 10, "modified_at": "now", "sha256": "abc"},
        },
        "/api/environment/health": {"checks": [{"name": "fresh_database", "ok": True, "message": "fresh_test"}]},
        "/api/sources": {"sources": [{"source_id": "source-a", "source_name": "Source A", "feed_url": "file:///feed.xml", "status": "active"}], "stats": {"total": 1, "active": 1}},
        "/api/runs": {"runs": [{"run_id": "run_1", "status": "success", "request": {"mode": "dry_run"}, "selected_source_count": 1, "new_items_count": 0, "started_at": "now"}]},
        "/api/events": {"events": [{"event_id": "event_1", "event_title": "Event A", "status": "needs_review"}]},
        "/api/review-queue": {"reviews": [{"id": 1, "review_type": "event_candidate", "target_type": "event", "target_id": "event_1"}]},
        "/api/items": {"items": [{"item_id": "item_1", "title": "Item A", "source_name": "Source A", "published_at": "now", "primary_cluster_id": "cluster_1"}]},
        "/api/clusters": {"clusters": [{"cluster_id": "cluster_1", "cluster_title": "Cluster A"}]},
        "/api/entities": {"entities": [{"entity_id": "ent_1", "entity_name": "OpenAI"}]},
        "/api/relations": {"relations": []},
        "/api/claims": {"claims": []},
        "/api/topics": {"topics": []},
        "/api/timeline": {"timeline": []},
        "/api/dedupe-groups": {"dedupe_groups": []},
        "/api/briefings/daily": {"briefings": []},
        "/api/reports": {"reports": []},
    }
    if path.startswith("/api/runs/run_1/summary"):
        return {"run": {"run_id": "run_1", "status": "success", "selected_source_count": 1, "new_items_count": 0, "duplicate_items_count": 0}, "sources": [], "recent_events": []}
    if path.startswith("/api/runs/run_1/events"):
        return {"events": [{"seq": 1, "event_type": "run_completed", "message": "done"}]}
    if path.startswith("/api/runs/run_1/items"):
        return {"items": []}
    if path.startswith("/api/items/item_1"):
        return {"item": {"item_id": "item_1", "title": "Item A"}, "semantic": [], "entities": []}
    if path.startswith("/api/sources/source-a"):
        return {"source": {"source_id": "source-a", "source_name": "Source A", "feed_url": "file:///feed.xml"}, "recent_items": [], "audit": []}
    return data.get(path, {})


def patch_backend(monkeypatch):
    def request(self, method, path, params=None, json=None):
        if path == "/api/sources/import/preview":
            return {"ok": True, "data": {"operation_id": "op_1", "stats": {"new": 1}, "sources": [{"source_name": "Source A", "feed_url": "file:///feed.xml", "status": "new"}]}, "error": None, "meta": {}}
        if path == "/api/runs/preview":
            return {"ok": True, "data": {"mode": json["mode"], "source_count": 1, "sources": [], "will_write_items": json["mode"] == "real_write"}, "error": None, "meta": {}}
        return {"ok": True, "data": fake_response(path), "error": None, "meta": {}}

    monkeypatch.setattr(BackendClient, "request", request)


def test_core_console_pages_render(monkeypatch):
    patch_backend(monkeypatch)
    client = TestClient(create_app())

    for path in [
        "/dashboard",
        "/environment",
        "/sources",
        "/runs",
        "/runs/new",
        "/items",
        "/dedupe-groups",
        "/clusters",
        "/events",
        "/entities",
        "/relations",
        "/claims",
        "/topics",
        "/timeline",
        "/review-queue",
        "/briefings",
        "/reports",
        "/agent-query",
        "/settings",
    ]:
        response = client.get(path)
        assert response.status_code == 200, path


def test_source_import_preview_and_run_preview_render(monkeypatch):
    patch_backend(monkeypatch)
    client = TestClient(create_app())

    source_preview = client.post("/sources/import/preview", data={"format": "urls", "content": "file:///feed.xml, Source A"})
    run_preview = client.post("/runs/preview", data={"source_ids": "source-a", "mode": "dry_run", "published_from": "", "published_to": "", "max_items_per_source": "2", "max_total_items": "10"})

    assert source_preview.status_code == 200
    assert "Import Preview" in source_preview.text
    assert run_preview.status_code == 200
    assert "Run Preview" in run_preview.text


def test_detail_pages_render(monkeypatch):
    patch_backend(monkeypatch)
    client = TestClient(create_app())

    assert client.get("/sources/source-a").status_code == 200
    assert client.get("/runs/run_1").status_code == 200
    assert client.get("/items/item_1").status_code == 200
