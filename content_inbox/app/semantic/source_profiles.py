from __future__ import annotations

from typing import Any

from app.semantic import db
from app.semantic.relations import insert_review
from app.storage import InboxStore
from app.utils import utc_now


def recompute_source_profiles(store: InboxStore) -> dict[str, Any]:
    now = utc_now()
    with store.connect() as conn:
        source_rows = conn.execute(
            """
            SELECT COALESCE(source_id, feed_url, source_name) AS source_id, COUNT(*) AS total_items
            FROM inbox_items
            GROUP BY COALESCE(source_id, feed_url, source_name)
            """
        ).fetchall()
        stats = {"sources": len(source_rows), "suggestions": 0}
        for row in source_rows:
            source_id = row["source_id"]
            total_items = int(row["total_items"] or 0)
            relation_counts = conn.execute(
                """
                SELECT primary_relation, COUNT(*) AS n
                FROM item_relations r
                JOIN inbox_items i ON i.item_id = r.item_a_id
                WHERE COALESCE(i.source_id, i.feed_url, i.source_name) = ?
                GROUP BY primary_relation
                """,
                (source_id,),
            ).fetchall()
            counts = {r["primary_relation"]: int(r["n"]) for r in relation_counts}
            signals = conn.execute(
                """
                SELECT AVG(incremental_value) AS inc_avg, AVG(report_value) AS report_avg,
                       AVG(CASE WHEN source_role = 'source_material' THEN 1.0 ELSE 0.0 END) AS source_rate,
                       SUM(CASE WHEN incremental_value >= 4 OR report_value >= 4 THEN 1 ELSE 0 END) AS high_value
                FROM source_signals
                WHERE source_id = ?
                """,
                (source_id,),
            ).fetchone()
            token_row = conn.execute(
                """
                SELECT COALESCE(SUM(total_tokens), 0) AS tokens
                FROM llm_call_logs
                WHERE status = 'ok'
                """
            ).fetchone()
            duplicate_rate = counts.get("duplicate", 0) / max(total_items, 1)
            near_duplicate_rate = counts.get("near_duplicate", 0) / max(total_items, 1)
            new_event_rate = float(signals["source_rate"] or 0.0)
            inc_avg = float(signals["inc_avg"] or 0.0)
            report_avg = float(signals["report_avg"] or 0.0)
            high_value = int(signals["high_value"] or 0)
            yield_score = round((inc_avg + report_avg + new_event_rate * 5.0) / 3.0, 3)
            suggestion = suggest_priority(duplicate_rate, near_duplicate_rate, yield_score, high_value, total_items)
            old = conn.execute("SELECT * FROM source_profiles WHERE source_id = ?", (source_id,)).fetchone()
            current_priority = old["llm_priority"] if old else "new_source_under_evaluation"
            conn.execute(
                """
                INSERT OR REPLACE INTO source_profiles (
                    source_id, total_items, llm_processed_items, duplicate_rate, near_duplicate_rate,
                    new_event_rate, incremental_value_avg, report_value_avg, source_item_rate,
                    representative_item_rate, llm_total_tokens, llm_high_value_outputs,
                    llm_yield_score, llm_priority, priority_suggestion, review_status,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM source_profiles WHERE source_id = ?), ?), ?)
                """,
                (
                    source_id,
                    total_items,
                    counts.get("related_with_new_info", 0) + high_value,
                    duplicate_rate,
                    near_duplicate_rate,
                    new_event_rate,
                    inc_avg,
                    report_avg,
                    new_event_rate,
                    0.0,
                    int(token_row["tokens"] or 0),
                    high_value,
                    yield_score,
                    current_priority,
                    suggestion,
                    "pending" if suggestion != current_priority else "none",
                    source_id,
                    now,
                    now,
                ),
            )
            if suggestion != current_priority:
                stats["suggestions"] += 1
    create_priority_reviews(store)
    return {"ok": True, "stats": stats}


def suggest_priority(duplicate_rate: float, near_duplicate_rate: float, yield_score: float, high_value: int, total_items: int) -> str:
    if total_items >= 10 and duplicate_rate + near_duplicate_rate > 0.85 and yield_score < 1.0:
        return "disabled_for_llm"
    if duplicate_rate + near_duplicate_rate > 0.65 and yield_score < 1.8:
        return "low"
    if yield_score >= 3.5 and high_value >= 2:
        return "high"
    if total_items >= 3:
        return "normal"
    return "new_source_under_evaluation"


def create_priority_reviews(store: InboxStore) -> None:
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM source_profiles
            WHERE priority_suggestion IS NOT NULL
              AND priority_suggestion != llm_priority
              AND review_status = 'pending'
            """
        ).fetchall()
    for row in rows:
        insert_review(
            store,
            "source_priority_suggestion",
            "source",
            row["source_id"],
            {
                "source_id": row["source_id"],
                "current_priority": row["llm_priority"],
                "priority_suggestion": row["priority_suggestion"],
                "llm_yield_score": row["llm_yield_score"],
                "duplicate_rate": row["duplicate_rate"],
                "near_duplicate_rate": row["near_duplicate_rate"],
                "reason": "source_profile recompute generated a priority suggestion",
            },
        )


def list_suggestions(store: InboxStore) -> list[dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM source_profiles
            WHERE priority_suggestion IS NOT NULL AND priority_suggestion != llm_priority
            ORDER BY updated_at DESC
            """
        ).fetchall()
    return db.rows_to_dicts(rows)


def get_profile(store: InboxStore, source_id: str) -> dict[str, Any] | None:
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM source_profiles WHERE source_id = ?", (source_id,)).fetchone()
    return dict(row) if row else None


def set_priority(store: InboxStore, source_id: str, priority: str) -> dict[str, Any]:
    now = utc_now()
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO source_profiles (source_id, llm_priority, review_status, created_at, updated_at)
            VALUES (?, ?, 'manual', ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET llm_priority = excluded.llm_priority,
                review_status = 'manual', updated_at = excluded.updated_at
            """,
            (source_id, priority, now, now),
        )
        row = conn.execute("SELECT * FROM source_profiles WHERE source_id = ?", (source_id,)).fetchone()
    return dict(row)
