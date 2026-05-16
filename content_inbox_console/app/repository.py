"""Read-only SQL queries for the content_inbox SQLite database.

All methods accept a sqlite3.Connection and return plain dicts/lists.
JSON columns are parsed before returning, with graceful fallback on malformed data.
"""

import json
import logging
import sqlite3
from typing import Any, Optional

logger = logging.getLogger(__name__)


def _safe_json(value: Optional[str], default: Any = None) -> Any:
    if default is None:
        default = {}
    if value is None:
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default


def _safe_json_list(value: Optional[str]) -> list[Any]:
    result = _safe_json(value, [])
    return result if isinstance(result, list) else []


class ConsoleRepository:
    def __init__(self) -> None:
        self._column_cache: dict[str, set[str]] = {}

    def _get_columns(self, conn: sqlite3.Connection, table: str) -> set[str]:
        if table not in self._column_cache:
            rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
            self._column_cache[table] = {r["name"] for r in rows}
        return self._column_cache[table]

    def safe_col(self, row: sqlite3.Row, key: str, default: Any = None) -> Any:
        if key in row.keys():
            return row[key]
        return default

    # ── inbox_items ──────────────────────────────────────────────

    def count_items(self, conn: sqlite3.Connection) -> int:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM inbox_items").fetchone()
        return row["cnt"] if row else 0

    def count_items_last_24h(self, conn: sqlite3.Connection) -> int:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM inbox_items WHERE created_at >= datetime('now', '-1 day')"
        ).fetchone()
        return row["cnt"] if row else 0

    def count_items_last_7d(self, conn: sqlite3.Connection) -> int:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM inbox_items WHERE created_at >= datetime('now', '-7 days')"
        ).fetchone()
        return row["cnt"] if row else 0

    def count_items_by_category(self, conn: sqlite3.Connection) -> list[dict]:
        rows = conn.execute(
            "SELECT source_category, COUNT(*) AS cnt FROM inbox_items "
            "WHERE source_category IS NOT NULL AND source_category != '' "
            "GROUP BY source_category ORDER BY cnt DESC"
        ).fetchall()
        return [{"source_category": r["source_category"], "count": r["cnt"]} for r in rows]

    def list_items(
        self,
        conn: sqlite3.Connection,
        *,
        source_id: Optional[str] = None,
        source_name: Optional[str] = None,
        source_category: Optional[str] = None,
        content_type: Optional[str] = None,
        keyword: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        min_score: Optional[float] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[dict], int]:
        cols = self._get_columns(conn, "inbox_items")

        where: list[str] = []
        params: list[Any] = []

        if source_id:
            where.append("source_id = ?")
            params.append(source_id)
        if source_name:
            where.append("source_name = ?")
            params.append(source_name)
        if source_category:
            where.append("source_category = ?")
            params.append(source_category)
        if content_type:
            where.append("content_type = ?")
            params.append(content_type)
        if keyword:
            where.append("(title LIKE ? OR summary LIKE ? OR url LIKE ?)")
            kw = f"%{keyword}%"
            params.extend([kw, kw, kw])
        if date_from:
            where.append("created_at >= ?")
            params.append(date_from)
        if date_to:
            where.append("created_at <= ?")
            params.append(date_to)

        where_clause = " WHERE " + " AND ".join(where) if where else ""

        count_sql = f"SELECT COUNT(*) AS cnt FROM inbox_items{where_clause}"
        count_row = conn.execute(count_sql, params).fetchone()
        total = count_row["cnt"] if count_row else 0

        select_cols = [
            "item_id", "dedupe_key", "url", "guid", "title",
            "source_name", "source_category", "content_type",
            "published_at", "author", "created_at", "last_seen_at",
            "seen_count", "source_id", "feed_url", "dedupe_version",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM inbox_items{where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?"
        rows = conn.execute(sql, params + [limit, offset]).fetchall()

        items = []
        for r in rows:
            item = dict(r)
            items.append(item)

        if min_score is not None and "screening_json" in cols:
            items = [
                it for it in items
                if _score_meets(it.get("screening_json"), min_score)
            ]

        return items, total

    def get_item(self, conn: sqlite3.Connection, item_id: str) -> Optional[dict]:
        cols = self._get_columns(conn, "inbox_items")
        select_cols = [
            "item_id", "dedupe_key", "url", "guid", "title",
            "source_name", "source_category", "content_type",
            "published_at", "author", "summary", "content_text",
            "screening_json", "clustering_json", "raw_json",
            "created_at", "updated_at", "last_seen_at", "seen_count",
            "source_id", "feed_url", "dedupe_version",
            "latest_raw_json", "latest_seen_summary",
            "embedding_text", "embedding_model",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM inbox_items WHERE item_id = ?"
        row = conn.execute(sql, [item_id]).fetchone()
        if not row:
            return None
        item = dict(row)
        item["screening_json"] = _safe_json(item.get("screening_json"))
        item["clustering_json"] = _safe_json(item.get("clustering_json"))
        return item

    def list_items_by_source(self, conn: sqlite3.Connection, source_id: str, limit: int = 50) -> list[dict]:
        cols = self._get_columns(conn, "inbox_items")
        select_cols = [
            "item_id", "title", "url", "published_at", "created_at",
            "source_name", "content_type",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM inbox_items WHERE source_id = ? ORDER BY created_at DESC LIMIT ?"
        rows = conn.execute(sql, [source_id, limit]).fetchall()
        return [dict(r) for r in rows]

    # ── rss_sources ──────────────────────────────────────────────

    def count_sources(self, conn: sqlite3.Connection) -> int:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM rss_sources WHERE deleted_at IS NULL").fetchone()
        return row["cnt"] if row else 0

    def count_sources_by_status(self, conn: sqlite3.Connection) -> dict[str, int]:
        rows = conn.execute(
            "SELECT status, COUNT(*) AS cnt FROM rss_sources WHERE deleted_at IS NULL GROUP BY status"
        ).fetchall()
        return {r["status"]: r["cnt"] for r in rows}

    def list_sources(
        self,
        conn: sqlite3.Connection,
        *,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        sort_by: str = "source_name",
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[dict], int]:
        cols = self._get_columns(conn, "rss_sources")

        where = ["deleted_at IS NULL"]
        params: list[Any] = []

        if status:
            where.append("status = ?")
            params.append(status)
        if keyword:
            where.append("(source_name LIKE ? OR feed_url LIKE ?)")
            kw = f"%{keyword}%"
            params.extend([kw, kw])

        where_clause = " WHERE " + " AND ".join(where)

        count_row = conn.execute(f"SELECT COUNT(*) AS cnt FROM rss_sources{where_clause}", params).fetchone()
        total = count_row["cnt"] if count_row else 0

        select_cols = [
            "source_id", "source_name", "source_category",
            "feed_url", "normalized_feed_url", "status", "priority",
            "tags_json", "notes", "last_fetch_at", "last_success_at",
            "last_failure_at", "last_error_code", "last_error_message",
            "consecutive_failures", "failure_count", "consecutive_failure_count",
            "last_new_items_count", "last_duplicate_items_count",
            "last_processed_items_count", "last_duration_ms",
            "last_ingest_at", "last_run_id", "created_at", "updated_at",
        ]
        available = [c for c in select_cols if c in cols]

        sort_map = {
            "source_name": "source_name ASC",
            "last_fetch_at": "COALESCE(last_fetch_at, '') DESC",
            "failure_count": "COALESCE(failure_count, 0) DESC",
        }
        order = sort_map.get(sort_by, "source_name ASC")

        sql = f"SELECT {', '.join(available)} FROM rss_sources{where_clause} ORDER BY {order} LIMIT ? OFFSET ?"
        rows = conn.execute(sql, params + [limit, offset]).fetchall()

        sources = []
        for r in rows:
            src = dict(r)
            src["tags_json"] = _safe_json_list(src.get("tags_json"))
            sources.append(src)
        return sources, total

    def get_source(self, conn: sqlite3.Connection, source_id: str) -> Optional[dict]:
        cols = self._get_columns(conn, "rss_sources")
        select_cols = [
            "source_id", "source_name", "source_category",
            "feed_url", "normalized_feed_url", "status", "priority",
            "tags_json", "notes", "config_json",
            "last_fetch_at", "last_success_at", "last_failure_at",
            "last_error_code", "last_error_message",
            "consecutive_failures", "failure_count", "consecutive_failure_count",
            "last_new_items_count", "last_duplicate_items_count",
            "last_processed_items_count", "last_duration_ms",
            "last_ingest_at", "last_run_id", "last_error_retryable",
            "last_feed_items_seen", "last_incremental_decision", "last_anchor_found",
            "remote_feed_url", "local_feed_url",
            "created_at", "updated_at",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM rss_sources WHERE source_id = ?"
        row = conn.execute(sql, [source_id]).fetchone()
        if not row:
            return None
        src = dict(row)
        src["tags_json"] = _safe_json_list(src.get("tags_json"))
        src["config_json"] = _safe_json(src.get("config_json"))
        return src

    # ── rss_ingest_runs ──────────────────────────────────────────

    def count_runs(self, conn: sqlite3.Connection) -> int:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM rss_ingest_runs").fetchone()
        return row["cnt"] if row else 0

    def get_last_run(self, conn: sqlite3.Connection) -> Optional[dict]:
        cols = self._get_columns(conn, "rss_ingest_runs")
        select_cols = [
            "run_id", "trigger_type", "source_mode", "status",
            "started_at", "finished_at", "duration_ms",
            "selected_source_count", "success_source_count",
            "failure_source_count", "new_items_count",
            "duplicate_items_count", "processed_items_count",
            "failed_items_count", "error_code", "error_message",
            "created_at",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM rss_ingest_runs ORDER BY started_at DESC LIMIT 1"
        row = conn.execute(sql).fetchone()
        return dict(row) if row else None

    def list_runs(
        self, conn: sqlite3.Connection, *, limit: int = 30, offset: int = 0,
    ) -> tuple[list[dict], int]:
        cols = self._get_columns(conn, "rss_ingest_runs")
        select_cols = [
            "run_id", "trigger_type", "source_mode", "status",
            "started_at", "finished_at", "duration_ms",
            "selected_source_count", "success_source_count",
            "failure_source_count", "new_items_count",
            "duplicate_items_count", "processed_items_count",
            "failed_items_count", "error_message", "created_at",
        ]
        available = [c for c in select_cols if c in cols]

        total = self.count_runs(conn)
        sql = f"SELECT {', '.join(available)} FROM rss_ingest_runs ORDER BY started_at DESC LIMIT ? OFFSET ?"
        rows = conn.execute(sql, [limit, offset]).fetchall()
        return [dict(r) for r in rows], total

    def get_run(self, conn: sqlite3.Connection, run_id: str) -> Optional[dict]:
        cols = self._get_columns(conn, "rss_ingest_runs")
        select_cols = [
            "run_id", "trigger_type", "source_mode", "status",
            "started_at", "finished_at", "duration_ms",
            "selected_source_count", "success_source_count",
            "failure_source_count", "new_items_count",
            "duplicate_items_count", "processed_items_count",
            "failed_items_count", "created_by", "request_json",
            "summary_json", "error_code", "error_message",
            "created_at", "updated_at",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM rss_ingest_runs WHERE run_id = ?"
        row = conn.execute(sql, [run_id]).fetchone()
        if not row:
            return None
        run = dict(row)
        run["request_json"] = _safe_json(run.get("request_json"))
        run["summary_json"] = _safe_json(run.get("summary_json"))
        return run

    def get_run_sources(self, conn: sqlite3.Connection, run_id: str) -> list[dict]:
        cols = self._get_columns(conn, "rss_ingest_run_sources")
        select_cols = [
            "id", "run_id", "source_id", "feed_url", "source_name",
            "source_category", "status", "started_at", "finished_at",
            "duration_ms", "error_code", "error_message", "retryable",
            "fetched_entries_count", "processed_entries_count",
            "new_items_count", "duplicate_items_count", "failed_items_count",
            "incremental_mode", "incremental_decision", "anchor_found",
            "anchor_index", "warnings_json",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM rss_ingest_run_sources WHERE run_id = ? ORDER BY source_name"
        rows = conn.execute(sql, [run_id]).fetchall()
        results = []
        for r in rows:
            rs = dict(r)
            rs["warnings_json"] = _safe_json_list(rs.get("warnings_json"))
            results.append(rs)
        return results

    # ── event_clusters ───────────────────────────────────────────

    def count_clusters(self, conn: sqlite3.Connection) -> int:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM event_clusters").fetchone()
        return row["cnt"] if row else 0

    def list_clusters(
        self, conn: sqlite3.Connection, *, limit: int = 30, offset: int = 0,
    ) -> tuple[list[dict], int]:
        cols = self._get_columns(conn, "event_clusters")
        select_cols = [
            "cluster_pk", "cluster_id", "cluster_title", "cluster_summary",
            "entities_json", "representative_item_id", "first_seen_at",
            "last_seen_at", "item_count", "status", "embedding_model",
            "created_at",
        ]
        available = [c for c in select_cols if c in cols]
        total = self.count_clusters(conn)
        sql = f"SELECT {', '.join(available)} FROM event_clusters ORDER BY last_seen_at DESC LIMIT ? OFFSET ?"
        rows = conn.execute(sql, [limit, offset]).fetchall()
        clusters = []
        for r in rows:
            c = dict(r)
            c["entities_json"] = _safe_json_list(c.get("entities_json"))
            clusters.append(c)
        return clusters, total

    def get_cluster(self, conn: sqlite3.Connection, cluster_id: str) -> Optional[dict]:
        cols = self._get_columns(conn, "event_clusters")
        select_cols = [
            "cluster_pk", "cluster_id", "cluster_title", "cluster_summary",
            "entities_json", "representative_item_id", "first_seen_at",
            "last_seen_at", "item_count", "status", "embedding_model",
            "created_at", "updated_at",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM event_clusters WHERE cluster_id = ?"
        row = conn.execute(sql, [cluster_id]).fetchone()
        if not row:
            return None
        c = dict(row)
        c["entities_json"] = _safe_json_list(c.get("entities_json"))
        return c

    def get_cluster_items(self, conn: sqlite3.Connection, cluster_id: str, limit: int = 50) -> list[dict]:
        cols = self._get_columns(conn, "inbox_items")
        select_cols = [
            "item_id", "title", "url", "published_at", "created_at",
            "source_name", "content_type",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"""
            SELECT {', '.join(available)} FROM inbox_items
            WHERE item_id IN (
                SELECT representative_item_id FROM event_clusters WHERE cluster_id = ?
                UNION
                SELECT item_id FROM inbox_items WHERE item_id != (
                    SELECT COALESCE(representative_item_id, '') FROM event_clusters WHERE cluster_id = ?
                )
            )
            ORDER BY created_at DESC LIMIT ?
        """
        rows = conn.execute(sql, [cluster_id, cluster_id, limit]).fetchall()
        return [dict(r) for r in rows]

    # ── database health ──────────────────────────────────────────

    def get_db_size(self, conn: sqlite3.Connection) -> int:
        page_count = conn.execute("PRAGMA page_count").fetchone()[0]
        page_size = conn.execute("PRAGMA page_size").fetchone()[0]
        return page_count * page_size

    def get_recent_failed_sources(self, conn: sqlite3.Connection, limit: int = 20) -> list[dict]:
        cols = self._get_columns(conn, "rss_sources")
        select_cols = [
            "source_id", "source_name", "feed_url", "status",
            "last_error_code", "last_error_message", "last_failure_at",
            "failure_count",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"""
            SELECT {', '.join(available)} FROM rss_sources
            WHERE status = 'broken' AND deleted_at IS NULL
            ORDER BY COALESCE(last_failure_at, '') DESC
            LIMIT ?
        """
        rows = conn.execute(sql, [limit]).fetchall()
        return [dict(r) for r in rows]

    def get_recent_items(self, conn: sqlite3.Connection, limit: int = 20) -> list[dict]:
        cols = self._get_columns(conn, "inbox_items")
        select_cols = [
            "item_id", "title", "url", "source_name", "published_at",
            "created_at", "content_type",
        ]
        available = [c for c in select_cols if c in cols]
        sql = f"SELECT {', '.join(available)} FROM inbox_items ORDER BY created_at DESC LIMIT ?"
        rows = conn.execute(sql, [limit]).fetchall()
        return [dict(r) for r in rows]

    def count_observed_sources(self, conn: sqlite3.Connection) -> int:
        from app.repositories.observed_sources import count_observed_sources as _cos
        return _cos(conn)


def _score_meets(screening_raw: Optional[str], min_score: float) -> bool:
    screening = _safe_json(screening_raw, {})
    if not screening:
        return True
    value_score = screening.get("value_score")
    if value_score is not None and isinstance(value_score, (int, float)) and value_score < min_score:
        return False
    return True
