from __future__ import annotations

import json

from app import cli


def test_cli_runs_list_get_and_sources_call_run_apis(monkeypatch, capsys) -> None:
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url))
        if url.endswith("/sources"):
            return 200, {"ok": True, "sources": []}
        if "/api/rss/runs/run-1" in url:
            return 200, {"ok": True, "run": {"run_id": "run-1"}}
        return 200, {"ok": True, "runs": [], "stats": {"total": 0}}

    monkeypatch.setattr(cli, "request_json", fake_request)

    assert cli.main(["runs", "list", "--json", "--limit", "5"]) == 0
    assert cli.main(["runs", "get", "run-1", "--json"]) == 0
    assert cli.main(["runs", "sources", "run-1", "--json"]) == 0

    output_lines = [json.loads(line) for line in capsys.readouterr().out.strip().splitlines()]
    assert output_lines[0]["ok"] is True
    assert output_lines[1]["run"]["run_id"] == "run-1"
    assert output_lines[2]["sources"] == []
    assert calls[0][0] == "GET"
    assert calls[0][1].endswith("/api/rss/runs?limit=5&offset=0")
