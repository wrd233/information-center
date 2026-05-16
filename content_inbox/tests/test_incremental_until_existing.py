from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.models import ContentAnalyzeRequest
from app.rss import parse_feed
from app.rss_runner import sort_entries_for_processing
from app.server import app, get_store
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def fixture_uri(name: str) -> str:
    return (FIXTURES / name).as_uri()


def test_fixed_limit_processes_only_requested_number(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze",
        json={"feed_url": fixture_uri("rss_many_items.xml"), "limit": 4, "screen": False},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is True
    assert body["total_items"] == 4
    assert body["new_items"] == 4
    assert "incremental_decision" not in body


def test_until_existing_new_source_baseline_uses_initial_limit(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_many_items.xml"),
            "source_name": "Fixture Many Items",
            "incremental_mode": "until_existing",
            "probe_limit": 20,
            "new_source_initial_limit": 5,
            "screen": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["incremental_decision"] == "new_source_initial_baseline"
    assert body["source_has_history"] is False
    assert body["anchor_found"] is False
    assert body["feed_items_seen"] == 10
    assert body["selected_items_for_processing"] == 5
    assert body["new_items"] == 5
    assert body["warnings"]


def test_until_existing_old_source_anchor_found_processes_before_anchor(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    preload = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_incremental_v1.xml"),
            "source_name": "Fixture Incremental",
            "limit": 5,
            "screen": False,
        },
    )
    assert preload.status_code == 200
    assert preload.json()["new_items"] == 5

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_incremental_v2.xml"),
            "source_name": "Fixture Incremental",
            "incremental_mode": "until_existing",
            "probe_limit": 20,
            "screen": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["incremental_decision"] == "until_existing_anchor_found"
    assert body["source_has_history"] is True
    assert body["anchor_found"] is True
    assert body["anchor_index"] == 3
    assert body["feed_items_seen"] == 4
    assert body["selected_items_for_processing"] == 3
    assert body["new_items"] == 3
    assert [item["normalized"]["title"] for item in body["items"]] == [
        "New 03",
        "New 02",
        "New 01",
    ]


def test_until_existing_old_source_no_anchor_uses_fallback_limit(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    preload = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_incremental_v1.xml"),
            "source_name": "Fixture Incremental",
            "limit": 2,
            "screen": False,
        },
    )
    assert preload.status_code == 200

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_many_items.xml"),
            "source_name": "Fixture Incremental",
            "incremental_mode": "until_existing",
            "probe_limit": 4,
            "old_source_no_anchor_limit": 3,
            "screen": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["incremental_decision"] == "old_source_no_anchor"
    assert body["source_has_history"] is True
    assert body["anchor_found"] is False
    assert body["feed_items_seen"] == 4
    assert body["selected_items_for_processing"] == 3
    assert body["total_items"] == 3
    assert "RSSHub route changes" in body["warnings"][0]


def test_probe_limit_stops_anchor_scan_before_later_existing_item(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)
    preload = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_incremental_v1.xml"),
            "source_name": "Fixture Incremental",
            "limit": 5,
            "screen": False,
        },
    )
    assert preload.status_code == 200

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": fixture_uri("rss_incremental_v2.xml"),
            "source_name": "Fixture Incremental",
            "incremental_mode": "until_existing",
            "probe_limit": 2,
            "old_source_no_anchor_limit": 2,
            "screen": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["incremental_decision"] == "old_source_no_anchor"
    assert body["anchor_found"] is False
    assert body["feed_items_seen"] == 2
    assert body["selected_items_for_processing"] == 2


def test_sort_entries_for_processing_old_to_new_with_undated_last() -> None:
    _meta, entries = parse_feed(fixture_uri("rss_order_change_v2.xml"), limit=3)

    ordered = sort_entries_for_processing(entries)

    assert [entry.title for entry in ordered] == ["Order Old", "Order New", "Order Undated"]


def test_preserve_source_entry_order_false_keeps_feed_order(tmp_path: Path, monkeypatch) -> None:
    client, _store = make_client(tmp_path)
    _meta, entries = parse_feed(fixture_uri("rss_order_change_v2.xml"), limit=3)

    def fake_parse_feed(*_args, **_kwargs):
        return {
            "source_name": "Fixture Order Change",
            "feed_url": "mock://order",
            "feed_title": "Fixture Order Change",
            "total_items_found": 3,
        }, entries

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)
    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [{"source_id": "order", "feed_url": "mock://order"}],
            "screen": False,
            "preserve_source_entry_order": False,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert [item["normalized"]["title"] for item in body["source_results"][0]["items"]] == [
        "Order Undated",
        "Order New",
        "Order Old",
    ]


def test_preserve_source_entry_order_true_currently_sorts_by_date_not_feed_order(tmp_path: Path, monkeypatch) -> None:
    client, _store = make_client(tmp_path)
    _meta, entries = parse_feed(fixture_uri("rss_order_change_v2.xml"), limit=3)

    def fake_parse_feed(*_args, **_kwargs):
        return {
            "source_name": "Fixture Order Change",
            "feed_url": "mock://order",
            "feed_title": "Fixture Order Change",
            "total_items_found": 3,
        }, entries

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)
    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [{"source_id": "order", "feed_url": "mock://order"}],
            "screen": False,
            "preserve_source_entry_order": True,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert [item["normalized"]["title"] for item in body["source_results"][0]["items"]] == [
        "Order Old",
        "Order New",
        "Order Undated",
    ]


def test_sort_helper_accepts_bad_date_as_undated() -> None:
    entries = [
        ContentAnalyzeRequest(title="bad", summary="bad", published_at="not a date"),
        ContentAnalyzeRequest(title="dated", summary="dated", published_at="2026-05-16T00:00:00+00:00"),
    ]

    assert [entry.title for entry in sort_entries_for_processing(entries)] == ["dated", "bad"]
