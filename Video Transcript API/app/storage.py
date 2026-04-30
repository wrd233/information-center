from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


class TaskStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, payload: dict, platform: str = "bilibili") -> dict:
        task_id = uuid.uuid4().hex
        now = utc_now()
        task = {
            "id": task_id,
            "platform": platform,
            "source_url": payload["url"],
            "status": "queued",
            "created_at": now,
            "updated_at": now,
            "note": payload.get("note"),
            "project": payload.get("project"),
            "options": {
                "select_page": payload.get("select_page", "ALL"),
                "download_audio": payload.get("download_audio", True),
                "download_audio_if_no_subtitle": payload.get(
                    "download_audio_if_no_subtitle", True
                ),
                "download_video": payload.get("download_video", True),
                "extract_audio": payload.get("extract_audio", True),
                "skip_existing_download_record": payload.get(
                    "skip_existing_download_record", False
                ),
            },
            "result": None,
            "error": None,
        }
        self.save(task)
        return task

    def save(self, task: dict) -> None:
        task["updated_at"] = utc_now()
        self.task_path(task["id"]).write_text(
            json.dumps(task, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get(self, task_id: str) -> dict | None:
        path = self.task_path(task_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list(self) -> list[dict]:
        tasks = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self.root.glob("*.json"), reverse=True)
        ]
        return sorted(tasks, key=lambda task: task["created_at"], reverse=True)

    def task_workspace(self, task_id: str) -> Path:
        path = self.root / task_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def task_path(self, task_id: str) -> Path:
        return self.root / f"{task_id}.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
