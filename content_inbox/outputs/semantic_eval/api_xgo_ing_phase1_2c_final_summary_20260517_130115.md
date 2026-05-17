# api.xgo.ing Phase 1.2c Final Summary

- generated_at: 2026-05-17T13:01:15.672744
- git commit: e7d51ad7bd188d0d986f52ec19a05ce2cbab9f41
- console UI modified: NO
- semantic --write-real-db used: NO
- scoped ingest real DB write: YES

## Source Refresh Summary

- backup paths: data/backups/content_inbox.sqlite3.before_api_xgo_semantic_phase1_2c_20260517_105648.sqlite3, data/backups/content_inbox.sqlite3.before_api_xgo_semantic_phase1_2c_20260517_111621.sqlite3
- selected sources: 151
- succeeded sources: 7
- failed sources: 144
- timed out sources: 143
- DB item delta: 283
- new items reported by successful sources: 2
- duplicates reported by successful sources: 68
- latest before/after: 2026-05-16T19:50:51+00:00 -> 2026-05-17T02:16:56+00:00
- failures_by_reason: `{"http_error": 1, "timeout": 143}`

## Probe Before/After

| metric | before | after |
|---|---:|---:|
| total_sources_matched | 151 | 151 |
| sources_with_items | 147 | 151 |
| zero_item_sources | 4 | 0 |
| total_items_via_rss_join | 782 | 1354 |
| latest_item_time | 2026-05-16T10:18:27+00:00 | 2026-05-17T02:16:56+00:00 |
| scope_missing_source_id_items | 0 | 0 |
| scope_missing_feed_url_items | 0 | 0 |
| html_entity_source_name_issues | 5 | 5 |

## Prompt / Chain Iteration Log

- Added local minimal-card tier for short/social RSS items, plus standard/full routing for richer content.
- Added stage-aware token budgeting and `relation_heavy` profile so item cards no longer consume the whole budget.
- Added `event_hotspots` sampling based on normalized entity/semantic-token hotspots in the scoped item set.
- Added relation/cluster candidate coverage counters and reporting.
- Reworked scoped ingest execution to explicit bounded subprocess scheduling with per-source timeout/retry and classified failures.
- Source priority reviews are now counted/created only per source when enough evidence exists; low-sample sources stay under evaluation.

## Evaluation Runs

| run | items | duration_s | calls | tokens | fallbacks | card_fail | relation_calls | non-different relations | cluster_calls | multi_item_clusters | failures | rate_limits |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| smoke c3 balanced | 50 | 476.0 | 61 | 179739 | 0 | 0 | 25 | 2 | 26 | 1 | 1 | 0 |
| smoke iter2 c3 relation_heavy | 50 | 429.0 | 68 | 194761 | 5 | 1 | 33 | 6 | 25 | 1 | 1 | 0 |
| medium 150 c3 | 150 | 965.4 | 139 | 427440 | 15 | 3 | 63 | 28 | 52 | 1 | 5 | 1 |
| cmp 150 c2 | 150 | 1061.5 | 137 | 431332 | 10 | 2 | 60 | 30 | 53 | 0 | 2 | 0 |
| cmp 150 c4 | 150 | 797.5 | 140 | 430957 | 20 | 4 | 62 | 33 | 54 | 0 | 5 | 0 |
| final 300 c4 | 300 | 1232.7 | 223 | 714640 | 35 | 7 | 97 | 30 | 82 | 0 | 9 | 0 |

## Final 300 Summary

- card tiers: `{"full": 99, "minimal": 96, "standard": 105}`
- relation distribution: `{"duplicate": 0, "near_duplicate": 7, "related_with_new_info": 23, "uncertain": 0, "different": 453}`
- cluster relation distribution: `{"new_info": 16, "source_material": 4}`
- stage starvation: False
- source priority reviews created: 0; pending reviews all types: 475

## Concurrency Recommendation

- recommended_concurrency: 4
- reason: concurrency=4 was fastest in the 150-item hotspot comparison, with no rate-limit or DB-lock errors and comparable relation/cluster coverage.

## Readiness Assessment

- semantic write-real-db recommended: NO

Blockers:
- Scoped ingest still times out on most sources and can leave partial writes before per-source kill.
- Final 300 run produced useful item-item relations but multi_item_cluster_count remained 0.
- Final run still had 35 heuristic fallbacks / 300 and 7 item-card failures.
- Relation/cluster stages still skip many candidates due stage budgets at 300-item scale.
- Review queue contains many non-source review entries; source priority reviews are now suppressed/aggregated but cluster/failure review noise still needs work.

## Tests

- `PYTHONPATH=. python3 -m py_compile app/semantic/cards.py app/semantic/evaluate.py app/semantic/probe.py app/semantic/cli.py app/semantic/relations.py app/semantic/clusters.py app/semantic/source_profiles.py` passed.
- `PYTHONPATH=. pytest -q tests/test_semantic_phase1.py` passed: 16 passed, 1 skipped.
- `PYTHONPATH=. pytest -q` passed: 219 passed, 11 skipped.

## Files Changed


## Key Reports

- `outputs/semantic_eval/api_xgo_ing_phase1_2c_probe_before_20260517_105638.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_probe_after_20260517_113505.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_ingest_20260517_111620.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_smoke_hotspots_c3/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_smoke_hotspots_c3_iter2/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_hotspots_150_c3/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_hotspots_150_c2_cmp/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_hotspots_150_c4_cmp/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_full_300_final/semantic_quality_summary.json`
- `outputs/semantic_eval/api_xgo_ing_phase1_2c_concurrency_comparison_20260517_123910.json`

## Known Issues / Next Steps

- Fix scoped ingest atomicity so a timed-out source cannot partially write without being reported as success/partial.
- Improve hotspot grouping/reporting so same event candidate sets are less broad and more cross-source-event focused.
- Add vector or embedding-based recall for cluster attachment, or a deterministic pre-cluster step for same entity/time windows.
- Reduce non-source review noise from budget skips/failures and cluster uncertainty.
- Consider raising relation/cluster stage budgets or reducing per-call prompt payloads before larger runs.
