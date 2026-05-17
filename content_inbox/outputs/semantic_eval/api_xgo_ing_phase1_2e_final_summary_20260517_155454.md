# Phase 1.2e Final Summary

## Plan mode summary
Implemented the confirmed Phase 1.2e plan with one corrective iteration after the first live run showed hotspot keys were still too noisy. Final run uses the second output directory.

## Code changes
- content_inbox/app/semantic/cards.py
- content_inbox/app/semantic/cli.py
- content_inbox/app/semantic/clusters.py
- content_inbox/app/semantic/evaluate.py
- content_inbox/app/semantic/evidence.py
- content_inbox/app/semantic/llm_client.py
- content_inbox/app/semantic/relations.py
- content_inbox/app/semantic/schemas.py
- content_inbox/tests/test_semantic_phase1.py

## Real DB writes
- ingest-source-scope: NO
- semantic --write-real-db: NO
- backup path: N/A

## Run parameters
- scope: api.xgo.ing*
- item_count: 300
- sample_mode: event_hotspots
- concurrency: 5
- stage budget profile: phase1_2e_profile
- model: deepseek-v4-flash
- write_real_db: false
- output dir: /Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_2e_full_300_c5_20260517_152936

## Evidence persistence
All Phase 1.2d evidence artifacts are still generated. Phase 1.2e also adds `candidate_generation.jsonl`, `candidate_suppression.jsonl`, `cost_quality_metrics.json`, and `phase1_2d_vs_1_2e_comparison.json`.

## Precision hardening results
- raw relations: 321
- unique relation pairs: 284
- duplicate direction suppressed / marked: 446
- relation distribution: `{"different": 314, "near_duplicate": 4, "related_with_new_info": 3}`
- event_relation_type distribution: `{"different": 36, "entity_overlap_only": 10, "same_account_boilerplate": 15, "same_event": 7, "same_product_different_event": 4, "same_topic_only": 249}`
- cluster_eligible count: 7
- candidate suppressions: 31
- high-priority suppressions: 0

## Hotspot results
- top hotspot keys: `[{"hotspot_key": "agent", "group_size": 90, "source_count": 54, "key_source": "event_phrase"}, {"hotspot_key": "api", "group_size": 32, "source_count": 24, "key_source": "entity"}, {"hotspot_key": "research", "group_size": 21, "source_count": 17, "key_source": "entity"}, {"hotspot_key": "claude", "group_size": 20, "source_count": 15, "key_source": "entity"}, {"hotspot_key": "launch", "group_size": 22, "source_count": 14, "key_source": "entity"}, {"hotspot_key": "github", "group_size": 16, "source_count": 14, "key_source": "entity"}, {"hotspot_key": "release", "group_size": 14, "source_count": 14, "key_source": "entity"}, {"hotspot_key": "openai", "group_size": 14, "source_count": 13, "key_source": "entity"}, {"hotspot_key": "google", "group_size": 14, "source_count": 13, "key_source": "entity"}, {"hotspot_key": "benchmark", "group_size": 13, "source_count": 11, "key_source": "entity"}]`
- xgo.ing selected hotspot count: 0
- BLOCKER: keys are no longer proxy domains, but still too broad (`agent`, `api`, `research`).

## Token-cost results
- total calls: 234 (1.2d baseline: 221)
- total tokens: 728728 (1.2d baseline: 737878)
- budget skips: 443
- non-different per 100k tokens: 0.961
- cluster eligible per 100k tokens: 0.961

## Cluster results
- candidate clusters/evidence rows: 88 LLM calls, 189 skips
- multi-item clusters: 1
- cluster relations: `{"new_info": 16, "source_material": 7}`

## Item-card retry results
- heuristic fallback cards: 18 (below 1.2d affected fallback target of 25)
- failed item-card call rows: 9
- card tiers: `{"full": 103, "minimal": 113, "standard": 84}`

## Review export
Generated after this summary; see paths below.

## Tests
- `PYTHONPATH=. python3 -m py_compile app/semantic/*.py`: PASS
- `PYTHONPATH=. pytest -q tests/test_semantic_phase1.py`: PASS
- `PYTHONPATH=. pytest -q`: PASS before final hotspot tightening; semantic suite rerun after tightening: PASS
- `git diff --check`: PASS
- Console UI diff check: no diff

## Readiness
- full semantic --write-real-db: NO
- only near_duplicate write: not recommended yet; near_duplicate count is small and includes promotional/link-only cases needing manual review.
- cluster write: NO
- recommendation: keep using dry-run evidence and prioritize hotspot/candidate ranking before any real semantic write.

## Known issues / blockers
- BLOCKER: budget skips remain high (443 rows)
- BLOCKER: event hotspot keys improved from proxy domains but still broad (agent/api/research)
- BLOCKER: multi-item clusters only 1
- BLOCKER: item-card failed call rows increased to 37 though final heuristic fallback is 18
- BLOCKER: relation/cluster candidate generation still overproduces high/medium candidates

## Next recommendations
- Make hotspot generation phrase/entity-pair based instead of single-token based.
- Lower card prompt output size and retry timeout exposure.
- Add candidate caps by priority so high/medium candidate_generation does not explode.
- Add stricter deterministic near_duplicate rules for short promotional link posts.
