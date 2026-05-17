# Semantic Phase 1.3 Refactor Audit

## Current-State Findings

Phase 1.2e proved the semantic pipeline could produce useful relation signals, but candidate generation inflated broad topic overlap into high-priority work. Hotspots such as `agent`, `api`, and `research` created expensive relation/cluster calls and one likely same-topic multi-item cluster.

Phase 1.2f corrected much of that precision risk, but recall overcorrected. The final 300-item run dropped to zero multi-item clusters, produced only a few same-event relations, and reported many item-card fallbacks and stage-budget skips.

## Complexity Hotspots

- `evaluate.py` mixed orchestration, budget policy, source sampling, report summary, readiness, and markdown rendering.
- `candidates.py` mixed token policy, event signature extraction, lane scoring, relation normalization, and hotspot selection.
- `clusters.py` mixed cluster retrieval, candidate scoring, attach policy, seed gating, cluster writes, and source-signal writes.
- `evidence.py` handled extraction, derived metrics, report rendering, review bundle construction, and phase comparison in one large module.

## Refactor Direction

Phase 1.3 introduces dedicated policy modules:

- `semantic/config.py`: thresholds, generic/proxy tokens, priorities, budget profiles.
- `semantic/signatures.py`: first-class event signatures with validation and invalid reasons.
- `semantic/budget.py`: advisory budgets and skip-tier accounting.
- `semantic/card_policy.py`: card tier selection and fallback classification.
- `semantic/relation_policy.py`: relation labels, fold mapping, and cluster eligibility.
- `semantic/cluster_policy.py`: attach and seed policy.
- `semantic/readiness.py`: readiness gates and final verdict.
- `semantic/write_rehearsal.py`: scoped real-write confirmation, backup, and rehearsal reporting.

## Active Prompt Versions

- `item_card_v1`
- `item_relation_v3`
- `item_cluster_relation_v3`
- `cluster_card_patch_v1`
- `source_review_v1`

`item_relation_v2` and `item_cluster_relation_v2` remain comparison artifacts and are not active in routing.

## Candidate Priority Behavior

Priority now records an explicit lane:

- `deterministic`
- `event_signature`
- `near_title`
- `same_actor_product`
- `same_thread`
- `exploratory_recall`
- `suppressed`

`must_run` is reserved for deterministic duplicates, very strong near-title duplicates, or very strong concrete signature matches. Generic-only overlap is suppressible and cannot become `must_run`.

## Item-Card Fallback Causes

Fallback evidence now separates:

- deterministic minimal cards;
- emergency heuristic fallback;
- LLM parse-error fallback;
- budget-skip fallback;
- empty/bad-input fallback.

Deterministic minimal cards are intentional for short social/RSS posts and are not counted as emergency heuristic fallback.

## Relation And Cluster Failure Modes Addressed

- `same_product_different_event` and `same_thread` are first-class relation labels with no fold/attach action.
- Canonical pair conflicts are persisted to `semantic_relation_conflicts` and exported as `relation_conflicts.jsonl`.
- Cluster attachment rejects same-thread, same-product-different-event, same-conference, generic-only, and entity-overlap-only decisions.
- Effective multi-item clusters are separated from reported/suspect multi-item clusters.

## Token And Budget Profile

Stage budgets are advisory by default in Phase 1.3. This avoids starving relation and cluster stages because item cards consumed their slice. Budget skips remain exported and readiness fails if `must_run` candidates are skipped.

## Readiness Blockers To Validate In Runs

- Event signature valid rate must be high enough on scoped data.
- `must_run` skipped candidates must be zero.
- Canonical relation conflicts must be zero or resolved.
- Emergency heuristic fallback must stay below the readiness threshold.
- Effective multi-item clusters must appear without suspect same-topic clusters.
- A scoped real-write rehearsal must pass before `READY_FOR_SCOPED_REAL_SEMANTIC_WRITE`.

