from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from app.semantic import db
from app.semantic.cards import generate_item_cards
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.candidates import assess_candidate
from app.semantic.relations import card_public, hours_apart, insert_review, normalized_entity_terms, semantic_tokens
from app.semantic.schemas import (
    CLUSTER_CARD_PROMPT_VERSION,
    ITEM_CLUSTER_PROMPT_VERSION,
    SCHEMA_VERSION,
    ClusterCardData,
    ItemClusterOutput,
    cluster_relation_action,
)
from app.storage import InboxStore, row_to_cluster
from app.utils import truncate, utc_now


def current_cluster_card(store: InboxStore, cluster_id: str) -> dict[str, Any] | None:
    with store.connect() as conn:
        row = conn.execute(
            "SELECT * FROM cluster_cards WHERE cluster_id = ? AND is_current = 1", (cluster_id,)
        ).fetchone()
    return dict(row) if row else None


def list_clusters(store: InboxStore, status: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    with store.connect() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM event_clusters WHERE status = ? ORDER BY last_seen_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM event_clusters ORDER BY last_seen_at DESC LIMIT ?", (limit,)
            ).fetchall()
    return [row_to_cluster(row) for row in rows]


def show_cluster(store: InboxStore, cluster_id: str) -> dict[str, Any] | None:
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM event_clusters WHERE cluster_id = ?", (cluster_id,)).fetchone()
        if not row:
            return None
        items = conn.execute(
            "SELECT * FROM cluster_items WHERE cluster_id = ? ORDER BY created_at DESC", (cluster_id,)
        ).fetchall()
    cluster = row_to_cluster(row)
    cluster["cluster_card"] = current_cluster_card(store, cluster_id)
    cluster["items"] = db.rows_to_dicts(items)
    return cluster


def candidate_clusters(
    store: InboxStore,
    item_card: dict[str, Any],
    max_candidates: int,
    *,
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    clusters = list_clusters(store, status=None, limit=200)
    item_terms = semantic_tokens(
        f"{item_card['canonical_title']} {item_card.get('event_hint') or ''} {item_card.get('short_summary') or ''}"
    )
    item_entities = normalized_entity_terms(json.loads(item_card["entities_json"] or "[]"))
    item = db.get_item(store, item_card["item_id"]) or {}
    scored: list[tuple[float, str, dict[str, Any]]] = []
    for cluster in clusters:
        if cluster["status"] == "merged":
            continue
        if cluster["status"] == "archived" and not include_archived:
            continue
        archived_penalty = -3 if cluster["status"] == "archived" else 0
        title_terms = semantic_tokens(f"{cluster['cluster_title']} {cluster['cluster_summary']}")
        score = float(len(item_terms & title_terms)) + len(item_entities & normalized_entity_terms(cluster["entities"])) * 4 + archived_penalty
        gap = hours_apart(
            item.get("published_at") or item.get("created_at"),
            cluster.get("last_seen_at") or cluster.get("first_seen_at"),
        )
        if gap is not None:
            if gap <= 24:
                score += 2
            elif gap <= 72:
                score += 1
        if score > 0:
            card = current_cluster_card(store, cluster["cluster_id"])
            cluster["cluster_card"] = card
            scored.append((score, cluster.get("last_seen_at") or "", cluster))
    scored.sort(key=lambda pair: (pair[0], pair[1]), reverse=True)
    return [cluster for _score, _seen, cluster in scored[:max_candidates]]


def process_item_clusters(
    store: InboxStore,
    *,
    limit: int = 100,
    live: bool = False,
    max_candidates: int = 3,
    max_calls: int | None = None,
    model: str | None = None,
    include_archived: bool = False,
    token_budget: int | None = None,
    global_call_limit: bool = False,
    patch_cards: bool = True,
) -> dict[str, Any]:
    generate_item_cards(store, limit=limit, live=False, force=False)
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT c.item_id
            FROM item_cards c
            LEFT JOIN cluster_items ci ON ci.item_id = c.item_id
            LEFT JOIN item_relations ir ON ir.item_a_id = c.item_id AND ir.should_fold = 1
            WHERE c.is_current = 1 AND ci.id IS NULL AND ir.id IS NULL
            ORDER BY c.created_at ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    client = SemanticLLMClient(
        store,
        live=live,
        model=model,
        max_calls=max_calls,
        token_budget=token_budget,
        global_call_limit=global_call_limit,
    )
    stats = {"selected": len(rows), "attached": 0, "created_clusters": 0, "review": 0, "llm_calls": 0, "candidate_clusters": 0, "no_candidate_items": 0, "llm_items": 0}
    for row in rows:
        item_id = row["item_id"]
        item_card = db.get_current_item_card(store, item_id)
        item = db.get_item(store, item_id)
        if not item or not item_card:
            continue
        candidates = candidate_clusters(store, item_card, max_candidates, include_archived=include_archived)
        if not candidates:
            stats["no_candidate_items"] += 1
            cluster_id = create_semantic_cluster(store, item, item_card, created_by="rule")
            insert_cluster_item(
                store,
                cluster_id,
                item_id,
                primary_relation="source_material" if item_card["content_role"] == "source_material" else "new_info",
                secondary_roles=[],
                same_event=True,
                same_topic=True,
                follow_up_event=False,
                confidence=0.6,
                incremental_value=3,
                report_value=3,
                should_update_cluster_card=True,
                should_notify=False,
                new_facts=[],
                new_angles=[],
                reason="created initial semantic cluster",
                evidence=[],
                decision_source="rule",
                llm_call_id=None,
                prompt_version=None,
                model="rule",
            )
            rebuild_cluster_card(store, cluster_id, live=False)
            stats["created_clusters"] += 1
            continue
        stats["candidate_clusters"] += len(candidates)
        input_data = {
            "new_item_card": card_public(item_card),
            "candidate_clusters": [cluster_prompt_payload(store, cluster) for cluster in candidates],
        }
        output, call_id, _reason = client.call_json(
            task_type="item_cluster_relation",
            prompt_version=ITEM_CLUSTER_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=ItemClusterOutput,
            max_tokens=2600,
            item_id=item_id,
            source_id=item.get("source_id") or item.get("feed_url") or item.get("source_name"),
            request_metadata={
                "prompt_variant": "full",
                "candidate_priority": "high" if any(same_event_cluster_candidate(store, item, item_card, cluster) for cluster in candidates) else "medium",
            },
        )
        stats["llm_calls"] = client.calls
        stats["llm_items"] += 1
        if not output:
            insert_review(store, "uncertain_cluster_relation", "item", item_id, {"reason": "LLM skipped or failed"})
            stats["review"] += 1
            continue
        decision = output.best_relation
        selected_cluster = next((cluster for cluster in candidates if cluster["cluster_id"] == decision.cluster_id), candidates[0] if candidates else None)
        if selected_cluster and decision.primary_relation != "follow_up" and not same_event_cluster_candidate(store, item, item_card, selected_cluster):
            payload = decision.model_dump()
            payload["attach_eligible"] = False
            payload.setdefault("attach_disqualifiers", [])
            payload["attach_disqualifiers"] = list(payload["attach_disqualifiers"] or []) + ["weak_cluster_seed_evidence"]
            insert_review(store, "same_topic", "item", item_id, payload)
            stats["review"] += 1
            continue
        if not cluster_decision_attach_eligible(decision):
            review_type = "same_topic" if decision.primary_relation in {"same_topic", "unrelated"} else "uncertain_cluster_relation"
            payload = decision.model_dump()
            payload.setdefault("attach_disqualifiers", [])
            payload["attach_eligible"] = False
            if not payload["attach_disqualifiers"]:
                payload["attach_disqualifiers"] = ["not_same_event_eligible"]
            insert_review(store, review_type, "item", item_id, payload)
            stats["review"] += 1
            continue
        action = cluster_relation_action(decision.primary_relation)
        if action == "create_follow_up_cluster":
            previous_cluster_id = decision.cluster_id or candidates[0]["cluster_id"]
            new_cluster_id = create_semantic_cluster(store, item, item_card, created_by="llm")
            insert_cluster_relation(store, previous_cluster_id, new_cluster_id, "follow_up", decision.confidence, decision.reason, call_id)
            target_cluster_id = new_cluster_id
            stats["created_clusters"] += 1
        elif decision.primary_relation in {"same_topic", "unrelated"}:
            insert_review(store, decision.primary_relation, "item", item_id, decision.model_dump())
            stats["review"] += 1
            continue
        elif decision.primary_relation == "uncertain":
            insert_review(store, "uncertain_cluster_relation", "item", item_id, decision.model_dump())
            stats["review"] += 1
            continue
        else:
            target_cluster_id = decision.cluster_id or candidates[0]["cluster_id"]
        insert_cluster_item(
            store,
            target_cluster_id,
            item_id,
            primary_relation=decision.primary_relation,
            secondary_roles=decision.secondary_roles,
            same_event=decision.same_event,
            same_topic=decision.same_topic,
            follow_up_event=decision.follow_up_event,
            confidence=decision.confidence,
            incremental_value=decision.incremental_value,
            report_value=decision.report_value,
            should_update_cluster_card=decision.should_update_cluster_card,
            should_notify=decision.should_notify,
            new_facts=decision.new_facts,
            new_angles=decision.new_angles,
            reason=decision.reason,
            evidence=decision.evidence,
            decision_source="llm",
            llm_call_id=call_id,
            prompt_version=ITEM_CLUSTER_PROMPT_VERSION,
            model=client.model,
        )
        stats["attached"] += 1
        if patch_cards and decision.should_update_cluster_card:
            patch_cluster_card(
                store,
                target_cluster_id,
                live=live,
                model=model,
                max_calls=max_calls,
                token_budget=token_budget,
                global_call_limit=global_call_limit,
            )
    return {"ok": True, "stats": stats}


def cluster_decision_attach_eligible(decision: Any) -> bool:
    relation_type = getattr(decision, "cluster_relation_type", "") or ""
    disqualifying_types = {"same_topic_only", "same_product_different_event", "same_thread", "same_conference", "entity_overlap_only", "different", "uncertain"}
    if relation_type in disqualifying_types:
        return False
    if not bool(getattr(decision, "same_event", False)) and getattr(decision, "primary_relation", "") != "source_material":
        return False
    if getattr(decision, "primary_relation", "") == "source_material" and not bool(getattr(decision, "same_event", False)):
        return False
    if getattr(decision, "confidence", 0.0) < 0.75:
        return False
    if getattr(decision, "attach_eligible", False) and bool(getattr(decision, "same_event", False)):
        return True
    return decision.primary_relation in {"source_material", "repeat", "new_info", "analysis", "experience", "context"} and (
        bool(decision.same_event)
    )


def same_event_cluster_candidate(store: InboxStore, item: dict[str, Any], item_card: dict[str, Any], cluster: dict[str, Any]) -> bool:
    with store.connect() as conn:
        row = conn.execute(
            """
            SELECT ii.*, ic.*
            FROM cluster_items ci
            JOIN inbox_items ii ON ii.item_id = ci.item_id
            JOIN item_cards ic ON ic.item_id = ci.item_id AND ic.is_current = 1
            WHERE ci.cluster_id = ?
            ORDER BY ci.created_at ASC
            LIMIT 1
            """,
            (cluster["cluster_id"],),
        ).fetchone()
    if not row:
        return False
    representative = dict(row)
    assessment = assess_candidate(item, representative, item_card, representative)
    return (
        assessment.candidate_priority in {"must_run", "high"}
        and not assessment.suppressed
        and (
            assessment.event_signature_match
            or any("same_actor_product_action_72h" in evidence for evidence in assessment.same_event_evidence)
            or any(evidence == "high_title_similarity" for evidence in assessment.same_event_evidence)
        )
    )


def cluster_prompt_payload(store: InboxStore, cluster: dict[str, Any]) -> dict[str, Any]:
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT ic.*
            FROM cluster_items ci
            JOIN item_cards ic ON ic.item_id = ci.item_id AND ic.is_current = 1
            WHERE ci.cluster_id = ?
            ORDER BY ci.report_value DESC, ci.created_at ASC
            LIMIT 3
            """,
            (cluster["cluster_id"],),
        ).fetchall()
    return {
        "cluster_id": cluster["cluster_id"],
        "status": cluster["status"],
        "cluster_title": cluster["cluster_title"],
        "cluster_summary": cluster["cluster_summary"],
        "cluster_card": cluster.get("cluster_card"),
        "representative_item_cards": [card_public(dict(row)) for row in rows],
    }


def create_semantic_cluster(store: InboxStore, item: dict[str, Any], item_card: dict[str, Any], *, created_by: str) -> str:
    cluster_id = f"cluster_{uuid.uuid4().hex}"
    now = utc_now()
    title = item_card["event_hint"] or item_card["canonical_title"]
    summary = item_card["short_summary"]
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO event_clusters (
                cluster_id, cluster_title, cluster_summary, entities_json, representative_item_id,
                first_seen_at, last_seen_at, last_major_update_at, item_count, status,
                cluster_vector_json, embedding_model, created_by, confidence, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 'active', '[]', NULL, ?, 0.6, ?, ?)
            """,
            (
                cluster_id,
                truncate(title, 180),
                summary,
                item_card["entities_json"],
                item["item_id"],
                now,
                now,
                now,
                created_by,
                now,
                now,
            ),
        )
    return cluster_id


def insert_cluster_item(
    store: InboxStore,
    cluster_id: str,
    item_id: str,
    *,
    primary_relation: str,
    secondary_roles: list[str],
    same_event: bool,
    same_topic: bool,
    follow_up_event: bool,
    confidence: float,
    incremental_value: int,
    report_value: int,
    should_update_cluster_card: bool,
    should_notify: bool,
    new_facts: list[str],
    new_angles: list[str],
    reason: str,
    evidence: list[str],
    decision_source: str,
    llm_call_id: int | None,
    prompt_version: str | None,
    model: str | None,
) -> None:
    now = utc_now()
    fingerprint = db.input_fingerprint({"cluster_id": cluster_id, "item_id": item_id, "primary": primary_relation})
    with store.connect() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO cluster_items (
                cluster_id, item_id, primary_relation, secondary_roles_json, same_event, same_topic,
                follow_up_event, confidence, incremental_value, report_value, should_update_cluster_card,
                should_notify, new_facts_json, new_angles_json, reason, evidence_json, decision_source,
                llm_call_id, schema_version, prompt_version, model, input_fingerprint, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cluster_id,
                item_id,
                primary_relation,
                db.dumps(secondary_roles),
                int(same_event),
                int(same_topic),
                int(follow_up_event),
                confidence,
                incremental_value,
                report_value,
                int(should_update_cluster_card),
                int(should_notify),
                db.dumps(new_facts),
                db.dumps(new_angles),
                reason,
                db.dumps(evidence),
                decision_source,
                llm_call_id,
                SCHEMA_VERSION,
                prompt_version,
                model,
                fingerprint,
                now,
                now,
            ),
        )
        if same_event:
            conn.execute(
                """
                UPDATE inbox_items SET primary_cluster_id = ?, semantic_status = 'clustered',
                    last_semantic_at = ?, updated_at = ?
                WHERE item_id = ?
                """,
                (cluster_id, now, now, item_id),
            )
            conn.execute(
                """
                UPDATE event_clusters
                SET last_seen_at = ?, last_major_update_at = CASE WHEN ? THEN ? ELSE last_major_update_at END,
                    item_count = (SELECT COUNT(*) FROM cluster_items WHERE cluster_id = ?),
                    updated_at = ?
                WHERE cluster_id = ?
                """,
                (now, int(should_update_cluster_card), now, cluster_id, now, cluster_id),
            )
        write_source_signal(conn, store, cluster_id, item_id, primary_relation, incremental_value, report_value, llm_call_id, now)


def write_source_signal(conn, store: InboxStore, cluster_id: str, item_id: str, primary_relation: str, incremental_value: int, report_value: int, llm_call_id: int | None, now: str) -> None:
    item = db.get_item(store, item_id)
    if not item:
        return
    source_id = item.get("source_id") or item.get("feed_url") or item.get("source_name")
    if not source_id:
        return
    source_role = "source_material" if primary_relation == "source_material" else "reporter"
    conn.execute(
        """
        INSERT OR REPLACE INTO source_signals (
            source_id, item_id, cluster_id, originality_delta, duplicate_signal,
            near_duplicate_signal, new_event_signal, incremental_value, report_value,
            source_role, llm_call_id, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            source_id,
            item_id,
            cluster_id,
            1 if primary_relation in {"source_material", "new_info", "analysis", "experience"} else 0,
            int(primary_relation == "repeat"),
            0,
            int(primary_relation in {"source_material", "new_info"}),
            incremental_value,
            report_value,
            source_role,
            llm_call_id,
            now,
            now,
        ),
    )


def insert_cluster_relation(store: InboxStore, from_cluster_id: str, to_cluster_id: str, relation_type: str, confidence: float, reason: str, llm_call_id: int | None) -> None:
    now = utc_now()
    with store.connect() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO cluster_relations (
                from_cluster_id, to_cluster_id, relation_type, confidence, reason,
                decision_source, llm_call_id, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, 'llm', ?, ?, ?)
            """,
            (from_cluster_id, to_cluster_id, relation_type, confidence, reason, llm_call_id, now, now),
        )


def rebuild_cluster_card(store: InboxStore, cluster_id: str, *, live: bool = False, model: str | None = None, max_calls: int | None = None) -> dict[str, Any]:
    return patch_cluster_card(store, cluster_id, live=live, model=model, max_calls=max_calls, full_rebuild=True)


def patch_cluster_card(
    store: InboxStore,
    cluster_id: str,
    *,
    live: bool = False,
    model: str | None = None,
    max_calls: int | None = None,
    token_budget: int | None = None,
    global_call_limit: bool = False,
    full_rebuild: bool = False,
) -> dict[str, Any]:
    cluster = show_cluster(store, cluster_id)
    if not cluster:
        return {"ok": False, "error": "cluster_not_found"}
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT ic.*
            FROM cluster_items ci
            JOIN item_cards ic ON ic.item_id = ci.item_id AND ic.is_current = 1
            WHERE ci.cluster_id = ? AND (ci.should_update_cluster_card = 1 OR ?)
            ORDER BY ci.created_at DESC
            LIMIT 10
            """,
            (cluster_id, int(full_rebuild)),
        ).fetchall()
    item_cards = [card_public(dict(row)) for row in rows]
    client = SemanticLLMClient(
        store,
        live=live,
        model=model,
        max_calls=max_calls,
        token_budget=token_budget,
        global_call_limit=global_call_limit,
    )
    input_data = {
        "cluster": {
            "cluster_id": cluster_id,
            "cluster_title": cluster["cluster_title"],
            "cluster_summary": cluster["cluster_summary"],
            "first_seen_at": cluster["first_seen_at"],
        },
        "current_cluster_card": current_cluster_card(store, cluster_id),
        "new_item_cards": item_cards,
        "full_rebuild": full_rebuild,
    }
    output, call_id, _reason = client.call_json(
        task_type="cluster_card_patch",
        prompt_version=CLUSTER_CARD_PROMPT_VERSION,
        schema_version=SCHEMA_VERSION,
        input_data=input_data,
        output_model=ClusterCardData,
        max_tokens=1800,
        cluster_id=cluster_id,
    )
    if output:
        card = output
    else:
        card = ClusterCardData(
            cluster_id=cluster_id,
            cluster_title=cluster["cluster_title"],
            main_entities=cluster["entities"],
            core_facts=[cluster["cluster_summary"]],
            representative_items=[cluster["representative_item_id"]],
            first_seen_at=cluster["first_seen_at"],
            last_major_update_at=utc_now(),
            confidence=cluster.get("confidence") or 0.6,
        )
    row = insert_cluster_card(store, card, call_id=call_id if output else None, model=client.model if output else "heuristic")
    return {"ok": True, "cluster_card": row, "llm_call_id": call_id}


def insert_cluster_card(store: InboxStore, card: ClusterCardData, *, call_id: int | None, model: str | None) -> dict[str, Any]:
    now = utc_now()
    fingerprint = db.input_fingerprint(card.model_dump())
    with store.connect() as conn:
        conn.execute("UPDATE cluster_cards SET is_current = 0, updated_at = ? WHERE cluster_id = ?", (now, card.cluster_id))
        version = conn.execute(
            "SELECT COALESCE(MAX(card_version), 0) + 1 AS next_version FROM cluster_cards WHERE cluster_id = ?",
            (card.cluster_id,),
        ).fetchone()["next_version"]
        cur = conn.execute(
            """
            INSERT INTO cluster_cards (
                cluster_id, card_version, schema_version, prompt_version, model, input_fingerprint,
                cluster_title, event_type, main_entities_json, core_facts_json, known_angles_json,
                representative_items_json, source_items_json, open_questions_json, first_seen_at,
                last_major_update_at, confidence, llm_call_id, is_current, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (
                card.cluster_id,
                version,
                SCHEMA_VERSION,
                CLUSTER_CARD_PROMPT_VERSION,
                model,
                fingerprint,
                card.cluster_title,
                card.event_type,
                db.dumps(card.main_entities),
                db.dumps(card.core_facts),
                db.dumps(card.known_angles),
                db.dumps(card.representative_items),
                db.dumps(card.source_items),
                db.dumps(card.open_questions),
                card.first_seen_at,
                card.last_major_update_at or now,
                card.confidence,
                call_id,
                now,
                now,
            ),
        )
        conn.execute(
            "UPDATE event_clusters SET cluster_card_id = ?, cluster_title = ?, updated_at = ? WHERE cluster_id = ?",
            (cur.lastrowid, card.cluster_title, now, card.cluster_id),
        )
        row = conn.execute("SELECT * FROM cluster_cards WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


def update_cluster_statuses(store: InboxStore, *, now_dt: datetime | None = None) -> dict[str, Any]:
    now_dt = now_dt or datetime.now(timezone.utc)
    now = now_dt.isoformat()
    cooling_cutoff = (now_dt - timedelta(days=3)).isoformat()
    archived_cutoff = (now_dt - timedelta(days=30)).isoformat()
    with store.connect() as conn:
        cooling = conn.execute(
            """
            UPDATE event_clusters SET status = 'cooling', updated_at = ?
            WHERE status IN ('active', 'reopened') AND COALESCE(last_major_update_at, last_seen_at) < ?
            """,
            (now, cooling_cutoff),
        ).rowcount
        archived = conn.execute(
            """
            UPDATE event_clusters SET status = 'archived', updated_at = ?
            WHERE status = 'cooling' AND COALESCE(last_major_update_at, last_seen_at) < ?
            """,
            (now, archived_cutoff),
        ).rowcount
    return {"ok": True, "updated": {"cooling": cooling, "archived": archived}}
