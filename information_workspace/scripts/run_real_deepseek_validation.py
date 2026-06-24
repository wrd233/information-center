from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.service import WorkspaceService
from app.time_utils import timestamp_slug, utc_now


def load_fixture(path: Path, limit: int) -> list[dict[str, Any]]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        metadata = item.get("metadata") or {}
        if metadata.get("fixture_group") in {"basic_news", "technical_article", "uncertain", "noise"}:
            items.append(item)
        if len(items) >= limit:
            break
    return items


def read_trace_summary(trace_dir: str | None, max_files: int = 12) -> list[dict[str, Any]]:
    if not trace_dir:
        return []
    root = Path(trace_dir)
    summaries = []
    for path in sorted(root.glob("*.json"))[:max_files]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            summaries.append({"path": str(path), "error": "invalid trace JSON"})
            continue
        summaries.append(
            {
                "path": str(path),
                "provider": data.get("provider"),
                "model": data.get("model"),
                "task_name": data.get("task_name"),
                "final_status": data.get("final_status"),
                "schema": data.get("schema_validation_result"),
                "semantic_check": data.get("semantic_check"),
            }
        )
    return summaries


def count_trace_warnings(trace_dir: str | None) -> int:
    if not trace_dir:
        return 0
    count = 0
    for path in Path(trace_dir).glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            count += 1
            continue
        if (data.get("semantic_check") or {}).get("status") == "warning":
            count += 1
        if data.get("final_status") != "succeeded":
            count += 1
    return count


def fixture_count(path: Path, *, fixture_group: str | None = None, test_purpose: str | None = None) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        metadata = item.get("metadata") or {}
        if fixture_group and metadata.get("fixture_group") != fixture_group:
            continue
        if test_purpose and test_purpose not in metadata.get("test_purpose", []):
            continue
        count += 1
    return count


def write_report(path: Path, *, verdict: str, settings: Settings, sections: list[str], failures: list[str]) -> None:
    path.write_text(
        "\n".join(
            [
                "# Real DeepSeek Validation",
                "",
                f"- Created: {utc_now()}",
                f"- Provider: {settings.llm_provider}",
                f"- Model: {settings.deepseek_model}",
                f"- DeepSeek key configured: {settings.deepseek_configured}",
                f"- Verdict: {verdict}",
                "",
                *sections,
                "",
                "## Failures / Gaps",
                "",
                *([f"- {item}" for item in failures] or ["- None"]),
                "",
                "## Secret Handling",
                "",
                "This script never prints or writes the API key. It only reports whether configuration exists.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run real DeepSeek validation without exposing secrets.")
    parser.add_argument("--fixture-file", default="fixtures/synthetic_materials/synthetic_materials_500.jsonl")
    parser.add_argument("--sample-limit", type=int, default=8)
    parser.add_argument("--light-concurrency", type=int, default=6)
    parser.add_argument("--all-light", action="store_true", help="Run light_understanding prompt_eval over all fixture materials. Required for final READY.")
    parser.add_argument("--all-topic", action="store_true", help="Run topic_structure over all applicable topic_structure fixture materials.")
    parser.add_argument("--import-sample", action="store_true", help="Also import a small fixture sample through the real upload/process API.")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    settings = Settings.from_env()
    service = WorkspaceService(settings)
    run_dir = settings.outputs_dir / "test_runs" / timestamp_slug()
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "real_deepseek_validation.md"
    failures: list[str] = []
    sections: list[str] = []

    if settings.llm_provider != "deepseek":
        failures.append(f"Expected llm_provider=deepseek, got {settings.llm_provider}")
    if not settings.deepseek_configured:
        failures.append("DEEPSEEK_API_KEY is not configured in the current runtime")
        write_report(report_path, verdict="BLOCKED", settings=settings, sections=sections, failures=failures)
        print(json.dumps({"verdict": "BLOCKED", "report_path": str(report_path), "failures": failures}, indent=2))
        return 2

    fixture = Path(args.fixture_file)
    if not fixture.is_absolute():
        fixture = base / fixture
    if not fixture.exists():
        failures.append(f"Fixture file does not exist: {fixture}")
        write_report(report_path, verdict="BLOCKED", settings=settings, sections=sections, failures=failures)
        print(json.dumps({"verdict": "BLOCKED", "report_path": str(report_path), "failures": failures}, indent=2))
        return 2

    try:
        light_limit = None if args.all_light else args.sample_limit
        light = service.prompt_eval(
            task="light_understanding",
            fixture_file=str(fixture),
            limit=light_limit,
            allow_mock_llm=False,
            concurrency=args.light_concurrency,
        )
        sections.extend(
            [
                "## light_understanding Prompt Eval",
                "",
                f"- Summary: {light['summary_path']}",
                f"- Trace dir: {light['trace_dir']}",
                f"- Coverage: `{json.dumps(light['coverage'], ensure_ascii=False)}`",
                f"- Succeeded: {light['succeeded']}",
                f"- Failed: {light['failed']}",
                f"- Semantic warnings: {count_trace_warnings(light.get('trace_dir'))}",
                "",
                "### Trace Semantic Samples",
                "",
                "```json",
                json.dumps(read_trace_summary(light.get("trace_dir")), ensure_ascii=False, indent=2),
                "```",
            ]
        )
        if light["failed"]:
            failures.append("light_understanding real DeepSeek prompt_eval had failures")
        light_warnings = count_trace_warnings(light.get("trace_dir"))
        if light_warnings:
            failures.append(f"light_understanding real DeepSeek prompt_eval had {light_warnings} semantic warning(s)")
        if not args.all_light:
            failures.append("light_understanding did not cover all 500+ fixture materials; rerun with --all-light for READY")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"light_understanding real DeepSeek validation failed: {exc}")

    eval_specs: list[tuple[str, dict[str, Any]]] = []
    event_groups = ["multi_source_same_event", "multi_day_event", "event_background", "weakly_related_event"]
    for group in event_groups:
        eval_specs.append(("event_candidate", {"fixture_group": group}))
    if args.all_topic:
        topic_groups = [
            "long_article",
            "opinion_piece",
            "technical_article",
            "topic_material",
            "topic_structure_refresh",
            "event_background",
            "conflicting_reports",
        ]
        for group in topic_groups:
            eval_specs.append(("topic_structure", {"fixture_group": group}))
    else:
        eval_specs.append(("topic_structure", {"test_purpose": "topic_structure", "limit": args.sample_limit * 4}))

    topic_actual_total = 0
    topic_expected_total = 0
    event_actual_total = 0
    event_expected_total = 0
    for task, kwargs in eval_specs:
        try:
            result = service.prompt_eval(task=task, fixture_file=str(fixture), allow_mock_llm=False, **kwargs)
            sections.extend(
                [
                    f"## {task} Prompt Eval",
                    "",
                    f"- Summary: {result['summary_path']}",
                    f"- Trace dir: {result['trace_dir']}",
                    f"- Coverage: `{json.dumps(result['coverage'], ensure_ascii=False)}`",
                    f"- Succeeded: {result['succeeded']}",
                    f"- Failed: {result['failed']}",
                    f"- Semantic warnings: {count_trace_warnings(result.get('trace_dir'))}",
                    "",
                    "### Trace Semantic Samples",
                    "",
                    "```json",
                    json.dumps(read_trace_summary(result.get("trace_dir")), ensure_ascii=False, indent=2),
                    "```",
                ]
            )
            if result["failed"]:
                failures.append(f"{task} real DeepSeek prompt_eval had failures")
            task_warnings = count_trace_warnings(result.get("trace_dir"))
            if task_warnings:
                failures.append(f"{task} real DeepSeek prompt_eval for {kwargs} had {task_warnings} semantic warning(s)")
            expected = result["coverage"].get("expected_count")
            actual = result["coverage"].get("actual_count")
            if task == "event_candidate":
                event_actual_total += int(actual or 0)
                event_expected_total += int(expected or 0)
                if actual < expected:
                    failures.append(f"event_candidate did not cover all materials for {kwargs}")
            if task == "topic_structure":
                topic_actual_total += int(actual or 0)
                topic_expected_total += int(expected or 0)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{task} real DeepSeek validation failed: {exc}")
    if event_expected_total and event_actual_total < event_expected_total:
        failures.append(f"event_candidate coverage incomplete: {event_actual_total}/{event_expected_total}")
    if args.all_topic:
        all_topic_expected = fixture_count(fixture, test_purpose="topic_structure")
        if topic_actual_total < all_topic_expected:
            failures.append(f"topic_structure coverage incomplete: {topic_actual_total}/{all_topic_expected}")
    else:
        failures.append("topic_structure did not cover all applicable fixture materials; rerun with --all-topic for READY")

    if args.import_sample:
        try:
            sample = load_fixture(fixture, args.sample_limit)
            app = create_app(settings)
            client = TestClient(app)
            upload = client.post("/api/materials/batch", json={"items": sample, "auto_process": False, "source": "real_deepseek_validation"})
            upload.raise_for_status()
            run_id = upload.json()["run_id"]
            process = client.post(f"/api/runs/{run_id}/process")
            process.raise_for_status()
            run = client.get(f"/api/runs/{run_id}")
            run.raise_for_status()
            sections.extend(
                [
                    "## Real API Import/Process Sample",
                    "",
                    f"- Run ID: {run_id}",
                    f"- Status: {run.json().get('status')}",
                    f"- Materials: {len(run.json().get('material_ids', []))}",
                ]
            )
            if run.json().get("status") != "succeeded":
                failures.append(f"Real API import/process sample did not succeed: {run.json().get('error_summary')}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"real API import/process sample failed: {exc}")

    verdict = "PASSED" if not failures else "PARTIAL"
    write_report(report_path, verdict=verdict, settings=settings, sections=sections, failures=failures)
    print(json.dumps({"verdict": verdict, "report_path": str(report_path), "failures": failures}, indent=2))
    return 0 if verdict == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
