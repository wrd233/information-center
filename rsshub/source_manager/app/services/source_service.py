from __future__ import annotations

from typing import Any

from app.adapters.native import NativeAdapter
from app.adapters.rsshub import RsshubAdapter
from app.adapters.wechat import WechatAdapter
from app.config import AppConfig, settings
from app.models.schemas import SourceCreate, SourceResponse, SourceUpdate
from app.storage.db import Database
from app.storage.repositories import EntryRepository, RunRepository, SourceRepository
from app.utils.url_normalize import normalize_url


class SourceService:
    def __init__(self, db: Database | None = None, config: AppConfig | None = None):
        self.config = config or settings
        self.db = db or Database(self.config.database_path)
        self.sources = SourceRepository(self.db)
        self.entries = EntryRepository(self.db)
        self.runs = RunRepository(self.db)

    def adapter_for(self, source: dict[str, Any]):
        source_type = source.get("source_type")
        if source_type == "rsshub":
            return RsshubAdapter(self.config)
        if source_type == "wechat":
            return WechatAdapter(self.config)
        return NativeAdapter(self.config)

    def resolved_url(self, source: dict[str, Any]) -> str | None:
        try:
            return self.adapter_for(source).resolve_url(source)
        except Exception:
            return source.get("feed_url")

    def as_response(self, source: dict[str, Any]) -> SourceResponse:
        return SourceResponse(**source, resolved_feed_url=self.resolved_url(source))

    def normalize_create(self, payload: SourceCreate) -> dict[str, Any]:
        data = payload.model_dump(exclude={"allow_duplicate", "check_before_save"})
        if data["source_type"] == "rsshub":
            data["adapter_id"] = data.get("adapter_id") or "rsshub_local"
            data["feed_url"] = data.get("feed_url") or None
        elif data["source_type"] == "wechat":
            data["adapter_id"] = data.get("adapter_id") or "wechat_local"
            identity = data.get("wechat_identity") or {}
            data["feed_url"] = data.get("feed_url") or identity.get("feed_url")
        else:
            data["adapter_id"] = data.get("adapter_id") or "native_default"
            if data.get("feed_url"):
                data["feed_url"] = normalize_url(data["feed_url"])
        data["rating"] = max(0, min(100, int(data.get("rating", 50))))
        data["category"] = data.get("category") or "未分类"
        return data

    def create(self, payload: SourceCreate) -> SourceResponse:
        data = self.normalize_create(payload)
        duplicates = self.sources.duplicate_candidates(data)
        if duplicates and not payload.allow_duplicate:
            raise ValueError(f"duplicate source: {duplicates[0]['source_id']}")
        if payload.check_before_save:
            adapter = self.adapter_for(data)
            result = adapter.check(data)
            data["status"] = "active" if result.ok else "paused"
            data["last_checked_at"] = result.checked_at
            data["last_check_status"] = "ok" if result.ok else "failed"
            data["last_check_error"] = result.error
        else:
            data["status"] = data.get("status") or "paused"
        return self.as_response(self.sources.create(data))

    def get(self, source_id: str) -> SourceResponse | None:
        source = self.sources.get(source_id)
        return self.as_response(source) if source else None

    def detail(self, source_id: str) -> dict[str, Any] | None:
        source = self.sources.get(source_id)
        if not source:
            return None
        return {
            "source": self.as_response(source),
            "recent_entries": self.entries.recent_for_source(source_id, 20),
            "recent_fetch_runs": self.runs.recent_for_source(source_id, 10),
        }

    def list(self, **filters: Any) -> tuple[list[SourceResponse], int, dict[str, Any]]:
        sources, total, stats = self.sources.list(**filters)
        return [self.as_response(source) for source in sources], total, stats

    def update(self, source_id: str, payload: SourceUpdate) -> SourceResponse | None:
        updates = payload.model_dump(exclude_unset=True)
        allow_duplicate = bool(updates.pop("allow_duplicate", False))
        current = self.sources.get(source_id)
        if not current:
            return None
        candidate = {**current, **updates}
        if candidate.get("source_type") == "native" and candidate.get("feed_url"):
            candidate["feed_url"] = normalize_url(candidate["feed_url"])
            updates["feed_url"] = candidate["feed_url"]
        duplicates = [item for item in self.sources.duplicate_candidates(candidate) if item["source_id"] != source_id]
        if duplicates and not allow_duplicate:
            raise ValueError(f"duplicate source: {duplicates[0]['source_id']}")
        updated = self.sources.update(source_id, updates)
        return self.as_response(updated) if updated else None

    def delete(self, source_id: str) -> SourceResponse | None:
        source = self.sources.soft_delete(source_id)
        return self.as_response(source) if source else None

    def batch_update(self, source_ids: list[str], updates: dict[str, Any]) -> list[SourceResponse]:
        results = []
        for source_id in source_ids:
            updated = self.sources.update(source_id, updates)
            if updated:
                results.append(self.as_response(updated))
        return results

