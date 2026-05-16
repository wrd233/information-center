"""Derive source information from inbox_items when rss_sources registry is empty."""

import logging
import sqlite3
from urllib.parse import urlparse
from typing import Any, Optional

logger = logging.getLogger(__name__)


def _extract_domain(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    try:
        parsed = urlparse(url)
        if parsed.netloc:
            return parsed.netloc
    except Exception:
        pass
    return None


def get_source_identity_columns(conn: sqlite3.Connection) -> list[str]:
    """Return available source-identity columns from inbox_items in priority order."""
    rows = conn.execute("PRAGMA table_info(inbox_items)").fetchall()
    existing = {r["name"] for r in rows}

    candidates = ["source_id", "source_name", "feed_url", "url"]
    available = [c for c in candidates if c in existing]
    if not available:
        return []

    # Prefer the first column that has non-null, non-empty distinct values
    for col in available:
        row = conn.execute(
            f"SELECT COUNT(DISTINCT {col}) AS dc FROM inbox_items WHERE {col} IS NOT NULL AND {col} != ''"
        ).fetchone()
        if row and row["dc"] and row["dc"] > 0:
            # Move this column to the front
            if col != available[0]:
                available.remove(col)
                available.insert(0, col)
            break

    return available


def count_observed_sources(conn: sqlite3.Connection) -> int:
    """Count distinct source identities inferred from inbox_items."""
    identity_cols = get_source_identity_columns(conn)
    if not identity_cols:
        return 0

    primary = identity_cols[0]
    sql = f"SELECT COUNT(DISTINCT {primary}) AS cnt FROM inbox_items WHERE {primary} IS NOT NULL AND {primary} != ''"
    row = conn.execute(sql).fetchone()
    return row["cnt"] if row else 0


def list_observed_sources(
    conn: sqlite3.Connection,
    *,
    keyword: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """List observed sources derived from inbox_items metadata."""
    identity_cols = get_source_identity_columns(conn)
    if not identity_cols:
        return [], 0

    primary = identity_cols[0]

    # Build select for available source-id columns
    select_parts = [f"{primary} AS observed_source_key"]
    for col in identity_cols:
        select_parts.append(f"MAX({col}) AS {col}")

    select_parts.append("COUNT(*) AS item_count")
    select_parts.append("MAX(created_at) AS latest_item_at")
    select_parts.append("MAX(published_at) AS latest_published_at")
    select_parts.append("MIN(created_at) AS first_item_at")

    # Get one example title
    rows = conn.execute("PRAGMA table_info(inbox_items)").fetchall()
    existing = {r["name"] for r in rows}
    if "title" in existing:
        select_parts.append(
            "(SELECT title FROM inbox_items AS sub WHERE sub.{primary} = main.{primary} ORDER BY created_at DESC LIMIT 1) AS example_title".format(
                primary=primary
            )
        )

    where_parts = [f"{primary} IS NOT NULL", f"{primary} != ''"]
    params: list[Any] = []
    if keyword:
        like_clauses = []
        for col in identity_cols:
            like_clauses.append(f"{col} LIKE ?")
            params.append(f"%{keyword}%")
        if like_clauses:
            where_parts.append(f"({' OR '.join(like_clauses)})")

    where_clause = " WHERE " + " AND ".join(where_parts)

    count_sql = f"SELECT COUNT(DISTINCT {primary}) AS cnt FROM inbox_items main{where_clause}"
    count_row = conn.execute(count_sql, params).fetchone()
    total = count_row["cnt"] if count_row else 0

    sql = (
        f"SELECT {', '.join(select_parts)} FROM inbox_items main"
        f"{where_clause} GROUP BY {primary}"
        f" ORDER BY item_count DESC LIMIT ? OFFSET ?"
    )
    rows = conn.execute(sql, params + [limit, offset]).fetchall()

    sources = [dict(r) for r in rows]

    # Add domain-derivation for url-based sources
    for src in sources:
        if not src.get("source_name") and src.get("feed_url"):
            src["source_name"] = src["feed_url"]
        elif not src.get("source_name") and src.get("url"):
            domain = _extract_domain(src.get("url"))
            if domain:
                src["source_name"] = domain

    return sources, total


def list_observed_source_items(
    conn: sqlite3.Connection,
    observed_source_key: str,
    *,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[dict], int]:
    """List items belonging to an observed source."""
    identity_cols = get_source_identity_columns(conn)
    if not identity_cols:
        return [], 0

    primary = identity_cols[0]

    rows = conn.execute("PRAGMA table_info(inbox_items)").fetchall()
    existing = {r["name"] for r in rows}
    select_cols = [
        "item_id", "title", "url", "published_at", "created_at",
        "source_name", "source_category", "content_type",
    ]
    available = [c for c in select_cols if c in existing]

    count_sql = f"SELECT COUNT(*) AS cnt FROM inbox_items WHERE {primary} = ?"
    count_row = conn.execute(count_sql, [observed_source_key]).fetchone()
    total = count_row["cnt"] if count_row else 0

    sql = f"SELECT {', '.join(available)} FROM inbox_items WHERE {primary} = ? ORDER BY created_at DESC LIMIT ? OFFSET ?"
    rows = conn.execute(sql, [observed_source_key, limit, offset]).fetchall()
    return [dict(r) for r in rows], total
