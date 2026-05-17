from __future__ import annotations

from typing import Any


FOLD_RELATIONS = {"duplicate", "near_duplicate"}
CLUSTER_SEED_RELATIONS = {"related_with_new_info"}
NON_ATTACH_RELATIONS = {"same_product_different_event", "same_thread", "different", "uncertain"}

RELATION_ACTIONS: dict[str, dict[str, Any]] = {
    "duplicate": {"should_fold": True, "cluster_seed_allowed": False, "thread_only": False},
    "near_duplicate": {"should_fold": True, "cluster_seed_allowed": False, "thread_only": False},
    "related_with_new_info": {"should_fold": False, "cluster_seed_allowed": True, "thread_only": False},
    "same_product_different_event": {"should_fold": False, "cluster_seed_allowed": False, "thread_only": True},
    "same_thread": {"should_fold": False, "cluster_seed_allowed": False, "thread_only": True},
    "different": {"should_fold": False, "cluster_seed_allowed": False, "thread_only": False},
    "uncertain": {"should_fold": False, "cluster_seed_allowed": False, "thread_only": False},
}

RELATION_REASON_CODES = {
    "deterministic_duplicate",
    "same_announcement_no_new_info",
    "same_event_new_fact",
    "same_product_different_feature",
    "same_thread_different_event",
    "generic_topic_overlap_only",
    "same_actor_different_event",
    "different_product",
    "different_event",
    "insufficient_content",
}


def relation_action(primary_relation: str) -> dict[str, Any]:
    return RELATION_ACTIONS.get(primary_relation, RELATION_ACTIONS["uncertain"])


def should_fold(primary_relation: str) -> bool:
    return bool(relation_action(primary_relation).get("should_fold"))


def relation_cluster_eligible(primary_relation: str, event_relation_type: str, confidence: float = 1.0) -> bool:
    if primary_relation in {"duplicate", "near_duplicate"}:
        return False
    if primary_relation not in CLUSTER_SEED_RELATIONS:
        return False
    if event_relation_type != "same_event":
        return False
    if primary_relation == "related_with_new_info" and confidence < 0.80:
        return False
    return True


def default_reason_code(primary_relation: str, event_relation_type: str, *, generic_only: bool = False) -> str:
    if generic_only:
        return "generic_topic_overlap_only"
    if primary_relation in {"duplicate", "near_duplicate"}:
        return "same_announcement_no_new_info"
    if primary_relation == "related_with_new_info":
        return "same_event_new_fact"
    if primary_relation == "same_product_different_event" or event_relation_type == "same_product_different_event":
        return "same_product_different_feature"
    if primary_relation == "same_thread" or event_relation_type == "same_thread":
        return "same_thread_different_event"
    if primary_relation == "uncertain":
        return "insufficient_content"
    return "different_event"


def normalize_primary_relation(primary_relation: str, event_relation_type: str) -> str:
    if primary_relation in RELATION_ACTIONS:
        return primary_relation
    if event_relation_type == "same_product_different_event":
        return "same_product_different_event"
    if event_relation_type in {"same_thread", "same_conference"}:
        return "same_thread"
    return "different" if primary_relation not in {"uncertain"} else "uncertain"
