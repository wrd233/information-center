from __future__ import annotations

import json
from typing import Any

from app.semantic.review_actions import apply_review_decision
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
    apply_result = apply_review_decision(store, dict(row), decision, reviewer=reviewer)
    with store.connect() as conn:
        conn.execute(
            """
            UPDATE review_queue
            SET status = ?, reviewed_at = ?, reviewer = ?, review_note = ?, updated_at = ?,
                applied_at = ?, applied_action = ?, apply_result_json = ?
            WHERE id = ?
            """,
            (
                decision,
                now,
                reviewer,
                note,
                now,
                now if apply_result.get("applied") else None,
                apply_result.get("action"),
                json.dumps(apply_result, ensure_ascii=False, sort_keys=True),
                review_id,
            ),
        )
        updated = conn.execute("SELECT * FROM review_queue WHERE id = ?", (review_id,)).fetchone()
    return {"ok": True, "review": dict(updated), "apply_result": apply_result}
