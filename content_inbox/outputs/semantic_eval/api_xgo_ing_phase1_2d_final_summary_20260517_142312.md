# api.xgo.ing Phase 1.2d Final Summary

- generated_at: 2026-05-17T14:23:12.819349
- git commit: b30e4834ebf710177acced15fca3e1befb97f550
- console UI modified: NO
- semantic --write-real-db: NO
- ingest-source-scope in this phase: NO

## Run Parameters

- scope: api.xgo.ing*
- item_count: 300
- sample_mode: event_hotspots
- concurrency: 5
- stage budget profile: relation_heavy
- model: deepseek-v4-flash
- duration_seconds: 1168.356
- actual_calls: 221
- actual_tokens: 737878

## Evidence Persistence

| artifact | status | count/path |
|---|---|---|
| semantic_items | YES | 300 |
| item_cards | YES | 300 |
| item_card_failures | YES | 25 |
| relations_all | YES | 479 |
| relations_interesting | YES | 60 |
| event_hotspots | YES | 50 |
| cluster_candidates | YES | 232 |
| cluster_attachments | YES | 431 |
| llm_calls/errors | YES | 636 |
| budget_skips | YES | 415 |

## Key Results

- relation distribution: `{"different": 449, "related_with_new_info": 24, "uncertain": 2, "near_duplicate": 4}`
- interesting distribution: `{"related_with_new_info": 24, "uncertain": 2, "near_duplicate": 4, "suspicious_different": 30}`
- item-card failures evidence rows: 25
- cluster candidates: 232
- cluster attachments: 431
- final clusters: 18
- multi-item clusters: 1
- budget skips: 415
- LLM errors: 8

## Relation Evidence Files

- all relations: `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_all.jsonl`
- interesting relations: `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_interesting.jsonl`
- suspicious different sample count: 30

## Readiness

- semantic --write-real-db recommended: NO

- BLOCKER: Multi-item clusters are still not stable in final run.
- BLOCKER: Cluster candidate alternatives are reconstructed from decisions/logs; future runs should persist pre-LLM candidate alternatives at generation time.
- BLOCKER: 25 item-card failure evidence rows were produced from failed LLM batches, although fallback cards existed for all 300 items.
- BLOCKER: 415 budget skip rows show relation/cluster stages still exhaust stage budgets at 300-item scale.
- BLOCKER: No fresh ingest was performed in 1.2d; ingest atomicity remains a known blocker from 1.2c.

## Reports

- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/semantic_quality_report.md`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/semantic_run_manifest.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_all.jsonl`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/relations_interesting.jsonl`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/item_card_failures.jsonl`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/cluster_attachments.jsonl`
- `outputs/semantic_eval/api_xgo_ing_phase1_2d_full_300_c5_20260517_140244/event_hotspots.jsonl`
