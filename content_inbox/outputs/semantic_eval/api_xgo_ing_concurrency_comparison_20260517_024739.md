# api.xgo.ing Concurrency Comparison

| concurrency | duration_s | calls | tokens | cache_hit_rate | calls/s | p50_ms | p95_ms | failures | rate_limits | db_locks | card_success | relation_success |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 594.173 | 44 | 206094 | 0.1845 | 0.0741 | 21257 | 30208 | 3 | 0 | 0 | 27 | 14 |
| 3 | 353.698 | 43 | 209040 | 0.1763 | 0.1216 | 22439 | 29555 | 1 | 0 | 0 | 29 | 13 |
| 4 | 398.016 | 49 | 212231 | 0.2352 | 0.1231 | 20752 | 33846 | 3 | 0 | 0 | 27 | 19 |

Recommended concurrency: **3**

concurrency=3 had the shortest duration with no rate-limit or DB-lock errors and fewer final failures than c2/c4 under the same 200k token budget; c4 did not improve throughput and had higher p95 latency/failures.

Note: c2 comparator reuses the corrected api_xgo_ing_full_150_c2 run copied into c2_cmp to avoid duplicate live token spend; c3 and c4 were fresh comparison runs.
