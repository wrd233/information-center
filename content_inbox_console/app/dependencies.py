"""FastAPI dependencies for the console application."""

import sqlite3
import logging
from typing import Generator

from fastapi import Request, HTTPException

from app.config import settings

logger = logging.getLogger(__name__)


def get_settings() -> "Settings":
    return settings


def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Open a read-only SQLite connection per request. Closed after the request finishes."""
    conn = None
    try:
        conn = sqlite3.connect(
            str(settings.database_path),
            timeout=settings.db_timeout,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA query_only = 1")
        yield conn
    except sqlite3.OperationalError as exc:
        logger.error("Failed to open database %s: %s", settings.database_path, exc)
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}")
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def verify_db_available() -> bool:
    """Check whether the database file exists and is readable. Called at startup."""
    path = settings.database_path
    if not path.exists():
        logger.warning("Database file not found: %s", path)
        return False
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1)
        conn.execute("SELECT 1 FROM sqlite_master LIMIT 1")
        conn.close()
        return True
    except Exception as exc:
        logger.warning("Database connection check failed: %s", exc)
        return False
