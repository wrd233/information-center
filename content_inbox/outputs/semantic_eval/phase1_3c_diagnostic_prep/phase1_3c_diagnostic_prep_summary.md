# Phase 1.3c Diagnostic Prep — Final Summary

## Files Analyzed

From `content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600/`:
- `semantic_items.jsonl` (300 items)
- `item_cards.jsonl` (300 cards)
- `event_signatures.jsonl` (300 signatures)
- `semantic_levels.jsonl` (300 deterministic levels)
- `llm_calls.jsonl` (330 LLM call records)
- `llm_errors.jsonl` (31 error records)
- `clusters_final.jsonl` (110 clusters)
- `relations_all.jsonl` (all relations)
- `stage_metrics.json` (cost/timing data)
- `phase1_3b_final_summary.md` / `.json`
- `phase1_3b_readiness_report.md` / `.json`

Also referenced:
- `phase1_3b_signature_benchmark_step1/` (existing 50-row benchmark)
- `phase1_3b_taxonomy_regression_step3/` (regression fixtures)

## Files Created (27 total)

All in `content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep/`:

### Task A — Chinese Event Detection (4 files)
- `phase1_3c_chinese_event_misses.md`
- `phase1_3c_chinese_event_misses.jsonl`
- `phase1_3c_chinese_trigger_recommendations.md`
- `phase1_3c_chinese_event_summary.json`

### Task B — Garbage Product Audit (5 files)
- `phase1_3c_garbage_product_audit.md`
- `phase1_3c_garbage_product_audit.jsonl`
- `phase1_3c_product_validator_rules.md`
- `phase1_3c_product_validator_rules.json`
- `phase1_3c_actor_validator_rules.md`

### Task C — LLM Failure Breakdown (4 files)
- `phase1_3c_llm_failure_breakdown.md`
- `phase1_3c_llm_failure_breakdown.json`
- `phase1_3c_llm_failure_examples.jsonl`
- `phase1_3c_prompt_contract_repair_recommendations.md`

### Task D — Token Cost Attribution (4 files)
- `phase1_3c_token_cost_attribution.md`
- `phase1_3c_token_cost_attribution.json`
- `phase1_3c_token_reduction_recommendations.md`
- `phase1_3c_high_cost_examples.jsonl`

### Task E — Effective Cluster Review (4 files)
- `phase1_3c_effective_cluster_review.md`
- `phase1_3c_effective_cluster_review.json`
- `phase1_3c_cluster_member_table.csv`
- `phase1_3c_cluster_quality_recommendations.md`

### Task F — Delta Benchmark (4 files)
- `phase1_3c_delta_benchmark.jsonl`
- `phase1_3c_delta_benchmark.csv`
- `phase1_3c_delta_benchmark.md`
- `phase1_3c_delta_fixture_recommendations.md`

### Task G — Codex Repair Input + Summary (2 files)
- `codex_phase1_3c_focused_repair_input.md`
- `phase1_3c_diagnostic_prep_summary.md` (this file)

### Diagnostic Scripts (7 files in `tools/`)
- `tools/analyze_chinese_misses.py`
- `tools/audit_garbage_products.py`
- `tools/breakdown_llm_failures.py`
- `tools/attribute_token_costs.py`
- `tools/review_effective_clusters.py`
- `tools/build_delta_benchmark.py`
- `tools/` directory

## Chinese Recall Findings

- **50 Chinese/mixed items** found in the 300-run (16.7% of items)
- **15 items** received `event_signature` (detection rate: 0.3 by item count, 0.3846 by the readiness gate formula)
- **4 likely false negative events**: Chinese items that are event-like but were classified as reject or thread
- **7 likely false negative threads**: Chinese items that should be thread_signature but got reject
- **10 trigger groups have coverage**, but the uncovered triggers are for `技术预览/内测/公测`, `漏洞/安全/修复/补丁`
- Root causes: missing trigger coverage for some groups, weak entity extraction from Chinese text, validator over-rejection, LLM fallback not invoked for Chinese items

## Garbage Product Findings

- **110 suspicious field instances** across non-reject signatures
- **36 blockers**: random alphanumeric tokens (sow0e7ym, iobqd8a9, ay4dy8o5, CERX3N35, etc.), date/month-day phrases (May 4th, June 4th), numeric fragments (around 1897, of 12M, a 24, up 130), URL fragments (com 1Dl), "for every" patterns (Git semantics for every file your agent)
- **74 warnings**: long phrases > 6 words, sentence punctuation in product names, verb-starting products, weak preposition starts
- **10 product validator rules** and **4 actor validator rules** generated as machine-readable JSON
- Known valid products that must NOT be rejected: OpenShell v0.0.40+, LangSmith Fleet, GitHub Copilot Desktop, NVIDIA Nemotron 3 Nano Omni, Shanghai Telecom Token calling plan, etc.

## LLM Failure Findings

- **All 31 failures are genuine JSON parse errors** from deepseek-v4-flash — not control-flow/budget miscounts
- **28/31 (90%)** are in `item_relation` stage
- Failure breakdown:
  - 18 unterminated strings (58%) — output truncation
  - 5 empty/non-JSON outputs (16%) — model returns blank
  - 3 missing commas (10%) — malformed JSON arrays
  - 3 unquoted properties (10%) — missing double quotes
  - 2 schema validation (6%) — string instead of list
- **15 of 31** succeed on single retry; 0 succeed on split retry
- **0 json_repair calls** were made despite 31 JSON failures — repair path not triggered
- **Prompt variant**: `short` variant had 25 failures, `full` variant had 6 failures — `short` variant is more fragile

## Token Cost Attribution

- **Total**: 877,140 tokens across 220 calls (2923.8 tokens/item)
- **By stage**:
  - item_relation: 539,265 tokens (61.5%) — 157 calls, 28 failed
  - item_card: 282,644 tokens (32.2%) — 54 calls, 3 failed
  - item_cluster_relation: 48,727 tokens (5.6%) — 6 calls, 0 failed
  - cluster_card_patch: 6,504 tokens (0.7%) — 3 calls, 0 failed
- **Cache hit rate**: 26.92% (236,160 cache-hit tokens)
- **Failure tokens**: ~estimated 15-20% of total tokens wasted on failed calls
- **Top recommendation**: Skip relation LLM for reject/content_signature items (saves ~150K tokens, low risk)
- **8 ranked recommendations** with savings estimates, quality risk, difficulty

## Cluster Review

- **2 effective multi-item clusters** (both `likely_valid`):
  1. **OpenAI Codex Chrome extension** (3 members, 1 source, 0-day window): Valid event but members from same source at same time — possible near_duplicates
  2. **DeepSeek V4 open-source** (2 members, 2 sources, 0.28-day window): Valid event but product is garbage (`com 1Dl` → should be `DeepSeek-V4 Preview`)
- **0 suspect clusters** — precision is good
- Both clusters can be written to DB after minor fixes (product correction for DeepSeek, duplicate check for Codex)
- Cluster seed rules are appropriately conservative — do not relax

## Delta Benchmark

- **30 rows** selected from 300-run evidence
- **Distribution**:
  - Chinese false negatives: 4 items
  - Garbage product blockers: 12 items
  - Valid products (must survive): 6 items
  - Cluster members: 5 items
  - Failure-related: 3 items
- Complements the existing 50-row Step 1 benchmark
- Avoids duplicating existing benchmark item IDs

## Top 10 Codex Repair Recommendations

1. **Add Chinese triggers and force LLM fallback for Chinese items** (P1)
2. **Apply 10 product validator rules to block garbage products** (P0)
3. **Reduce item_relation batch size from 8-9 to 4-5 pairs** (P2/P3)
4. **Add split retry for JSON parse failures in item_relation** (P3)
5. **Skip relation LLM for reject/content_signature items** (P4)
6. **Relax schema: accept string or list for evidence fields** (P3)
7. **Fix DeepSeek cluster product: `com 1Dl` → `DeepSeek-V4 Preview`** (P5)
8. **Validate validator tightening with 80-item rerun** (P0)
9. **Add delta benchmark fixtures to regression tests** (P1)
10. **Trim item_card fields in relation prompts for token savings** (P4)

## Whether Codex Should Proceed Immediately

**Yes, proceed with focused repair.** The diagnostic analysis is complete and the repair actions are concrete and well-scoped. The 31 LLM failures are well-understood (JSON parse), the garbage products have clear patterns, and the Chinese detection gaps have specific missing triggers identified.

## Remaining Uncertainties Requiring Human Review

1. **Chinese item classification**: 3 items classified as `uncertain_needs_human_review` — a Chinese speaker should verify these
2. **Cluster near_duplicate status**: Whether the 3 Codex cluster members are truly distinct or near_duplicates of the same tweet needs human verification
3. **DeepSeek model reliability**: If JSON parse failures persist after batch size reduction, consider switching from `deepseek-v4-flash` to `deepseek-v4` for relation tasks
4. **Token budget vs quality tradeoff**: Some token reduction recommendations may impact relation quality — human review needed on the quality/speed tradeoff
