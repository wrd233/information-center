from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> TestClient:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app)


def test_content_analyze_deduplicates_without_rescreening(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    payload = {
        "url": "https://example.com/article#fragment",
        "title": "AI Agent 自动化实践",
        "source_name": "Manual",
        "source_category": "Articles/AI",
        "summary": "介绍 AI Agent 如何帮助个人信息管理。",
        "screen": False,
    }

    first = client.post("/api/content/analyze", json=payload)
    second = client.post("/api/content/analyze", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    first_body = first.json()
    second_body = second.json()
    assert first_body["is_duplicate"] is False
    assert second_body["is_duplicate"] is True
    assert first_body["item_id"] == second_body["item_id"]
    assert first_body["screening"]["screening_method"] == "none"


def test_rss_analyze_and_query_inbox(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    feed_path = Path(__file__).parent / "sample_feed.xml"

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": feed_path.as_uri(),
            "source_category": "Articles/AI",
            "limit": 2,
            "screen": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["total_items"] == 2
    assert body["new_items"] == 2

    inbox = client.get("/api/inbox?min_score=3&limit=10")
    assert inbox.status_code == 200
    inbox_body = inbox.json()
    assert inbox_body["ok"] is True
    assert len(inbox_body["items"]) == 2
    assert inbox_body["items"][0]["screening"]["suggested_action"] == "review"


def test_screen_true_requires_model_key(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    old_key = settings.openai_api_key
    settings.openai_api_key = ""
    try:
        response = client.post(
            "/api/content/analyze",
            json={
                "title": "需要模型粗筛的内容",
                "summary": "没有 API key 时不应该走本地粗筛。",
                "screen": True,
            },
        )
    finally:
        settings.openai_api_key = old_key
    assert response.status_code == 502
    assert "requires" in response.json()["detail"]
