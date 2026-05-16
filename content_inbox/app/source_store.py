from __future__ import annotations

from typing import Any

from app.storage import InboxStore


class SourceStore:
    def __init__(self, store: InboxStore):
        self.store = store

    def create(self, payload: dict[str, Any]) -> tuple[dict[str, Any], bool]:
        return self.store.create_rss_source(payload)

    def get(self, source_id: str) -> dict[str, Any] | None:
        return self.store.get_rss_source(source_id)

    def list(self, filters: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
        return self.store.list_rss_sources(filters)

    def update(self, source_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        return self.store.update_rss_source(source_id, updates)

    def disable(self, source_id: str) -> dict[str, Any] | None:
        return self.store.disable_rss_source(source_id)
