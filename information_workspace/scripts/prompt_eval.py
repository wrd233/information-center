from __future__ import annotations

import argparse
import json

from app.config import Settings
from app.service import WorkspaceService


def main() -> int:
    parser = argparse.ArgumentParser(description="Run prompt_eval for information_workspace.")
    parser.add_argument("--task", required=True, choices=["light_understanding", "event_candidate", "topic_structure"])
    parser.add_argument("--material-id", action="append", default=[])
    parser.add_argument("--run-id")
    parser.add_argument("--fixture-file")
    parser.add_argument("--fixture-group")
    parser.add_argument("--test-purpose")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--allow-mock-llm", action="store_true", help="Test-only mode; cannot count as READY validation.")
    args = parser.parse_args()

    service = WorkspaceService(Settings.from_env())
    result = service.prompt_eval(
        task=args.task,
        material_ids=args.material_id,
        run_id=args.run_id,
        fixture_file=args.fixture_file,
        fixture_group=args.fixture_group,
        test_purpose=args.test_purpose,
        limit=args.limit,
        allow_mock_llm=args.allow_mock_llm,
        concurrency=args.concurrency,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
