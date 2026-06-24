from __future__ import annotations

import argparse
import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def load_items(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Import synthetic materials through the upload API.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--auto-process", action="store_true")
    parser.add_argument("--allow-mock-llm", action="store_true", help="Test-only mode; cannot count as READY validation.")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_absolute():
        path = Path.cwd() / path
    items = load_items(path)
    app = create_app(Settings.from_env())
    client = TestClient(app)
    run_ids: list[str] = []
    for start in range(0, len(items), args.batch_size):
        batch = items[start : start + args.batch_size]
        response = client.post(
            f"/api/materials/batch?allow_mock_llm={'true' if args.allow_mock_llm else 'false'}",
            json={"items": batch, "auto_process": False, "source": "synthetic_fixture_import"},
        )
        response.raise_for_status()
        run_id = response.json()["run_id"]
        run_ids.append(run_id)
        if args.auto_process:
            process = client.post(f"/api/runs/{run_id}/process?allow_mock_llm={'true' if args.allow_mock_llm else 'false'}")
            process.raise_for_status()
    print(json.dumps({"imported": len(items), "run_ids": run_ids, "auto_process": args.auto_process, "allow_mock_llm": args.allow_mock_llm}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
