from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_schema(db_path: Path) -> None:
    with connect(db_path) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY,
                source_id TEXT UNIQUE NOT NULL,
                source_type TEXT NOT NULL,
                display_name TEXT NOT NULL,
                status TEXT NOT NULL,
                category TEXT NOT NULL,
                tags_json TEXT,
                rating INTEGER NOT NULL DEFAULT 50,
                notes TEXT,
                adapter_id TEXT,
                route_path TEXT,
                feed_url TEXT,
                original_feed_url TEXT,
                wechat_identity_json TEXT,
                last_checked_at TEXT,
                last_check_status TEXT,
                last_check_error TEXT,
                last_success_at TEXT,
                last_failure_at TEXT,
                consecutive_failures INTEGER DEFAULT 0,
                last_error TEXT,
                total_entries_seen INTEGER DEFAULT 0,
                last_fetch_new_count INTEGER DEFAULT 0,
                last_fetch_existing_count INTEGER DEFAULT 0,
                last_fetch_scanned_count INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT,
                disabled_at TEXT
            );

            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY,
                entry_id TEXT UNIQUE NOT NULL,
                source_id TEXT NOT NULL,
                guid TEXT,
                url TEXT,
                normalized_url TEXT,
                identity_key TEXT NOT NULL,
                title TEXT,
                published_at TEXT,
                first_seen_at TEXT,
                last_seen_at TEXT,
                seen_count INTEGER DEFAULT 1,
                summary_excerpt TEXT,
                content_hash TEXT,
                summary_hash TEXT,
                created_at TEXT,
                updated_at TEXT,
                UNIQUE(source_id, identity_key)
            );

            CREATE TABLE IF NOT EXISTS fetch_runs (
                id INTEGER PRIMARY KEY,
                fetch_run_id TEXT UNIQUE NOT NULL,
                source_id TEXT NOT NULL,
                status TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT,
                fetched_count INTEGER DEFAULT 0,
                scanned_count INTEGER DEFAULT 0,
                new_count INTEGER DEFAULT 0,
                existing_count INTEGER DEFAULT 0,
                stopped_reason TEXT,
                error_message TEXT,
                include_raw INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS fetch_run_entries (
                id INTEGER PRIMARY KEY,
                fetch_run_id TEXT NOT NULL,
                entry_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                position INTEGER NOT NULL,
                seen_status TEXT NOT NULL,
                identity_key TEXT NOT NULL,
                seen_at TEXT
            );

            CREATE TABLE IF NOT EXISTS import_runs (
                id INTEGER PRIMARY KEY,
                import_run_id TEXT UNIQUE NOT NULL,
                import_type TEXT NOT NULL,
                filename TEXT,
                started_at TEXT,
                finished_at TEXT,
                status TEXT NOT NULL,
                created_count INTEGER DEFAULT 0,
                updated_count INTEGER DEFAULT 0,
                skipped_count INTEGER DEFAULT 0,
                duplicate_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                strategy TEXT,
                error_summary TEXT,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS rating_adjustments (
                id INTEGER PRIMARY KEY,
                source_id TEXT NOT NULL,
                old_rating INTEGER NOT NULL,
                delta INTEGER NOT NULL,
                new_rating INTEGER NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT,
                actor TEXT
            );

            CREATE TABLE IF NOT EXISTS batch_runs (
                id INTEGER PRIMARY KEY,
                batch_run_id TEXT UNIQUE NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                total_count INTEGER DEFAULT 0,
                pending_count INTEGER DEFAULT 0,
                running_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                skipped_count INTEGER DEFAULT 0,
                cancelled_count INTEGER DEFAULT 0,
                started_at TEXT,
                finished_at TEXT,
                elapsed_ms INTEGER,
                options_json TEXT,
                created_by TEXT,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS batch_run_items (
                id INTEGER PRIMARY KEY,
                batch_run_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                display_name TEXT,
                source_type TEXT,
                status TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT,
                elapsed_ms INTEGER,
                http_status INTEGER,
                content_type TEXT,
                error_type TEXT,
                error_message TEXT,
                failure_stage TEXT,
                entries_found INTEGER DEFAULT 0,
                entries_new INTEGER DEFAULT 0,
                entries_existing INTEGER DEFAULT 0,
                stopped_reason TEXT,
                result_json TEXT,
                created_at TEXT,
                updated_at TEXT,
                UNIQUE(batch_run_id, source_id)
            );

            CREATE INDEX IF NOT EXISTS idx_sources_type_status ON sources(source_type, status);
            CREATE INDEX IF NOT EXISTS idx_sources_category ON sources(category);
            CREATE INDEX IF NOT EXISTS idx_entries_source_seen ON entries(source_id, last_seen_at);
            CREATE INDEX IF NOT EXISTS idx_fetch_runs_source_started ON fetch_runs(source_id, started_at);
            CREATE INDEX IF NOT EXISTS idx_fetch_run_entries_run ON fetch_run_entries(fetch_run_id);
            CREATE INDEX IF NOT EXISTS idx_batch_runs_status ON batch_runs(status, created_at);
            CREATE INDEX IF NOT EXISTS idx_batch_run_items_run ON batch_run_items(batch_run_id, status);
            """
        )
