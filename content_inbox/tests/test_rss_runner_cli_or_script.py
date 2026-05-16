from __future__ import annotations

import csv
import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.server import app, get_store
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"
SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "run_rss_sources_to_content_inbox.py"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def load_script_module():
    module_name = f"run_rss_sources_to_content_inbox_eval_{time.time_ns()}"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def write_sources_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "title": "Good Basic",
            "category_path": "Fixtures",
            "local_xml_url": (FIXTURES / "rss_basic.xml").as_uri(),
            "xml_url": "",
            "status": "active",
            "enabled": "true",
            "priority": "",
        },
        {
            "title": "Bad Malformed",
            "category_path": "Fixtures",
            "local_xml_url": (FIXTURES / "rss_malformed.xml").as_uri(),
            "xml_url": "",
            "status": "active",
            "enabled": "true",
            "priority": "",
        },
        {
            "title": "Empty",
            "category_path": "Fixtures",
            "local_xml_url": (FIXTURES / "rss_empty.xml").as_uri(),
            "xml_url": "",
            "status": "active",
            "enabled": "true",
            "priority": "",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["title", "category_path", "local_xml_url", "xml_url", "status", "enabled", "priority"],
        )
        writer.writeheader()
        writer.writerows(rows)


def test_batch_api_one_source_failure_does_not_block_others(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {
                    "source_id": "good",
                    "feed_url": (FIXTURES / "rss_basic.xml").as_uri(),
                    "source_name": "Good Basic",
                },
                {
                    "source_id": "bad",
                    "feed_url": (FIXTURES / "rss_malformed.xml").as_uri(),
                    "source_name": "Bad Malformed",
                },
                {
                    "source_id": "empty",
                    "feed_url": (FIXTURES / "rss_empty.xml").as_uri(),
                    "source_name": "Empty",
                },
            ],
            "screen": False,
            "max_concurrent_sources": 2,
            "include_items": True,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["successful_sources"] == 2
    assert body["failed_sources"] == 1
    assert body["source_results"][0]["source_id"] == "good"
    assert body["source_results"][1]["source_id"] == "bad"
    assert "failed to parse feed" in body["source_results"][1]["error"]
    assert body["source_results"][2]["source_id"] == "empty"


def test_batch_api_incremental_parameters_are_applied(tmp_path: Path) -> None:
    client, _store = make_client(tmp_path)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {
                    "source_id": "many",
                    "feed_url": (FIXTURES / "rss_many_items.xml").as_uri(),
                    "source_name": "Fixture Many Items",
                }
            ],
            "screen": False,
            "incremental_mode": "until_existing",
            "probe_limit": 4,
            "new_source_initial_limit": 3,
            "old_source_no_anchor_limit": 2,
        },
    )

    result = response.json()["source_results"][0]
    assert response.status_code == 200
    assert result["incremental_mode"] == "until_existing"
    assert result["incremental_decision"] == "new_source_initial_baseline"
    assert result["probe_limit"] == 4
    assert result["new_source_initial_limit"] == 3
    assert result["old_source_no_anchor_limit"] == 2
    assert result["selected_items_for_processing"] == 3


def test_script_dry_run_writes_machine_readable_artifacts_but_stdout_is_not_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_sources_csv(csv_path)

    monkeypatch.setattr(module, "request_json", lambda *args, **kwargs: {"ok": True, "_status": 200})
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_rss_sources_to_content_inbox.py",
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--all",
            "--dry-run",
            "--no-screen",
        ],
    )

    exit_code = module.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.startswith("[INFO]")
    with pytest.raises(json.JSONDecodeError):
        json.loads(captured.out)

    run_dir = module.latest_run_dir(output_dir / "runs")
    assert run_dir is not None
    assert (run_dir / "selected_sources.csv").exists()
    assert (run_dir / "report.md").exists()
    assert (run_dir / "run_state.json").exists()


def test_script_forwards_incremental_options_to_api(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_sources_csv(csv_path)
    calls: list[dict] = []

    monkeypatch.setattr(module, "request_json", lambda *args, **kwargs: {"ok": True, "_status": 200})
    monkeypatch.setattr(module, "query_inbox", lambda *args, **kwargs: {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"})
    monkeypatch.setattr(module, "query_inbox_view", lambda *args, **kwargs: {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"})

    def fake_analyze(**kwargs):
        calls.append(kwargs)
        return {
            "ok": True,
            "_status": 200,
            "total_items": 0,
            "new_items": 0,
            "duplicate_items": 0,
            "screened_items": 0,
            "recommended_items": 0,
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
            "incremental_mode": "until_existing",
            "incremental_decision": "new_source_initial_baseline",
            "source_has_history": False,
            "probe_limit": kwargs["probe_limit"],
            "feed_items_seen": 0,
            "anchor_found": False,
            "anchor_index": None,
            "selected_items_for_processing": 0,
            "warnings": [],
        }

    monkeypatch.setattr(module, "analyze_rss_source", fake_analyze)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_rss_sources_to_content_inbox.py",
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "1",
            "--no-screen",
            "--incremental-mode",
            "until_existing",
            "--probe-limit",
            "7",
            "--new-source-initial-limit",
            "3",
            "--old-source-no-anchor-limit",
            "4",
            "--sleep",
            "0",
        ],
    )

    assert module.main() == 0
    assert calls
    assert calls[0]["incremental_mode"] == "until_existing"
    assert calls[0]["probe_limit"] == 7
    assert calls[0]["new_source_initial_limit"] == 3
    assert calls[0]["old_source_no_anchor_limit"] == 4
