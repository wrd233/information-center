from __future__ import annotations

import json
from typing import Any

from app.semantic.operational_pipeline import CREATED_BY, SCHEMA_VERSION, classify_item_eventness
from app.semantic.signatures import extract_event_signature
from app.semantic.source_profiles import set_priority
from app.storage import InboxStore
from app.utils import stable_hash, utc_now


def apply_review_decision(store: InboxStore, review: dict[str, Any], decision: str, *, reviewer: str = "cli") -> dict[str, Any]:
    if decision not in {"approved", "rejected"}:
        return {"applied": False, "action": "status_only", "reason": "decision does not apply pipeline changes"}
    review_type = review["review_type"]
    if review_type == "source_priority_suggestion" and decision == "approved":
        suggestion = _loads(review["suggestion_json"])
        priority = suggestion.get("priority_suggestion")
        if priority:
            profile = set_priority(store, review["target_id"], priority)
            return {"applied": True, "action": "source_priority_set", "profile": profile}
    if review_type == "event_relation_review":
        return apply_event_relation_review(store, review, decision, reviewer=reviewer)
    if review_type == "eventness_review":
        return apply_eventness_review(store, review, decision, reviewer=reviewer)
    return {"applied": False, "action": "status_only", "reason": f"no apply handler for {review_type}"}


def apply_event_relation_review(store: InboxStore, review: dict[str, Any], decision: str, *, reviewer: str) -> dict[str, Any]:
    suggestion = _loads(review["suggestion_json"])
    item_ids = str(review["target_id"]).split(":", 1)
    if len(item_ids) != 2:
        return {"applied": False, "action": "invalid_item_pair", "target_id": review["target_id"]}
    left_id, right_id = item_ids
    now = utc_now()
    if decision == "rejected":
        with store.connect() as conn:
            conn.execute(
                "UPDATE event_candidate_pairs SET status = 'review_rejected' WHERE (item_a_id = ? AND item_b_id = ?) OR (item_a_id = ? AND item_b_id = ?)",
                (left_id, right_id, right_id, left_id),
            )
            _write_review_signal(conn, store, left_id, review_acceptance=-1, now=now)
            _write_review_signal(conn, store, right_id, review_acceptance=-1, now=now)
        return {"applied": True, "action": "event_relation_rejected", "item_ids": item_ids}

    with store.connect() as conn:
        left = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (left_id,)).fetchone()
        right = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (right_id,)).fetchone()
        if not left or not right:
            return {"applied": False, "action": "missing_item", "item_ids": item_ids}
        left_item = dict(left)
        right_item = dict(right)
        cluster_id = left_item.get("primary_cluster_id") or right_item.get("primary_cluster_id")
        if not cluster_id:
            cluster_id = _create_review_cluster(conn, left_item, now)
        event_id = _ensure_review_event(conn, cluster_id, left_item, now)
        for item, role in [(left_item, "source_material"), (right_item, "same_event_new_info")]:
            conn.execute(
                """
                INSERT OR REPLACE INTO cluster_items(
                    cluster_id, item_id, primary_relation, same_event, same_topic, confidence,
                    incremental_value, report_value, reason, evidence_json, decision_source,
                    schema_version, input_fingerprint, created_at, updated_at
                )
                VALUES (?, ?, ?, 1, 1, ?, ?, ?, ?, ?, 'human_review', ?, ?, ?, ?)
                """,
                (
                    cluster_id,
                    item["item_id"],
                    role,
                    0.88,
                    3 if role != "source_material" else 2,
                    3,
                    "Approved event relation review.",
                    json.dumps({"review_id": review["id"], "reviewer": reviewer, "suggestion": suggestion, "schema_version": SCHEMA_VERSION}, ensure_ascii=False),
                    SCHEMA_VERSION,
                    stable_hash(json.dumps({"review_id": review["id"], "cluster_id": cluster_id, "item_id": item["item_id"], "role": role}, sort_keys=True)),
                    now,
                    now,
                ),
            )
            conn.execute("UPDATE inbox_items SET primary_cluster_id = ?, semantic_status = 'clustered', last_semantic_at = ?, updated_at = ? WHERE item_id = ?", (cluster_id, now, now, item["item_id"]))
            conn.execute("INSERT OR IGNORE INTO event_items(event_id, item_id, role, created_at) VALUES (?, ?, ?, ?)", (event_id, item["item_id"], "supporting" if role != "source_material" else "source_material", now))
            _write_review_signal(
                conn,
                store,
                item["item_id"],
                cluster_id=cluster_id,
                discovery_value=1 if role == "source_material" else 0,
                fact_value=1 if role == "source_material" else 0,
                incremental_value=2 if role != "source_material" else 0,
                review_acceptance=1,
                now=now,
            )
        conn.execute(
            "UPDATE events SET status = 'ready', confidence = MAX(confidence, 0.88), updated_at = ? WHERE event_id = ?",
            (now, event_id),
        )
        conn.execute(
            "UPDATE event_candidate_pairs SET status = 'review_approved', relation_type = COALESCE(relation_type, 'same_event_new_info'), decision_source = 'human_review', confidence = MAX(confidence, 0.88) WHERE (item_a_id = ? AND item_b_id = ?) OR (item_a_id = ? AND item_b_id = ?)",
            (left_id, right_id, right_id, left_id),
        )
    return {"applied": True, "action": "event_relation_approved", "event_id": event_id, "cluster_id": cluster_id, "item_ids": item_ids}


def apply_eventness_review(store: InboxStore, review: dict[str, Any], decision: str, *, reviewer: str) -> dict[str, Any]:
    item_id = review["target_id"]
    now = utc_now()
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        if not row:
            return {"applied": False, "action": "missing_item", "item_id": item_id}
        item = dict(row)
        if decision == "rejected":
            _write_review_signal(conn, store, item_id, non_event_noise=1, review_acceptance=-1, now=now)
            return {"applied": True, "action": "eventness_rejected", "item_id": item_id}
        cluster_id = _create_review_cluster(conn, item, now)
        event_id = _ensure_review_event(conn, cluster_id, item, now, status="ready")
        conn.execute("INSERT OR IGNORE INTO event_items(event_id, item_id, role, created_at) VALUES (?, ?, 'source_material', ?)", (event_id, item_id, now))
        _write_review_signal(conn, store, item_id, cluster_id=cluster_id, discovery_value=1, fact_value=1, review_acceptance=1, now=now)
    return {"applied": True, "action": "eventness_approved", "event_id": event_id, "cluster_id": cluster_id, "item_id": item_id}


def _create_review_cluster(conn: Any, item: dict[str, Any], now: str) -> str:
    signature = extract_event_signature(item)
    eventness = classify_item_eventness(item, signature)
    cluster_id = "cluster_" + stable_hash(f"{SCHEMA_VERSION}:review:{item['item_id']}")[:16]
    title = item.get("title") or signature.product_or_model or item["item_id"]
    summary = item.get("summary") or title
    evidence = {"schema_version": SCHEMA_VERSION, "created_by": "human_review", "signature": signature.model_dump(), "eventness": eventness}
    conn.execute(
        """
        INSERT OR REPLACE INTO event_clusters(
            cluster_id, cluster_title, cluster_summary, entities_json, representative_item_id,
            first_seen_at, last_seen_at, item_count, status, created_by, confidence, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'active', ?, 0.88, ?, ?)
        """,
        (
            cluster_id,
            title,
            summary,
            json.dumps({"actor": signature.actor, "product": signature.product_or_model, "action": signature.action, "evidence": evidence}, ensure_ascii=False),
            item["item_id"],
            item.get("published_at") or now,
            item.get("published_at") or now,
            "human_review",
            now,
            now,
        ),
    )
    conn.execute("UPDATE inbox_items SET primary_cluster_id = ?, semantic_status = 'clustered', last_semantic_at = ?, updated_at = ? WHERE item_id = ?", (cluster_id, now, now, item["item_id"]))
    return cluster_id


def _ensure_review_event(conn: Any, cluster_id: str, item: dict[str, Any], now: str, *, status: str = "ready") -> str:
    signature = extract_event_signature(item)
    event_id = "event_" + stable_hash(cluster_id)[:16]
    title = item.get("title") or signature.product_or_model or item["item_id"]
    summary = item.get("summary") or title
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "created_by": "human_review",
        "input_fingerprint": stable_hash(json.dumps({"cluster_id": cluster_id, "item_id": item["item_id"]}, sort_keys=True)),
        "primary_cluster_id": cluster_id,
        "decision_source": "human_review",
    }
    conn.execute(
        """
        INSERT OR REPLACE INTO events(
            event_id, event_title, event_summary, event_type, event_time, status, importance,
            confidence, primary_cluster_id, evidence_json, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, 2, 0.88, ?, ?, ?, ?)
        """,
        (
            event_id,
            title,
            summary,
            signature.action if signature.action != "other" else "event",
            signature.date_bucket or item.get("published_at"),
            status,
            cluster_id,
            json.dumps(evidence, ensure_ascii=False),
            now,
            now,
        ),
    )
    return event_id


def _write_review_signal(
    conn: Any,
    store: InboxStore,
    item_id: str,
    *,
    cluster_id: str | None = None,
    discovery_value: int = 0,
    fact_value: int = 0,
    incremental_value: int = 0,
    interpretation_value: int = 0,
    duplicate_noise: int = 0,
    non_event_noise: int = 0,
    review_acceptance: int = 0,
    now: str,
) -> None:
    row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
    if not row:
        return
    item = dict(row)
    source_id = item.get("source_id") or item.get("feed_url") or item.get("source_name")
    if not source_id:
        return
    conn.execute(
        """
        INSERT INTO source_signals(
            source_id, item_id, cluster_id, discovery_value, fact_value, incremental_value,
            interpretation_value, duplicate_noise, non_event_noise, review_acceptance,
            source_role, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'reviewed', ?, ?)
        ON CONFLICT(source_id, item_id) DO UPDATE SET
            cluster_id = COALESCE(excluded.cluster_id, source_signals.cluster_id),
            discovery_value = source_signals.discovery_value + excluded.discovery_value,
            fact_value = source_signals.fact_value + excluded.fact_value,
            incremental_value = source_signals.incremental_value + excluded.incremental_value,
            interpretation_value = source_signals.interpretation_value + excluded.interpretation_value,
            duplicate_noise = source_signals.duplicate_noise + excluded.duplicate_noise,
            non_event_noise = source_signals.non_event_noise + excluded.non_event_noise,
            review_acceptance = source_signals.review_acceptance + excluded.review_acceptance,
            updated_at = excluded.updated_at
        """,
        (
            source_id,
            item_id,
            cluster_id,
            discovery_value,
            fact_value,
            incremental_value,
            interpretation_value,
            duplicate_noise,
            non_event_noise,
            review_acceptance,
            now,
            now,
        ),
    )


def _loads(value: Any) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(str(value))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}
