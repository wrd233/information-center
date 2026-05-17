# Step 3 Summary — Phase 1.3b Taxonomy, Regression Fixtures, and Codex Input

**Generated**: 2026-05-17
**Input**: 50-row Step 1 benchmark from Phase 1.3 `api_xgo_ing_phase1_3_round_c_80_live_tuned`

---

## What Was Done

1. Reclassified all 50 benchmark rows into four semantic levels
2. Created a comprehensive action taxonomy with English and Chinese triggers
3. Defined actor/product extraction rules addressing 8 known failure modes
4. Defined accept/reject decision flows preventing both over-clustering and over-rejection
5. Defined relation boundary rules for 6 relation types
6. Defined cluster seed rules with allowed/disallowed sources
7. Generated 3 regression fixture files (33 signature + 17 relation + 6 cluster)
8. Wrote detailed Codex implementation brief
9. Created machine-readable taxonomy rules (JSON)

## Semantic Level Distribution

| Level | Count | % |
|---|---|---|
| `event_signature` | 29 | 58% |
| `thread_signature` | 8 | 16% |
| `reject` | 12 | 24% |
| `content_signature` | 1 | 2% |

### Key insight

Only 58% of benchmark rows qualify as event_signature. The remaining 42% should either form threads without clustering (16%), be indexed as content only (2%), or be rejected entirely (24%). This four-way split is the single most important change from Phase 1.3's binary accept/reject model.

## Fixture Row Counts

| Fixture File | Rows |
|---|---|
| `regression_fixture_phase1_3b_signature.jsonl` | 33 (all single items) |
| `regression_fixture_phase1_3b_relations.jsonl` | 17 (all pairs + cluster candidates) |
| `regression_fixture_phase1_3b_clusters.jsonl` | 6 (2 event_cluster, 2 thread_candidate, 1 event_cluster fold, 1 reject) |

## Top Taxonomy Changes

1. **Four semantic levels instead of binary accept/reject**: event_signature, thread_signature, content_signature, reject
2. **Chinese action triggers added** for all 19 action types: 发布, 推出, 上线, 开源, 支持, 官宣, 融资, 超过, 套餐, etc.
3. **Action taxonomy expanded** from current implicit set to 19 explicit actions with cluster/thread eligibility defaults
4. **Invalid product rules**: URL fragments, number fragments, date fragments, sentence fragments > 8 words are never valid products
5. **Invalid actor rules**: Former employer, integration target, product-as-org are never valid actors
6. **research_paper demoted**: Paper announcements are thread_signature, not event_signature (different papers = different events)
7. **Recurring format detection**: YC launches, paper feeds, and same-source recurring formats are thread_signature
8. **Coordinated launch detection**: Same-source same-timestamp posts with overlapping content form event clusters

## Top Relation Boundary Decisions

1. **near_duplicate**: Fold (should_fold=True). Cross-language duplicates included. Main post + link follow-up is near_duplicate.
2. **related_with_new_info**: Can seed event cluster. Sequential version releases and coordinated launches.
3. **same_product_different_event**: Thread only, no event cluster. Codex features, YC launches.
4. **same_thread**: Thread only, no event cluster. Same company different topics, same-source philosophy.
5. **different**: False positive from candidate generation. Generic token overlap.
6. **low_signal**: Both items rejected → no relation except deterministic duplicate.

## Top Cluster Seed Rules

**Allowed**:
- near_duplicate with confidence >= 0.85
- related_with_new_info with same concrete event
- Same source + same timestamp + coordinated launch
- Sequential versioned releases of same product
- Cross-source matching actor + product + action

**Disallowed**:
- Generic token overlap (agent, AI, API, model, research, paper, code, cli, data)
- Same source only
- Same actor only
- Same product family only
- same_thread and same_product_different_event relations
- CJK substring overlap without semantic validation
- Recurring feed format without concrete event identity

## Top 10 Codex Implementation Recommendations

1. **Hybrid extraction**: Deterministic fast path for obvious patterns + LLM fallback for complex/Chinese items
2. **Four-level semantic output**: Every item gets event_signature, thread_signature, content_signature, or reject
3. **Chinese language support**: Action triggers for 发布, 推出, 上线, 套餐, 官宣, etc. across all action types
4. **Product name validator**: Reject URL fragments, number fragments, date fragments, sentence fragments > 8 words
5. **Actor disambiguation**: Former employer ≠ actor, integration target ≠ actor, product ≠ organization
6. **Candidate lane split**: event_signature → precision lanes; thread_signature → thread lanes only; reject → no lanes
7. **Cluster seed gating**: Only event_signature items can seed event clusters; thread_signature items cannot
8. **Recurring format detection**: Same-source same-format content (YC launches, paper feeds) → thread_signature
9. **Coordinated launch detection**: Same-source same-timestamp overlapping content → event cluster
10. **Regression test suite**: Run fixture tests before any live run; benchmark FNR < 0.2 and FPR < 0.1

## Known Uncertainties

1. **Human review needed**: All semantic_level assignments are Claude's judgment. The `human_label` field in the benchmark is intentionally empty.
2. **content_signature is under-represented**: Only 1 row in the benchmark. This category may need expansion as more content types are encountered.
3. **Chinese trigger coverage**: Chinese triggers were derived from the 80-item sample. Additional triggers may be needed for broader Chinese content.
4. **LLM extraction cost**: The hybrid approach adds LLM calls. Cost impact should be measured in the 20-item smoke test before scaling.
5. **Cross-language cluster threshold**: The benchmark has only 1 cross-language near-duplicate pair. More evidence is needed for generalizable thresholds.

## Human Review Recommended Before Codex

- [ ] All 50 semantic_level assignments reviewed by a human
- [ ] Chinese trigger lists reviewed by a native Chinese speaker
- [ ] Action taxonomy coverage reviewed against broader RSS sources
- [ ] Cluster seed rules tested against a broader sample (300+ items)
- [ ] LLM prompt few-shot examples reviewed for bias

## Files Created

| File | Size | Purpose |
|---|---|---|
| `signature_benchmark_with_taxonomy.jsonl` | — | 50 rows with semantic_level |
| `signature_benchmark_with_taxonomy.csv` | — | CSV version |
| `signature_taxonomy_recommendations.md` | — | Full taxonomy documentation |
| `signature_taxonomy_rules.json` | — | Machine-readable rules |
| `regression_fixture_phase1_3b_signature.jsonl` | 33 rows | Signature regression tests |
| `regression_fixture_phase1_3b_relations.jsonl` | 17 rows | Relation regression tests |
| `regression_fixture_phase1_3b_clusters.jsonl` | 6 rows | Cluster regression tests |
| `codex_implementation_input.md` | — | Codex implementation brief |
| `step3_summary.md` | — | This file |
