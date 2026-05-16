from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


NAME_COLUMNS = ["source_name", "title", "name", "源名称"]
CATEGORY_COLUMNS = ["source_category", "category_path", "category", "分类"]
FEED_COLUMNS = ["feed_url", "rss_url", "url", "local_xml_url", "xml_url"]


def first_value(row: dict[str, str], names: list[str]) -> str:
    normalized = {key.strip().lower(): value for key, value in row.items()}
    for name in names:
        value = normalized.get(name.lower())
        if value and str(value).strip():
            return str(value).strip()
    return ""


def read_source_csv(path: Path, *, default_status: str = "active", default_category: str | None = None, source_id_column: str | None = None) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cleaned = {str(k).strip(): "" if v is None else str(v).strip() for k, v in row.items() if k}
            feed_url = first_value(cleaned, FEED_COLUMNS)
            source_name = first_value(cleaned, NAME_COLUMNS)
            if not feed_url or not source_name:
                continue
            source_id = cleaned.get(source_id_column or "", "") if source_id_column else ""
            sources.append(
                {
                    "source_id": source_id or None,
                    "source_name": source_name,
                    "source_category": first_value(cleaned, CATEGORY_COLUMNS) or default_category,
                    "feed_url": feed_url,
                    "status": default_status,
                    "priority": 0,
                    "tags": [],
                    "notes": "",
                    "config": {},
                }
            )
    return sources
