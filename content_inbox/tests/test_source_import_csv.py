from __future__ import annotations

import csv
import json
from pathlib import Path

from app import cli
from app.source_importer import read_source_csv


def write_csv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["源名称", "分类", "rss_url", "source_id"])
        writer.writeheader()
        writer.writerow({"源名称": "源 A", "分类": "科技", "rss_url": "https://example.com/a.xml", "source_id": "source-a"})
        writer.writerow({"源名称": "", "分类": "科技", "rss_url": "https://example.com/skip.xml", "source_id": "skip"})


def test_read_source_csv_supports_common_column_aliases(tmp_path: Path) -> None:
    csv_path = tmp_path / "sources.csv"
    write_csv(csv_path)

    sources = read_source_csv(csv_path, source_id_column="source_id")

    assert sources == [
        {
            "source_id": "source-a",
            "source_name": "源 A",
            "source_category": "科技",
            "feed_url": "https://example.com/a.xml",
            "status": "active",
            "priority": 0,
            "tags": [],
            "notes": "",
            "config": {},
        }
    ]


def test_cli_sources_import_csv_dry_run_outputs_json_without_api_calls(tmp_path: Path, monkeypatch, capsys) -> None:
    csv_path = tmp_path / "sources.csv"
    write_csv(csv_path)

    def fail_request(*_args, **_kwargs):
        raise AssertionError("dry-run should not call the API")

    monkeypatch.setattr(cli, "request_json", fail_request)
    exit_code = cli.main(["sources", "import-csv", "--csv", str(csv_path), "--dry-run", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    data = json.loads(captured.out)
    assert data["ok"] is True
    assert data["dry_run"] is True
    assert data["sources"][0]["source_id"] is None
    assert captured.err == ""


def test_cli_sources_import_csv_upsert_updates_conflict(tmp_path: Path, monkeypatch, capsys) -> None:
    csv_path = tmp_path / "sources.csv"
    write_csv(csv_path)
    calls = []

    def fake_request(method, url, payload=None, timeout=30):
        calls.append((method, url, payload))
        if method == "POST":
            return 409, {"ok": False, "error": {"error_code": "source_conflict", "message": "exists", "retryable": False}}
        return 200, {"ok": True, "source": {"source_id": payload["source_id"]}}

    monkeypatch.setattr(cli, "request_json", fake_request)
    exit_code = cli.main(
        [
            "sources",
            "import-csv",
            "--csv",
            str(csv_path),
            "--source-id-column",
            "source_id",
            "--upsert",
            "--json",
        ]
    )

    assert exit_code == 0
    assert [call[0] for call in calls] == ["POST", "PATCH"]
    assert json.loads(capsys.readouterr().out)["stats"]["updated"] == 1
