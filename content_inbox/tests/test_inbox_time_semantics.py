from __future__ import annotations

from datetime import date, datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from app.models import ContentAnalyzeRequest
from app.processor import process_content_thread_safe
from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def add_item(store: InboxStore, title: str, *, created_at: str, published_at: str | None = None) -> str:
    result = process_content_thread_safe(
        store,
        ContentAnalyzeRequest(
            title=title,
            url=f"https://example.com/{title}",
            source_name="Time Source",
            published_at=published_at,
            screen=False,
        ),
    )
    with store.connect() as conn:
        conn.execute(
            "UPDATE inbox_items SET created_at = ?, published_at = ? WHERE item_id = ?",
            (created_at, published_at, result.item_id),
        )
    return result.item_id


def test_inbox_specific_date_and_created_range_use_created_at(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_item(store, "inside", created_at="2026-05-16T12:00:00+00:00")
    add_item(store, "outside", created_at="2026-05-15T12:00:00+00:00")

    by_date = client.get("/api/inbox?date=2026-05-16&include_silent=true&include_ignored=true").json()
    by_range = client.get(
        "/api/inbox?created_from=2026-05-16T00:00:00+00:00&created_to=2026-05-16T23:59:59+00:00"
        "&include_silent=true&include_ignored=true"
    ).json()

    assert [item["title"] for item in by_date["items"]] == ["inside"]
    assert by_date["filters"]["resolved_timezone"] == "UTC"
    assert [item["title"] for item in by_range["items"]] == ["inside"]


def test_inbox_published_range_is_separate_from_created_range(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_item(
        store,
        "published-inside",
        created_at="2026-05-10T12:00:00+00:00",
        published_at="2026-05-16T08:00:00+00:00",
    )

    body = client.get(
        "/api/inbox?published_from=2026-05-16T00:00:00+00:00&published_to=2026-05-16T23:59:59+00:00"
        "&include_silent=true&include_ignored=true"
    ).json()

    assert [item["title"] for item in body["items"]] == ["published-inside"]


def test_inbox_today_with_timezone_reports_resolved_timezone(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    zone = ZoneInfo("Asia/Shanghai")
    local_today = datetime.now(zone).date()
    created_at = datetime.combine(local_today, time(hour=1), tzinfo=zone).astimezone(timezone.utc).isoformat()
    add_item(store, "local-today", created_at=created_at)

    body = client.get("/api/inbox?date=today&tz=Asia/Shanghai&include_silent=true&include_ignored=true").json()

    assert body["filters"]["resolved_timezone"] == "Asia/Shanghai"
    assert body["stats"]["returned"] >= 1
    assert "local-today" in {item["title"] for item in body["items"]}
