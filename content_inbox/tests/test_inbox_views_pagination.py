from __future__ import annotations

import json
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


def add_item(
    store: InboxStore,
    title: str,
    *,
    action: str = "read",
    notification: str = "manual_review",
) -> None:
    result = process_content_thread_safe(
        store,
        ContentAnalyzeRequest(
            title=title,
            url=f"https://example.com/{title}",
            source_name="View Source",
            screen=False,
        ),
    )
    with store.connect() as conn:
        row = conn.execute("SELECT screening_json, clustering_json FROM inbox_items WHERE item_id = ?", (result.item_id,)).fetchone()
        screening = json.loads(row["screening_json"])
        clustering = json.loads(row["clustering_json"])
        screening["suggested_action"] = action
        clustering["notification_decision"] = notification
        conn.execute(
            "UPDATE inbox_items SET screening_json = ?, clustering_json = ? WHERE item_id = ?",
            (json.dumps(screening), json.dumps(clustering), result.item_id),
        )


def titles(body: dict) -> set[str]:
    return {item["title"] for item in body["items"]}


def test_inbox_views_apply_expected_defaults(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_item(store, "ignored", action="ignore", notification="manual_review")
    add_item(store, "silent-read", action="read", notification="silent")
    add_item(store, "pushed", action="read", notification="full_push")

    all_view = client.get("/api/inbox?view=all&limit=10").json()
    readable = client.get("/api/inbox?view=readable&limit=10").json()
    recommended = client.get("/api/inbox?view=recommended&limit=10").json()
    notifications = client.get("/api/inbox?view=notifications&limit=10").json()

    assert titles(all_view) == {"ignored", "silent-read", "pushed"}
    assert titles(readable) == {"silent-read", "pushed"}
    assert titles(recommended) == {"pushed"}
    assert titles(notifications) == {"pushed"}


def test_inbox_pagination_stats_are_agent_friendly(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    for idx in range(3):
        add_item(store, f"item-{idx}", action="read", notification="manual_review")

    body = client.get("/api/inbox?view=all&limit=1&offset=1").json()

    assert body["ok"] is True
    assert body["stats"]["matched_before_post_filters"] == 3
    assert body["stats"]["matched_after_post_filters"] == 1
    assert body["stats"]["returned"] == 1
    assert body["stats"]["limit"] == 1
    assert body["stats"]["offset"] == 1
