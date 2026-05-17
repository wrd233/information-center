# api.xgo.ing Phase 1.2c Concurrency Comparison

- recommended_concurrency: 4
- reason: concurrency=4 was fastest in the 150-item hotspot comparison, with no rate-limit or DB-lock errors and comparable relation/cluster coverage.

| run | duration_s | calls | tokens | rate_limits | failures | avg_ms | p50_ms | p95_ms | relation_calls | non_different_relations | cluster_calls | multi_item_clusters |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c2 | 1061.5 | 137 | 431332 | 0 | 2 | 10396.8 | 7691 | 28603 | 60 | 30 | 53 | 0 |
| c3 | 965.4 | 139 | 427440 | 1 | 5 | 11750.9 | 8298 | 29756 | 63 | 28 | 52 | 1 |
| c4 | 797.5 | 140 | 430957 | 0 | 5 | 11060.0 | 8355 | 27528 | 62 | 33 | 54 | 0 |
