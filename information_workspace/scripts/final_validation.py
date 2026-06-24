from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from app.config import Settings
from app.service import WorkspaceService
from app.time_utils import timestamp_slug, utc_now


def run_command(command: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(command, cwd=str(cwd), text=True, capture_output=True, check=False)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def scan_real_deepseek_traces(outputs_dir: Path) -> dict[str, Any]:
    trace_roots = [outputs_dir / "llm_traces", outputs_dir / "prompt_evals"]
    counts: dict[str, int] = {}
    examples: list[str] = []
    failed = 0
    warnings = 0
    for root in trace_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("provider") != "deepseek":
                continue
            if (data.get("semantic_check") or {}).get("status") == "warning":
                warnings += 1
            task = data.get("task_name", "unknown")
            if data.get("final_status") == "succeeded":
                counts[task] = counts.get(task, 0) + 1
                if len(examples) < 8:
                    examples.append(str(path))
            else:
                failed += 1
    return {"counts": counts, "examples": examples, "failed": failed, "warnings": warnings}


def latest_real_deepseek_report(outputs_dir: Path) -> str | None:
    reports = sorted((outputs_dir / "test_runs").glob("*/real_deepseek_validation.md"))
    if not reports:
        return None
    return str(reports[-1])


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    run_dir = base / "outputs" / "test_runs" / timestamp_slug()
    run_dir.mkdir(parents=True, exist_ok=True)
    settings = Settings.from_env()
    service = WorkspaceService(settings)
    commands = []
    failures = []

    for command in [
        [sys.executable, "fixtures/synthetic_materials/validate_synthetic_materials.py", "fixtures/synthetic_materials/synthetic_materials_500.jsonl"],
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "scripts/run_api_smoke.py", "--allow-mock-llm"],
        [sys.executable, "frontend/smoke_frontend.py", "--allow-mock-llm"],
        [sys.executable, "-m", "compileall", "app", "scripts", "frontend/smoke_frontend.py", "fixtures/synthetic_materials", "tests"],
    ]:
        code, output = run_command(command, base)
        commands.append({"command": " ".join(command), "exit_code": code, "output": output[-1200:]})
        if code != 0:
            failures.append(f"command failed: {' '.join(command)}")

    health = service.health()
    with service.connect() as conn:
        synthetic_material_count = conn.execute("SELECT COUNT(*) AS count FROM materials WHERE synthetic=1").fetchone()["count"]
        synthetic_deepseek_light_count = conn.execute(
            """
            SELECT COUNT(DISTINCT l.material_id) AS count
            FROM llm_call_summaries l
            JOIN materials m ON m.id=l.material_id
            WHERE m.synthetic=1
              AND l.task_name='light_understanding'
              AND l.provider='deepseek'
              AND l.status='succeeded'
            """
        ).fetchone()["count"]
    deepseek_ready = bool(health["deepseek_configured"] and health["llm_provider"] == "deepseek")
    if not deepseek_ready:
        failures.append("DeepSeek key is not configured in the current runtime")
    if synthetic_material_count < 500:
        failures.append(f"Synthetic materials in SQLite below 500: {synthetic_material_count}")
    if synthetic_deepseek_light_count < 500:
        failures.append(f"Synthetic materials with successful real DeepSeek light_understanding below 500: {synthetic_deepseek_light_count}")

    real_traces = scan_real_deepseek_traces(settings.outputs_dir)
    latest_real_report = latest_real_deepseek_report(settings.outputs_dir)
    required_real_tasks = {"light_understanding", "event_candidate", "topic_structure"}
    missing_real_tasks = sorted(task for task in required_real_tasks if real_traces["counts"].get(task, 0) == 0)
    if missing_real_tasks:
        failures.append(f"Missing successful real DeepSeek traces for tasks: {', '.join(missing_real_tasks)}")
    if not latest_real_report:
        failures.append("No real DeepSeek validation report found")
    else:
        latest_real_text = Path(latest_real_report).read_text(encoding="utf-8")
        if "Verdict: PASSED" not in latest_real_text:
            failures.append("Latest real DeepSeek validation report is not PASSED")

    verdict = "READY" if not failures else "PARTIAL"
    report = run_dir / "final_validation_report.md"
    report.write_text(
        "\n".join(
            [
                "# Final Validation Report",
                "",
                f"- Created: {utc_now()}",
                f"- Database path: {settings.db_path}",
                f"- Outputs path: {settings.outputs_dir}",
                f"- DeepSeek configured: {health['deepseek_configured']}",
                f"- LLM provider: {health['llm_provider']}",
                f"- Final status: {verdict}",
                f"- Latest real DeepSeek validation report: {latest_real_report or 'not found'}",
                f"- Synthetic materials in SQLite: {synthetic_material_count}",
                f"- Synthetic materials with real DeepSeek light_understanding: {synthetic_deepseek_light_count}",
                "",
                "## Commands",
                "",
                *[f"- `{item['command']}` -> {item['exit_code']}" for item in commands],
                "",
                "## Command Output Summaries",
                "",
                "```json",
                json.dumps(commands, indent=2),
                "```",
                "",
                "## Failures And Unfinished Items",
                "",
                *([f"- {item}" for item in failures] or ["- None"]),
                "",
                "## Real DeepSeek Trace Evidence",
                "",
                "```json",
                json.dumps(real_traces, indent=2),
                "```",
                "",
                "## Safety Check",
                "",
                "This validation script does not print or inspect `.env`; it only reports whether a DeepSeek key appears configured through application settings.",
            ]
        ),
        encoding="utf-8",
    )
    summary = run_dir / "summary.md"
    summary.write_text(
        f"# Test Run Summary\n\n- Created: {utc_now()}\n- Final validation report: {report}\n- Verdict: {verdict}\n",
        encoding="utf-8",
    )
    print(json.dumps({"verdict": verdict, "summary_path": str(summary), "final_validation_report": str(report), "failures": failures}, indent=2))
    return 0 if verdict == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
