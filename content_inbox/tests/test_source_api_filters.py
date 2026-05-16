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


def create_source(client: TestClient, source_id: str, **overrides) -> dict:
    payload = {
        "source_id": source_id,
        "source_name": f"Source {source_id}",
        "source_category": "Tech/AI",
        "feed_url": f"https://example.com/{source_id}.xml",
        "status": "active",
        "priority": 2,
        "tags": ["tech", "ai"],
        "notes": "agent ready",
        "config": {"screen": False},
    }
    payload.update(overrides)
    response = client.post("/api/rss/sources", json=payload)
    assert response.status_code == 200
    return response.json()["source"]


def test_source_list_supports_extended_filters_and_sort(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    create_source(client, "alpha", priority=1, tags=["tech", "ai"])
    create_source(client, "beta", source_category="Media/Video", priority=5, tags=["video"])
    store.record_rss_source_failure(
        "beta",
        run_id="run-beta",
        finished_at="2026-05-16T01:00:00+00:00",
        error_code="rss_fetch_timeout",
        error_message="timeout",
        retryable=True,
    )

    tagged = client.get("/api/rss/sources?tag=ai&sort=priority:desc").json()
    errored = client.get("/api/rss/sources?has_error=true&retryable=true").json()
    keyword = client.get("/api/rss/sources?keyword=agent").json()
    priority = client.get("/api/rss/sources?priority_min=4&priority_max=5").json()

    assert [source["source_id"] for source in tagged["sources"]] == ["alpha"]
    assert [source["source_id"] for source in errored["sources"]] == ["beta"]
    assert {source["source_id"] for source in keyword["sources"]} == {"alpha", "beta"}
    assert [source["source_id"] for source in priority["sources"]] == ["beta"]


def test_get_source_can_include_recent_items_and_health(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    create_source(client, "alpha")
    result = process_content_thread_safe(
        store,
        ContentAnalyzeRequest(
            title="Recent",
            url="https://example.com/recent",
            source_id="alpha",
            feed_url="https://example.com/alpha.xml",
            source_name="Source alpha",
            source_category="Tech/AI",
            content_type="article",
            screen=False,
        ),
    )
    assert result.item_id

    body = client.get("/api/rss/sources/alpha?include_recent_items=true").json()

    assert body["health"]["status"] == "active"
    assert body["latest_ingest"] is None
    assert body["recent_items"][0]["source_id"] == "alpha"
