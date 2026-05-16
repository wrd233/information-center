from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.server import app, get_store
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> TestClient:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app)


def test_malformed_rss_analyze_returns_structured_parse_error(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze",
        json={"feed_url": (FIXTURES / "rss_malformed.xml").as_uri(), "screen": False},
    )

    body = response.json()
    assert response.status_code == 400
    assert body["ok"] is False
    assert body["error"]["error_code"] == "rss_parse_error"
    assert body["error"]["retryable"] is False


def test_source_not_found_error_envelope(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.get("/api/rss/sources/missing")

    assert response.status_code == 404
    assert response.json()["error"] == {
        "error_code": "source_not_found",
        "message": "RSS source not found",
        "retryable": False,
        "source_id": "missing",
        "feed_url": None,
    }


def test_duplicate_source_error_envelope(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    payload = {
        "source_id": "dup",
        "source_name": "Dup",
        "feed_url": "https://example.com/dup",
    }
    assert client.post("/api/rss/sources", json=payload).status_code == 200

    response = client.post("/api/rss/sources", json={**payload, "feed_url": "https://example.com/other"})

    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "source_conflict"


def test_disabled_source_error_envelope(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    client.post(
        "/api/rss/sources",
        json={
            "source_id": "disabled",
            "source_name": "Disabled",
            "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
            "status": "disabled",
        },
    )

    response = client.post("/api/rss/sources/disabled/ingest", json={"screen": False})

    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "source_disabled"
