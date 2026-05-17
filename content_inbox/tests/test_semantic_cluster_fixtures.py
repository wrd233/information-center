from __future__ import annotations

import json
from pathlib import Path

from app.semantic.cluster_policy import relation_can_seed_cluster


FIXTURE = Path(__file__).parent / "fixtures" / "semantic_cluster_benchmark_phase1_3b.jsonl"


def load_rows() -> list[dict]:
    return [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_phase1_3b_cluster_fixture_types_are_respected() -> None:
    rows = load_rows()
    assert any(row["expected_cluster_type"] == "event_cluster" for row in rows)
    assert any(row["expected_cluster_type"] == "thread_candidate" for row in rows)
    assert any(row["expected_cluster_type"] == "reject" for row in rows)


def test_phase1_3b_event_cluster_seed_policy() -> None:
    can_seed, reason = relation_can_seed_cluster("related_with_new_info", "same_event", 0.82)
    assert can_seed
    assert reason == "related_new_info_seed"


def test_phase1_3b_thread_and_reject_clusters_cannot_seed_event_clusters() -> None:
    rows = load_rows()
    for row in rows:
        if not row["expected_should_form_event_cluster"]:
            for relation in ("same_thread", "same_product_different_event", "different", "uncertain"):
                can_seed, _reason = relation_can_seed_cluster(relation, row["expected_cluster_type"], 0.95)
                assert not can_seed, row["fixture_id"]


def test_phase1_3b_fixture_expected_signatures_avoid_garbage_products() -> None:
    garbage = {"fkr2wvd129", "nrjiqrd2fg", "u4n62", "may 14", "our 25", "for 50", "just 0.3"}
    for row in load_rows():
        signature = row.get("expected_signature") or {}
        product = str(signature.get("product_or_model") or "").lower()
        assert product not in garbage
