from __future__ import annotations

import json

from app.config import Settings
from app.service import WorkspaceService


def main() -> int:
    service = WorkspaceService(Settings.from_env())
    print(json.dumps(service.cleanup_synthetic(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
