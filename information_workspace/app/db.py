from __future__ import annotations

from pathlib import Path
import sqlite3


SCHEMA_VERSION = 1


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_info (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ingest_runs (
          id TEXT PRIMARY KEY,
          status TEXT NOT NULL,
          source TEXT NOT NULL,
          auto_process INTEGER NOT NULL DEFAULT 0,
          synthetic INTEGER NOT NULL DEFAULT 0,
          item_count INTEGER NOT NULL DEFAULT 0,
          accepted_count INTEGER NOT NULL DEFAULT 0,
          failed_count INTEGER NOT NULL DEFAULT 0,
          material_count INTEGER NOT NULL DEFAULT 0,
          duplicate_count INTEGER NOT NULL DEFAULT 0,
          noise_count INTEGER NOT NULL DEFAULT 0,
          candidate_event_count INTEGER NOT NULL DEFAULT 0,
          trace_paths_json TEXT NOT NULL DEFAULT '[]',
          report_paths_json TEXT NOT NULL DEFAULT '[]',
          error_summary TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ingest_run_items (
          id TEXT PRIMARY KEY,
          run_id TEXT NOT NULL REFERENCES ingest_runs(id) ON DELETE CASCADE,
          raw_json TEXT NOT NULL,
          validation_status TEXT NOT NULL DEFAULT 'pending',
          error TEXT,
          material_id TEXT,
          created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS run_steps (
          id TEXT PRIMARY KEY,
          run_id TEXT NOT NULL REFERENCES ingest_runs(id) ON DELETE CASCADE,
          step_name TEXT NOT NULL,
          status TEXT NOT NULL,
          started_at TEXT,
          finished_at TEXT,
          input_count INTEGER NOT NULL DEFAULT 0,
          output_count INTEGER NOT NULL DEFAULT 0,
          skipped_count INTEGER NOT NULL DEFAULT 0,
          failed_count INTEGER NOT NULL DEFAULT 0,
          message TEXT,
          error_summary TEXT,
          UNIQUE(run_id, step_name)
        );

        CREATE TABLE IF NOT EXISTS run_logs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          run_id TEXT NOT NULL REFERENCES ingest_runs(id) ON DELETE CASCADE,
          step_name TEXT,
          level TEXT NOT NULL,
          message TEXT NOT NULL,
          details_json TEXT NOT NULL DEFAULT '{}',
          created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS materials (
          id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          content_text TEXT NOT NULL,
          source_name TEXT NOT NULL,
          source_type TEXT NOT NULL,
          url TEXT,
          external_id TEXT,
          author TEXT,
          published_at TEXT,
          fetched_at TEXT,
          language TEXT,
          content_html TEXT,
          summary_from_source TEXT,
          tags_from_source_json TEXT NOT NULL DEFAULT '[]',
          upstream_score REAL,
          upstream_reason TEXT,
          metadata_json TEXT NOT NULL DEFAULT '{}',
          raw_payload_json TEXT NOT NULL DEFAULT '{}',
          content_hash TEXT NOT NULL,
          title_hash TEXT NOT NULL,
          light_understanding_json TEXT,
          light_understanding_status TEXT NOT NULL DEFAULT 'pending',
          llm_trace_path TEXT,
          synthetic INTEGER NOT NULL DEFAULT 0,
          ignored INTEGER NOT NULL DEFAULT 0,
          is_duplicate INTEGER NOT NULL DEFAULT 0,
          duplicate_of TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_materials_content_hash ON materials(content_hash);
        CREATE INDEX IF NOT EXISTS idx_materials_external_id ON materials(external_id);
        CREATE INDEX IF NOT EXISTS idx_materials_url ON materials(url);
        CREATE INDEX IF NOT EXISTS idx_materials_source_type ON materials(source_type);
        CREATE INDEX IF NOT EXISTS idx_materials_synthetic ON materials(synthetic);

        CREATE TABLE IF NOT EXISTS material_relations (
          id TEXT PRIMARY KEY,
          primary_material_id TEXT NOT NULL,
          related_material_id TEXT NOT NULL,
          relation_type TEXT NOT NULL,
          reason TEXT NOT NULL,
          score REAL,
          run_id TEXT,
          created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS llm_call_summaries (
          id TEXT PRIMARY KEY,
          task_name TEXT NOT NULL,
          provider TEXT NOT NULL,
          model TEXT NOT NULL,
          prompt_file TEXT NOT NULL,
          prompt_version TEXT NOT NULL,
          status TEXT NOT NULL,
          material_id TEXT,
          run_id TEXT,
          trace_path TEXT,
          semantic_check_json TEXT NOT NULL DEFAULT '{}',
          error_summary TEXT,
          created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS events (
          id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          status TEXT NOT NULL,
          center_description_json TEXT NOT NULL DEFAULT '{}',
          user_focus TEXT,
          sleeping_reason TEXT,
          pinned INTEGER NOT NULL DEFAULT 0,
          favorite INTEGER NOT NULL DEFAULT 0,
          ignored_candidate INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          last_meaningful_update_at TEXT
        );

        CREATE TABLE IF NOT EXISTS event_materials (
          id TEXT PRIMARY KEY,
          event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
          material_id TEXT NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
          role TEXT NOT NULL,
          note TEXT,
          created_at TEXT NOT NULL,
          UNIQUE(event_id, material_id, role)
        );

        CREATE TABLE IF NOT EXISTS event_updates (
          id TEXT PRIMARY KEY,
          event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
          update_json TEXT NOT NULL,
          supporting_material_ids_json TEXT NOT NULL DEFAULT '[]',
          created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS topics (
          id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          goal TEXT NOT NULL,
          organization TEXT NOT NULL,
          pinned INTEGER NOT NULL DEFAULT 0,
          current_structure_json TEXT NOT NULL DEFAULT '{}',
          candidate_structure_json TEXT NOT NULL DEFAULT '{}',
          node_constraints_json TEXT NOT NULL DEFAULT '{}',
          last_structure_refresh_at TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS topic_materials (
          id TEXT PRIMARY KEY,
          topic_id TEXT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
          material_id TEXT REFERENCES materials(id) ON DELETE CASCADE,
          event_id TEXT REFERENCES events(id) ON DELETE CASCADE,
          entry_type TEXT NOT NULL,
          referenced_by_current_structure INTEGER NOT NULL DEFAULT 0,
          added_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS exports (
          id TEXT PRIMARY KEY,
          object_type TEXT NOT NULL,
          object_id TEXT NOT NULL,
          file_path TEXT NOT NULL,
          material_count INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        """
    )
    conn.execute(
        "INSERT OR REPLACE INTO schema_info(key, value) VALUES('schema_version', ?)",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


def schema_version(conn: sqlite3.Connection) -> int:
    row = conn.execute(
        "SELECT value FROM schema_info WHERE key = 'schema_version'"
    ).fetchone()
    return int(row["value"]) if row else 0
