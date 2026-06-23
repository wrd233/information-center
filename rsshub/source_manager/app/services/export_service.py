from __future__ import annotations

from typing import Any

from app.config import AppConfig, settings
from app.services.source_service import SourceService
from app.utils.csv_io import write_csv
from app.utils.opml import build_opml


CLEAN_FIELDS = [
    "source_id",
    "display_name",
    "source_type",
    "category",
    "tags",
    "rating",
    "status",
    "adapter_id",
    "route_path",
    "feed_url",
    "original_feed_url",
    "notes",
]

FULL_EXTRA_FIELDS = [
    "last_checked_at",
    "last_check_status",
    "last_success_at",
    "last_failure_at",
    "consecutive_failures",
    "last_error",
    "total_entries_seen",
    "last_fetch_new_count",
    "last_fetch_existing_count",
    "last_fetch_scanned_count",
]


class ExportService:
    def __init__(self, source_service: SourceService, config: AppConfig | None = None):
        self.source_service = source_service
        self.config = config or settings

    def export_rows(self, include_disabled: bool = False) -> list[dict[str, Any]]:
        sources, _total, _stats = self.source_service.sources.list(include_disabled=include_disabled, limit=100000)
        rows = []
        for source in sources:
            row = dict(source)
            row["tags"] = ",".join(row.get("tags") or [])
            rows.append(row)
        return rows

    def csv(self, mode: str = "clean") -> str:
        fields = CLEAN_FIELDS + (FULL_EXTRA_FIELDS if mode == "full" else [])
        return write_csv(self.export_rows(include_disabled=True), fields)

    def opml(self, profile: str = "local") -> str:
        profile_config = self.config.export_profiles.get(profile, self.config.export_profiles.get("local", {}))
        rows = []
        sources, _total, _stats = self.source_service.sources.list(include_disabled=False, limit=100000)
        for source in sources:
            feed_url = self.profile_url(source, profile_config)
            if feed_url:
                rows.append({"display_name": source["display_name"], "category": source["category"], "feed_url": feed_url})
        return build_opml(rows)

    def profile_url(self, source: dict[str, Any], profile_config: dict[str, Any]) -> str | None:
        if profile_config.get("prefer_original_feed_url") and source.get("original_feed_url"):
            return source["original_feed_url"]
        if source.get("source_type") == "rsshub" and source.get("route_path"):
            base = profile_config.get("rsshub_base_url") or self.config.adapters.get("rsshub_local", {}).get("base_url")
            return str(base).rstrip("/") + source["route_path"]
        if source.get("source_type") == "wechat":
            if source.get("feed_url"):
                return source["feed_url"]
            identity = source.get("wechat_identity") or {}
            if identity.get("feed_url"):
                return identity["feed_url"]
        return source.get("feed_url") or source.get("original_feed_url")

