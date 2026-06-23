from __future__ import annotations

from typing import Any

from app.config import AppConfig, settings
from app.models.schemas import ImportStrategy, SourceCreate, SourceUpdate
from app.services.source_service import SourceService
from app.utils.csv_io import parse_csv
from app.utils.opml import parse_opml
from app.utils.url_normalize import normalize_url, route_from_rsshub_url


def priority_to_rating(value: str | None) -> int:
    mapping = {"p0": 90, "p1": 75, "p2": 50, "p3": 30}
    return mapping.get((value or "").strip().lower(), 50)


def import_status(value: str | None) -> str:
    text = (value or "").strip().lower()
    if text in {"active", "paused", "disabled"}:
        return text
    return "paused"


class ImportService:
    def __init__(self, source_service: SourceService, config: AppConfig | None = None):
        self.source_service = source_service
        self.config = config or settings

    def infer_source(self, row: dict[str, str]) -> dict[str, Any]:
        feed_url = row.get("feed_url") or row.get("xml_url") or row.get("xmlurl") or row.get("rss_url") or ""
        local_url = row.get("local_xml_url") or ""
        preferred_url = local_url or feed_url
        tags = row.get("tags") or ""
        tags_list = [item.strip() for item in tags.replace("、", ",").split(",") if item.strip()]
        category = row.get("category") or row.get("category_path") or row.get("top_category") or "未分类"
        display_name = row.get("display_name") or row.get("title") or preferred_url
        rsshub_bases = [
            str(adapter.get("base_url"))
            for adapter in self.config.adapters.values()
            if adapter.get("type") == "rsshub" and adapter.get("base_url")
        ]
        route_path = route_from_rsshub_url(preferred_url, rsshub_bases)
        if route_path:
            source_type = "rsshub"
            adapter_id = "rsshub_local"
            feed_value = None
        elif "8003/feed/" in preferred_url or "MP_WXS_" in preferred_url:
            source_type = "wechat"
            adapter_id = "wechat_local"
            feed_value = preferred_url
        else:
            source_type = "native"
            adapter_id = "native_default"
            feed_value = normalize_url(preferred_url)
        rating = row.get("rating")
        if rating is None or rating == "":
            rating = priority_to_rating(row.get("priority"))
        return {
            "source_type": source_type,
            "display_name": display_name,
            "status": import_status(row.get("status")),
            "category": category or "未分类",
            "tags": tags_list,
            "rating": int(rating) if str(rating).isdigit() else priority_to_rating(row.get("priority")),
            "notes": row.get("notes") or row.get("source_comment") or None,
            "adapter_id": adapter_id,
            "route_path": route_path,
            "feed_url": feed_value,
            "original_feed_url": row.get("original_feed_url") or feed_url or None,
            "wechat_identity": {"feed_url": feed_value} if source_type == "wechat" and feed_value else {},
        }

    def rows_for(self, import_type: str, content: str) -> list[dict[str, Any]]:
        raw_rows = parse_csv(content) if import_type == "csv" else parse_opml(content)
        return [self.infer_source(row) for row in raw_rows]

    def preview(self, import_type: str, content: str, filename: str | None = None) -> dict[str, Any]:
        items = []
        summary = {"new": 0, "duplicate": 0, "skipped": 0, "failed": 0, "update": 0}
        for index, row in enumerate(self.rows_for(import_type, content), start=1):
            try:
                duplicates = self.source_service.sources.duplicate_candidates(row)
                action = "duplicate" if duplicates else "new"
                summary[action] += 1
                items.append(
                    {
                        "index": index,
                        "action": action,
                        "duplicate_source_ids": [item["source_id"] for item in duplicates],
                        "source": row,
                    }
                )
            except Exception as exc:
                summary["failed"] += 1
                items.append({"index": index, "action": "failed", "error": str(exc), "source": row})
        return {"ok": True, "import_type": import_type, "filename": filename, "summary": summary, "items": items}

    def commit(
        self,
        import_type: str,
        content: str,
        *,
        filename: str | None = None,
        strategy: ImportStrategy = "skip",
    ) -> dict[str, Any]:
        preview = self.preview(import_type, content, filename)
        summary = {"created": 0, "updated": 0, "skipped": 0, "duplicate": 0, "failed": 0}
        created_ids: list[str] = []
        for item in preview["items"]:
            if item["action"] == "failed":
                summary["failed"] += 1
                continue
            source_data = item["source"]
            duplicates = item["duplicate_source_ids"]
            if duplicates:
                if strategy == "skip":
                    summary["skipped"] += 1
                    summary["duplicate"] += 1
                    continue
                target_id = duplicates[0]
                updates = self.updates_for_strategy(source_data, strategy)
                if updates:
                    self.source_service.update(target_id, SourceUpdate(**updates, allow_duplicate=True))
                    summary["updated"] += 1
                else:
                    summary["skipped"] += 1
                continue
            try:
                created = self.source_service.create(SourceCreate(**source_data, allow_duplicate=True))
                created_ids.append(created.source_id)
                summary["created"] += 1
            except Exception:
                summary["failed"] += 1
        run_id = self.source_service.runs.create_import_run(
            {
                "import_type": import_type,
                "filename": filename,
                "status": "ok" if summary["failed"] == 0 else "partial_failed",
                "created_count": summary["created"],
                "updated_count": summary["updated"],
                "skipped_count": summary["skipped"],
                "duplicate_count": summary["duplicate"],
                "failed_count": summary["failed"],
                "strategy": strategy,
            }
        )
        return {"ok": summary["failed"] == 0, "import_run_id": run_id, "summary": summary, "created_source_ids": created_ids}

    def updates_for_strategy(self, source_data: dict[str, Any], strategy: str) -> dict[str, Any]:
        clean = {
            key: source_data.get(key)
            for key in [
                "display_name",
                "status",
                "category",
                "tags",
                "rating",
                "notes",
                "adapter_id",
                "route_path",
                "feed_url",
                "original_feed_url",
                "wechat_identity",
            ]
        }
        if strategy == "fill_empty":
            return {key: value for key, value in clean.items() if value not in (None, "", [], {})}
        if strategy == "overwrite_metadata":
            return {key: clean[key] for key in ["status", "category", "tags", "rating", "notes"] if clean.get(key) is not None}
        if strategy == "overwrite_all":
            return {key: value for key, value in clean.items() if value is not None}
        return {}

