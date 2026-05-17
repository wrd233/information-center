from __future__ import annotations

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

from app.semantic import db
from app.semantic.cards import generate_item_cards
from app.semantic.candidates import (
    CandidateAssessment,
    assess_candidate,
    deterministic_duplicate,
    normalize_relation_label,
    relation_cluster_eligible,
    relation_pair_key,
)
from app.semantic.config import PRIORITY_ORDER
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.relation_policy import default_reason_code
from app.semantic.schemas import (
    ITEM_RELATION_PROMPT_VERSION,
    SCHEMA_VERSION,
    ItemRelationOutput,
    item_relation_should_fold,
)
from app.storage import InboxStore
from app.utils import normalize_url, stable_hash, utc_now


def card_public(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": row["item_id"],
        "canonical_title": row["canonical_title"],
        "short_summary": row["short_summary"],
        "entities": json.loads(row["entities_json"] or "[]"),
        "event_hint": row["event_hint"],
        "content_role": row["content_role"],
        "confidence": row["confidence"],
    }


def hard_relation(new_item: dict[str, Any], candidate_item: dict[str, Any]) -> tuple[str, list[str]] | None:
    return deterministic_duplicate(new_item, candidate_item)


def normalized_entity_terms(values: list[str]) -> set[str]:
    terms: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        lowered = text.lower()
        terms.add(lowered)
        compact = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", lowered)
        if compact:
            terms.add(compact)
    return terms


def semantic_tokens(text: str) -> set[str]:
    raw = re.findall(r"[A-Za-z][A-Za-z0-9_.+-]{2,}|[\u4e00-\u9fff]{2,8}", text.lower())
    stop = {"the", "and", "with", "from", "that", "this", "for", "about", "after", "before", "using"}
    return {token for token in raw if token not in stop}


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def hours_apart(left: str | None, right: str | None) -> float | None:
    a = parse_time(left)
    b = parse_time(right)
    if not a or not b:
        return None
    return abs((a - b).total_seconds()) / 3600


def ensure_candidate_event_table(store: InboxStore) -> None:
    with store.connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic_candidate_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stage TEXT NOT NULL,
                item_a_id TEXT,
                item_b_id TEXT,
                relation_pair_key TEXT,
                candidate_priority TEXT,
                candidate_score REAL,
                candidate_score_components_json TEXT,
                candidate_suppression_reason TEXT,
                status TEXT NOT NULL,
                metadata_json TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def ensure_relation_conflict_table(store: InboxStore) -> None:
    with store.connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic_relation_conflicts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                relation_pair_key TEXT NOT NULL,
                existing_relation_id INTEGER,
                existing_primary_relation TEXT,
                attempted_primary_relation TEXT,
                item_a_id TEXT,
                item_b_id TEXT,
                reason TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def insert_candidate_event(
    store: InboxStore,
    *,
    stage: str,
    item_a_id: str | None,
    item_b_id: str | None,
    pair_key: str | None,
    assessment: CandidateAssessment | None,
    status: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    ensure_candidate_event_table(store)
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO semantic_candidate_events (
                stage, item_a_id, item_b_id, relation_pair_key, candidate_priority,
                candidate_score, candidate_score_components_json, candidate_suppression_reason,
                status, metadata_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                stage,
                item_a_id,
                item_b_id,
                pair_key,
                assessment.candidate_priority if assessment else None,
                assessment.candidate_score if assessment else None,
                db.dumps(assessment.candidate_score_components if assessment else {}),
                assessment.candidate_suppression_reason if assessment else None,
                status,
                db.dumps(metadata or {}),
                utc_now(),
            ),
        )


def find_relation_candidates(store: InboxStore, item_id: str, max_candidates: int, *, include_suppressed: bool = False) -> list[dict[str, Any]]:
    new_card = db.get_current_item_card(store, item_id)
    if not new_card:
        return []
    new_item = db.get_item(store, item_id) or {}
    cards = db.list_current_item_cards(store, exclude_item_id=item_id, limit=500)
    new_terms = semantic_tokens(
        f"{new_card['canonical_title']} {new_card.get('event_hint') or ''} {new_card.get('short_summary') or ''}"
    )
    new_entities = normalized_entity_terms(json.loads(new_card["entities_json"] or "[]"))
    scored: list[tuple[float, int, str, dict[str, Any]]] = []
    for card in cards:
        candidate_item = db.get_item(store, card["item_id"]) or {}
        terms = semantic_tokens(f"{card['canonical_title']} {card.get('event_hint') or ''} {card.get('short_summary') or ''}")
        score = float(len(new_terms & terms))
        try:
            score += len(new_entities & normalized_entity_terms(json.loads(card["entities_json"] or "[]"))) * 4
        except Exception:
            pass
        if (new_item.get("source_id") or "") != (candidate_item.get("source_id") or ""):
            score += 0.75
        gap = hours_apart(new_item.get("published_at") or new_item.get("created_at"), candidate_item.get("published_at") or candidate_item.get("created_at"))
        if gap is not None:
            if gap <= 24:
                score += 2
            elif gap <= 72:
                score += 1
        if normalize_url(new_item.get("url") or "") and normalize_url(new_item.get("url") or "") == normalize_url(candidate_item.get("url") or ""):
            score += 10
        assessment = assess_candidate(new_item, candidate_item, new_card, card)
        score = max(score, assessment.candidate_score)
        if score > 0 or include_suppressed:
            enriched = dict(card)
            enriched["_candidate_item"] = candidate_item
            enriched["_candidate_assessment"] = assessment
            enriched["_relation_pair_key"] = relation_pair_key(new_item, candidate_item)
            scored.append((score, PRIORITY_ORDER.get(assessment.candidate_priority, 0), card["created_at"], enriched))
    scored.sort(key=lambda pair: (pair[1], pair[0], pair[2]), reverse=True)
    if include_suppressed:
        return [card for _score, _priority, _created, card in scored[: max(max_candidates * 3, max_candidates)]]
    runnable = [card for _score, _priority, _created, card in scored if not card["_candidate_assessment"].suppressed]
    lows = [card for card in runnable if card["_candidate_assessment"].candidate_priority == "low"]
    non_lows = [card for card in runnable if card["_candidate_assessment"].candidate_priority != "low"]
    return (non_lows + lows[: max(1, max_candidates // 3)])[:max_candidates]


def process_item_relations(
    store: InboxStore,
    *,
    limit: int = 100,
    live: bool = False,
    max_candidates: int = 5,
    max_calls: int | None = None,
    model: str | None = None,
    token_budget: int | None = None,
    global_call_limit: bool = False,
    concurrency: int = 1,
) -> dict[str, Any]:
    generate_item_cards(store, limit=limit, live=False, force=False)
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT c.item_id
            FROM item_cards c
            LEFT JOIN item_relations r ON r.item_a_id = c.item_id
            WHERE c.is_current = 1 AND r.id IS NULL
            ORDER BY c.created_at ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    stats = {"selected": len(rows), "written": 0, "folded": 0, "review": 0, "llm_calls": 0, "candidate_pairs": 0, "no_candidate_items": 0, "llm_items": 0}
    ensure_candidate_event_table(store)
    seen_pair_keys: set[str] = set()
    seen_lock = threading.Lock()

    def process_one(row: Any) -> dict[str, int]:
        client = SemanticLLMClient(
            store,
            live=live,
            model=model,
            max_calls=max_calls,
            token_budget=token_budget,
            global_call_limit=global_call_limit,
        )
        local = {"written": 0, "folded": 0, "review": 0, "llm_calls": 0, "candidate_pairs": 0, "no_candidate_items": 0, "llm_items": 0}
        item_id = row["item_id"]
        item = db.get_item(store, item_id)
        new_card = db.get_current_item_card(store, item_id)
        if not item or not new_card:
            return local
        candidates_all = find_relation_candidates(store, item_id, max_candidates, include_suppressed=True)
        for candidate_card in candidates_all:
            assessment: CandidateAssessment = candidate_card["_candidate_assessment"]
            candidate_item = candidate_card.get("_candidate_item") or db.get_item(store, candidate_card["item_id"]) or {}
            insert_candidate_event(
                store,
                stage="item_relation",
                item_a_id=item_id,
                item_b_id=candidate_card["item_id"],
                pair_key=candidate_card.get("_relation_pair_key"),
                assessment=assessment,
                status="suppressed" if assessment.suppressed else "generated",
                metadata={
                    "candidate_generation_reason": "; ".join(assessment.same_event_evidence or assessment.disqualifiers),
                    "lane": assessment.lane,
                    "item_a_title": item.get("title"),
                    "item_b_title": candidate_item.get("title"),
                    **assessment.model_dump(),
                },
            )
        candidates = [candidate for candidate in candidates_all if not candidate["_candidate_assessment"].suppressed][:max_candidates]
        if not candidates:
            local["no_candidate_items"] += 1
            return local
        if all(candidate["_candidate_assessment"].candidate_priority == "low" for candidate in candidates):
            for candidate_card in candidates:
                insert_candidate_event(
                    store,
                    stage="item_relation",
                    item_a_id=item_id,
                    item_b_id=candidate_card["item_id"],
                    pair_key=candidate_card.get("_relation_pair_key"),
                    assessment=candidate_card.get("_candidate_assessment"),
                    status="skipped_low_priority_relation_set",
                    metadata={"reason": "all candidates were low priority; skipped LLM relation call"},
                )
            local["no_candidate_items"] += 1
            return local
        local["candidate_pairs"] += len(candidates)
        hard_written = False
        for candidate_card in candidates:
            candidate_item = db.get_item(store, candidate_card["item_id"])
            if not candidate_item:
                continue
            pair_key = candidate_card.get("_relation_pair_key") or relation_pair_key(item, candidate_item)
            with seen_lock:
                if pair_key in seen_pair_keys:
                    insert_candidate_event(
                        store,
                        stage="item_relation",
                        item_a_id=item_id,
                        item_b_id=candidate_card["item_id"],
                        pair_key=pair_key,
                        assessment=candidate_card.get("_candidate_assessment"),
                        status="duplicate_direction_suppressed",
                        metadata={"duplicate_of_relation_id": None},
                    )
                    continue
                seen_pair_keys.add(pair_key)
            hard = hard_relation(item, candidate_item)
            if hard:
                primary, roles = hard
                insert_item_relation(
                    store,
                    item_id,
                    candidate_card["item_id"],
                    primary_relation=primary,
                    secondary_roles=roles,
                    confidence=1.0,
                    canonical_item_id=candidate_card["item_id"],
                    new_information=[],
                    reason="deterministic duplicate rule matched",
                    evidence=roles + ["reason_code=deterministic_duplicate"],
                    decision_source="rule",
                    llm_call_id=None,
                    prompt_version=None,
                    model="rule",
                )
                assessment = candidate_card.get("_candidate_assessment")
                insert_candidate_event(
                    store,
                    stage="item_relation",
                    item_a_id=item_id,
                    item_b_id=candidate_card["item_id"],
                    pair_key=pair_key,
                    assessment=assessment,
                    status="rule_relation_written",
                    metadata={"primary_relation": primary, "event_relation_type": "same_event", "cluster_eligible": True},
                )
                local["written"] += 1
                local["folded"] += 1
                hard_written = True
                break
        if hard_written:
            return local
        input_data = {
            "new_item_card": card_public(new_card),
            "candidate_item_cards": [card_public(card) for card in candidates],
        }
        output, call_id, _reason = client.call_json(
            task_type="item_relation",
            prompt_version=ITEM_RELATION_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=ItemRelationOutput,
            max_tokens=2200,
            item_id=item_id,
            source_id=item.get("source_id") or item.get("feed_url") or item.get("source_name"),
            request_metadata={
                "prompt_variant": "full" if any(c["_candidate_assessment"].candidate_priority in {"must_run", "high"} for c in candidates) else "short",
                "candidate_priorities": [c["_candidate_assessment"].candidate_priority for c in candidates],
                "candidate_scores": [c["_candidate_assessment"].candidate_score for c in candidates],
                "candidate_lanes": [c["_candidate_assessment"].lane for c in candidates],
                "candidate_event_signature_keys": [c["_candidate_assessment"].event_signature_key for c in candidates],
                "candidate_positive_features": [c["_candidate_assessment"].positive_features for c in candidates],
                "candidate_negative_features": [c["_candidate_assessment"].negative_features for c in candidates],
                "candidate_time_window_hours": [c["_candidate_assessment"].time_window_hours for c in candidates],
            },
        )
        local["llm_calls"] = client.calls
        local["llm_items"] += 1
        if not output:
            insert_review(store, "uncertain_relation", "item", item_id, {"reason": "LLM skipped or failed"})
            local["review"] += 1
            return local
        for relation in output.relations:
            candidate_item = db.get_item(store, relation.candidate_item_id) or {}
            candidate_card = next((card for card in candidates if card["item_id"] == relation.candidate_item_id), None)
            assessment = candidate_card.get("_candidate_assessment") if candidate_card else assess_candidate(item, candidate_item, new_card, db.get_current_item_card(store, relation.candidate_item_id))
            primary_relation, event_relation_type, cluster_eligible, disqualifiers = normalize_relation_label(
                relation.primary_relation,
                assessment,
                reason=relation.reason,
                evidence=relation.evidence,
                new_information=relation.new_information,
            )
            insert_item_relation(
                store,
                item_id,
                relation.candidate_item_id,
                primary_relation=primary_relation,
                secondary_roles=relation.secondary_roles,
                confidence=relation.confidence,
                canonical_item_id=relation.canonical_item_id,
                new_information=relation.new_information,
                reason=relation.reason,
                evidence=relation.evidence
                + [f"event_relation_type={event_relation_type}", f"cluster_eligible={cluster_eligible}"]
                + [f"reason_code={relation.reason_code or default_reason_code(primary_relation, event_relation_type, generic_only=assessment.generic_only)}"]
                + [f"disqualifier={d}" for d in disqualifiers],
                decision_source="llm",
                llm_call_id=call_id,
                prompt_version=ITEM_RELATION_PROMPT_VERSION,
                model=client.model,
            )
            insert_candidate_event(
                store,
                stage="item_relation",
                item_a_id=item_id,
                item_b_id=relation.candidate_item_id,
                pair_key=relation_pair_key(item, candidate_item) if candidate_item else None,
                assessment=assessment,
                status="llm_relation_written",
                metadata={
                    "primary_relation": primary_relation,
                    "raw_primary_relation": relation.primary_relation,
                    "event_relation_type": event_relation_type,
                    "cluster_eligible": cluster_eligible,
                    "reason_code": relation.reason_code or default_reason_code(primary_relation, event_relation_type, generic_only=assessment.generic_only),
                    "disqualifiers": disqualifiers,
                    "same_event_evidence": relation.same_event_evidence or assessment.same_event_evidence,
                    "new_info_evidence": relation.new_info_evidence or relation.new_information,
                },
            )
            local["written"] += 1
            if item_relation_should_fold(primary_relation):
                local["folded"] += 1
            if primary_relation == "uncertain":
                insert_review(store, "uncertain_relation", "item", item_id, relation.model_dump())
                local["review"] += 1
        return local

    if concurrency > 1 and len(rows) > 1:
        with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
            futures = [executor.submit(process_one, row) for row in rows]
            for future in as_completed(futures):
                local = future.result()
                for key in ["written", "folded", "review", "llm_calls", "candidate_pairs", "no_candidate_items", "llm_items"]:
                    stats[key] += int(local[key])
    else:
        for row in rows:
            local = process_one(row)
            for key in ["written", "folded", "review", "llm_calls", "candidate_pairs", "no_candidate_items", "llm_items"]:
                stats[key] += int(local[key])
    return {"ok": True, "stats": stats}


def insert_item_relation(
    store: InboxStore,
    item_a_id: str,
    item_b_id: str,
    *,
    primary_relation: str,
    secondary_roles: list[str],
    confidence: float,
    canonical_item_id: str | None,
    new_information: list[str],
    reason: str,
    evidence: list[str],
    decision_source: str,
    llm_call_id: int | None,
    prompt_version: str | None,
    model: str | None,
) -> None:
    now = utc_now()
    fingerprint = db.input_fingerprint({"a": item_a_id, "b": item_b_id, "primary": primary_relation, "roles": secondary_roles})
    should_fold = item_relation_should_fold(primary_relation)
    ensure_relation_conflict_table(store)
    left_item = db.get_item(store, item_a_id) or {"item_id": item_a_id}
    right_item = db.get_item(store, item_b_id) or {"item_id": item_b_id}
    pair_key = relation_pair_key(left_item, right_item)
    with store.connect() as conn:
        existing_rows = conn.execute("SELECT * FROM item_relations").fetchall()
        for existing in existing_rows:
            existing_left = db.get_item(store, existing["item_a_id"]) or {"item_id": existing["item_a_id"]}
            existing_right = db.get_item(store, existing["item_b_id"]) or {"item_id": existing["item_b_id"]}
            if relation_pair_key(existing_left, existing_right) != pair_key:
                continue
            if existing["primary_relation"] != primary_relation:
                conn.execute(
                    """
                    INSERT INTO semantic_relation_conflicts (
                        relation_pair_key, existing_relation_id, existing_primary_relation,
                        attempted_primary_relation, item_a_id, item_b_id, reason, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        pair_key,
                        existing["id"],
                        existing["primary_relation"],
                        primary_relation,
                        item_a_id,
                        item_b_id,
                        "conflicting canonical pair verdict",
                        now,
                    ),
                )
                return
            return
        conn.execute(
            """
            INSERT OR IGNORE INTO item_relations (
                item_a_id, item_b_id, primary_relation, secondary_roles_json, confidence,
                should_fold, canonical_item_id, new_information_json, reason, evidence_json,
                decision_source, llm_call_id, schema_version, prompt_version, model,
                input_fingerprint, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_a_id,
                item_b_id,
                primary_relation,
                db.dumps(secondary_roles),
                confidence,
                int(should_fold),
                canonical_item_id,
                db.dumps(new_information),
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
        if should_fold:
            conn.execute(
                """
                UPDATE inbox_items
                SET semantic_status = 'folded', last_semantic_at = ?, updated_at = ?
                WHERE item_id = ?
                """,
                (now, now, item_a_id),
            )


def insert_review(store: InboxStore, review_type: str, target_type: str, target_id: str, suggestion: dict[str, Any]) -> int:
    now = utc_now()
    with store.connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO review_queue (review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at)
            VALUES (?, ?, ?, 'pending', ?, ?, ?, ?)
            """,
            (review_type, target_type, target_id, db.dumps(suggestion), str(suggestion.get("reason", "")), now, now),
        )
    return int(cur.lastrowid)
