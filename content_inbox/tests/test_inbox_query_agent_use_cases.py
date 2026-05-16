from __future__ import annotations

import json
from datetime import date, datetime, time, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from app.models import NormalizedContent, ScreeningResult
from app.server import app, get_store, resolve_date_filters
from app.storage import InboxStore


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def screening(action: str = "review", score: int = 3) -> ScreeningResult:
    return ScreeningResult(
        summary="Agent query summary",
        category="Agent",
        value_score=score,
        personal_relevance=score,
        suggested_action=action,
        followup_type="manual_review" if action == "review" else "none",
        reason="test",
        screening_method="none",
        screening_status="ok",
    )


def insert_item(
    store: InboxStore,
    *,
    dedupe_key: str,
    title: str,
    source_name: str = "Query Source",
    source_category: str = "Query/Category",
    content_type: str = "article",
    summary: str = "Agent query summary",
    created_at: str,
    action: str = "review",
) -> str:
    inserted = store.insert(
        dedupe_key,
        NormalizedContent(
            title=title,
            url=f"https://query.example.com/{dedupe_key}",
            source_name=source_name,
            source_category=source_category,
            content_type=content_type,
            summary=summary,
            published_at=created_at,
        ),
        screening(action=action),
    )
    with store.connect() as conn:
        conn.execute(
            """
            UPDATE inbox_items
            SET created_at = ?, updated_at = ?, last_seen_at = ?
            WHERE item_id = ?
            """,
            (created_at, created_at, created_at, inserted["item_id"]),
        )
    return inserted["item_id"]


def test_date_today_uses_utc_date_boundaries() -> None:
    filters = resolve_date_filters("today", None, None)
    target = date.today()

    assert filters["from"] == datetime.combine(target, time.min, tzinfo=timezone.utc).isoformat()
    assert filters["to"] == datetime.combine(target, time.max, tzinfo=timezone.utc).isoformat()


def test_inbox_query_date_today_response_is_agent_friendly_json(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    today_start = datetime.combine(date.today(), time(hour=1), tzinfo=timezone.utc).isoformat()
    yesterday = "2026-05-15T23:00:00+00:00"
    insert_item(store, dedupe_key="today", title="Today Agent Item", created_at=today_start)
    insert_item(store, dedupe_key="old", title="Old Agent Item", created_at=yesterday)

    response = client.get("/api/inbox?date=today&include_silent=true&include_ignored=true&limit=10")

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert set(body.keys()) == {"ok", "filters", "stats", "items"}
    assert body["filters"]["from"].endswith("+00:00")
    assert body["filters"]["to"].endswith("+00:00")
    assert [item["title"] for item in body["items"]] == ["Today Agent Item"]
    json.dumps(body, ensure_ascii=False)


def test_inbox_query_specific_date_and_from_to(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    insert_item(store, dedupe_key="d1", title="May 16 Item", created_at="2026-05-16T08:00:00+00:00")
    insert_item(store, dedupe_key="d2", title="May 17 Item", created_at="2026-05-17T08:00:00+00:00")

    by_date = client.get("/api/inbox?date=2026-05-16&include_silent=true&include_ignored=true")
    by_range = client.get(
        "/api/inbox?from=2026-05-17T00:00:00+00:00&to=2026-05-17T23:59:59+00:00"
        "&include_silent=true&include_ignored=true"
    )

    assert [item["title"] for item in by_date.json()["items"]] == ["May 16 Item"]
    assert [item["title"] for item in by_range.json()["items"]] == ["May 17 Item"]


def test_inbox_query_keyword_source_content_type_and_pagination(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    insert_item(
        store,
        dedupe_key="ai-1",
        title="AI Workflow",
        source_name="Source A",
        content_type="article",
        created_at="2026-05-16T08:00:00+00:00",
    )
    insert_item(
        store,
        dedupe_key="video-1",
        title="Video Workflow",
        source_name="Source B",
        content_type="video",
        summary="Contains retrieval keyword",
        created_at="2026-05-16T09:00:00+00:00",
    )
    insert_item(
        store,
        dedupe_key="ai-2",
        title="Second AI Workflow",
        source_name="Source A",
        content_type="article",
        created_at="2026-05-16T10:00:00+00:00",
    )

    keyword = client.get("/api/inbox?keyword=retrieval&include_silent=true&include_ignored=true")
    source = client.get("/api/inbox?source_name=Source%20A&include_silent=true&include_ignored=true")
    content_type = client.get("/api/inbox?content_type=video&include_silent=true&include_ignored=true")
    page_one = client.get("/api/inbox?include_silent=true&include_ignored=true&limit=1&offset=0")
    page_two = client.get("/api/inbox?include_silent=true&include_ignored=true&limit=1&offset=1")

    assert [item["title"] for item in keyword.json()["items"]] == ["Video Workflow"]
    assert [item["title"] for item in source.json()["items"]] == [
        "Second AI Workflow",
        "AI Workflow",
    ]
    assert [item["title"] for item in content_type.json()["items"]] == ["Video Workflow"]
    assert page_one.json()["items"][0]["title"] == "Second AI Workflow"
    assert page_two.json()["items"][0]["title"] == "Video Workflow"


def test_default_query_excludes_ignored_items_for_agent_use(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    insert_item(
        store,
        dedupe_key="ignored",
        title="Ignored Item",
        created_at="2026-05-16T08:00:00+00:00",
        action="ignore",
    )
    insert_item(
        store,
        dedupe_key="review",
        title="Review Item",
        created_at="2026-05-16T09:00:00+00:00",
        action="review",
    )

    response = client.get("/api/inbox?include_silent=true&limit=10")

    assert [item["title"] for item in response.json()["items"]] == ["Review Item"]
