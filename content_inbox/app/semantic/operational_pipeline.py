from __future__ import annotations

import json
import re
from typing import Any

from app.semantic.candidates import assess_candidate, deterministic_duplicate
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.schemas import ITEM_RELATION_PROMPT_VERSION, ItemRelationOutput
from app.semantic.signatures import EventSignature, extract_event_signature
from app.storage import InboxStore
from app.utils import normalize_url, stable_hash, utc_now


SCHEMA_VERSION = "operational_v3"
CREATED_BY = "operational_v3_rule"
HARD_NEGATIVE_DISQUALIFIERS = {
    "generic_entity_overlap",
    "generic_only_overlap",
    "same_account_boilerplate",
    "wide_time_window",
    "semantic_level_reject",
    "proxy_domain_only",
}


def normalized_title(value: str) -> str:
    return re.sub(r"\W+", " ", (value or "").lower()).strip()[:80] or "untitled"


def extract_terms(text: str) -> list[str]:
    words = re.findall(r"\b[A-Z][A-Za-z0-9][A-Za-z0-9_.-]{1,}\b", text or "")
    keywords = re.findall(r"\b(ai|openai|model|agent|security|funding|launch|release|policy|china|market)\b", (text or "").lower())
    terms = list(dict.fromkeys(words[:6] + [kw.title() for kw in keywords[:6]]))
    return terms[:8]


EVENTNESS_NON_EVENT_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("ad", ("sponsored", "advertisement", "promo code", "limited offer", "成人", "广告", "优惠券")),
    ("digest", ("digest", "newsletter", "roundup", "weekly recap", "daily briefing", "market wrap", "日报", "周报", "简报", "综述", "汇总")),
    ("content", ("how to", "tutorial", "guide", "case study", "opinion", "analysis:", "教程", "指南", "如何", "观点", "案例")),
)


def _json_loads(value: Any, fallback: Any) -> Any:
    if value in (None, ""):
        return fallback
    try:
        return json.loads(str(value))
    except Exception:
        return fallback


def classify_item_eventness(row: dict[str, Any], signature: EventSignature | None = None) -> dict[str, Any]:
    title = row.get("title") or ""
    summary = row.get("summary") or ""
    text = f"{title}\n{summary}".strip()
    lowered = text.lower()
    negative_features: list[str] = []

    if not re.sub(r"https?://\S+", "", lowered).strip():
        return {"decision": "low_signal", "confidence": 0.95, "reasons": ["pure_link_or_empty"], "negative_features": ["pure_link_or_empty"]}
    if len(re.findall(r"[A-Za-z0-9\u4e00-\u9fff]", title)) < 8:
        return {"decision": "low_signal", "confidence": 0.9, "reasons": ["short_or_symbolic_title"], "negative_features": ["short_or_symbolic_title"]}

    for decision, needles in EVENTNESS_NON_EVENT_PATTERNS:
        hits = [needle for needle in needles if needle in lowered]
        if hits:
            negative_features.extend(hits)
            return {"decision": decision, "confidence": 0.88 if decision == "content" else 0.93, "reasons": [f"{decision}_keyword"], "negative_features": negative_features}

    signature = signature or extract_event_signature(row)
    if signature.semantic_level == "event_signature" and signature.is_concrete:
        return {"decision": "event", "confidence": max(0.9, signature.confidence), "reasons": ["concrete_event_signature"], "negative_features": negative_features}
    if signature.semantic_level == "thread_signature":
        return {"decision": "thread", "confidence": max(0.62, signature.confidence), "reasons": ["thread_signature"], "negative_features": signature.invalid_reasons}
    if signature.semantic_level == "content_signature":
        return {"decision": "content", "confidence": max(0.7, signature.confidence), "reasons": ["content_signature"], "negative_features": signature.invalid_reasons}
    return {"decision": "unknown", "confidence": 0.55, "reasons": ["no_concrete_event_signature"], "negative_features": signature.invalid_reasons}


def _source_variants_from_raw(*values: Any) -> dict[str, list[str]]:
    urls: list[str] = []
    canonical_urls: list[str] = []
    guids: list[str] = []
    source_ids: list[str] = []
    for value in values:
        raw = _json_loads(value, {})
        if not isinstance(raw, dict):
            continue
        for key in ("url", "link"):
            if raw.get(key):
                urls.append(str(raw[key]))
                normalized = normalize_url(str(raw[key]))
                if normalized:
                    canonical_urls.append(normalized)
        if raw.get("guid"):
            guids.append(str(raw["guid"]))
        if raw.get("source_id"):
            source_ids.append(str(raw["source_id"]))
    return {
        "url_variants": sorted(set(urls))[:10],
        "canonical_url_variants": sorted(set(canonical_urls))[:10],
        "guid_variants": sorted(set(guids))[:10],
        "source_ids": sorted(set(source_ids))[:10],
    }


def _dedupe_method(row: dict[str, Any]) -> str:
    key = row.get("dedupe_key") or ""
    if key.startswith("url:"):
        return "url"
    if key.startswith("guid:"):
        return "guid"
    if "title_date" in key:
        return "title_date"
    if "content" in key:
        return "title_content"
    return "dedupe_key"


def _insert_review(conn: Any, review_type: str, target_type: str, target_id: str, suggestion: dict[str, Any], reason: str, now: str) -> None:
    conn.execute(
        "INSERT INTO review_queue(review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (review_type, target_type, target_id, "pending", json.dumps(suggestion, ensure_ascii=False), reason, now, now),
    )


def _write_source_signal(
    conn: Any,
    item: dict[str, Any],
    *,
    cluster_id: str | None = None,
    discovery_value: int = 0,
    fact_value: int = 0,
    incremental_value: int = 0,
    interpretation_value: int = 0,
    duplicate_noise: int = 0,
    non_event_noise: int = 0,
    report_value: int = 0,
    source_role: str = "unknown",
    now: str,
) -> None:
    source_id = item.get("source_id") or item.get("feed_url") or item.get("source_name")
    if not source_id:
        return
    conn.execute(
        """
        INSERT OR REPLACE INTO source_signals(
            source_id, item_id, cluster_id, discovery_value, fact_value, originality_delta,
            duplicate_signal, near_duplicate_signal, new_event_signal, incremental_value,
            interpretation_value, duplicate_noise, non_event_noise, report_value,
            source_role, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            source_id,
            item["item_id"],
            cluster_id,
            discovery_value,
            fact_value,
            1 if discovery_value or fact_value or incremental_value or interpretation_value else 0,
            1 if duplicate_noise else 0,
            0,
            1 if discovery_value else 0,
            incremental_value,
            interpretation_value,
            duplicate_noise,
            non_event_noise,
            report_value,
            source_role,
            now,
            now,
        ),
    )


def _insert_semantic_extraction(conn: Any, row: dict[str, Any], now: str, eventness: dict[str, Any], signature: EventSignature) -> None:
    item_id = row["item_id"]
    title = row["title"]
    body = f"{title}\n{row['summary'] or ''}"
    terms = extract_terms(body)
    extraction_id = f"se_{stable_hash(item_id)[:16]}"
    normalized = {
        "entities": terms,
        "topics": [row["source_category"] or "General"],
        "claims": [title] if title else [],
        "eventness": eventness,
        "signature": signature.model_dump(),
        "schema_version": SCHEMA_VERSION,
        "created_by": CREATED_BY,
        "input_fingerprint": stable_hash(json.dumps({"item_id": item_id, "eventness": eventness, "signature": signature.model_dump()}, ensure_ascii=False, sort_keys=True)),
    }
    conn.execute(
        "INSERT OR REPLACE INTO semantic_extractions(extraction_id, item_id, processor, confidence, needs_review, raw_output_json, normalized_output_json, evidence_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            extraction_id,
            item_id,
            SCHEMA_VERSION,
            "high" if eventness["decision"] == "event" else "medium",
            0 if eventness["decision"] == "event" and signature.is_concrete else 1,
            json.dumps({"title": title}, ensure_ascii=False),
            json.dumps(normalized, ensure_ascii=False),
            json.dumps({"eventness": eventness, "signature_invalid_reasons": signature.invalid_reasons, "schema_version": SCHEMA_VERSION, "created_by": CREATED_BY}, ensure_ascii=False),
            now,
        ),
    )
    for term in terms:
        entity_id = "ent_" + stable_hash(term.lower())[:16]
        conn.execute(
            "INSERT OR IGNORE INTO entities(entity_id, entity_name, entity_type, confidence, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (entity_id, term, "keyword", 0.45, now, now),
        )
        conn.execute(
            "INSERT OR IGNORE INTO item_entities(item_id, entity_id, confidence, evidence_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (item_id, entity_id, 0.45, json.dumps([{"title": title, "schema_version": SCHEMA_VERSION}], ensure_ascii=False), now),
        )
    topic_name = row["source_category"] or "General"
    topic_id = "topic_" + stable_hash(topic_name.lower())[:16]
    conn.execute(
        "INSERT OR IGNORE INTO topics(topic_id, topic_name, topic_summary, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (topic_id, topic_name, f"Items categorized as {topic_name}", now, now),
    )
    conn.execute("INSERT OR IGNORE INTO topic_items(topic_id, item_id, confidence, created_at) VALUES (?, ?, ?, ?)", (topic_id, item_id, 0.5, now))


def _event_title(signature: EventSignature, representative: dict[str, Any]) -> str:
    if signature.actor and signature.product_or_model and signature.action != "other":
        return f"{signature.actor} {signature.action.replace('_', ' ')} {signature.product_or_model}"
    return representative["title"]


def _event_summary(signature: EventSignature, members: list[dict[str, Any]]) -> str:
    representative = members[0]
    if signature.actor and signature.product_or_model and signature.action != "other":
        return f"{signature.actor} {signature.action.replace('_', ' ')} {signature.product_or_model}; supported by {len(members)} item(s)."
    return representative.get("summary") or representative["title"]


def _relation_from_candidate(left: dict[str, Any], right: dict[str, Any], assessment: Any) -> tuple[str, int, int, int, str]:
    hard = deterministic_duplicate(left, right)
    if hard:
        relation = "item_duplicate" if hard[0] == "duplicate" else "near_duplicate"
        return relation, 1, 1, 0, "deterministic_duplicate"
    if assessment.candidate_priority in {"must_run", "high"} and not set(assessment.disqualifiers) & {"generic_entity_overlap", "generic_only_overlap", "same_account_boilerplate", "wide_time_window", "semantic_level_reject"}:
        return "same_event_repeat", 1, 1, 0, "high_confidence_same_event"
    if assessment.candidate_priority == "medium":
        return "uncertain", 0, 1, 1, "medium_candidate_requires_review"
    if assessment.candidate_priority == "suppress":
        return "non_event" if "semantic_level_reject" in assessment.disqualifiers else "different", 0, 0, 0, assessment.candidate_suppression_reason or "suppressed_candidate"
    return "same_topic_different_event", 0, 1, 1, "low_confidence_same_topic"


def _candidate_fingerprint(run_id: str, left_id: str, right_id: str | None, assessment: Any, status: str) -> str:
    return stable_hash(json.dumps({"run_id": run_id, "left": left_id, "right": right_id, "assessment": assessment.model_dump(), "status": status}, ensure_ascii=False, sort_keys=True))


def candidate_hard_negative(assessment: Any) -> bool:
    return bool(
        getattr(assessment, "suppressed", False)
        or assessment.candidate_priority == "suppress"
        or (set(assessment.disqualifiers) & HARD_NEGATIVE_DISQUALIFIERS)
    )


def adjudicate_candidate_with_llm(
    store: InboxStore,
    *,
    run_id: str,
    left: dict[str, Any],
    right: dict[str, Any],
    assessment: Any,
    live: bool = False,
    model: str | None = None,
    max_calls: int | None = None,
    client: SemanticLLMClient | None = None,
) -> dict[str, Any]:
    """Return an auditable LLM recommendation without applying an auto-merge."""
    if candidate_hard_negative(assessment):
        return {
            "status": "skipped_hard_negative",
            "decision_source": "rule",
            "llm_call_id": None,
            "should_auto_merge": False,
            "reason": "hard negative candidate is not eligible for LLM adjudication",
            "disqualifiers": list(assessment.disqualifiers),
        }
    if assessment.candidate_priority not in {"medium", "high"} and assessment.lane not in {"same_event_recall", "same_actor_product", "exploratory_recall"}:
        return {
            "status": "skipped_not_gated",
            "decision_source": "rule",
            "llm_call_id": None,
            "should_auto_merge": False,
            "reason": "candidate is outside operational LLM relation gates",
            "disqualifiers": list(assessment.disqualifiers),
        }

    llm = client or SemanticLLMClient(store, live=live, model=model, max_calls=max_calls)
    input_data = {
        "new_item_card": {
            "item_id": left["item_id"],
            "title": left.get("title"),
            "summary": left.get("summary"),
            "published_at": left.get("published_at"),
        },
        "candidate_item_cards": [
            {
                "item_id": right["item_id"],
                "title": right.get("title"),
                "summary": right.get("summary"),
                "published_at": right.get("published_at"),
                "candidate_priority": assessment.candidate_priority,
                "lane": assessment.lane,
                "positive_features": assessment.positive_features,
                "negative_features": assessment.negative_features,
                "disqualifiers": assessment.disqualifiers,
            }
        ],
        "policy": {
            "do_not_auto_merge": True,
            "hard_negatives_already_filtered": True,
            "medium_or_uncertain_requires_review_apply": True,
        },
    }
    output, call_id, reason = llm.call_json(
        task_type="operational_relation",
        prompt_version=ITEM_RELATION_PROMPT_VERSION,
        schema_version=SCHEMA_VERSION,
        input_data=input_data,
        output_model=ItemRelationOutput,
        max_tokens=1200,
        item_id=left["item_id"],
        source_id=left.get("source_id") or left.get("feed_url") or left.get("source_name"),
        request_metadata={
            "run_id": run_id,
            "candidate_priority": assessment.candidate_priority,
            "candidate_lane": assessment.lane,
            "created_by": CREATED_BY,
        },
    )
    if not output:
        return {
            "status": "llm_failed_review_required",
            "decision_source": "llm",
            "llm_call_id": call_id,
            "should_auto_merge": False,
            "reason": reason,
            "disqualifiers": list(assessment.disqualifiers),
        }
    relation = next((rel for rel in output.relations if rel.candidate_item_id == right["item_id"]), output.relations[0] if output.relations else None)
    if relation is None:
        return {
            "status": "llm_empty_review_required",
            "decision_source": "llm",
            "llm_call_id": call_id,
            "should_auto_merge": False,
            "reason": "LLM returned no relation decisions",
            "disqualifiers": list(assessment.disqualifiers),
        }
    return {
        "status": "llm_review_recommended",
        "decision_source": "llm",
        "llm_call_id": call_id,
        "should_auto_merge": False,
        "relation": relation.model_dump(),
        "reason": relation.reason,
        "confidence": relation.confidence,
        "positive_features": relation.same_event_evidence or relation.evidence,
        "negative_features": relation.disqualifiers,
        "disqualifiers": list(assessment.disqualifiers) + list(relation.disqualifiers),
    }


def generate_information_objects(
    store: InboxStore,
    run_id: str,
    item_ids: list[str],
    *,
    live_relation_llm: bool = False,
    relation_llm_model: str | None = None,
    relation_llm_max_calls: int | None = None,
) -> dict[str, Any]:
    if not item_ids:
        return {"item_count": 0}
    now = utc_now()
    stats = {
        "item_count": 0,
        "schema_version": SCHEMA_VERSION,
        "created_by": CREATED_BY,
        "eventness": {},
        "signature": {"event_signature": 0, "thread_signature": 0, "content_signature": 0, "reject": 0, "invalid": 0},
        "candidates_by_priority": {},
        "candidates_by_lane": {},
        "disqualifiers_by_reason": {},
        "alias_hit_count": 0,
        "auto_merged": 0,
        "review_required": 0,
        "rejected_non_event": 0,
        "clusters_created_or_updated": 0,
        "events_created_or_updated": 0,
        "llm_calls": 0,
    }
    with store.connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM inbox_items WHERE item_id IN ({','.join('?' for _ in item_ids)})",
            item_ids,
        ).fetchall()
        stats["item_count"] = len(rows)
        enriched: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            signature = extract_event_signature(item)
            eventness = classify_item_eventness(item, signature)
            stats["eventness"][eventness["decision"]] = stats["eventness"].get(eventness["decision"], 0) + 1
            stats["signature"][signature.semantic_level] = stats["signature"].get(signature.semantic_level, 0) + 1
            if signature.invalid_reasons:
                stats["signature"]["invalid"] += 1
            stats["alias_hit_count"] += len(signature.alias_hits)
            _insert_semantic_extraction(conn, item, now, eventness, signature)
            enriched.append({"item": item, "signature": signature, "eventness": eventness})
            if eventness["decision"] != "event":
                stats["rejected_non_event"] += 1
                _write_source_signal(conn, item, non_event_noise=1, source_role="non_event", now=now)
                _insert_review(
                    conn,
                    "eventness_review",
                    "item",
                    item["item_id"],
                    {
                        "eventness": eventness,
                        "signature": signature.model_dump(),
                        "action": "review_item_eventness",
                        "run_id": run_id,
                        "schema_version": SCHEMA_VERSION,
                        "created_by": CREATED_BY,
                        "input_fingerprint": stable_hash(json.dumps({"run_id": run_id, "item_id": item["item_id"], "eventness": eventness}, ensure_ascii=False, sort_keys=True)),
                    },
                    "Item did not pass eventness gate; it will not be materialized as an event automatically.",
                    now,
                )

        event_like = [entry for entry in enriched if entry["eventness"]["decision"] == "event" and entry["signature"].is_concrete]
        parent = {entry["item"]["item_id"]: entry["item"]["item_id"] for entry in event_like}

        def find(item_id: str) -> str:
            while parent[item_id] != item_id:
                parent[item_id] = parent[parent[item_id]]
                item_id = parent[item_id]
            return item_id

        def union(left: str, right: str) -> None:
            root_left = find(left)
            root_right = find(right)
            if root_left != root_right:
                parent[root_right] = root_left

        relation_rows: list[dict[str, Any]] = []
        for idx, left_entry in enumerate(event_like):
            for right_entry in event_like[idx + 1 :]:
                left = left_entry["item"]
                right = right_entry["item"]
                assessment = assess_candidate(left, right)
                stats["candidates_by_priority"][assessment.candidate_priority] = stats["candidates_by_priority"].get(assessment.candidate_priority, 0) + 1
                stats["candidates_by_lane"][assessment.lane] = stats["candidates_by_lane"].get(assessment.lane, 0) + 1
                for disqualifier in assessment.disqualifiers:
                    stats["disqualifiers_by_reason"][disqualifier] = stats["disqualifiers_by_reason"].get(disqualifier, 0) + 1
                relation_type, same_event, same_topic, review_required, reason = _relation_from_candidate(left, right, assessment)
                status = "auto_merge" if same_event and relation_type in {"same_event_repeat", "same_event_new_info", "near_duplicate", "item_duplicate"} else ("review" if review_required else "rejected")
                candidate_fp = _candidate_fingerprint(run_id, left["item_id"], right["item_id"], assessment, status)
                conn.execute(
                    """
                    INSERT INTO event_candidate_pairs(
                        run_id, item_a_id, item_b_id, candidate_score, candidate_priority, lane,
                        relation_type, decision_source, confidence, reason_code,
                        features_json, positive_features_json, negative_features_json, disqualifiers_json,
                        schema_version, created_by, input_fingerprint, status, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'rule', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        left["item_id"],
                        right["item_id"],
                        assessment.candidate_score,
                        assessment.candidate_priority,
                        assessment.lane,
                        relation_type,
                        min(1.0, max(0.0, float(assessment.candidate_score) / 6.0)),
                        assessment.reason_code or reason,
                        json.dumps(assessment.model_dump(), ensure_ascii=False),
                        json.dumps(assessment.positive_features, ensure_ascii=False),
                        json.dumps(assessment.negative_features, ensure_ascii=False),
                        json.dumps(assessment.disqualifiers, ensure_ascii=False),
                        SCHEMA_VERSION,
                        CREATED_BY,
                        candidate_fp,
                        status,
                        now,
                    ),
                )
                relation_rows.append({"left": left, "right": right, "assessment": assessment, "relation_type": relation_type, "same_event": same_event, "same_topic": same_topic, "review_required": review_required, "reason": reason})
                if same_event:
                    union(left["item_id"], right["item_id"])
                    stats["auto_merged"] += 1
                elif review_required:
                    llm_suggestion: dict[str, Any] | None = None
                    if live_relation_llm and assessment.candidate_priority in {"medium", "high"}:
                        llm_suggestion = adjudicate_candidate_with_llm(
                            store,
                            run_id=run_id,
                            left=left,
                            right=right,
                            assessment=assessment,
                            live=True,
                            model=relation_llm_model,
                            max_calls=relation_llm_max_calls,
                        )
                        stats["llm_calls"] += 1 if llm_suggestion.get("llm_call_id") else 0
                        conn.execute(
                            """
                            UPDATE event_candidate_pairs
                            SET status = ?, decision_source = ?, llm_call_id = ?, confidence = COALESCE(?, confidence),
                                positive_features_json = ?, negative_features_json = ?, disqualifiers_json = ?
                            WHERE input_fingerprint = ?
                            """,
                            (
                                llm_suggestion["status"],
                                llm_suggestion["decision_source"],
                                llm_suggestion.get("llm_call_id"),
                                llm_suggestion.get("confidence"),
                                json.dumps(llm_suggestion.get("positive_features", []), ensure_ascii=False),
                                json.dumps(llm_suggestion.get("negative_features", []), ensure_ascii=False),
                                json.dumps(llm_suggestion.get("disqualifiers", assessment.disqualifiers), ensure_ascii=False),
                                candidate_fp,
                            ),
                        )
                    stats["review_required"] += 1
                    _insert_review(
                        conn,
                        "event_relation_review",
                        "item_pair",
                        f"{left['item_id']}:{right['item_id']}",
                        {
                            "relation_type": relation_type,
                            "candidate": assessment.model_dump(),
                            "action": "review_relation",
                            "run_id": run_id,
                            "schema_version": SCHEMA_VERSION,
                            "created_by": CREATED_BY,
                            "input_fingerprint": _candidate_fingerprint(run_id, left["item_id"], right["item_id"], assessment, "review"),
                            "llm_suggestion": llm_suggestion,
                        },
                        reason,
                        now,
                    )

        groups: dict[str, list[dict[str, Any]]] = {}
        for entry in event_like:
            groups.setdefault(find(entry["item"]["item_id"]), []).append(entry)

        for root, members in groups.items():
            representative_entry = max(members, key=lambda entry: (entry["signature"].confidence, len(entry["item"].get("summary") or ""), entry["item"]["title"]))
            signature = representative_entry["signature"]
            member_items = [entry["item"] for entry in members]
            cluster_key = signature.signature_key or root
            cluster_id = "cluster_" + stable_hash(f"{SCHEMA_VERSION}:{cluster_key}")[:16]
            input_fingerprint = stable_hash(json.dumps({"cluster_id": cluster_id, "members": sorted(entry["item"]["item_id"] for entry in members), "signature": signature.model_dump()}, ensure_ascii=False, sort_keys=True))
            evidence = {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "created_by": CREATED_BY,
                "input_fingerprint": input_fingerprint,
                "signature": signature.model_dump(),
                "eventness": [entry["eventness"] for entry in members],
                "member_item_ids": [entry["item"]["item_id"] for entry in members],
                "decision_source": "rule",
            }
            conn.execute(
                """
                INSERT OR REPLACE INTO event_clusters(cluster_id, cluster_title, cluster_summary, entities_json, representative_item_id, first_seen_at, last_seen_at, item_count, status, created_by, confidence, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cluster_id,
                    _event_title(signature, representative_entry["item"]),
                    _event_summary(signature, member_items),
                    json.dumps({"actor": signature.actor, "product": signature.product_or_model, "action": signature.action, "signature_key": signature.signature_key}, ensure_ascii=False),
                    representative_entry["item"]["item_id"],
                    min((entry["item"].get("published_at") or now) for entry in members),
                    max((entry["item"].get("published_at") or now) for entry in members),
                    len(members),
                    "active" if len(members) > 1 else "needs_review",
                    CREATED_BY,
                    min(0.98, max(0.72, signature.confidence if len(members) == 1 else signature.confidence + 0.05)),
                    now,
                    now,
                ),
            )
            for member in members:
                item = member["item"]
                item_relation = "source_material" if item["item_id"] == representative_entry["item"]["item_id"] else "same_event_repeat"
                relation = next((row for row in relation_rows if item["item_id"] in {row["left"]["item_id"], row["right"]["item_id"]} and row["same_event"]), None)
                if relation:
                    item_relation = relation["relation_type"]
                discovery_value = 1 if item["item_id"] == representative_entry["item"]["item_id"] else 0
                fact_value = 1 if item["item_id"] == representative_entry["item"]["item_id"] else 0
                incremental_value = 2 if item_relation in {"same_event_new_info", "related_with_new_info"} else 0
                duplicate_noise = 1 if item_relation in {"same_event_repeat", "near_duplicate", "item_duplicate"} else 0
                item_evidence = {
                    "schema_version": SCHEMA_VERSION,
                    "run_id": run_id,
                    "created_by": CREATED_BY,
                    "input_fingerprint": stable_hash(cluster_id + item["item_id"] + json.dumps(member["signature"].model_dump(), sort_keys=True)),
                    "signature": member["signature"].model_dump(),
                    "eventness": member["eventness"],
                    "cluster_evidence": evidence,
                }
                conn.execute(
                    """
                    INSERT OR REPLACE INTO cluster_items(cluster_id, item_id, primary_relation, same_event, same_topic, confidence, reason, evidence_json, decision_source, schema_version, input_fingerprint, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cluster_id,
                        item["item_id"],
                        item_relation,
                        1,
                        1,
                        member["signature"].confidence,
                        "High-confidence event signature/relation materialization.",
                        json.dumps(item_evidence, ensure_ascii=False),
                        "rule",
                        SCHEMA_VERSION,
                        item_evidence["input_fingerprint"],
                        now,
                        now,
                    ),
                )
                _write_source_signal(
                    conn,
                    item,
                    cluster_id=cluster_id,
                    discovery_value=discovery_value,
                    fact_value=fact_value,
                    incremental_value=incremental_value,
                    duplicate_noise=duplicate_noise,
                    report_value=3 if discovery_value or incremental_value else 1,
                    source_role="source_material" if discovery_value else "reporter",
                    now=now,
                )
                conn.execute("UPDATE inbox_items SET primary_cluster_id = ? WHERE item_id = ?", (cluster_id, item["item_id"]))
            event_id = "event_" + stable_hash(cluster_id)[:16]
            relation_summary: dict[str, int] = {}
            for member in members:
                relation = "source_material" if member["item"]["item_id"] == representative_entry["item"]["item_id"] else "same_event_repeat"
                relation_summary[relation] = relation_summary.get(relation, 0) + 1
            event_evidence = {
                **evidence,
                "primary_cluster_id": cluster_id,
                "source_item_count": len(members),
                "source_count": len({entry["item"].get("source_id") or entry["item"].get("source_name") for entry in members}),
                "relation_summary": relation_summary,
            }
            conn.execute(
                "INSERT OR REPLACE INTO events(event_id, event_title, event_summary, event_type, event_time, status, importance, confidence, primary_cluster_id, evidence_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id,
                    _event_title(signature, representative_entry["item"]),
                    _event_summary(signature, member_items),
                    signature.action if signature.action != "other" else "event",
                    signature.date_bucket,
                    "ready" if len(members) > 1 else "needs_review",
                    min(5, max(1, len(members) + (1 if len(members) > 1 else 0))),
                    min(0.98, max(0.72, signature.confidence if len(members) == 1 else signature.confidence + 0.05)),
                    cluster_id,
                    json.dumps(event_evidence, ensure_ascii=False),
                    now,
                    now,
                ),
            )
            for member in members:
                role = "source_material" if member["item"]["item_id"] == representative_entry["item"]["item_id"] else "supporting"
                conn.execute("INSERT OR IGNORE INTO event_items(event_id, item_id, role, created_at) VALUES (?, ?, ?, ?)", (event_id, member["item"]["item_id"], role, now))
            if len(members) == 1:
                stats["review_required"] += 1
                _insert_review(conn, "event_candidate", "event", event_id, {"action": "review_event", "evidence": event_evidence}, "Single-item event cluster needs review before high-confidence use.", now)
            stats["clusters_created_or_updated"] += 1
            stats["events_created_or_updated"] += 1
    return stats


def run_dedupe_stage(store: InboxStore, run_id: str, item_ids: list[str]) -> dict[str, Any]:
    now = utc_now()
    created = 0
    explained_duplicates = 0
    seen_multiple = 0
    with store.connect() as conn:
        rows = conn.execute(
            f"SELECT item_id, dedupe_key, url, guid, title, source_id, source_name, source_category, published_at, created_at, last_seen_at, seen_count, raw_json, latest_raw_json, latest_seen_summary FROM inbox_items WHERE item_id IN ({','.join('?' for _ in item_ids)})",
            item_ids,
        ).fetchall() if item_ids else []
        groups: dict[str, list[Any]] = {}
        for row in rows:
            key = row["dedupe_key"] or normalize_url(row["url"] or "") or normalized_title(row["title"])
            groups.setdefault(key, []).append(row)
        for key, members in groups.items():
            group_id = "dg_" + stable_hash(key)[:16]
            primary = members[0]["item_id"]
            total_seen = sum(int(member["seen_count"] or 1) for member in members)
            if total_seen > len(members):
                explained_duplicates += 1
            seen_multiple += sum(1 for member in members if int(member["seen_count"] or 1) > 1)
            variants: dict[str, set[str]] = {}
            for member in members:
                merged = _source_variants_from_raw(member["raw_json"], member["latest_raw_json"])
                for variant_key, values in merged.items():
                    variants.setdefault(variant_key, set()).update(values)
            evidence = {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "created_by": CREATED_BY,
                "input_fingerprint": stable_hash(json.dumps({"run_id": run_id, "dedupe_key": key, "members": [member["item_id"] for member in members]}, ensure_ascii=False, sort_keys=True)),
                "dedupe_key": key,
                "dedupe_method": _dedupe_method(dict(members[0])),
                "canonical_item_id": primary,
                "member_count": len(members),
                "seen_count": total_seen,
                "source_count": len({member["source_id"] or member["source_name"] for member in members}),
                "first_seen_at": min(member["created_at"] or now for member in members),
                "last_seen_at": max(member["last_seen_at"] or now for member in members),
                "latest_seen_summaries": [member["latest_seen_summary"] for member in members if member["latest_seen_summary"]][:5],
                "url_variants": sorted(variants.get("url_variants", set()))[:10],
                "canonical_url_variants": sorted(variants.get("canonical_url_variants", set()))[:10],
                "guid_variants": sorted(variants.get("guid_variants", set()))[:10],
                "source_ids": sorted(variants.get("source_ids", set()))[:10],
            }
            conn.execute(
                "INSERT OR REPLACE INTO dedupe_groups(dedupe_group_id, primary_item_id, dedupe_method, confidence, evidence_json, review_status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (group_id, primary, evidence["dedupe_method"], 0.9 if total_seen > 1 else 0.55, json.dumps(evidence, ensure_ascii=False), "reviewed" if total_seen == 1 else "explained", now, now),
            )
            for member in members:
                role = "canonical" if member["item_id"] == primary else _dedupe_method(dict(member))
                conn.execute("INSERT OR IGNORE INTO dedupe_group_items(dedupe_group_id, item_id, role, created_at) VALUES (?, ?, ?, ?)", (group_id, member["item_id"], role, now))
            created += 1
    coverage = explained_duplicates / seen_multiple if seen_multiple else 1.0
    return {"dedupe_groups_created_or_updated": created, "seen_count_gt_1_items": seen_multiple, "dedupe_explanation_count": explained_duplicates, "dedupe_explanation_coverage": round(coverage, 4), "schema_version": SCHEMA_VERSION}
