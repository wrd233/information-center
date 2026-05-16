from __future__ import annotations

import json

from app import cli


def test_cli_inbox_json_stdout_is_valid_json(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url, payload))
        return 200, {"ok": True, "items": [], "filters": {}, "stats": {"total": 0}}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["inbox", "--json", "--limit", "20", "--keyword", "AI"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""
    parsed = json.loads(captured.out)
    assert parsed["ok"] is True
    assert "[INFO]" not in captured.out
    assert "keyword=AI" in calls[0][1]
    assert "limit=20" in calls[0][1]


def test_cli_inbox_api_unreachable_returns_nonzero_with_json_stdout(monkeypatch, capsys) -> None:
    def fake_request(method, url, payload=None, timeout=30):
        return 0, {
            "ok": False,
            "error": {"error_code": "api_unreachable", "message": "connection refused", "retryable": True},
        }

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["inbox", "--json", "--limit", "20"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert json.loads(captured.out)["error"]["error_code"] == "api_unreachable"
    assert "content-inbox CLI error" in captured.err


def test_cli_inbox_today_with_timezone_converts_to_from_to(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append(url)
        return 200, {"ok": True, "items": [], "filters": {}, "stats": {}}

    monkeypatch.setattr(cli, "request_json", fake_request)

    exit_code = cli.main(["inbox", "--json", "--today", "--tz", "Asia/Shanghai"])

    assert exit_code == 0
    _captured = capsys.readouterr()
    assert "date=today" not in calls[0]
    assert "from=" in calls[0]
    assert "to=" in calls[0]
