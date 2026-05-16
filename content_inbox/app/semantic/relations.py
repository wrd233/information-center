from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.semantic import db
from app.semantic.cards import generate_item_cards
from app.semantic.llm_client import SemanticLLMClient
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
    roles: list[str] = []
    if new_item.get("url") and candidate_item.get("url") and normalize_url(new_item["url"]) == normalize_url(candidate_item["url"]):
        roles.append("same_url")
    if new_item.get("guid") and candidate_item.get("guid") and new_item["guid"] == candidate_item["guid"]:
        roles.append("same_guid")
    if roles:
        return "duplicate", roles
    if stable_hash((new_item.get("title") or "").strip().lower()) == stable_hash((candidate_item.get("title") or "").strip().lower()):
        return "near_duplicate", ["same_title_hash"]
    return None


def find_relation_candidates(store: InboxStore, item_id: str, max_candidates: int) -> list[dict[str, Any]]:
    new_card = db.get_current_item_card(store, item_id)
    if not new_card:
        return []
    cards = db.list_current_item_cards(store, exclude_item_id=item_id, limit=200)
    new_terms = set((new_card["canonical_title"] + " " + (new_card["event_hint"] or "")).lower().split())
    scored: list[tuple[int, dict[str, Any]]] = []
    for card in cards:
        terms = set((card["canonical_title"] + " " + (card["event_hint"] or "")).lower().split())
        score = len(new_terms & terms)
        try:
            score += len(set(json.loads(new_card["entities_json"] or "[]")) & set(json.loads(card["entities_json"] or "[]"))) * 2
        except Exception:
            pass
        if score > 0:
            scored.append((score, card))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [card for _score, card in scored[:max_candidates]]


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
    stats = {"selected": len(rows), "written": 0, "folded": 0, "review": 0, "llm_calls": 0}

    def process_one(row: Any) -> dict[str, int]:
        client = SemanticLLMClient(
            store,
            live=live,
            model=model,
            max_calls=max_calls,
            token_budget=token_budget,
            global_call_limit=global_call_limit,
        )
        local = {"written": 0, "folded": 0, "review": 0, "llm_calls": 0}
        item_id = row["item_id"]
        item = db.get_item(store, item_id)
        new_card = db.get_current_item_card(store, item_id)
        if not item or not new_card:
            return local
        candidates = find_relation_candidates(store, item_id, max_candidates)
        if not candidates:
            return local
        hard_written = False
        for candidate_card in candidates:
            candidate_item = db.get_item(store, candidate_card["item_id"])
            if not candidate_item:
                continue
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
                    evidence=roles,
                    decision_source="rule",
                    llm_call_id=None,
                    prompt_version=None,
                    model="rule",
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
            max_tokens=1400,
            item_id=item_id,
            source_id=item.get("source_id") or item.get("feed_url") or item.get("source_name"),
        )
        local["llm_calls"] = client.calls
        if not output:
            insert_review(store, "uncertain_relation", "item", item_id, {"reason": "LLM skipped or failed"})
            local["review"] += 1
            return local
        for relation in output.relations:
            insert_item_relation(
                store,
                item_id,
                relation.candidate_item_id,
                primary_relation=relation.primary_relation,
                secondary_roles=relation.secondary_roles,
                confidence=relation.confidence,
                canonical_item_id=relation.canonical_item_id,
                new_information=relation.new_information,
                reason=relation.reason,
                evidence=relation.evidence,
                decision_source="llm",
                llm_call_id=call_id,
                prompt_version=ITEM_RELATION_PROMPT_VERSION,
                model=client.model,
            )
            local["written"] += 1
            if item_relation_should_fold(relation.primary_relation):
                local["folded"] += 1
            if relation.primary_relation == "uncertain":
                insert_review(store, "uncertain_relation", "item", item_id, relation.model_dump())
                local["review"] += 1
        return local

    if concurrency > 1 and len(rows) > 1:
        with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
            futures = [executor.submit(process_one, row) for row in rows]
            for future in as_completed(futures):
                local = future.result()
                for key in ["written", "folded", "review", "llm_calls"]:
                    stats[key] += int(local[key])
    else:
        for row in rows:
            local = process_one(row)
            for key in ["written", "folded", "review", "llm_calls"]:
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
    with store.connect() as conn:
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
