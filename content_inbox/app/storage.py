from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from app.models import NormalizedContent, ScreeningResult
from app.utils import utc_now


class InboxStore:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS inbox_items (
                    item_id TEXT PRIMARY KEY,
                    dedupe_key TEXT NOT NULL UNIQUE,
                    url TEXT,
                    guid TEXT,
                    title TEXT NOT NULL,
                    source_name TEXT NOT NULL,
                    source_category TEXT,
                    content_type TEXT NOT NULL,
                    published_at TEXT,
                    author TEXT,
                    summary TEXT,
                    content_text TEXT,
                    screening_json TEXT NOT NULL,
                    raw_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL,
                    seen_count INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_created_at ON inbox_items(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_source_name ON inbox_items(source_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_content_type ON inbox_items(content_type)")

    def get_by_dedupe_key(self, dedupe_key: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM inbox_items WHERE dedupe_key = ?", (dedupe_key,)
            ).fetchone()
        return row_to_item(row) if row else None

    def mark_seen(self, item_id: str) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE inbox_items
                SET last_seen_at = ?, updated_at = ?, seen_count = seen_count + 1
                WHERE item_id = ?
                """,
                (now, now, item_id),
            )
            row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        return row_to_item(row)

    def insert(
        self,
        dedupe_key: str,
        normalized: NormalizedContent,
        screening: ScreeningResult,
        raw: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        item_id = f"item_{uuid.uuid4().hex}"
        now = utc_now()
        payload = normalized.model_dump()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO inbox_items (
                    item_id, dedupe_key, url, guid, title, source_name, source_category,
                    content_type, published_at, author, summary, content_text,
                    screening_json, raw_json, created_at, updated_at, last_seen_at, seen_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    item_id,
                    dedupe_key,
                    payload.get("url"),
                    payload.get("guid"),
                    payload["title"],
                    payload["source_name"],
                    payload.get("source_category"),
                    payload["content_type"],
                    payload.get("published_at"),
                    payload.get("author"),
                    payload.get("summary"),
                    payload.get("content_text"),
                    json.dumps(screening.model_dump(), ensure_ascii=False),
                    json.dumps(raw or {}, ensure_ascii=False),
                    now,
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        return row_to_item(row)

    def query(self, filters: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
        clauses: list[str] = []
        params: list[Any] = []

        if filters.get("from"):
            clauses.append("created_at >= ?")
            params.append(filters["from"])
        if filters.get("to"):
            clauses.append("created_at <= ?")
            params.append(filters["to"])
        for column in ["source_name", "source_category", "content_type"]:
            if filters.get(column):
                clauses.append(f"{column} = ?")
                params.append(filters[column])
        if filters.get("keyword"):
            clauses.append("(title LIKE ? OR summary LIKE ? OR screening_json LIKE ?)")
            keyword = f"%{filters['keyword']}%"
            params.extend([keyword, keyword, keyword])

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        limit = int(filters.get("limit", 50))
        offset = int(filters.get("offset", 0))

        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM inbox_items {where_sql} ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (*params, limit, offset),
            ).fetchall()
            total = conn.execute(
                f"SELECT COUNT(*) AS total FROM inbox_items {where_sql}", params
            ).fetchone()["total"]

        items = [row_to_item(row) for row in rows]
        return filter_screening(items, filters), int(total)


def row_to_item(row: sqlite3.Row) -> dict[str, Any]:
    screening = json.loads(row["screening_json"])
    return {
        "item_id": row["item_id"],
        "dedupe_key": row["dedupe_key"],
        "title": row["title"],
        "url": row["url"],
        "guid": row["guid"],
        "source_name": row["source_name"],
        "source_category": row["source_category"],
        "content_type": row["content_type"],
        "published_at": row["published_at"],
        "author": row["author"],
        "summary": row["summary"],
        "content_text": row["content_text"],
        "screening": screening,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "last_seen_at": row["last_seen_at"],
        "seen_count": row["seen_count"],
    }


def filter_screening(items: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    actions = set(filters.get("suggested_action") or [])
    for item in items:
        screening = item["screening"]
        if filters.get("category") and screening.get("category") != filters["category"]:
            continue
        if filters.get("followup_type") and screening.get("followup_type") != filters["followup_type"]:
            continue
        if filters.get("tag") and filters["tag"] not in screening.get("tags", []):
            continue
        if filters.get("min_score") and screening.get("value_score", 0) < filters["min_score"]:
            continue
        if filters.get("min_relevance") and screening.get("personal_relevance", 0) < filters["min_relevance"]:
            continue
        if actions and screening.get("suggested_action") not in actions:
            continue
        if not filters.get("include_ignored") and screening.get("suggested_action") == "ignore":
            continue
        result.append(public_item(item))
    return result


def public_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": item["item_id"],
        "title": item["title"],
        "url": item["url"],
        "source_name": item["source_name"],
        "source_category": item["source_category"],
        "content_type": item["content_type"],
        "published_at": item["published_at"],
        "author": item["author"],
        "summary": item["summary"],
        "screening": item["screening"],
        "created_at": item["created_at"],
        "last_seen_at": item["last_seen_at"],
        "seen_count": item["seen_count"],
    }

