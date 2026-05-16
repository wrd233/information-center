from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.models import ContentAnalyzeRequest
from app.server import app, get_store
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def test_until_existing_source_history_prefers_source_id_over_name(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    client.post(
        "/api/rss/analyze",
        json={
            "feed_url": (FIXTURES / "rss_incremental_v1.xml").as_uri(),
            "source_id": "stable-source",
            "source_name": "Old Name",
            "limit": 5,
            "screen": False,
        },
    )

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": (FIXTURES / "rss_incremental_v2.xml").as_uri(),
            "source_id": "stable-source",
            "source_name": "Renamed Source",
            "incremental_mode": "until_existing",
            "probe_limit": 20,
            "screen": False,
        },
    )

    body = response.json()
    assert body["source_has_history"] is True
    assert body["incremental_decision"] == "until_existing_anchor_found"


def test_stop_on_first_existing_false_continues_scanning_probe_window(tmp_path: Path, monkeypatch) -> None:
    client, _store = make_client(tmp_path)
    existing = ContentAnalyzeRequest(
        title="Existing",
        url="https://example.com/existing",
        source_id="scan-source",
        source_name="Scan Source",
        screen=False,
    )
    later_new = ContentAnalyzeRequest(
        title="Later New",
        url="https://example.com/later-new",
        source_id="scan-source",
        source_name="Scan Source",
        screen=False,
    )

    client.post(
        "/api/content/analyze",
        json=existing.model_dump(),
    )

    def fake_parse_feed(*_args, **_kwargs):
        return {
            "source_name": "Scan Source",
            "feed_url": "mock://scan",
            "feed_title": "Scan Source",
            "total_items_found": 2,
        }, [existing, later_new]

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)
    stopped = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": "mock://scan",
            "source_id": "scan-source",
            "source_name": "Scan Source",
            "incremental_mode": "until_existing",
            "probe_limit": 2,
            "stop_on_first_existing": True,
            "screen": False,
        },
    ).json()
    continued = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": "mock://scan",
            "source_id": "scan-source",
            "source_name": "Scan Source",
            "incremental_mode": "until_existing",
            "probe_limit": 2,
            "stop_on_first_existing": False,
            "screen": False,
        },
    ).json()

    assert stopped["selected_items_for_processing"] == 0
    assert continued["selected_items_for_processing"] == 1
    assert continued["new_items"] == 1
