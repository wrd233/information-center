from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.config import settings
from app.models import ClusteringResult, NormalizedContent, ScreeningResult
from app.utils import normalize_url, stable_hash, utc_now


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
            self.ensure_column(conn, "inbox_items", "source_id", "TEXT")
            self.ensure_column(conn, "inbox_items", "feed_url", "TEXT")
            self.ensure_column(conn, "inbox_items", "dedupe_version", "INTEGER DEFAULT 1")
            self.ensure_column(conn, "inbox_items", "latest_raw_json", "TEXT")
            self.ensure_column(conn, "inbox_items", "latest_seen_summary", "TEXT")
            self.ensure_column(conn, "inbox_items", "semantic_status", "TEXT DEFAULT 'pending'")
            self.ensure_column(conn, "inbox_items", "primary_cluster_id", "TEXT")
            self.ensure_column(conn, "inbox_items", "semantic_error", "TEXT")
            self.ensure_column(conn, "inbox_items", "semantic_attempts", "INTEGER NOT NULL DEFAULT 0")
            self.ensure_column(conn, "inbox_items", "last_semantic_at", "TEXT")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rss_sources (
                    source_id TEXT PRIMARY KEY,
                    source_name TEXT NOT NULL,
                    source_category TEXT,
                    feed_url TEXT NOT NULL,
                    normalized_feed_url TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    priority INTEGER NOT NULL DEFAULT 3,
                    tags_json TEXT NOT NULL DEFAULT '[]',
                    notes TEXT,
                    config_json TEXT NOT NULL DEFAULT '{}',
                    last_fetch_at TEXT,
                    last_success_at TEXT,
                    last_failure_at TEXT,
                    last_error_code TEXT,
                    last_error_message TEXT,
                    consecutive_failures INTEGER NOT NULL DEFAULT 0,
                    last_run_id TEXT,
                    last_new_items INTEGER NOT NULL DEFAULT 0,
                    last_duplicate_items INTEGER NOT NULL DEFAULT 0,
                    last_processed_items INTEGER NOT NULL DEFAULT 0,
                    last_feed_items_seen INTEGER NOT NULL DEFAULT 0,
                    last_incremental_decision TEXT,
                    last_anchor_found INTEGER,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(normalized_feed_url)
                )
                """
            )
            self.ensure_column(conn, "rss_sources", "local_feed_url", "TEXT")
            self.ensure_column(conn, "rss_sources", "remote_feed_url", "TEXT")
            self.ensure_column(conn, "rss_sources", "deleted_at", "TEXT")
            self.ensure_column(conn, "rss_sources", "last_ingest_at", "TEXT")
            self.ensure_column(conn, "rss_sources", "last_error_retryable", "INTEGER")
            self.ensure_column(conn, "rss_sources", "failure_count", "INTEGER NOT NULL DEFAULT 0")
            self.ensure_column(conn, "rss_sources", "consecutive_failure_count", "INTEGER NOT NULL DEFAULT 0")
            self.ensure_column(conn, "rss_sources", "last_new_items_count", "INTEGER NOT NULL DEFAULT 0")
            self.ensure_column(conn, "rss_sources", "last_duplicate_items_count", "INTEGER NOT NULL DEFAULT 0")
            self.ensure_column(conn, "rss_sources", "last_processed_items_count", "INTEGER NOT NULL DEFAULT 0")
            self.ensure_column(conn, "rss_sources", "last_duration_ms", "INTEGER")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rss_ingest_runs (
                    run_id TEXT PRIMARY KEY,
                    trigger_type TEXT NOT NULL,
                    source_mode TEXT,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    duration_ms INTEGER,
                    selected_source_count INTEGER DEFAULT 0,
                    success_source_count INTEGER DEFAULT 0,
                    failure_source_count INTEGER DEFAULT 0,
                    new_items_count INTEGER DEFAULT 0,
                    duplicate_items_count INTEGER DEFAULT 0,
                    processed_items_count INTEGER DEFAULT 0,
                    failed_items_count INTEGER DEFAULT 0,
                    created_by TEXT,
                    request_json TEXT,
                    summary_json TEXT,
                    error_code TEXT,
                    error_message TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rss_ingest_run_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    source_id TEXT,
                    feed_url TEXT,
                    source_name TEXT,
                    source_category TEXT,
                    status TEXT NOT NULL,
                    started_at TEXT,
                    finished_at TEXT,
                    duration_ms INTEGER,
                    error_code TEXT,
                    error_message TEXT,
                    retryable INTEGER,
                    fetched_entries_count INTEGER DEFAULT 0,
                    processed_entries_count INTEGER DEFAULT 0,
                    new_items_count INTEGER DEFAULT 0,
                    duplicate_items_count INTEGER DEFAULT 0,
                    failed_items_count INTEGER DEFAULT 0,
                    incremental_mode TEXT,
                    incremental_decision TEXT,
                    anchor_found INTEGER,
                    anchor_index INTEGER,
                    warnings_json TEXT,
                    result_json TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
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
            self.ensure_column(conn, "event_clusters", "last_major_update_at", "TEXT")
            self.ensure_column(conn, "event_clusters", "source_material_item_id", "TEXT")
            self.ensure_column(conn, "event_clusters", "cluster_card_id", "INTEGER")
            self.ensure_column(conn, "event_clusters", "created_by", "TEXT DEFAULT 'legacy'")
            self.ensure_column(conn, "event_clusters", "confidence", "REAL NOT NULL DEFAULT 0.0")
            self.ensure_column(conn, "event_clusters", "merged_into_cluster_id", "TEXT")
            self.init_semantic_schema(conn)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_created_at ON inbox_items(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_source_name ON inbox_items(source_name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_content_type ON inbox_items(content_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_source_id ON inbox_items(source_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_published_at ON inbox_items(published_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_semantic_status ON inbox_items(semantic_status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_inbox_primary_cluster_id ON inbox_items(primary_cluster_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rss_sources_status ON rss_sources(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rss_runs_started_at ON rss_ingest_runs(started_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_rss_run_sources_run_id ON rss_ingest_run_sources(run_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_clusters_status ON event_clusters(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_clusters_last_seen ON event_clusters(last_seen_at)")

    def init_semantic_schema(self, conn: sqlite3.Connection) -> None:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS item_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                card_version INTEGER NOT NULL DEFAULT 1,
                schema_version TEXT NOT NULL,
                prompt_version TEXT,
                model TEXT,
                input_fingerprint TEXT NOT NULL,
                canonical_title TEXT NOT NULL,
                language TEXT NOT NULL DEFAULT 'unknown',
                short_summary TEXT NOT NULL,
                embedding_text TEXT NOT NULL,
                entities_json TEXT NOT NULL DEFAULT '[]',
                event_hint TEXT,
                content_role TEXT NOT NULL DEFAULT 'unknown',
                confidence REAL NOT NULL DEFAULT 0.0,
                warnings_json TEXT NOT NULL DEFAULT '[]',
                key_facts_json TEXT NOT NULL DEFAULT '[]',
                key_opinions_json TEXT NOT NULL DEFAULT '[]',
                cited_sources_json TEXT NOT NULL DEFAULT '[]',
                source_material_candidates_json TEXT NOT NULL DEFAULT '[]',
                quality_hints_json TEXT NOT NULL DEFAULT '{}',
                llm_call_id INTEGER,
                is_current INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_item_cards_current
            ON item_cards(item_id, is_current)
            WHERE is_current = 1
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS item_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_a_id TEXT NOT NULL,
                item_b_id TEXT NOT NULL,
                primary_relation TEXT NOT NULL,
                secondary_roles_json TEXT NOT NULL DEFAULT '[]',
                confidence REAL NOT NULL DEFAULT 0.0,
                should_fold INTEGER NOT NULL DEFAULT 0,
                canonical_item_id TEXT,
                new_information_json TEXT NOT NULL DEFAULT '[]',
                reason TEXT NOT NULL DEFAULT '',
                evidence_json TEXT NOT NULL DEFAULT '[]',
                decision_source TEXT NOT NULL,
                llm_call_id INTEGER,
                schema_version TEXT NOT NULL,
                prompt_version TEXT,
                model TEXT,
                input_fingerprint TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(item_a_id, item_b_id, primary_relation, input_fingerprint)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cluster_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cluster_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                primary_relation TEXT NOT NULL,
                secondary_roles_json TEXT NOT NULL DEFAULT '[]',
                same_event INTEGER NOT NULL DEFAULT 0,
                same_topic INTEGER NOT NULL DEFAULT 0,
                follow_up_event INTEGER NOT NULL DEFAULT 0,
                confidence REAL NOT NULL DEFAULT 0.0,
                incremental_value INTEGER NOT NULL DEFAULT 0,
                report_value INTEGER NOT NULL DEFAULT 0,
                should_update_cluster_card INTEGER NOT NULL DEFAULT 0,
                should_notify INTEGER NOT NULL DEFAULT 0,
                new_facts_json TEXT NOT NULL DEFAULT '[]',
                new_angles_json TEXT NOT NULL DEFAULT '[]',
                reason TEXT NOT NULL DEFAULT '',
                evidence_json TEXT NOT NULL DEFAULT '[]',
                decision_source TEXT NOT NULL,
                llm_call_id INTEGER,
                schema_version TEXT NOT NULL,
                prompt_version TEXT,
                model TEXT,
                input_fingerprint TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(cluster_id, item_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cluster_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cluster_id TEXT NOT NULL,
                card_version INTEGER NOT NULL DEFAULT 1,
                schema_version TEXT NOT NULL,
                prompt_version TEXT,
                model TEXT,
                input_fingerprint TEXT NOT NULL,
                cluster_title TEXT NOT NULL,
                event_type TEXT,
                main_entities_json TEXT NOT NULL DEFAULT '[]',
                core_facts_json TEXT NOT NULL DEFAULT '[]',
                known_angles_json TEXT NOT NULL DEFAULT '[]',
                representative_items_json TEXT NOT NULL DEFAULT '[]',
                source_items_json TEXT NOT NULL DEFAULT '[]',
                open_questions_json TEXT NOT NULL DEFAULT '[]',
                first_seen_at TEXT,
                last_major_update_at TEXT,
                confidence REAL NOT NULL DEFAULT 0.0,
                llm_call_id INTEGER,
                is_current INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_cluster_cards_current
            ON cluster_cards(cluster_id, is_current)
            WHERE is_current = 1
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cluster_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_cluster_id TEXT NOT NULL,
                to_cluster_id TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                confidence REAL NOT NULL DEFAULT 0.0,
                reason TEXT NOT NULL DEFAULT '',
                decision_source TEXT NOT NULL DEFAULT 'rule',
                llm_call_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(from_cluster_id, to_cluster_id, relation_type)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS source_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                cluster_id TEXT,
                originality_delta INTEGER NOT NULL DEFAULT 0,
                duplicate_signal INTEGER NOT NULL DEFAULT 0,
                near_duplicate_signal INTEGER NOT NULL DEFAULT 0,
                new_event_signal INTEGER NOT NULL DEFAULT 0,
                incremental_value INTEGER NOT NULL DEFAULT 0,
                report_value INTEGER NOT NULL DEFAULT 0,
                source_role TEXT NOT NULL DEFAULT 'unknown',
                llm_call_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(source_id, item_id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS source_profiles (
                source_id TEXT PRIMARY KEY,
                total_items INTEGER NOT NULL DEFAULT 0,
                llm_processed_items INTEGER NOT NULL DEFAULT 0,
                duplicate_rate REAL NOT NULL DEFAULT 0.0,
                near_duplicate_rate REAL NOT NULL DEFAULT 0.0,
                new_event_rate REAL NOT NULL DEFAULT 0.0,
                incremental_value_avg REAL NOT NULL DEFAULT 0.0,
                report_value_avg REAL NOT NULL DEFAULT 0.0,
                source_item_rate REAL NOT NULL DEFAULT 0.0,
                representative_item_rate REAL NOT NULL DEFAULT 0.0,
                llm_total_tokens INTEGER NOT NULL DEFAULT 0,
                llm_high_value_outputs INTEGER NOT NULL DEFAULT 0,
                llm_yield_score REAL NOT NULL DEFAULT 0.0,
                llm_priority TEXT NOT NULL DEFAULT 'new_source_under_evaluation',
                priority_suggestion TEXT,
                review_status TEXT NOT NULL DEFAULT 'none',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_call_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_type TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_version TEXT,
                schema_version TEXT,
                input_fingerprint TEXT NOT NULL,
                latency_ms INTEGER,
                status TEXT NOT NULL,
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                total_tokens INTEGER,
                cache_hit_tokens INTEGER,
                cache_miss_tokens INTEGER,
                request_json TEXT,
                raw_output TEXT,
                parsed_output_json TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_type TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                suggestion_json TEXT NOT NULL DEFAULT '{}',
                reason TEXT NOT NULL DEFAULT '',
                llm_call_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                reviewed_at TEXT,
                reviewer TEXT,
                review_note TEXT
            )
            """
        )
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_item_cards_item ON item_cards(item_id)",
            "CREATE INDEX IF NOT EXISTS idx_item_cards_fingerprint ON item_cards(input_fingerprint)",
            "CREATE INDEX IF NOT EXISTS idx_item_relations_item_a ON item_relations(item_a_id)",
            "CREATE INDEX IF NOT EXISTS idx_item_relations_item_b ON item_relations(item_b_id)",
            "CREATE INDEX IF NOT EXISTS idx_item_relations_primary ON item_relations(primary_relation)",
            "CREATE INDEX IF NOT EXISTS idx_cluster_items_cluster ON cluster_items(cluster_id)",
            "CREATE INDEX IF NOT EXISTS idx_cluster_items_item ON cluster_items(item_id)",
            "CREATE INDEX IF NOT EXISTS idx_cluster_items_primary ON cluster_items(primary_relation)",
            "CREATE INDEX IF NOT EXISTS idx_cluster_cards_cluster ON cluster_cards(cluster_id)",
            "CREATE INDEX IF NOT EXISTS idx_cluster_relations_from ON cluster_relations(from_cluster_id)",
            "CREATE INDEX IF NOT EXISTS idx_cluster_relations_to ON cluster_relations(to_cluster_id)",
            "CREATE INDEX IF NOT EXISTS idx_source_signals_source ON source_signals(source_id)",
            "CREATE INDEX IF NOT EXISTS idx_source_profiles_priority ON source_profiles(llm_priority)",
            "CREATE INDEX IF NOT EXISTS idx_llm_call_logs_task ON llm_call_logs(task_type)",
            "CREATE INDEX IF NOT EXISTS idx_llm_call_logs_status ON llm_call_logs(status)",
            "CREATE INDEX IF NOT EXISTS idx_llm_call_logs_fingerprint ON llm_call_logs(input_fingerprint)",
            "CREATE INDEX IF NOT EXISTS idx_review_queue_status ON review_queue(status)",
            "CREATE INDEX IF NOT EXISTS idx_review_queue_target ON review_queue(target_type, target_id)",
        ]
        for sql in indexes:
            conn.execute(sql)

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

    def has_source_history(
        self,
        source_name: str,
        source_category: str | None,
        *,
        source_id: str | None = None,
        feed_url: str | None = None,
    ) -> bool:
        """Check whether any items from this source exist in the database.

        Source identity is determined by source_name + source_category.
        Limitation: feed_url is not stored as a column (only inside raw_json TEXT),
        so two different feeds sharing the same name+category will be treated
        as the same source. For this feature's purpose (distinguishing new
        sources from old sources), this is acceptable.
        """
        with self.connect() as conn:
            if source_id:
                row = conn.execute(
                    "SELECT 1 FROM inbox_items WHERE source_id = ?", (source_id,)
                ).fetchone()
                if row is not None:
                    return True
            if feed_url:
                normalized_feed_url = normalize_url(feed_url) or feed_url.strip()
                row = conn.execute(
                    "SELECT 1 FROM inbox_items WHERE feed_url = ?",
                    (normalized_feed_url,),
                ).fetchone()
                if row is not None:
                    return True
            if source_category is not None:
                row = conn.execute(
                    "SELECT 1 FROM inbox_items WHERE source_name = ? AND source_category = ?",
                    (source_name, source_category),
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT 1 FROM inbox_items WHERE source_name = ? AND source_category IS NULL",
                    (source_name,),
                ).fetchone()
        return row is not None

    def mark_seen(self, item_id: str) -> dict[str, Any]:
        return self.mark_seen_with_latest(item_id)

    def mark_seen_with_latest(
        self,
        item_id: str,
        *,
        latest_raw: dict[str, Any] | None = None,
        latest_seen_summary: str | None = None,
    ) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE inbox_items
                SET last_seen_at = ?, updated_at = ?, seen_count = seen_count + 1,
                    latest_raw_json = COALESCE(?, latest_raw_json),
                    latest_seen_summary = COALESCE(?, latest_seen_summary)
                WHERE item_id = ?
                """,
                (
                    now,
                    now,
                    json.dumps(latest_raw, ensure_ascii=False) if latest_raw is not None else None,
                    latest_seen_summary,
                    item_id,
                ),
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
                    item_id, dedupe_key, url, guid, source_id, feed_url, title, source_name, source_category,
                    content_type, published_at, author, summary, content_text,
                    screening_json, clustering_json, embedding_text, embedding_model,
                    raw_json, dedupe_version, latest_raw_json, latest_seen_summary,
                    created_at, updated_at, last_seen_at, seen_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """,
                (
                    item_id,
                    dedupe_key,
                    payload.get("url"),
                    payload.get("guid"),
                    payload.get("source_id"),
                    payload.get("feed_url"),
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
                    int(payload.get("dedupe_version") or 1),
                    json.dumps(raw or {}, ensure_ascii=False),
                    payload.get("summary"),
                    now,
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        return row_to_item(row)

    def generate_source_id(self, feed_url: str) -> str:
        normalized = normalize_url(feed_url) or feed_url.strip()
        return re.sub(r"[^A-Za-z0-9]+", "-", normalized.lower()).strip("-")[:64] or "source"

    def generate_source_id_from_parts(
        self,
        source_category: str | None,
        source_name: str | None,
        feed_url: str,
    ) -> str:
        normalized = normalize_url(feed_url) or feed_url.strip()
        base_text = "-".join(part for part in [source_category, source_name] if part)
        ascii_text = unicodedata.normalize("NFKD", base_text).encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^A-Za-z0-9]+", "-", ascii_text.lower()).strip("-")
        if len(slug) < 3:
            parsed_host = re.sub(r"[^A-Za-z0-9]+", "-", normalized.lower()).strip("-")
            slug = parsed_host[:40] or "source"
        candidate = slug[:64]
        suffix = stable_hash("source-id:" + normalized)[:8]
        with self.connect() as conn:
            if not conn.execute(
                "SELECT 1 FROM rss_sources WHERE source_id = ?", (candidate,)
            ).fetchone():
                return candidate
        return f"{candidate[:55]}-{suffix}"

    def create_rss_source(self, payload: dict[str, Any]) -> tuple[dict[str, Any], bool]:
        feed_url = str(payload["feed_url"]).strip()
        normalized_feed_url = normalize_url(feed_url) or feed_url
        source_id = (
            payload.get("source_id")
            or self.generate_source_id_from_parts(
                payload.get("source_category"), payload.get("source_name"), feed_url
            )
        ).strip()
        now = utc_now()
        tags = payload.get("tags") or []
        config = payload.get("config") or {}
        with self.connect() as conn:
            if conn.execute(
                "SELECT 1 FROM rss_sources WHERE source_id = ?", (source_id,)
            ).fetchone():
                raise ValueError("source_id_conflict")
            if conn.execute(
                "SELECT 1 FROM rss_sources WHERE normalized_feed_url = ?",
                (normalized_feed_url,),
            ).fetchone():
                raise ValueError("feed_url_conflict")
            conn.execute(
                """
                INSERT INTO rss_sources (
                    source_id, source_name, source_category, feed_url, normalized_feed_url,
                    status, priority, tags_json, notes, config_json,
                    local_feed_url, remote_feed_url, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_id,
                    payload["source_name"],
                    payload.get("source_category"),
                    feed_url,
                    normalized_feed_url,
                    payload.get("status", "active"),
                    int(payload.get("priority", 0)),
                    json.dumps(tags, ensure_ascii=False),
                    payload.get("notes"),
                    json.dumps(config, ensure_ascii=False),
                    payload.get("local_feed_url"),
                    payload.get("remote_feed_url"),
                    now,
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM rss_sources WHERE source_id = ?", (source_id,)
            ).fetchone()
        return row_to_source(row), True

    def get_rss_source(self, source_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM rss_sources WHERE source_id = ?", (source_id,)
            ).fetchone()
        return row_to_source(row) if row else None

    def list_rss_sources(self, filters: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
        clauses: list[str] = []
        params: list[Any] = []
        if filters.get("status"):
            clauses.append("status = ?")
            params.append(filters["status"])
        if filters.get("category"):
            clauses.append("source_category LIKE ?")
            params.append(f"%{filters['category']}%")
        if filters.get("tag"):
            clauses.append("tags_json LIKE ?")
            params.append(f"%{filters['tag']}%")
        if filters.get("keyword"):
            clauses.append("(source_id LIKE ? OR source_name LIKE ? OR feed_url LIKE ? OR notes LIKE ?)")
            keyword = f"%{filters['keyword']}%"
            params.extend([keyword, keyword, keyword, keyword])
        if filters.get("priority_min") is not None:
            clauses.append("priority >= ?")
            params.append(int(filters["priority_min"]))
        if filters.get("priority_max") is not None:
            clauses.append("priority <= ?")
            params.append(int(filters["priority_max"]))
        if filters.get("has_error") is not None:
            clauses.append("last_error_code IS NOT NULL" if filters["has_error"] else "last_error_code IS NULL")
        if filters.get("retryable") is not None:
            clauses.append("last_error_retryable = ?")
            params.append(1 if filters["retryable"] else 0)
        if filters.get("last_success_before"):
            clauses.append("last_success_at < ?")
            params.append(filters["last_success_before"])
        if filters.get("last_failure_after"):
            clauses.append("last_failure_at > ?")
            params.append(filters["last_failure_after"])
        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        limit = int(filters.get("limit", 100))
        offset = int(filters.get("offset", 0))
        sort = filters.get("sort") or "priority:asc,source_name:asc"
        allowed_sort = {
            "priority": "priority",
            "source_name": "source_name",
            "last_success_at": "last_success_at",
            "last_failure_at": "last_failure_at",
            "updated_at": "updated_at",
            "status": "status",
        }
        order_terms = []
        for raw_part in str(sort).split(","):
            field, _, direction = raw_part.partition(":")
            column = allowed_sort.get(field.strip())
            if column:
                direction_sql = "DESC" if direction.strip().lower() == "desc" else "ASC"
                order_terms.append(f"{column} {direction_sql}")
        order_sql = ", ".join(order_terms) or "priority ASC, source_name ASC"
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT * FROM rss_sources
                {where_sql}
                ORDER BY {order_sql}
                LIMIT ? OFFSET ?
                """,
                (*params, limit, offset),
            ).fetchall()
            stats_row = conn.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
                    SUM(CASE WHEN status = 'paused' THEN 1 ELSE 0 END) AS paused,
                    SUM(CASE WHEN status = 'disabled' THEN 1 ELSE 0 END) AS disabled,
                    SUM(CASE WHEN status = 'broken' THEN 1 ELSE 0 END) AS broken
                FROM rss_sources
                """
            ).fetchone()
        stats = {
            "total": int(stats_row["total"] or 0),
            "active": int(stats_row["active"] or 0),
            "paused": int(stats_row["paused"] or 0),
            "disabled": int(stats_row["disabled"] or 0),
            "broken": int(stats_row["broken"] or 0),
        }
        return [row_to_source(row) for row in rows], stats

    def update_rss_source(self, source_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        current = self.get_rss_source(source_id)
        if current is None:
            return None
        assignments: list[str] = []
        params: list[Any] = []
        field_map = {
            "source_name": "source_name",
            "source_category": "source_category",
            "status": "status",
            "priority": "priority",
            "notes": "notes",
            "local_feed_url": "local_feed_url",
            "remote_feed_url": "remote_feed_url",
        }
        for key, column in field_map.items():
            if key in updates:
                assignments.append(f"{column} = ?")
                params.append(updates[key])
        if "feed_url" in updates:
            feed_url = str(updates["feed_url"]).strip()
            normalized_feed_url = normalize_url(feed_url) or feed_url
            with self.connect() as conn:
                row = conn.execute(
                    """
                    SELECT source_id FROM rss_sources
                    WHERE normalized_feed_url = ? AND source_id != ?
                    """,
                    (normalized_feed_url, source_id),
                ).fetchone()
            if row:
                raise ValueError("feed_url_conflict")
            assignments.extend(["feed_url = ?", "normalized_feed_url = ?"])
            params.extend([feed_url, normalized_feed_url])
        if "tags" in updates:
            assignments.append("tags_json = ?")
            params.append(json.dumps(updates["tags"] or [], ensure_ascii=False))
        if "config" in updates:
            assignments.append("config_json = ?")
            params.append(json.dumps(updates["config"] or {}, ensure_ascii=False))
        if not assignments:
            return current
        assignments.append("updated_at = ?")
        params.append(utc_now())
        params.append(source_id)
        with self.connect() as conn:
            conn.execute(
                f"UPDATE rss_sources SET {', '.join(assignments)} WHERE source_id = ?",
                params,
            )
            row = conn.execute(
                "SELECT * FROM rss_sources WHERE source_id = ?", (source_id,)
            ).fetchone()
        return row_to_source(row)

    def disable_rss_source(self, source_id: str) -> dict[str, Any] | None:
        return self.update_rss_source(source_id, {"status": "disabled"})

    def record_rss_source_success(
        self,
        source_id: str,
        *,
        run_id: str,
        finished_at: str,
        new_items: int,
        duplicate_items: int,
        processed_items: int,
        feed_items_seen: int,
        incremental_decision: str | None,
        anchor_found: bool | None,
        duration_ms: int | None = None,
    ) -> dict[str, Any] | None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE rss_sources
                SET last_fetch_at = ?, last_ingest_at = ?, last_success_at = ?, last_failure_at = NULL,
                    last_error_code = NULL, last_error_message = NULL,
                    last_error_retryable = NULL, consecutive_failures = 0,
                    consecutive_failure_count = 0, last_run_id = ?, last_new_items = ?,
                    last_duplicate_items = ?, last_processed_items = ?,
                    last_new_items_count = ?, last_duplicate_items_count = ?,
                    last_processed_items_count = ?, last_duration_ms = ?,
                    last_feed_items_seen = ?, last_incremental_decision = ?,
                    last_anchor_found = ?, updated_at = ?
                WHERE source_id = ?
                """,
                (
                    finished_at,
                    finished_at,
                    finished_at,
                    run_id,
                    new_items,
                    duplicate_items,
                    processed_items,
                    new_items,
                    duplicate_items,
                    processed_items,
                    duration_ms,
                    feed_items_seen,
                    incremental_decision,
                    None if anchor_found is None else int(anchor_found),
                    finished_at,
                    source_id,
                ),
            )
            row = conn.execute(
                "SELECT * FROM rss_sources WHERE source_id = ?", (source_id,)
            ).fetchone()
        return row_to_source(row) if row else None

    def record_rss_source_failure(
        self,
        source_id: str,
        *,
        run_id: str,
        finished_at: str,
        error_code: str,
        error_message: str,
        retryable: bool = True,
        duration_ms: int | None = None,
        broken_threshold: int = 5,
    ) -> dict[str, Any] | None:
        with self.connect() as conn:
            current = conn.execute(
                "SELECT status, consecutive_failure_count FROM rss_sources WHERE source_id = ?",
                (source_id,),
            ).fetchone()
            new_consecutive = int((current["consecutive_failure_count"] if current else 0) or 0) + 1
            new_status = (
                "broken"
                if current
                and current["status"] == "active"
                and new_consecutive >= broken_threshold
                else (current["status"] if current else "active")
            )
            conn.execute(
                """
                UPDATE rss_sources
                SET last_fetch_at = ?, last_ingest_at = ?, last_failure_at = ?, last_error_code = ?,
                    last_error_message = ?, last_error_retryable = ?,
                    failure_count = failure_count + 1,
                    consecutive_failures = consecutive_failures + 1,
                    consecutive_failure_count = consecutive_failure_count + 1,
                    status = ?, last_run_id = ?, last_duration_ms = ?, updated_at = ?
                WHERE source_id = ?
                """,
                (
                    finished_at,
                    finished_at,
                    finished_at,
                    error_code,
                    error_message,
                    int(retryable),
                    new_status,
                    run_id,
                    duration_ms,
                    finished_at,
                    source_id,
                ),
            )
            row = conn.execute(
                "SELECT * FROM rss_sources WHERE source_id = ?", (source_id,)
            ).fetchone()
        return row_to_source(row) if row else None

    def create_ingest_run(self, run: dict[str, Any]) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO rss_ingest_runs (
                    run_id, trigger_type, source_mode, status, started_at, finished_at,
                    duration_ms, selected_source_count, success_source_count,
                    failure_source_count, new_items_count, duplicate_items_count,
                    processed_items_count, failed_items_count, created_by,
                    request_json, summary_json, error_code, error_message,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run["run_id"],
                    run.get("trigger_type", "api"),
                    run.get("source_mode"),
                    run.get("status", "running"),
                    run["started_at"],
                    run.get("finished_at"),
                    run.get("duration_ms"),
                    int(run.get("selected_source_count", 0)),
                    int(run.get("success_source_count", 0)),
                    int(run.get("failure_source_count", 0)),
                    int(run.get("new_items_count", 0)),
                    int(run.get("duplicate_items_count", 0)),
                    int(run.get("processed_items_count", 0)),
                    int(run.get("failed_items_count", 0)),
                    run.get("created_by"),
                    json.dumps(run.get("request") or {}, ensure_ascii=False),
                    json.dumps(run.get("summary") or {}, ensure_ascii=False),
                    run.get("error_code"),
                    run.get("error_message"),
                    run.get("created_at", now),
                    run.get("updated_at", now),
                ),
            )
            row = conn.execute(
                "SELECT * FROM rss_ingest_runs WHERE run_id = ?", (run["run_id"],)
            ).fetchone()
        return row_to_ingest_run(row)

    def create_ingest_run_source(self, result: dict[str, Any]) -> dict[str, Any]:
        now = utc_now()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO rss_ingest_run_sources (
                    run_id, source_id, feed_url, source_name, source_category, status,
                    started_at, finished_at, duration_ms, error_code, error_message,
                    retryable, fetched_entries_count, processed_entries_count,
                    new_items_count, duplicate_items_count, failed_items_count,
                    incremental_mode, incremental_decision, anchor_found, anchor_index,
                    warnings_json, result_json, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result["run_id"],
                    result.get("source_id"),
                    result.get("feed_url"),
                    result.get("source_name"),
                    result.get("source_category"),
                    result.get("status", "success"),
                    result.get("started_at"),
                    result.get("finished_at"),
                    result.get("duration_ms"),
                    result.get("error_code"),
                    result.get("error_message"),
                    None if result.get("retryable") is None else int(bool(result.get("retryable"))),
                    int(result.get("fetched_entries_count", 0)),
                    int(result.get("processed_entries_count", 0)),
                    int(result.get("new_items_count", 0)),
                    int(result.get("duplicate_items_count", 0)),
                    int(result.get("failed_items_count", 0)),
                    result.get("incremental_mode"),
                    result.get("incremental_decision"),
                    None if result.get("anchor_found") is None else int(bool(result.get("anchor_found"))),
                    result.get("anchor_index"),
                    json.dumps(result.get("warnings") or [], ensure_ascii=False),
                    json.dumps(result.get("result") or {}, ensure_ascii=False),
                    now,
                ),
            )
            row = conn.execute(
                "SELECT * FROM rss_ingest_run_sources WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
        return row_to_ingest_run_source(row)

    def list_ingest_runs(self, limit: int = 50, offset: int = 0) -> tuple[list[dict[str, Any]], int]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM rss_ingest_runs
                ORDER BY started_at DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            ).fetchall()
            total = conn.execute("SELECT COUNT(*) AS total FROM rss_ingest_runs").fetchone()["total"]
        return [row_to_ingest_run(row) for row in rows], int(total)

    def get_ingest_run(self, run_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM rss_ingest_runs WHERE run_id = ?", (run_id,)
            ).fetchone()
        return row_to_ingest_run(row) if row else None

    def list_ingest_run_sources(self, run_id: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM rss_ingest_run_sources
                WHERE run_id = ?
                ORDER BY id ASC
                """,
                (run_id,),
            ).fetchall()
        return [row_to_ingest_run_source(row) for row in rows]

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

        if filters.get("created_from") or filters.get("from"):
            clauses.append("created_at >= ?")
            params.append(filters.get("created_from") or filters["from"])
        if filters.get("created_to") or filters.get("to"):
            clauses.append("created_at <= ?")
            params.append(filters.get("created_to") or filters["to"])
        if filters.get("published_from"):
            clauses.append("published_at >= ?")
            params.append(filters["published_from"])
        if filters.get("published_to"):
            clauses.append("published_at <= ?")
            params.append(filters["published_to"])
        for column in ["source_id", "source_name", "source_category", "content_type"]:
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
        "source_id": row["source_id"],
        "feed_url": row["feed_url"],
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
        "dedupe_version": row["dedupe_version"],
        "latest_raw_json": row["latest_raw_json"],
        "latest_seen_summary": row["latest_seen_summary"],
        "semantic_status": row["semantic_status"],
        "primary_cluster_id": row["primary_cluster_id"],
        "semantic_error": row["semantic_error"],
        "semantic_attempts": row["semantic_attempts"],
        "last_semantic_at": row["last_semantic_at"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "last_seen_at": row["last_seen_at"],
        "seen_count": row["seen_count"],
    }


def row_to_source(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "source_id": row["source_id"],
        "source_name": row["source_name"],
        "source_category": row["source_category"],
        "feed_url": row["feed_url"],
        "normalized_feed_url": row["normalized_feed_url"],
        "local_feed_url": row["local_feed_url"],
        "remote_feed_url": row["remote_feed_url"],
        "status": row["status"],
        "priority": row["priority"],
        "tags": json.loads(row["tags_json"] or "[]"),
        "notes": row["notes"],
        "config": json.loads(row["config_json"] or "{}"),
        "last_fetch_at": row["last_fetch_at"],
        "last_success_at": row["last_success_at"],
        "last_failure_at": row["last_failure_at"],
        "last_error_code": row["last_error_code"],
        "last_error_message": row["last_error_message"],
        "consecutive_failures": row["consecutive_failures"],
        "failure_count": row["failure_count"],
        "consecutive_failure_count": row["consecutive_failure_count"],
        "last_ingest_at": row["last_ingest_at"],
        "last_error_retryable": None
        if row["last_error_retryable"] is None
        else bool(row["last_error_retryable"]),
        "last_run_id": row["last_run_id"],
        "last_new_items": row["last_new_items"],
        "last_duplicate_items": row["last_duplicate_items"],
        "last_processed_items": row["last_processed_items"],
        "last_new_items_count": row["last_new_items_count"],
        "last_duplicate_items_count": row["last_duplicate_items_count"],
        "last_processed_items_count": row["last_processed_items_count"],
        "last_feed_items_seen": row["last_feed_items_seen"],
        "last_duration_ms": row["last_duration_ms"],
        "last_incremental_decision": row["last_incremental_decision"],
        "last_anchor_found": None
        if row["last_anchor_found"] is None
        else bool(row["last_anchor_found"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "deleted_at": row["deleted_at"],
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
        "last_major_update_at": row["last_major_update_at"],
        "source_material_item_id": row["source_material_item_id"],
        "cluster_card_id": row["cluster_card_id"],
        "created_by": row["created_by"],
        "confidence": row["confidence"],
        "merged_into_cluster_id": row["merged_into_cluster_id"],
        "cluster_vector": json.loads(row["cluster_vector_json"] or "[]"),
        "embedding_model": row["embedding_model"],
    }


def row_to_ingest_run(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "run_id": row["run_id"],
        "trigger_type": row["trigger_type"],
        "source_mode": row["source_mode"],
        "status": row["status"],
        "started_at": row["started_at"],
        "finished_at": row["finished_at"],
        "duration_ms": row["duration_ms"],
        "selected_source_count": row["selected_source_count"],
        "success_source_count": row["success_source_count"],
        "failure_source_count": row["failure_source_count"],
        "new_items_count": row["new_items_count"],
        "duplicate_items_count": row["duplicate_items_count"],
        "processed_items_count": row["processed_items_count"],
        "failed_items_count": row["failed_items_count"],
        "created_by": row["created_by"],
        "request": json.loads(row["request_json"] or "{}"),
        "summary": json.loads(row["summary_json"] or "{}"),
        "error_code": row["error_code"],
        "error_message": row["error_message"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def row_to_ingest_run_source(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "run_id": row["run_id"],
        "source_id": row["source_id"],
        "feed_url": row["feed_url"],
        "source_name": row["source_name"],
        "source_category": row["source_category"],
        "status": row["status"],
        "started_at": row["started_at"],
        "finished_at": row["finished_at"],
        "duration_ms": row["duration_ms"],
        "error_code": row["error_code"],
        "error_message": row["error_message"],
        "retryable": None if row["retryable"] is None else bool(row["retryable"]),
        "fetched_entries_count": row["fetched_entries_count"],
        "processed_entries_count": row["processed_entries_count"],
        "new_items_count": row["new_items_count"],
        "duplicate_items_count": row["duplicate_items_count"],
        "failed_items_count": row["failed_items_count"],
        "incremental_mode": row["incremental_mode"],
        "incremental_decision": row["incremental_decision"],
        "anchor_found": None if row["anchor_found"] is None else bool(row["anchor_found"]),
        "anchor_index": row["anchor_index"],
        "warnings": json.loads(row["warnings_json"] or "[]"),
        "result": json.loads(row["result_json"] or "{}"),
        "created_at": row["created_at"],
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
        "source_id": item.get("source_id"),
        "feed_url": item.get("feed_url"),
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
        "dedupe_version": item.get("dedupe_version"),
        "latest_raw_json": item.get("latest_raw_json"),
        "latest_seen_summary": item.get("latest_seen_summary"),
    }


def public_screening(screening: dict[str, Any]) -> dict[str, Any]:
    public = dict(screening)
    public.pop("raw_model_response", None)
    return public
