from __future__ import annotations

import csv
import importlib.util
import json
import sys
import threading
import time
from pathlib import Path

import pytest


SCRIPT_PATH = Path("/Users/wangrundong/work/infomation-center/content_inbox/scripts/run_rss_sources_to_content_inbox.py")


def load_script_module():
    module_name = f"run_rss_sources_to_content_inbox_{time.time_ns()}"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def write_test_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["title", "category_path", "local_xml_url", "xml_url", "status", "enabled", "priority"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def invoke_main(module, monkeypatch: pytest.MonkeyPatch, argv: list[str]) -> int:
    monkeypatch.setattr(sys, "argv", ["run_rss_sources_to_content_inbox.py", *argv])
    return module.main()


def basic_csv_rows(count: int) -> list[dict[str, str]]:
    rows = []
    for index in range(count):
        rows.append(
            {
                "title": f"Source {index + 1}",
                "category_path": "Videos/Test",
                "local_xml_url": f"http://127.0.0.1/feed/{index + 1}",
                "xml_url": f"https://example.com/feed/{index + 1}",
                "status": "active",
                "enabled": "true",
                "priority": "",
            }
        )
    return rows


def test_parse_args_concurrency_default_is_one(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    monkeypatch.setattr(sys, "argv", ["run_rss_sources_to_content_inbox.py"])
    args = module.parse_args()
    assert args.concurrency == 1


def test_parse_args_rejects_concurrency_less_than_one(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    monkeypatch.setattr(sys, "argv", ["run_rss_sources_to_content_inbox.py", "--concurrency", "0"])
    with pytest.raises(SystemExit):
        module.parse_args()


def test_concurrency_two_runs_sources_in_parallel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_test_csv(csv_path, basic_csv_rows(4))

    def fake_health(*args, **kwargs):
        return {"ok": True, "_status": 200}

    def fake_inbox(*args, **kwargs):
        return {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"}

    monkeypatch.setattr(module, "request_json", fake_health)
    monkeypatch.setattr(module, "query_inbox", fake_inbox)
    monkeypatch.setattr(module, "query_inbox_view", fake_inbox)

    def fake_analyze(*args, **kwargs):
        time.sleep(0.1)
        return {
            "ok": True,
            "_status": 200,
            "total_items": 1,
            "new_items": 1,
            "duplicate_items": 0,
            "screened_items": 1,
            "recommended_items": 1,
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
        }

    monkeypatch.setattr(module, "analyze_rss_source", fake_analyze)

    start = time.perf_counter()
    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "4",
            "--concurrency",
            "2",
            "--sleep",
            "0",
        ],
    )
    elapsed = time.perf_counter() - start

    assert exit_code == 0
    assert elapsed < 0.35


def test_parallel_results_csv_keeps_sequence_order(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_test_csv(csv_path, basic_csv_rows(3))

    def fake_health(*args, **kwargs):
        return {"ok": True, "_status": 200}

    def fake_inbox(*args, **kwargs):
        return {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"}

    monkeypatch.setattr(module, "request_json", fake_health)
    monkeypatch.setattr(module, "query_inbox", fake_inbox)
    monkeypatch.setattr(module, "query_inbox_view", fake_inbox)

    def fake_analyze(api_base, source, **kwargs):
        if source.source_name == "Source 1":
            time.sleep(0.12)
        elif source.source_name == "Source 2":
            time.sleep(0.01)
        else:
            time.sleep(0.03)
        return {
            "ok": True,
            "_status": 200,
            "total_items": 1,
            "new_items": 1,
            "duplicate_items": 0,
            "screened_items": 1,
            "recommended_items": 1,
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
        }

    monkeypatch.setattr(module, "analyze_rss_source", fake_analyze)

    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "3",
            "--concurrency",
            "2",
            "--sleep",
            "0",
        ],
    )

    assert exit_code == 0
    run_dir = module.latest_run_dir(output_dir / "runs")
    assert run_dir is not None
    rows = module.read_csv_rows(run_dir / "source_results.csv")
    assert [row["sequence"] for row in rows] == ["1", "2", "3"]


def test_single_source_failure_does_not_block_others(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_test_csv(csv_path, basic_csv_rows(3))

    def fake_health(*args, **kwargs):
        return {"ok": True, "_status": 200}

    def fake_inbox(*args, **kwargs):
        return {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"}

    monkeypatch.setattr(module, "request_json", fake_health)
    monkeypatch.setattr(module, "query_inbox", fake_inbox)
    monkeypatch.setattr(module, "query_inbox_view", fake_inbox)

    def fake_analyze(api_base, source, **kwargs):
        if source.source_name == "Source 2":
            return {"ok": False, "_status": 500, "error": {"detail": "boom"}}
        return {
            "ok": True,
            "_status": 200,
            "total_items": 1,
            "new_items": 1,
            "duplicate_items": 0,
            "screened_items": 1,
            "recommended_items": 1,
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
        }

    monkeypatch.setattr(module, "analyze_rss_source", fake_analyze)

    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "3",
            "--concurrency",
            "2",
            "--sleep",
            "0",
        ],
    )

    assert exit_code == 1
    run_dir = module.latest_run_dir(output_dir / "runs")
    assert run_dir is not None
    rows = module.read_csv_rows(run_dir / "source_results.csv")
    assert [row["status"] for row in rows] == ["success", "failed", "success"]


def test_dry_run_does_not_call_analyze(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_test_csv(csv_path, basic_csv_rows(2))

    def fake_health(*args, **kwargs):
        return {"ok": True, "_status": 200}

    monkeypatch.setattr(module, "request_json", fake_health)

    def fail_analyze(*args, **kwargs):
        raise AssertionError("analyze_rss_source should not be called during dry-run")

    monkeypatch.setattr(module, "analyze_rss_source", fail_analyze)

    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "2",
            "--dry-run",
            "--concurrency",
            "3",
        ],
    )

    assert exit_code == 0
    run_dir = module.latest_run_dir(output_dir / "runs")
    assert run_dir is not None
    state = json.loads((run_dir / "run_state.json").read_text(encoding="utf-8"))
    assert state["status"] == "dry_run"
    assert state["args"]["concurrency"] == 3


def test_resume_skips_completed_source_ids(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_test_csv(csv_path, basic_csv_rows(3))

    def fake_health(*args, **kwargs):
        return {"ok": True, "_status": 200}

    def fake_inbox(*args, **kwargs):
        return {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"}

    monkeypatch.setattr(module, "request_json", fake_health)
    monkeypatch.setattr(module, "query_inbox", fake_inbox)
    monkeypatch.setattr(module, "query_inbox_view", fake_inbox)

    seen: list[str] = []

    def fake_analyze(api_base, source, **kwargs):
        seen.append(source.source_name)
        return {
            "ok": True,
            "_status": 200,
            "total_items": 1,
            "new_items": 1,
            "duplicate_items": 0,
            "screened_items": 1,
            "recommended_items": 1,
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
        }

    monkeypatch.setattr(module, "analyze_rss_source", fake_analyze)

    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "3",
            "--concurrency",
            "1",
            "--sleep",
            "0",
        ],
    )
    assert exit_code == 0

    run_dir = module.latest_run_dir(output_dir / "runs")
    assert run_dir is not None
    first_rows = module.read_csv_rows(run_dir / "source_results.csv")
    first_source_id = first_rows[0]["source_id"]
    state = json.loads((run_dir / "run_state.json").read_text(encoding="utf-8"))
    state["status"] = "running"
    state["completed_source_ids"] = [first_source_id]
    state["successful_source_ids"] = [first_source_id]
    state["completed_count"] = 1
    state["successful_count"] = 1
    (run_dir / "run_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    with (run_dir / "source_results.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=module.results_csv_headers())
        writer.writeheader()
        writer.writerow(first_rows[0])

    seen.clear()
    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "3",
            "--concurrency",
            "2",
            "--sleep",
            "0",
            "--resume",
        ],
    )

    assert exit_code == 0
    assert seen == ["Source 2", "Source 3"]


def test_max_consecutive_failures_stops_new_submissions_and_saves_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_script_module()
    csv_path = tmp_path / "sources.csv"
    output_dir = tmp_path / "outputs"
    write_test_csv(csv_path, basic_csv_rows(4))

    def fake_health(*args, **kwargs):
        return {"ok": True, "_status": 200}

    monkeypatch.setattr(module, "request_json", fake_health)

    started = threading.Event()
    release = threading.Event()
    seen: list[str] = []

    def fake_analyze(api_base, source, **kwargs):
        seen.append(source.source_name)
        started.set()
        if source.source_name in {"Source 1", "Source 2"}:
            release.wait(timeout=1)
            return {"ok": False, "_status": 500, "error": {"detail": "boom"}}
        return {
            "ok": True,
            "_status": 200,
            "total_items": 1,
            "new_items": 1,
            "duplicate_items": 0,
            "screened_items": 1,
            "recommended_items": 1,
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
        }

    monkeypatch.setattr(module, "analyze_rss_source", fake_analyze)

    def fake_inbox(*args, **kwargs):
        return {"ok": True, "_status": 200, "items": [], "stats": {}, "_query_mode": "from"}

    monkeypatch.setattr(module, "query_inbox", fake_inbox)
    monkeypatch.setattr(module, "query_inbox_view", fake_inbox)

    def release_soon():
        started.wait(timeout=1)
        time.sleep(0.05)
        release.set()

    worker = threading.Thread(target=release_soon)
    worker.start()
    exit_code = invoke_main(
        module,
        monkeypatch,
        [
            "--csv",
            str(csv_path),
            "--output-dir",
            str(output_dir),
            "--count",
            "4",
            "--concurrency",
            "2",
            "--sleep",
            "0",
            "--max-consecutive-failures",
            "2",
        ],
    )
    worker.join()

    assert exit_code == 4
    assert seen == ["Source 1", "Source 2"]
    run_dir = module.latest_run_dir(output_dir / "runs")
    assert run_dir is not None
    state = json.loads((run_dir / "run_state.json").read_text(encoding="utf-8"))
    assert state["status"] == "stopped_consecutive_failures"
    assert state["completed_count"] == 2
