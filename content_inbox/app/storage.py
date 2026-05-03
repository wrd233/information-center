from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.config import settings
from app.models import ClusteringResult, NormalizedContent, ScreeningResult
from app.utils import utc_now


class InboxStore:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.vec_available = False
        self.init_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def load_vec(self, conn: sqlite3.Connection) -> bool:
        try:
            import sqlite_vec

            if not hasattr(conn, "load_extension"):
                return False
            sqlite_vec.load(conn)
            return True
        except Exception:
            return False

    def init_schema(self) -> None:
        with self.connect() as conn:
            self.vec_available = self.load_vec(conn)
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
                    clustering_json TEXT,
                    embedding_text TEXT,
                    embedding_model TEXT,
                    raw_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL,
                    seen_count INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            self.ensure_column(conn, "inbox_items", "clustering_json", "TEXT")
            self.ensure_column(conn, "inbox_items", "embedding_text", "TEXT")
            self.ensure_column(conn, "inbox_items", "embedding_model", "TEXT")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS event_clusters (
                    cluster_pk INTEGER PRIMARY KEY AUTOINCREMENT,
                    cluster_id TEXT NOT NULL UNIQUE,
                    cluster_title TEXT NOT NULL,
                    cluster_summary TEXT NOT NULL,
                    entities_json TEXT NOT NULL,
                    representative_item_id TEXT NOT NULL,
                    first_seen_at TEXT NOT NULL,
                    last_seen_at TEXT NOT NULL,
                    item_count INTEGER NOT NULL DEFAULT 1,
                    status TEXT NOT NULL DEFAULT 'active',
                    cluster_vector_json TEXT,
                    embedding_model TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            if self.vec_available:
                dimensions = int(settings.embedding.get("dimensions", 1536))
                conn.execute(
                    f"""
                    CREATE VIRTUAL TABLE IF NOT EXISTS vec_event_clusters
                    USING vec0(embedding float[{dimensions}] distance_metric=cosine)
                    """
                )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_created_at ON inbox_items(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_source_name ON inbox_items(source_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_content_type ON inbox_items(content_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_clusters_status ON event_clusters(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_clusters_last_seen ON event_clusters(last_seen_at)")

    def ensure_column(
        self, conn: sqlite3.Connection, table_name: str, column_name: str, column_type: str
    ) -> None:
        columns = {
            row["name"]
            for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        if column_name not in columns:
            conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    def archive_stale_clusters(self) -> None:
        days = int(settings.clustering.get("archive_after_days", 7))
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE event_clusters
                SET status = 'archived', updated_at = ?
                WHERE status = 'active' AND last_seen_at < ?
                """,
                (now, cutoff),
            )

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
        clustering: ClusteringResult | None = None,
        raw: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        item_id = f"item_{uuid.uuid4().hex}"
        now = utc_now()
        payload = normalized.model_dump()
        clustering = clustering or ClusteringResult()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO inbox_items (
                    item_id, dedupe_key, url, guid, title, source_name, source_category,
                    content_type, published_at, author, summary, content_text,
                    screening_json, clustering_json, embedding_text, embedding_model,
                    raw_json, created_at, updated_at, last_seen_at, seen_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
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
                    json.dumps(clustering.model_dump(), ensure_ascii=False),
                    clustering.embedding_text,
                    clustering.embedding_model,
                    json.dumps(raw or {}, ensure_ascii=False),
                    now,
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        return row_to_item(row)

    def update_item_clustering(self, item_id: str, clustering: ClusteringResult) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE inbox_items
                SET clustering_json = ?, embedding_text = ?, embedding_model = ?, updated_at = ?
                WHERE item_id = ?
                """,
                (
                    json.dumps(clustering.model_dump(), ensure_ascii=False),
                    clustering.embedding_text,
                    clustering.embedding_model,
                    now,
                    item_id,
                ),
            )
            row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        return row_to_item(row)

    def create_cluster(
        self,
        title: str,
        summary: str,
        entities: list[str],
        representative_item_id: str,
        vector: list[float],
        embedding_model: str,
    ) -> dict[str, Any]:
        cluster_id = f"cluster_{uuid.uuid4().hex}"
        now = utc_now()
        with self.connect() as conn:
            if self.vec_available:
                self.load_vec(conn)
            conn.execute(
                """
                INSERT INTO event_clusters (
                    cluster_id, cluster_title, cluster_summary, entities_json,
                    representative_item_id, first_seen_at, last_seen_at, item_count,
                    status, cluster_vector_json, embedding_model, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'active', ?, ?, ?, ?)
                """,
                (
                    cluster_id,
                    title,
                    summary,
                    json.dumps(sorted(set(entities)), ensure_ascii=False),
                    representative_item_id,
                    now,
                    now,
                    json.dumps(vector),
                    embedding_model,
                    now,
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM event_clusters WHERE cluster_id = ?", (cluster_id,)
            ).fetchone()
            self.upsert_cluster_vector(conn, row["cluster_pk"], vector)
        return row_to_cluster(row)

    def update_cluster(
        self,
        cluster_id: str,
        entities: list[str],
        cluster_summary: str | None = None,
        vector: list[float] | None = None,
        embedding_model: str | None = None,
    ) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as conn:
            if self.vec_available:
                self.load_vec(conn)
            row = conn.execute(
                "SELECT * FROM event_clusters WHERE cluster_id = ?", (cluster_id,)
            ).fetchone()
            if not row:
                raise ValueError(f"cluster not found: {cluster_id}")
            merged_entities = sorted(set(json.loads(row["entities_json"]) + entities))
            conn.execute(
                """
                UPDATE event_clusters
                SET entities_json = ?, cluster_summary = ?, last_seen_at = ?,
                    item_count = item_count + 1, cluster_vector_json = COALESCE(?, cluster_vector_json),
                    embedding_model = COALESCE(?, embedding_model), updated_at = ?
                WHERE cluster_id = ?
                """,
                (
                    json.dumps(merged_entities, ensure_ascii=False),
                    cluster_summary or row["cluster_summary"],
                    now,
                    json.dumps(vector) if vector else None,
                    embedding_model,
                    now,
                    cluster_id,
                ),
            )
            updated = conn.execute(
                "SELECT * FROM event_clusters WHERE cluster_id = ?", (cluster_id,)
            ).fetchone()
            if vector:
                self.upsert_cluster_vector(conn, updated["cluster_pk"], vector)
        return row_to_cluster(updated)

    def upsert_cluster_vector(
        self, conn: sqlite3.Connection, cluster_pk: int, vector: list[float]
    ) -> None:
        if not self.vec_available:
            return
        import sqlite_vec

        if not self.load_vec(conn):
            raise RuntimeError("sqlite-vec extension failed to load")
        conn.execute("DELETE FROM vec_event_clusters WHERE rowid = ?", (cluster_pk,))
        conn.execute(
            "INSERT INTO vec_event_clusters(rowid, embedding) VALUES (?, ?)",
            (cluster_pk, sqlite_vec.serialize_float32(vector)),
        )

    def search_active_clusters(self, vector: list[float], top_k: int) -> list[dict[str, Any]]:
        if not self.vec_available:
            raise RuntimeError("sqlite-vec is not available")
        import sqlite_vec

        with self.connect() as conn:
            if not self.load_vec(conn):
                raise RuntimeError("sqlite-vec extension failed to load")
            rows = conn.execute(
                """
                SELECT c.*, v.distance
                FROM vec_event_clusters v
                JOIN event_clusters c ON c.cluster_pk = v.rowid
                WHERE v.embedding MATCH ? AND k = ? AND c.status = 'active'
                ORDER BY v.distance
                """,
                (sqlite_vec.serialize_float32(vector), top_k),
            ).fetchall()
        results = []
        for row in rows:
            cluster = row_to_cluster(row)
            cluster["distance"] = float(row["distance"])
            cluster["similarity"] = max(0.0, min(1.0, 1.0 - float(row["distance"])))
            results.append(cluster)
        return results

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
        return filter_items(items, filters), int(total)


def row_to_item(row: sqlite3.Row) -> dict[str, Any]:
    screening = json.loads(row["screening_json"])
    clustering = json.loads(row["clustering_json"]) if row["clustering_json"] else {}
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
        "clustering": clustering,
        "embedding_text": row["embedding_text"],
        "embedding_model": row["embedding_model"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "last_seen_at": row["last_seen_at"],
        "seen_count": row["seen_count"],
    }


def row_to_cluster(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "cluster_pk": row["cluster_pk"],
        "cluster_id": row["cluster_id"],
        "cluster_title": row["cluster_title"],
        "cluster_summary": row["cluster_summary"],
        "entities": json.loads(row["entities_json"]),
        "representative_item_id": row["representative_item_id"],
        "first_seen_at": row["first_seen_at"],
        "last_seen_at": row["last_seen_at"],
        "item_count": row["item_count"],
        "status": row["status"],
        "cluster_vector": json.loads(row["cluster_vector_json"] or "[]"),
        "embedding_model": row["embedding_model"],
    }


def filter_items(items: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    actions = set(filters.get("suggested_action") or [])
    notification_decisions = set(filters.get("notification_decision") or [])
    priorities = set(filters.get("priority") or [])
    for item in items:
        screening = item["screening"]
        clustering = item["clustering"]
        need_matches = screening.get("need_matches") or []
        topic_matches = screening.get("topic_matches") or []
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
        if filters.get("cluster_id") and clustering.get("cluster_id") != filters["cluster_id"]:
            continue
        if filters.get("cluster_relation") and clustering.get("cluster_relation") != filters["cluster_relation"]:
            continue
        if notification_decisions and clustering.get("notification_decision") not in notification_decisions:
            continue
        if filters.get("min_similarity") is not None:
            similarity = clustering.get("max_similarity")
            if similarity is None or similarity < filters["min_similarity"]:
                continue
        if filters.get("only_new_events") and clustering.get("cluster_relation") != "new_event":
            continue
        if filters.get("only_incremental") and clustering.get("cluster_relation") != "incremental_update":
            continue
        if (
            not filters.get("include_silent")
            and clustering.get("notification_decision") == "silent"
        ):
            continue
        if filters.get("needs_more_context") is not None and screening.get("needs_more_context") != filters.get("needs_more_context"):
            continue
        if filters.get("need_id"):
            filtered_need_matches = [
                match
                for match in need_matches
                if match.get("need_id") == filters["need_id"]
            ]
            if not filtered_need_matches:
                continue
            if filters.get("min_need_score") is not None and not any(
                int(match.get("score", 0)) >= filters["min_need_score"] for match in filtered_need_matches
            ):
                continue
            if priorities and not any(match.get("priority") in priorities for match in filtered_need_matches):
                continue
            if not filters.get("include_maybe") and not any(
                match.get("decision") == "include" for match in filtered_need_matches
            ):
                continue
        elif filters.get("min_need_score") is not None:
            if not any(int(match.get("score", 0)) >= filters["min_need_score"] for match in need_matches):
                continue
        elif priorities:
            if not any(match.get("priority") in priorities for match in need_matches):
                continue
        if filters.get("topic_id"):
            filtered_topic_matches = [
                match
                for match in topic_matches
                if match.get("topic_id") == filters["topic_id"]
            ]
            if not filtered_topic_matches:
                continue
        result.append(item)

    if filters.get("need_id"):
        need_id = filters["need_id"]
        result.sort(
            key=lambda item: need_sort_key(
                next(
                    (
                        match
                        for match in (item["screening"].get("need_matches") or [])
                        if match.get("need_id") == need_id
                    ),
                    {},
                )
            )
        )
    elif filters.get("topic_id"):
        topic_id = filters["topic_id"]
        result.sort(
            key=lambda item: topic_sort_key(
                next(
                    (
                        match
                        for match in (item["screening"].get("topic_matches") or [])
                        if match.get("topic_id") == topic_id
                    ),
                    {},
                )
            )
        )

    return [public_item(item) for item in result]


def need_sort_key(match: dict[str, Any]) -> tuple[int, int, str]:
    return (
        -int(match.get("score", 0) or 0),
        priority_rank(match.get("priority")),
        str(match.get("need_id", "")),
    )


def topic_sort_key(match: dict[str, Any]) -> tuple[int, str, str]:
    return (
        -int(match.get("score", 0) or 0),
        str(match.get("update_type", "")),
        str(match.get("topic_id", "")),
    )


def priority_rank(priority: Any) -> int:
    value = str(priority or "").upper()
    mapping = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    return mapping.get(value, 9)


def public_item(item: dict[str, Any]) -> dict[str, Any]:
    clustering = item["clustering"] or {}
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
        "screening": public_screening(item["screening"]),
        "clustering": clustering,
        "notification_decision": clustering.get("notification_decision"),
        "cluster_relation": clustering.get("cluster_relation"),
        "incremental_summary": clustering.get("incremental_summary", ""),
        "created_at": item["created_at"],
        "last_seen_at": item["last_seen_at"],
        "seen_count": item["seen_count"],
    }


def public_screening(screening: dict[str, Any]) -> dict[str, Any]:
    public = dict(screening)
    public.pop("raw_model_response", None)
    return public
