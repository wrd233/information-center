# Operational Event Aggregation v3

Status: canonical current plan and checkpoint log.

Last updated: 2026-06-01.

## Checkpoint Policy

This work proceeds in checkpoints. Each checkpoint must keep the repository green before the next one starts:

- `PYTHONPATH=. pytest -q`
- `PYTHONPATH=. python3 scripts/evaluate_ops_quality.py`
- Relevant docs updated in the same checkpoint.

Safety gates outrank recall:

- Auto-merge precision must not regress from the current baseline.
- Digest/generic false event rate must remain `0`.
- Medium/uncertain candidates must not auto-merge.
- Hard negatives must not enter LLM adjudication.
- LLM parse failures must not auto-merge.

## Baseline Before Operational v3

Captured by `scripts/evaluate_ops_quality.py` on 2026-06-01.

| Metric | Baseline |
|---|---:|
| Full pytest | `271 passed, 11 skipped` |
| Process dedupe precision/recall/F1 | `100.0% / 100.0% / 100.0%` |
| Same-event precision/recall/F1 | `100.0% / 27.3% / 42.9%` |
| Auto-merge precision | `100.0%` |
| Digest/generic false event rate | `0.0%` |
| Medium review rate | `100.0%` |
| Candidate counts by priority | `{'low': 7, 'must_run': 1, 'high': 1, 'medium': 1}` |
| Candidate counts by lane | `{'exploratory_recall': 4, 'exact_signature_alias': 1, 'same_event_recall': 2, 'same_thread': 3}` |
| Candidate counts by status | `{'review': 8, 'auto_merge': 2}` |
| Briefing quality score | `77.8%` |
| Run report quality score | `66.7%` |

## Source Scoring Dimensions

Operational v3 keeps source value as dimensions rather than a single score:

- `discovery_value`: source first seeds a trusted event or cluster.
- `fact_value`: source contributes source material, official evidence, cited facts, or high-confidence core facts.
- `incremental_value`: source adds new facts to an existing event.
- `interpretation_value`: source contributes analysis, context, contrarian, risk, market, or technical angles.
- `duplicate_noise`: source mostly contributes duplicates, near-duplicates, or repeats.
- `non_event_noise`: source contributes digest, generic, low-signal, or content-only items rejected by eventness.
- `review_acceptance`: accepted review decisions increase trust; rejected decisions reduce trust.

## Checkpoint Log

- Checkpoint 1: baseline and guardrails started. Baseline commands passed; behavior unchanged.
- Checkpoint 2: idempotent schema substrate added for candidate audit, review apply audit, and dimensional source scoring fields.
- Checkpoint 3: rule-only operational v3 extracted into `app/semantic/operational_pipeline.py`; `ops_api.py` now delegates dedupe and event-object generation to that module. Synthetic eval preserved auto-merge precision at `100.0%`, kept digest/generic false event rate at `0.0%`, and improved briefing/report generated-template scores.
- Checkpoint 4: optional schema-bound operational relation LLM adjudication added. It is default-off, skips hard negatives before LLM, logs live-disabled skips, and converts parse failures or recommendations into review-only outcomes.
- Checkpoint 5: review apply now performs real event relation/eventness effects for handled review types and stores `apply_result_json`. Source scoring recompute now preserves `discovery_value`, `fact_value`, `incremental_value`, `interpretation_value`, `duplicate_noise`, `non_event_noise`, and `review_acceptance` dimensions.
