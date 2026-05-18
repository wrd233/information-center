# Phase 1.3 Complexity Control Report

## Modules Added

- `semantic/config.py`: centralized thresholds, generic tokens, budget profiles.
- `semantic/signatures.py`: first-class event signature extraction and validation.
- `semantic/budget.py`: advisory budgets and skip-tier accounting.
- `semantic/card_policy.py`: card tier and fallback classification policy.
- `semantic/relation_policy.py`: relation labels, fold mapping, cluster eligibility.
- `semantic/cluster_policy.py`: cluster attach and seed policy.
- `semantic/readiness.py`: production readiness gates.
- `semantic/write_rehearsal.py`: scoped write confirmation, backup, and rehearsal reports.

## Active Prompt Versions

- item cards: `item_card_v1`
- item relation: `item_relation_v3`
- item-cluster relation: `item_cluster_relation_v3`
- cluster card patch: `cluster_card_patch_v1`

## Active Relation Labels

{
  "different": "no action",
  "duplicate": "fold, same-event duplicate evidence",
  "near_duplicate": "fold, same-event repeat evidence",
  "related_with_new_info": "do not fold, may seed/attach same-event cluster with confidence",
  "same_product_different_event": "do not fold or attach, thread evidence only",
  "same_thread": "do not fold or attach, thread evidence only",
  "uncertain": "review only"
}

## Remaining Complexity Debt

- `evaluate.py` and `evidence.py` still contain legacy report-rendering helpers; Phase 1.3 isolates new concepts but does not fully move all markdown rendering into `reports.py`.
- Existing SQLite schema remains backward-compatible, so some new semantic fields are persisted in evidence/metadata rather than dedicated columns.
- Candidate generation is deterministic and lexical/signature based; vector indexes remain a future recall enhancement.
