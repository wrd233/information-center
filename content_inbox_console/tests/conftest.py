"""Test fixtures for content_inbox_console tests."""

import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.dependencies import get_db_connection


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Create a temporary SQLite database with the expected schema."""
    path = tmp_path / "test.sqlite3"
    conn = sqlite3.connect(str(path))
    conn.executescript("""
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
            screening_json TEXT NOT NULL DEFAULT '{}',
            clustering_json TEXT,
            raw_json TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            seen_count INTEGER NOT NULL DEFAULT 1,
            source_id TEXT,
            feed_url TEXT
        );

        CREATE TABLE IF NOT EXISTS rss_sources (
            source_id TEXT PRIMARY KEY,
            source_name TEXT NOT NULL,
            source_category TEXT,
            feed_url TEXT NOT NULL,
            normalized_feed_url TEXT NOT NULL UNIQUE,
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
            failure_count INTEGER NOT NULL DEFAULT 0,
            last_run_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            deleted_at TEXT
        );

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
            error_code TEXT,
            error_message TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

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
            new_items_count INTEGER DEFAULT 0,
            duplicate_items_count INTEGER DEFAULT 0,
            failed_items_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS event_clusters (
            cluster_pk INTEGER PRIMARY KEY AUTOINCREMENT,
            cluster_id TEXT NOT NULL UNIQUE,
            cluster_title TEXT NOT NULL,
            cluster_summary TEXT NOT NULL,
            entities_json TEXT NOT NULL DEFAULT '[]',
            representative_item_id TEXT NOT NULL,
            first_seen_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            item_count INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'active',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    return path


@pytest.fixture
def client(db_path: Path) -> TestClient:
    """FastAPI TestClient with test database."""
    app = create_app()

    app.state.db_available = True
    original_path = app.state.settings.database_path

    app.state.settings.database_path = db_path

    def _override_get_db():
        conn = sqlite3.connect(str(db_path), timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = 1")
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db_connection] = _override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    app.state.settings.database_path = original_path


@pytest.fixture
def populated_db(db_path: Path) -> Path:
    """Database with sample data for testing."""
    conn = sqlite3.connect(str(db_path))

    conn.execute(
        "INSERT OR REPLACE INTO rss_sources(source_id, source_name, feed_url, normalized_feed_url, status, priority, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
        ("source_1", "Test Source 1", "https://example.com/feed1.xml", "https://example.com/feed1.xml", "active", 3),
    )
    conn.execute(
        "INSERT OR REPLACE INTO rss_sources(source_id, source_name, feed_url, normalized_feed_url, status, priority, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
        ("source_2", "Test Source 2", "https://example.com/feed2.xml", "https://example.com/feed2.xml", "broken", 5),
    )

    conn.execute(
        "INSERT OR REPLACE INTO inbox_items(item_id, dedupe_key, title, source_name, source_category, content_type, screening_json, created_at, updated_at, last_seen_at, source_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), datetime('now'), ?)",
        ("item_1", "dedupe_1", "Test Article 1", "Test Source 1", "tech", "article", '{"value_score": 5, "suggested_action": "read"}', "source_1"),
    )
    conn.execute(
        "INSERT OR REPLACE INTO inbox_items(item_id, dedupe_key, title, source_name, source_category, content_type, screening_json, created_at, updated_at, last_seen_at, source_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), datetime('now'), ?)",
        ("item_2", "dedupe_2", "Test Article 2", "Test Source 2", "ai", "article", '{"value_score": 8, "suggested_action": "save"}', "source_2"),
    )

    conn.execute(
        "INSERT OR REPLACE INTO rss_ingest_runs(run_id, trigger_type, source_mode, status, started_at, finished_at, duration_ms, selected_source_count, success_source_count, failure_source_count, new_items_count, duplicate_items_count, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, datetime('now'), datetime('now'), ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
        ("run_1", "cli", "batch", "success", 5000, 2, 1, 1, 2, 0),
    )

    conn.execute(
        "INSERT OR REPLACE INTO rss_ingest_run_sources(run_id, source_id, feed_url, source_name, status, new_items_count, duplicate_items_count, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))",
        ("run_1", "source_1", "https://example.com/feed1.xml", "Test Source 1", "success", 1, 0),
    )
    conn.execute(
        "INSERT OR REPLACE INTO rss_ingest_run_sources(run_id, source_id, feed_url, source_name, status, new_items_count, duplicate_items_count, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))",
        ("run_1", "source_2", "https://example.com/feed2.xml", "Test Source 2", "failed", 1, 0),
    )

    conn.execute(
        "INSERT OR REPLACE INTO event_clusters(cluster_id, cluster_title, cluster_summary, entities_json, representative_item_id, first_seen_at, last_seen_at, item_count, status, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'), ?, 'active', datetime('now'), datetime('now'))",
        ("cluster_1", "Test Cluster", "A test cluster about AI", '["AI", "ML"]', "item_1", 2),
    )

    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def populated_client(populated_db: Path) -> TestClient:
    """FastAPI TestClient with populated test database."""
    app = create_app()
    app.state.db_available = True
    original_path = app.state.settings.database_path
    app.state.settings.database_path = populated_db

    def _override_get_db():
        conn = sqlite3.connect(str(populated_db), timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = 1")
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db_connection] = _override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    app.state.settings.database_path = original_path


@pytest.fixture
def legacy_db(db_path: Path) -> Path:
    """Database with inbox_items having source_name but empty rss_sources and rss_ingest_runs."""
    conn = sqlite3.connect(str(db_path))

    conn.execute(
        "INSERT OR REPLACE INTO inbox_items(item_id, dedupe_key, title, source_name, source_category, content_type, screening_json, created_at, updated_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), datetime('now'))",
        ("item_a", "dedupe_a", "Article A", "Blog A", "tech", "article", '{"value_score": 5}'),
    )
    conn.execute(
        "INSERT OR REPLACE INTO inbox_items(item_id, dedupe_key, title, source_name, source_category, content_type, screening_json, created_at, updated_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), datetime('now'))",
        ("item_b", "dedupe_b", "Article B", "Blog A", "tech", "article", '{"value_score": 3}'),
    )
    conn.execute(
        "INSERT OR REPLACE INTO inbox_items(item_id, dedupe_key, title, source_name, source_category, content_type, screening_json, created_at, updated_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), datetime('now'))",
        ("item_c", "dedupe_c", "Article C", "Blog B", "ai", "article", '{"value_score": 8}'),
    )

    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def legacy_client(legacy_db: Path, tmp_path: Path) -> TestClient:
    """TestClient with legacy database (no rss_sources, but items have source_name)."""
    app = create_app()
    app.state.db_available = True
    original_path = app.state.settings.database_path
    app.state.settings.database_path = legacy_db

    outputs_dir = tmp_path / "outputs" / "runs"
    outputs_dir.mkdir(parents=True)
    run_dir = outputs_dir / "rss_run_20260101_120000"
    run_dir.mkdir()
    (run_dir / "final_report.md").write_text("# Run Report\n\nOPML sources: 50\nFirst pass new: 200\nFirst pass dup: 50\nSuccess: 48\nFail: 2\n")
    original_outputs = app.state.settings.outputs_path
    app.state.settings.outputs_path = outputs_dir

    def _override_get_db():
        conn = sqlite3.connect(str(legacy_db), timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = 1")
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db_connection] = _override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    app.state.settings.database_path = original_path
    app.state.settings.outputs_path = original_outputs
