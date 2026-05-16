from __future__ import annotations

import json
from typing import Any

from app.semantic.source_profiles import set_priority
from app.storage import InboxStore
from app.utils import utc_now


def list_reviews(store: InboxStore, status: str = "pending", limit: int = 50) -> list[dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM review_queue
            WHERE status = ?
            ORDER BY created_at ASC
            LIMIT ?
            """,
            (status, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def decide_review(store: InboxStore, review_id: int, decision: str, *, reviewer: str = "cli", note: str = "") -> dict[str, Any]:
    now = utc_now()
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM review_queue WHERE id = ?", (review_id,)).fetchone()
        if not row:
            return {"ok": False, "error": "review_not_found"}
        suggestion = json.loads(row["suggestion_json"] or "{}")
        if decision == "approved" and row["review_type"] == "source_priority_suggestion":
            priority = suggestion.get("priority_suggestion")
            if priority:
                set_priority(store, row["target_id"], priority)
        conn.execute(
            """
            UPDATE review_queue
            SET status = ?, reviewed_at = ?, reviewer = ?, review_note = ?, updated_at = ?
            WHERE id = ?
            """,
            (decision, now, reviewer, note, now, review_id),
        )
        updated = conn.execute("SELECT * FROM review_queue WHERE id = ?", (review_id,)).fetchone()
    return {"ok": True, "review": dict(updated)}
