from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.semantic.config import READINESS_THRESHOLDS


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    value: Any
    threshold: Any
    reason: str

    def model_dump(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "value": self.value,
            "threshold": self.threshold,
            "reason": self.reason,
        }


def _rate(count: int, total: int) -> float:
    return round(count / max(total, 1), 4)


def assess_readiness(summary: dict[str, Any], *, real_write_rehearsal_passed: bool = False) -> dict[str, Any]:
    cards = summary.get("item_cards") or {}
    relations = summary.get("item_relations") or {}
    clusters = summary.get("item_clusters") or {}
    errors = summary.get("errors_fallbacks") or {}
    signatures = summary.get("event_signatures") or {}
    item_count = int((summary.get("input_sample") or {}).get("items_sampled") or cards.get("item_cards_generated") or 0)
    heuristic = int(cards.get("heuristic_card_fallback_count") or 0)
    parse_fallback = int(cards.get("parse_error_fallback_count") or 0)
    budget_fallback = int(cards.get("budget_skip_fallback_count") or 0)
    must_run_skips = int(relations.get("must_run_skips") or relations.get("skipped_must_run_candidates") or 0)
    conflicts = int(relations.get("pair_conflict_count") or 0)
    db_locks = int(errors.get("db_lock_errors") or 0)
    effective_clusters = int(clusters.get("effective_multi_item_cluster_count") or clusters.get("multi_item_cluster_likely_valid_count") or 0)
    suspect_clusters = int(clusters.get("suspect_multi_item_cluster_count") or clusters.get("multi_item_cluster_suspect_count") or 0)
    valid_signature_rate = float(signatures.get("valid_signature_rate") or 0.0)

    gates = [
        GateResult("heuristic_fallback_rate", _rate(heuristic, item_count) < READINESS_THRESHOLDS.heuristic_fallback_max_rate, _rate(heuristic, item_count), f"< {READINESS_THRESHOLDS.heuristic_fallback_max_rate}", "heuristic emergency fallback must stay low"),
        GateResult("parse_failure_fallback_rate", _rate(parse_fallback, item_count) < READINESS_THRESHOLDS.parse_failure_fallback_max_rate, _rate(parse_fallback, item_count), f"< {READINESS_THRESHOLDS.parse_failure_fallback_max_rate}", "parse failures must not dominate cards"),
        GateResult("budget_skip_fallback_rate", _rate(budget_fallback, item_count) < READINESS_THRESHOLDS.budget_skip_fallback_max_rate, _rate(budget_fallback, item_count), f"< {READINESS_THRESHOLDS.budget_skip_fallback_max_rate}", "budget fallback must not starve candidate-bearing cards"),
        GateResult("skipped_must_run_candidates", must_run_skips <= READINESS_THRESHOLDS.max_skipped_must_run, must_run_skips, READINESS_THRESHOLDS.max_skipped_must_run, "must-run candidates are protected"),
        GateResult("pair_relation_conflicts", conflicts <= READINESS_THRESHOLDS.max_pair_conflicts, conflicts, READINESS_THRESHOLDS.max_pair_conflicts, "canonical pair verdicts cannot conflict"),
        GateResult("db_lock_errors", db_locks <= READINESS_THRESHOLDS.max_db_lock_errors, db_locks, READINESS_THRESHOLDS.max_db_lock_errors, "no DB lock errors"),
        GateResult("event_signature_valid_rate", valid_signature_rate >= READINESS_THRESHOLDS.event_signature_valid_min_rate, valid_signature_rate, f">= {READINESS_THRESHOLDS.event_signature_valid_min_rate}", "signatures are concrete enough"),
        GateResult("effective_multi_item_clusters", effective_clusters >= READINESS_THRESHOLDS.effective_cluster_min_count, effective_clusters, f">= {READINESS_THRESHOLDS.effective_cluster_min_count}", "dry-run produced useful same-event clusters"),
        GateResult("suspect_multi_item_clusters", suspect_clusters == 0, suspect_clusters, 0, "no suspect multi-item clusters accepted"),
        GateResult("small_scoped_real_write_rehearsal", real_write_rehearsal_passed, real_write_rehearsal_passed, True, "production readiness requires a scoped write rehearsal"),
    ]
    passed = all(gate.passed for gate in gates)
    return {
        "verdict": "READY_FOR_SCOPED_REAL_SEMANTIC_WRITE" if passed else "NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE",
        "ready": passed,
        "gates": [gate.model_dump() for gate in gates],
        "blockers": [gate.model_dump() for gate in gates if not gate.passed],
    }

