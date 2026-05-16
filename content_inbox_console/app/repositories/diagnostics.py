"""Database and filesystem diagnostics for content_inbox_console."""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

EXPECTED_TABLES = [
    "inbox_items",
    "rss_sources",
    "rss_ingest_runs",
    "rss_ingest_run_sources",
    "event_clusters",
]


def get_db_diagnostics(database_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "db_path": str(database_path),
        "db_exists": database_path.exists(),
        "db_readable": False,
        "tables": {},
        "error": None,
    }

    if not database_path.exists():
        return result

    try:
        conn = sqlite3.connect(str(database_path), timeout=3)
        conn.row_factory = sqlite3.Row
    except Exception as exc:
        result["error"] = str(exc)
        return result

    result["db_readable"] = True

    try:
        existing_tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        existing_names = {r["name"] for r in existing_tables}

        for table in EXPECTED_TABLES:
            info: dict[str, Any] = {"exists": table in existing_names, "count": None}
            if info["exists"]:
                try:
                    row = conn.execute(f"SELECT COUNT(*) AS cnt FROM {table}").fetchone()
                    info["count"] = row["cnt"] if row else 0
                except Exception as exc:
                    info["error"] = str(exc)
            result["tables"][table] = info
    finally:
        conn.close()

    return result


def get_outputs_diagnostics(outputs_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "outputs_path": str(outputs_path),
        "outputs_exists": outputs_path.exists(),
        "run_directory_count": 0,
        "error": None,
    }

    if not outputs_path.exists():
        return result

    try:
        count = 0
        for child in outputs_path.iterdir():
            if child.is_dir() and child.name not in (".", ".."):
                count += 1
        result["run_directory_count"] = count
    except Exception as exc:
        result["error"] = str(exc)

    return result


def compute_warnings(
    db_diag: dict[str, Any],
    outputs_diag: dict[str, Any],
) -> list[str]:
    warnings: list[str] = []

    tables = db_diag.get("tables", {})
    inbox = tables.get("inbox_items", {})
    sources = tables.get("rss_sources", {})
    runs = tables.get("rss_ingest_runs", {})
    runs_sources = tables.get("rss_ingest_run_sources", {})
    clusters = tables.get("event_clusters", {})

    if inbox.get("count", 0) is not None and sources.get("count", 0) is not None:
        if inbox["count"] > 0 and sources["count"] == 0:
            warnings.append(
                f"rss_sources is empty but inbox_items has {inbox['count']} rows — "
                "source registry was likely never populated"
            )

    db_runs = runs.get("count", 0) or 0
    db_run_sources = runs_sources.get("count", 0) or 0
    if db_runs == 0 and outputs_diag.get("run_directory_count", 0) > 0:
        warnings.append(
            f"rss_ingest_runs is empty but outputs/runs contains "
            f"{outputs_diag['run_directory_count']} run directories"
        )

    if db_run_sources == 0 and db_runs > 0:
        warnings.append(
            "rss_ingest_runs has rows but rss_ingest_run_sources is empty — "
            "per-source breakdowns may be missing"
        )

    if not db_diag.get("db_exists"):
        warnings.append("Database file not found at configured path")

    if not outputs_diag.get("outputs_exists"):
        warnings.append("Outputs path does not exist or is not mounted")

    return warnings
