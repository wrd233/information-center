from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def source_payload(**overrides):
    payload = {
        "source_id": "rsshub-36kr",
        "source_name": "36氪",
        "source_category": "科技/商业",
        "feed_url": "https://example.com/36kr/rss?utm_source=test",
        "status": "active",
        "priority": 2,
        "tags": ["tech", "business"],
        "notes": "RSSHub route",
        "config": {"incremental_mode": "until_existing", "screen": False},
    }
    payload.update(overrides)
    return payload


def test_register_source_success(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post("/api/rss/sources", json=source_payload())

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["created"] is True
    assert body["source"]["source_id"] == "rsshub-36kr"
    assert body["source"]["normalized_feed_url"] == "https://example.com/36kr/rss"
    assert body["source"]["config"]["screen"] is False


def test_register_source_auto_generates_stable_source_id(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    payload = source_payload(source_id=None, feed_url="https://example.com/auto")

    response = client.post("/api/rss/sources", json=payload)

    body = response.json()
    assert response.status_code == 200
    assert body["source"]["source_id"] == store.generate_source_id("https://example.com/auto")


def test_register_duplicate_source_id_conflict(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    assert client.post("/api/rss/sources", json=source_payload()).status_code == 200

    response = client.post(
        "/api/rss/sources",
        json=source_payload(feed_url="https://example.com/other"),
    )

    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "source_conflict"


def test_register_duplicate_normalized_feed_url_conflict(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    assert client.post("/api/rss/sources", json=source_payload()).status_code == 200

    response = client.post(
        "/api/rss/sources",
        json=source_payload(source_id="other", feed_url="https://example.com/36kr/rss#fragment"),
    )

    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "source_conflict"


def test_list_sources_filters_and_stats(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    client.post("/api/rss/sources", json=source_payload(source_id="active-a", status="active"))
    client.post(
        "/api/rss/sources",
        json=source_payload(
            source_id="paused-a",
            feed_url="https://example.com/paused",
            status="paused",
            source_category="科技/AI",
        ),
    )

    response = client.get("/api/rss/sources?status=paused&category=AI&limit=1&offset=0")

    body = response.json()
    assert response.status_code == 200
    assert [source["source_id"] for source in body["sources"]] == ["paused-a"]
    assert body["stats"] == {"total": 2, "active": 1, "paused": 1, "disabled": 0, "broken": 0}


def test_get_missing_source_returns_structured_not_found(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.get("/api/rss/sources/missing")

    assert response.status_code == 404
    assert response.json()["error"]["error_code"] == "source_not_found"


def test_patch_updates_status_priority_config_and_feed_url_conflict(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    client.post("/api/rss/sources", json=source_payload())
    client.post(
        "/api/rss/sources",
        json=source_payload(source_id="other", feed_url="https://example.com/other"),
    )

    response = client.patch(
        "/api/rss/sources/rsshub-36kr",
        json={"status": "paused", "priority": 4, "config": {"screen": False, "limit": 7}},
    )
    conflict = client.patch(
        "/api/rss/sources/rsshub-36kr",
        json={"feed_url": "https://example.com/other"},
    )

    assert response.status_code == 200
    assert response.json()["source"]["status"] == "paused"
    assert response.json()["source"]["priority"] == 4
    assert response.json()["source"]["config"]["limit"] == 7
    assert conflict.status_code == 409
    assert conflict.json()["error"]["error_code"] == "source_conflict"


def test_delete_soft_disables_source(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    client.post("/api/rss/sources", json=source_payload())

    response = client.delete("/api/rss/sources/rsshub-36kr")
    get_response = client.get("/api/rss/sources/rsshub-36kr")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "source_id": "rsshub-36kr", "status": "disabled"}
    assert get_response.json()["source"]["status"] == "disabled"
