from __future__ import annotations

import json
import sqlite3
from typing import Any

from app.storage.db import Database
from app.utils.ids import new_entry_id, new_fetch_run_id, new_import_run_id, new_source_id
from app.utils.time import utc_now


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return dict(row)


def source_from_row(row: sqlite3.Row | dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    data = dict(row)
    data["tags"] = json.loads(data.pop("tags_json") or "[]")
    data["wechat_identity"] = json.loads(data.pop("wechat_identity_json") or "{}")
    return data


def source_to_db(data: dict[str, Any]) -> dict[str, Any]:
    result = dict(data)
    if "tags" in result:
        result["tags_json"] = json.dumps(result.pop("tags"), ensure_ascii=False)
    if "wechat_identity" in result:
        result["wechat_identity_json"] = json.dumps(result.pop("wechat_identity"), ensure_ascii=False)
    return result


class SourceRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        now = utc_now()
        source_id = data.get("source_id") or new_source_id()
        values = {
            "source_id": source_id,
            "source_type": data["source_type"],
            "display_name": data["display_name"],
            "status": data.get("status") or "paused",
            "category": data.get("category") or "未分类",
            "tags": data.get("tags") or [],
            "rating": int(data.get("rating", 50)),
            "notes": data.get("notes"),
            "adapter_id": data.get("adapter_id"),
            "route_path": data.get("route_path"),
            "feed_url": data.get("feed_url"),
            "original_feed_url": data.get("original_feed_url"),
            "wechat_identity": data.get("wechat_identity") or {},
            "last_checked_at": data.get("last_checked_at"),
            "last_check_status": data.get("last_check_status"),
            "last_check_error": data.get("last_check_error"),
            "created_at": now,
            "updated_at": now,
        }
        db_values = source_to_db(values)
        columns = ", ".join(db_values.keys())
        placeholders = ", ".join("?" for _ in db_values)
        with self.db.connect() as conn:
            conn.execute(f"INSERT INTO sources ({columns}) VALUES ({placeholders})", list(db_values.values()))
        return self.get(source_id) or {}

    def get(self, source_id: str) -> dict[str, Any] | None:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM sources WHERE source_id = ?", (source_id,)).fetchone()
        return source_from_row(row)

    def list(
        self,
        *,
        search: str | None = None,
        source_type: str | None = None,
        category: str | None = None,
        status: str | None = None,
        rating_min: int | None = None,
        rating_max: int | None = None,
        include_disabled: bool = False,
        sort: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int, dict[str, Any]]:
        where = []
        params: list[Any] = []
        if not include_disabled and not status:
            where.append("status != 'disabled'")
        if search:
            like = f"%{search}%"
            where.append("(display_name LIKE ? OR feed_url LIKE ? OR route_path LIKE ? OR tags_json LIKE ?)")
            params.extend([like, like, like, like])
        if source_type:
            where.append("source_type = ?")
            params.append(source_type)
        if category:
            where.append("category = ?")
            params.append(category)
        if status:
            where.append("status = ?")
            params.append(status)
        if rating_min is not None:
            where.append("rating >= ?")
            params.append(rating_min)
        if rating_max is not None:
            where.append("rating <= ?")
            params.append(rating_max)
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        order_sql = {
            "name": "display_name ASC",
            "rating_asc": "rating ASC, category ASC, display_name ASC",
            "updated": "updated_at DESC",
        }.get(sort or "", "rating DESC, category ASC, display_name ASC")
        with self.db.connect() as conn:
            total = int(conn.execute(f"SELECT COUNT(*) AS c FROM sources {where_sql}", params).fetchone()["c"])
            rows = conn.execute(
                f"SELECT * FROM sources {where_sql} ORDER BY {order_sql} LIMIT ? OFFSET ?",
                [*params, limit, offset],
            ).fetchall()
            stats_row = conn.execute(
                """
                SELECT
                  COUNT(*) AS total,
                  SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
                  SUM(CASE WHEN status = 'broken' THEN 1 ELSE 0 END) AS broken,
                  MAX(last_success_at) AS latest_success_at,
                  SUM(last_fetch_new_count) AS recent_new_entries
                FROM sources
                """
            ).fetchone()
        stats = dict(stats_row)
        stats["active"] = stats.get("active") or 0
        stats["broken"] = stats.get("broken") or 0
        stats["recent_new_entries"] = stats.get("recent_new_entries") or 0
        return [source_from_row(row) or {} for row in rows], total, stats

    def update(self, source_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        updates = {key: value for key, value in updates.items() if key not in {"allow_duplicate", "source_id"}}
        if not updates:
            return self.get(source_id)
        updates["updated_at"] = utc_now()
        if updates.get("status") == "disabled" and "disabled_at" not in updates:
            updates["disabled_at"] = utc_now()
        db_updates = source_to_db(updates)
        assignments = ", ".join(f"{key} = ?" for key in db_updates)
        with self.db.connect() as conn:
            conn.execute(f"UPDATE sources SET {assignments} WHERE source_id = ?", [*db_updates.values(), source_id])
        return self.get(source_id)

    def soft_delete(self, source_id: str) -> dict[str, Any] | None:
        return self.update(source_id, {"status": "disabled", "disabled_at": utc_now()})

    def update_check(self, source_id: str, *, ok: bool, error: str | None) -> dict[str, Any] | None:
        return self.update(
            source_id,
            {
                "last_checked_at": utc_now(),
                "last_check_status": "ok" if ok else "failed",
                "last_check_error": error,
            },
        )

    def update_fetch_success(self, source_id: str, *, new_count: int, existing_count: int, scanned_count: int) -> None:
        source = self.get(source_id)
        status = "active" if source and source.get("status") == "broken" else (source or {}).get("status", "active")
        self.update(
            source_id,
            {
                "status": status,
                "last_success_at": utc_now(),
                "consecutive_failures": 0,
                "last_error": None,
                "total_entries_seen": int((source or {}).get("total_entries_seen") or 0) + scanned_count,
                "last_fetch_new_count": new_count,
                "last_fetch_existing_count": existing_count,
                "last_fetch_scanned_count": scanned_count,
            },
        )

    def update_fetch_failure(self, source_id: str, *, error: str, threshold: int) -> None:
        source = self.get(source_id) or {}
        failures = int(source.get("consecutive_failures") or 0) + 1
        status = source.get("status") or "active"
        if status == "active" and failures >= threshold:
            status = "broken"
        self.update(
            source_id,
            {
                "status": status,
                "last_failure_at": utc_now(),
                "consecutive_failures": failures,
                "last_error": error,
            },
        )

    def duplicate_candidates(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        source_type = data.get("source_type")
        where = ["source_type = ?", "status != 'disabled'"]
        params: list[Any] = [source_type]
        if source_type == "rsshub":
            where.extend(["adapter_id = ?", "route_path = ?"])
            params.extend([data.get("adapter_id"), data.get("route_path")])
        elif source_type == "native":
            where.append("feed_url = ?")
            params.append(data.get("feed_url"))
        elif source_type == "wechat":
            ident = data.get("wechat_identity") or {}
            strong = [ident.get("biz"), ident.get("mp_id"), ident.get("fakeid")]
            strong = [value for value in strong if value]
            if strong:
                parts = ["wechat_identity_json LIKE ?" for _ in strong]
                where.append("(" + " OR ".join(parts) + ")")
                params.extend([f"%{value}%" for value in strong])
            else:
                where.append("feed_url = ?")
                params.append(data.get("feed_url") or ident.get("feed_url"))
        else:
            return []
        with self.db.connect() as conn:
            rows = conn.execute(f"SELECT * FROM sources WHERE {' AND '.join(where)}", params).fetchall()
        return [source_from_row(row) or {} for row in rows]


class EntryRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_by_identity(self, source_id: str, identity_key: str) -> dict[str, Any] | None:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM entries WHERE source_id = ? AND identity_key = ?", (source_id, identity_key)
            ).fetchone()
        return row_to_dict(row)

    def upsert_seen(self, data: dict[str, Any]) -> tuple[dict[str, Any], str]:
        now = utc_now()
        existing = self.get_by_identity(data["source_id"], data["identity_key"])
        with self.db.connect() as conn:
            if existing:
                conn.execute(
                    """
                    UPDATE entries
                    SET last_seen_at = ?, seen_count = seen_count + 1, updated_at = ?
                    WHERE entry_id = ?
                    """,
                    (now, now, existing["entry_id"]),
                )
                return self.get_by_identity(data["source_id"], data["identity_key"]) or existing, "existing"
            entry_id = data.get("entry_id") or new_entry_id()
            values = {
                **data,
                "entry_id": entry_id,
                "first_seen_at": now,
                "last_seen_at": now,
                "seen_count": 1,
                "created_at": now,
                "updated_at": now,
            }
            columns = ", ".join(values.keys())
            placeholders = ", ".join("?" for _ in values)
            conn.execute(f"INSERT INTO entries ({columns}) VALUES ({placeholders})", list(values.values()))
        return self.get_by_identity(data["source_id"], data["identity_key"]) or values, "new"

    def recent_for_source(self, source_id: str, limit: int = 20) -> list[dict[str, Any]]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM entries WHERE source_id = ? ORDER BY last_seen_at DESC LIMIT ?",
                (source_id, limit),
            ).fetchall()
        return [row_to_dict(row) or {} for row in rows]


class RunRepository:
    def __init__(self, db: Database):
        self.db = db

    def start_fetch_run(self, source_id: str, include_raw: bool) -> str:
        now = utc_now()
        run_id = new_fetch_run_id()
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO fetch_runs
                  (fetch_run_id, source_id, status, started_at, include_raw, created_at, updated_at)
                VALUES (?, ?, 'running', ?, ?, ?, ?)
                """,
                (run_id, source_id, now, int(include_raw), now, now),
            )
        return run_id

    def finish_fetch_run(self, run_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        updates = {**updates, "finished_at": utc_now(), "updated_at": utc_now()}
        assignments = ", ".join(f"{key} = ?" for key in updates)
        with self.db.connect() as conn:
            conn.execute(f"UPDATE fetch_runs SET {assignments} WHERE fetch_run_id = ?", [*updates.values(), run_id])
            row = conn.execute("SELECT * FROM fetch_runs WHERE fetch_run_id = ?", (run_id,)).fetchone()
        data = row_to_dict(row) or {}
        data["include_raw"] = bool(data.get("include_raw"))
        return data

    def add_run_entry(self, run_id: str, entry_id: str, source_id: str, position: int, seen_status: str, identity_key: str) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO fetch_run_entries
                  (fetch_run_id, entry_id, source_id, position, seen_status, identity_key, seen_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (run_id, entry_id, source_id, position, seen_status, identity_key, utc_now()),
            )

    def recent_for_source(self, source_id: str, limit: int = 10) -> list[dict[str, Any]]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM fetch_runs WHERE source_id = ? ORDER BY started_at DESC LIMIT ?",
                (source_id, limit),
            ).fetchall()
        results = []
        for row in rows:
            data = row_to_dict(row) or {}
            data["include_raw"] = bool(data.get("include_raw"))
            results.append(data)
        return results

    def create_import_run(self, data: dict[str, Any]) -> str:
        now = utc_now()
        run_id = new_import_run_id()
        values = {
            "import_run_id": run_id,
            "import_type": data["import_type"],
            "filename": data.get("filename"),
            "started_at": now,
            "finished_at": now,
            "status": data.get("status", "ok"),
            "created_count": data.get("created_count", 0),
            "updated_count": data.get("updated_count", 0),
            "skipped_count": data.get("skipped_count", 0),
            "duplicate_count": data.get("duplicate_count", 0),
            "failed_count": data.get("failed_count", 0),
            "strategy": data.get("strategy"),
            "error_summary": data.get("error_summary"),
            "created_at": now,
            "updated_at": now,
        }
        columns = ", ".join(values.keys())
        placeholders = ", ".join("?" for _ in values)
        with self.db.connect() as conn:
            conn.execute(f"INSERT INTO import_runs ({columns}) VALUES ({placeholders})", list(values.values()))
        return run_id

    def list_import_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM import_runs ORDER BY started_at DESC LIMIT ?", (limit,)).fetchall()
        return [row_to_dict(row) or {} for row in rows]


class RatingRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_adjustment(self, source_id: str, old_rating: int, delta: int, new_rating: int, reason: str, actor: str) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO rating_adjustments
                  (source_id, old_rating, delta, new_rating, reason, created_at, actor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (source_id, old_rating, delta, new_rating, reason, utc_now(), actor),
            )

