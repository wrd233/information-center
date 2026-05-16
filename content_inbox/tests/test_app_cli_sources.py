from __future__ import annotations

import json

from app import cli


def test_cli_sources_list_outputs_json(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url, payload))
        return 200, {"ok": True, "sources": [], "stats": {"total": 0}}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["sources", "list", "--json", "--status", "active"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(captured.out)["ok"] is True
    assert calls[0][0] == "GET"
    assert "status=active" in calls[0][1]


def test_cli_sources_get_outputs_json(monkeypatch, capsys) -> None:
    def fake_request(method, url, payload=None, timeout=30):
        return 200, {"ok": True, "source": {"source_id": "rsshub-36kr"}}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["sources", "get", "rsshub-36kr", "--json"])

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out)["source"]["source_id"] == "rsshub-36kr"


def test_cli_sources_register_posts_payload(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url, payload))
        return 200, {"ok": True, "source": {"source_id": payload["source_id"]}, "created": True}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(
        [
            "sources",
            "register",
            "--source-id",
            "rsshub-36kr",
            "--name",
            "36氪",
            "--feed-url",
            "http://rsshub:1200/36kr/news/latest",
            "--config-json",
            '{"screen": false}',
            "--json",
        ]
    )

    assert exit_code == 0
    assert calls[0][0] == "POST"
    assert calls[0][2]["source_name"] == "36氪"
    assert calls[0][2]["config"] == {"screen": False}
    assert json.loads(capsys.readouterr().out)["created"] is True


def test_cli_sources_update_patches_payload(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url, payload))
        return 200, {"ok": True, "source": {"source_id": "rsshub-36kr", "status": payload["status"]}}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["sources", "update", "rsshub-36kr", "--status", "paused", "--json"])

    assert exit_code == 0
    assert calls[0][0] == "PATCH"
    assert calls[0][2] == {"status": "paused"}
    assert json.loads(capsys.readouterr().out)["source"]["status"] == "paused"


def test_cli_sources_ingest_posts_payload(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url, payload))
        return 200, {"ok": True, "run": {"status": "success"}, "source": {}, "items": []}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["sources", "ingest", "rsshub-36kr", "--json", "--screen", "false", "--limit", "10"])

    assert exit_code == 0
    assert calls[0][0] == "POST"
    assert calls[0][1].endswith("/api/rss/sources/rsshub-36kr/ingest")
    assert calls[0][2]["screen"] is False
    assert calls[0][2]["limit"] == 10
    assert json.loads(capsys.readouterr().out)["run"]["status"] == "success"


def test_cli_sources_error_returns_nonzero(monkeypatch, capsys) -> None:
    def fake_request(method, url, payload=None, timeout=30):
        return 404, {
            "ok": False,
            "error": {"error_code": "source_not_found", "message": "missing", "retryable": False},
        }

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["sources", "get", "missing", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert json.loads(captured.out)["error"]["error_code"] == "source_not_found"
    assert "content-inbox CLI error" in captured.err
