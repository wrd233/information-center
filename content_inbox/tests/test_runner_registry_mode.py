from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

import pytest


SCRIPT_PATH = Path("/Users/wangrundong/work/infomation-center/content_inbox/scripts/run_rss_sources_to_content_inbox.py")


def load_script_module():
    module_name = f"run_rss_sources_to_content_inbox_registry_{time.time_ns()}"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def invoke_main(module, monkeypatch: pytest.MonkeyPatch, argv: list[str]) -> int:
    monkeypatch.setattr(sys, "argv", ["run_rss_sources_to_content_inbox.py", *argv])
    return module.main()


def test_runner_registry_mode_reads_active_sources_and_calls_source_ingest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    output_dir = tmp_path / "outputs"
    ingest_urls = []

    def fake_request(method, url, payload=None, timeout=120, api_key=None):
        if "/api/rss/sources?" in url:
            return {
                "ok": True,
                "_status": 200,
                "sources": [
                    {
                        "source_id": "source-a",
                        "source_name": "Source A",
                        "source_category": "Registry",
                        "feed_url": "https://example.com/a.xml",
                        "status": "active",
                        "priority": 1,
                    }
                ],
            }
        if url.endswith("/health"):
            return {"ok": True, "_status": 200}
        if url.endswith("/api/rss/sources/source-a/ingest"):
            ingest_urls.append(url)
            return {
                "ok": True,
                "_status": 200,
                "run": {
                    "status": "success",
                    "stats": {"fetched_entries": 1, "processed_entries": 1, "new_items": 1, "duplicate_items": 0, "failed_items": 0},
                    "incremental": {"mode": "fixed_limit", "decision": None, "anchor_found": None, "warnings": []},
                },
                "source": {},
            }
        return {"ok": True, "_status": 200}

    monkeypatch.setattr(module, "request_json", fake_request)
    monkeypatch.setattr(module, "query_inbox", lambda *a, **k: {"ok": True, "items": [], "stats": {}, "_query_mode": "date"})
    monkeypatch.setattr(module, "query_inbox_view", lambda *a, **k: {"ok": True, "items": [], "stats": {}, "_query_mode": "date"})

    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--source-mode",
            "registry",
            "--output-dir",
            str(output_dir),
            "--count",
            "1",
            "--sleep",
            "0",
            "--no-screen",
        ],
    )

    run_dir = module.latest_run_dir(output_dir / "runs")
    metadata = json.loads((run_dir / "metadata.json").read_text())
    rows = module.read_csv_rows(run_dir / "source_results.csv")

    assert exit_code == 0
    assert ingest_urls == ["http://127.0.0.1:8787/api/rss/sources/source-a/ingest"]
    assert metadata["source_mode"] == "registry"
    assert rows[0]["source_id"] == "source-a"
    assert rows[0]["status"] == "success"
