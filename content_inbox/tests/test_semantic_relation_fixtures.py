from __future__ import annotations

import json
from pathlib import Path

from app.semantic.cluster_policy import relation_can_seed_cluster
from app.semantic.relation_policy import RELATION_REASON_CODES, default_reason_code, relation_cluster_eligible, should_fold


FIXTURE = Path(__file__).parent / "fixtures" / "semantic_relation_benchmark_phase1_3b.jsonl"


def load_rows() -> list[dict]:
    return [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_phase1_3b_relation_fold_policy() -> None:
    rows = load_rows()
    for row in rows:
        relation = row["expected_relation"]
        assert should_fold(relation) is bool(row["expected_should_fold"]), row["fixture_id"]


def test_phase1_3b_thread_relations_do_not_seed_event_clusters() -> None:
    for relation in {"same_thread", "same_product_different_event", "different", "uncertain", "low_signal"}:
        assert not relation_cluster_eligible(relation, relation)
        can_seed, reason = relation_can_seed_cluster(relation, relation, 0.95)
        assert not can_seed
        assert reason


def test_phase1_3b_near_duplicates_fold_but_do_not_inflate_clusters() -> None:
    assert should_fold("near_duplicate")
    assert not relation_cluster_eligible("near_duplicate", "same_event", 0.95)
    can_seed, reason = relation_can_seed_cluster("near_duplicate", "same_event", 0.95)
    assert not can_seed
    assert reason == "fold_relation_not_event_cluster_seed"


def test_phase1_3b_related_with_new_info_can_seed_only_at_high_confidence() -> None:
    assert relation_cluster_eligible("related_with_new_info", "same_event", 0.8)
    assert not relation_cluster_eligible("related_with_new_info", "same_product_different_event", 0.95)
    assert not relation_cluster_eligible("related_with_new_info", "same_event", 0.79)


def test_default_reason_codes_are_registered() -> None:
    cases = [
        ("different", "same_event"),
        ("same", "same_event"),
        ("same", "update"),
        ("same", "background"),
        ("duplicate", "same_event"),
        ("near_duplicate", "same_event"),
        ("related_with_new_info", "same_event"),
        ("same_product_different_event", "same_product_different_event"),
        ("same_thread", "same_thread"),
        ("uncertain", "different"),
    ]

    for primary_relation, event_relation_type in cases:
        assert default_reason_code(primary_relation, event_relation_type) in RELATION_REASON_CODES
    assert default_reason_code("different", "different", generic_only=True) in RELATION_REASON_CODES
