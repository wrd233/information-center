from __future__ import annotations

from typing import Any

from app.semantic.config import CLUSTER_THRESHOLDS


DISQUALIFYING_CLUSTER_TYPES = {
    "same_topic_only",
    "same_product_different_event",
    "same_thread",
    "same_conference",
    "entity_overlap_only",
    "different",
    "uncertain",
}


def cluster_relation_action(primary_relation: str) -> str:
    mapping = {
        "source_material": "attach_update_card",
        "repeat": "attach_no_core_update",
        "new_info": "attach_update_card",
        "analysis": "attach_maybe_update_card",
        "experience": "attach_maybe_update_card",
        "context": "attach_context",
        "follow_up": "create_follow_up_cluster",
        "same_topic": "do_not_attach",
        "unrelated": "do_not_attach",
        "uncertain": "review",
    }
    return mapping.get(primary_relation, "review")


def cluster_decision_attach_eligible(decision: Any) -> bool:
    relation_type = getattr(decision, "cluster_relation_type", "") or ""
    primary = getattr(decision, "primary_relation", "") or ""
    same_event = bool(getattr(decision, "same_event", False))
    if relation_type in DISQUALIFYING_CLUSTER_TYPES:
        return False
    if primary in {"same_topic", "unrelated", "uncertain", "follow_up"}:
        return False
    if not same_event:
        return False
    if float(getattr(decision, "confidence", 0.0) or 0.0) < CLUSTER_THRESHOLDS.attach_confidence:
        return False
    if getattr(decision, "attach_eligible", False):
        return True
    return primary in {"source_material", "repeat", "new_info", "analysis", "experience", "context"}


def relation_can_seed_cluster(primary_relation: str, event_relation_type: str, confidence: float) -> tuple[bool, str]:
    if event_relation_type != "same_event":
        return False, "not_same_event"
    if primary_relation in {"duplicate", "near_duplicate"}:
        if confidence >= CLUSTER_THRESHOLDS.near_duplicate_seed_confidence:
            return True, "near_duplicate_seed"
        return False, "near_duplicate_confidence_below_threshold"
    if primary_relation == "related_with_new_info":
        if confidence >= CLUSTER_THRESHOLDS.related_new_info_seed_confidence:
            return True, "related_new_info_seed"
        return False, "related_new_info_confidence_below_threshold"
    return False, "relation_type_cannot_seed"

