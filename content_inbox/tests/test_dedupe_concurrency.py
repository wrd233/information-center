from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from fastapi.testclient import TestClient

from app.server import app, get_store
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def test_concurrent_content_analyze_same_url_inserts_one_row(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    payload = {
        "url": "https://example.com/concurrent?utm_source=x#frag",
        "title": "Concurrent Item",
        "source_name": "Concurrent Source",
        "summary": "Concurrent summary",
        "screen": False,
    }

    def submit() -> dict:
        response = client.post("/api/content/analyze", json=payload)
        assert response.status_code == 200
        return response.json()

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = [future.result() for future in as_completed([executor.submit(submit) for _ in range(20)])]

    assert sum(1 for result in results if not result["is_duplicate"]) == 1
    assert sum(1 for result in results if result["is_duplicate"]) == 19
    items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 50})
    assert total == 1
    assert items[0]["seen_count"] == 20


def test_concurrent_rss_analyze_same_feed_does_not_duplicate_rows(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    payload = {
        "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
        "limit": 2,
        "screen": False,
    }

    def submit() -> dict:
        response = client.post("/api/rss/analyze", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["ok"] is True
        return body

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = [future.result() for future in as_completed([executor.submit(submit) for _ in range(10)])]

    assert sum(result["new_items"] for result in results) == 2
    assert sum(result["duplicate_items"] for result in results) == 18
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 50})
    assert total == 2


def test_mixed_content_and_rss_ingestion_share_dedupe_state(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    content_payload = {
        "url": "https://fixtures.example.com/items/one",
        "title": "Manual Duplicate Of RSS",
        "source_name": "Manual",
        "summary": "Manual summary",
        "screen": False,
    }
    rss_payload = {
        "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
        "limit": 1,
        "screen": False,
    }

    def submit_content() -> dict:
        response = client.post("/api/content/analyze", json=content_payload)
        assert response.status_code == 200
        return response.json()

    def submit_rss() -> dict:
        response = client.post("/api/rss/analyze", json=rss_payload)
        assert response.status_code == 200
        return response.json()

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(submit_content) for _ in range(10)]
        futures.extend(executor.submit(submit_rss) for _ in range(10))
        results = [future.result() for future in as_completed(futures)]

    content_new = sum(1 for result in results if "is_duplicate" in result and not result["is_duplicate"])
    rss_new = sum(result.get("new_items", 0) for result in results)
    assert content_new + rss_new == 1
    _items, total = store.query({"include_silent": True, "include_ignored": True, "limit": 50})
    assert total == 1
