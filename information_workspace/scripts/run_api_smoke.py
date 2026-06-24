from __future__ import annotations

import argparse
import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.time_utils import timestamp_slug, utc_now


def sample_material(index: int = 1) -> dict:
    return {
        "title": f"API smoke material {index}",
        "content_text": "This synthetic API smoke material validates upload, run processing, search, detail, Event, Topic, and export behavior without claiming to be real news.",
        "source_name": "API Smoke",
        "source_type": "api",
        "metadata": {
            "synthetic": True,
            "fixture_group": "api_smoke",
            "test_purpose": ["api_smoke"],
            "expected_behavior": "exercise core API path",
            "generated_by": "codex_goal_04",
            "event_key": "api_smoke_event",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run API smoke against an isolated temp SQLite database.")
    parser.add_argument("--allow-mock-llm", action="store_true")
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    run_dir = base / "outputs" / "test_runs" / timestamp_slug()
    run_dir.mkdir(parents=True, exist_ok=True)
    settings = Settings.from_env()
    settings = Settings(
        db_path=run_dir / "api_smoke.db",
        outputs_dir=base / "outputs",
        deepseek_api_key=settings.deepseek_api_key,
        deepseek_model=settings.deepseek_model,
        llm_provider=settings.llm_provider,
        api_host=settings.api_host,
        api_port=settings.api_port,
    )
    app = create_app(settings)
    client = TestClient(app)
    commands = []
    failures = []

    def record(name: str, response):
        commands.append(f"{name}: {response.status_code}")
        if response.status_code >= 400:
            failures.append(f"{name}: {response.text}")
        return response

    suffix = "true" if args.allow_mock_llm else "false"
    upload = record(
        "POST /api/materials/batch",
        client.post(
            f"/api/materials/batch?allow_mock_llm={suffix}",
            json={"items": [sample_material(1), sample_material(2)], "auto_process": False, "source": "api_smoke"},
        ),
    )
    upload.raise_for_status()
    run_id = upload.json()["run_id"]
    process = record("POST /api/runs/{id}/process", client.post(f"/api/runs/{run_id}/process?allow_mock_llm={suffix}"))
    process.raise_for_status()
    run = record("GET /api/runs/{id}", client.get(f"/api/runs/{run_id}"))
    run.raise_for_status()
    materials = record("GET /api/materials", client.get("/api/materials?include_noise=true&synthetic=true"))
    materials.raise_for_status()
    material_ids = [item["id"] for item in materials.json()["items"]]
    detail = record("GET /api/materials/{id}", client.get(f"/api/materials/{material_ids[0]}"))
    detail.raise_for_status()
    event = record(
        "POST /api/events/from-materials",
        client.post(f"/api/events/from-materials?allow_mock_llm={suffix}", json={"material_ids": material_ids[:1], "user_focus": "API smoke"}),
    )
    event.raise_for_status()
    topic = record(
        "POST /api/topics",
        client.post("/api/topics", json={"title": "API Smoke Topic", "goal": "Validate API flow", "organization": "Evidence first", "material_ids": material_ids}),
    )
    topic.raise_for_status()
    topic_id = topic.json()["id"]
    refresh = record(
        "POST /api/topics/{id}/refresh-structure",
        client.post(f"/api/topics/{topic_id}/refresh-structure", json={"include_new_materials": True, "allow_mock_llm": args.allow_mock_llm}),
    )
    refresh.raise_for_status()
    confirm = record("POST /api/topics/{id}/confirm-candidate", client.post(f"/api/topics/{topic_id}/confirm-candidate"))
    confirm.raise_for_status()
    export = record("POST /api/exports/topic/{id}", client.post(f"/api/exports/topic/{topic_id}"))
    export.raise_for_status()

    summary = run_dir / "summary.md"
    summary.write_text(
        "\n".join(
            [
                "# API Smoke Summary",
                "",
                f"- Created: {utc_now()}",
                f"- Database: {settings.db_path}",
                f"- allow_mock_llm: {args.allow_mock_llm}",
                f"- Run ID: {run_id}",
                f"- Material IDs: {', '.join(material_ids)}",
                f"- Export path: {export.json()['file_path']}",
                f"- Result: {'FAILED' if failures else 'PASSED'}",
                "",
                "## Commands",
                "",
                *[f"- {item}" for item in commands],
                "",
                "## Failures",
                "",
                *([f"- {item}" for item in failures] or ["- None"]),
                "",
                "Mock LLM mode is test-only and does not satisfy final DeepSeek READY validation." if args.allow_mock_llm else "DeepSeek mode was requested for this smoke.",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"summary_path": str(summary), "run_id": run_id, "material_ids": material_ids, "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
