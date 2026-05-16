from __future__ import annotations

from typing import Any

from app.storage import InboxStore


class RunStore:
    def __init__(self, store: InboxStore):
        self.store = store

    def create_run(self, run: dict[str, Any]) -> dict[str, Any]:
        return self.store.create_ingest_run(run)

    def create_source_result(self, result: dict[str, Any]) -> dict[str, Any]:
        return self.store.create_ingest_run_source(result)

    def list_runs(self, limit: int = 50, offset: int = 0) -> tuple[list[dict[str, Any]], int]:
        return self.store.list_ingest_runs(limit=limit, offset=offset)

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        return self.store.get_ingest_run(run_id)

    def list_run_sources(self, run_id: str) -> list[dict[str, Any]]:
        return self.store.list_ingest_run_sources(run_id)
