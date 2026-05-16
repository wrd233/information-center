from __future__ import annotations

import json

from app import cli


def test_cli_success_stdout_is_json_and_stderr_is_clean(monkeypatch, capsys) -> None:
    def fake_request(method, url, payload=None, timeout=30):
        return 200, {"ok": True, "items": [], "stats": {"returned": 0}, "filters": {}}

    monkeypatch.setattr(cli, "request_json", fake_request)
    exit_code = cli.main(["inbox", "--json", "--limit", "1"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert json.loads(captured.out)["ok"] is True
    assert captured.err == ""


def test_cli_api_unreachable_still_outputs_json_error(monkeypatch, capsys) -> None:
    def fake_request(method, url, payload=None, timeout=30):
        return 0, {
            "ok": False,
            "error": {"error_code": "api_unreachable", "message": "connection refused", "retryable": True},
        }

    monkeypatch.setattr(cli, "request_json", fake_request)
    exit_code = cli.main(["inbox", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert json.loads(captured.out)["error"]["error_code"] == "api_unreachable"
    assert "content-inbox CLI error" in captured.err


def test_cli_inbox_today_tz_converts_to_range_before_calling_api(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append(url)
        return 200, {"ok": True, "items": [], "stats": {}, "filters": {}}

    monkeypatch.setattr(cli, "request_json", fake_request)
    exit_code = cli.main(["inbox", "--today", "--tz", "Asia/Shanghai", "--json"])

    assert exit_code == 0
    assert "from=" in calls[0]
    assert "to=" in calls[0]
    assert "date=today" not in calls[0]
