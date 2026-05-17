# Codex Phase 1.3c Focused Repair Input

## 1. Current State Summary

Phase 1.3b 300-item dry-run metrics:

| Metric | Value | Gate | Status |
|---|---|---|---|
| Items evaluated | 300 | — | — |
| Total tokens | 877,140 | — | — |
| Tokens per item | 2923.8 | < 2000 | FAIL |
| event_signature_valid_rate | 0.9821 | >= 0.6 | PASS |
| Chinese event detection rate | 0.3846 | >= 0.5 | FAIL |
| Effective multi-item clusters | 2 | >= 1 | PASS |
| Suspect multi-item clusters | 0 | 0 | PASS |
| Final LLM failures | 31 | low | FAIL |
| Parse failures | 2 | — | — |
| Must-run skips | 0 | 0 | PASS |
| Pair conflicts | 0 | 0 | PASS |
| Accepted garbage products | 4+ found | 0 | FAIL |

**Verdict**: NOT_READY_FOR_SCOPED_REAL_SEMANTIC_WRITE

## 2. Files Likely to Modify

### Primary Modification Targets

| File | Purpose | Priority |
|---|---|---|
| `app/semantic/signatures.py` | Deterministic signature extraction — add Chinese triggers, fix garbage product detection, improve actor extraction | P0 |
| `app/semantic/config.py` | Thresholds, stopwords, action aliases — add Chinese trigger lists, garbage patterns | P0 |
| `app/semantic/candidates.py` | Candidate pair generation — filter out reject/content_signature items from LLM relation path | P1 |
| `app/semantic/relations.py` | Relation processing — reduce batch size, improve JSON repair | P2 |
| `app/semantic/relation_policy.py` | Relation label normalization — rule-based handling for same_thread/same_product lanes | P2 |
| `app/semantic/cluster_policy.py` | Cluster attach/seed rules — verify no regression | P3 |
| `app/semantic/readiness.py` | Readiness gates — validate tightened checks work | P3 |
| `prompts/event_signature_v1.md` | LLM signature prompt — add Chinese examples, JSON contract hardening | P1 |
| `prompts/item_relation_v3.md` | Relation prompt — reduce batch size, add JSON format anchor | P2 |
| `tests/fixtures/semantic_signature_benchmark_phase1_3b.jsonl` | Add delta benchmark rows | P1 |

### Do NOT Modify
- Console UI templates/static files
- `prompts/item_card_v1.md` (card quality is acceptable)
- `prompts/item_cluster_relation_v3.md` (cluster relations had 0 failures)
- Production DB files

## 3. Exact Repairs Requested (by Priority)

### P0: Validate Validator Tightening With Focused Rerun

**Problem**: Codex tightened product validation after the 300-run, but the tightening hasn't been validated in a live run.

**Actions**:
1. Run 80-item focused validation (`semantic --dry-run --source-scope api.xgo.ing --max-items 80`) after applying the validator rules from `phase1_3c_product_validator_rules.json`
2. Confirm `accepted_garbage_product_count = 0` in the rerun
3. Verify no valid products are rejected (check OpenShell, LangSmith Fleet, GitHub Copilot Desktop, etc.)
4. If garbage products still appear, apply the specific blocker rules from the product validator rules JSON

**Success criteria**: 0 accepted garbage products AND all known valid products pass.

### P1: Improve Chinese Event Recall

**Problem**: Chinese detection rate 0.3846 (15/50 Chinese items get event_signature). 4 likely false negative events, 7 likely false negative threads found.

**Root causes identified** (from `phase1_3c_chinese_event_misses.md`):
1. Missing trigger coverage — several Chinese event trigger groups have zero hits
2. Weak entity extraction — Chinese item cards fail to identify actors/products
3. Validator over-rejection — `missing_concrete_actor_or_product` rejects valid Chinese items
4. LLM fallback not invoked for Chinese event-like items

**Actions**:
1. Add to `signatures.py` the complete Chinese trigger list from `phase1_3c_chinese_trigger_recommendations.md`:
   - `技术预览/预览版/内测/公测` → `availability`
   - `套餐/免费/降价/价格/折扣/优惠` → `pricing`
   - `超过/超越/领先/采用率/市场份额/用户数/增长` → `adoption_metric`
   - `官宣/新公司/联合创始人/创业/成立/融资` → `company_launch`
   - `大会/活动/直播/研讨会/峰会/报名` → `event`
   - `评测/跑分/榜单/基准/准确率` → `benchmark`
2. Force LLM fallback when: item has CJK characters + detected product entity + event-like trigger
3. Reduce `missing_concrete_actor_or_product` rejection severity for Chinese items with detected entities
4. Test with benchmark Chinese items (target: >= 0.75 detection rate on benchmark)

**Success criteria**: Chinese event detection rate >= 0.5 in live dry-run.

### P2: Enforce Product/Actor Validator Rules

**Problem**: 36 blocker-level garbage product/actor findings, 74 warning-level. Examples: random tokens (sow0e7ym, iobqd8a9), date fragments (May 4th, June 4th), numeric fragments (around 1897, of 12M), long phrases as products.

**Actions**:
1. Apply all 10 product validator rules from `phase1_3c_product_validator_rules.json`
2. Apply actor validator rules: former employer ≠ actor, product ≠ organization, prefer empty over wrong
3. Add exceptions list for known valid products
4. Add `reject product if matches short alphanumeric pattern` as a hard blocker
5. Add `reject product if starts with verb phrase` (e.g., "Give Your Chat Agent", "Meet Replit Parallel Agents")

**Success criteria**: 0 accepted garbage products AND valid products preserved.

### P3: Reduce Final LLM Failures

**Problem**: 31 final failures, all JSON parse errors from deepseek-v4-flash. 28/31 in item_relation stage. 18 unterminated strings, 5 empty outputs, 3 missing commas, 3 unquoted properties, 2 schema validation.

**Actions**:
1. **Reduce item_relation batch size**: From 8-9 pairs to 4-5 pairs per call (addresses unterminated strings — smaller output = less truncation)
2. **Add split retry**: When batch of N fails, split into 2 batches of N/2
3. **Schema relaxation**: Accept both string and list for `new_information`, `same_event_evidence`, `new_info_evidence` fields — auto-coerce to list
4. **JSON repair**: Ensure json_repair path is triggered for unterminated string errors (currently 0 json_repair calls despite 31 failures)
5. **Strict JSON mode**: Verify API calls use `response_format: { type: "json_object" }`

**Success criteria**: Final failures reduced to < 10 in 300-item run, with remaining failures categorized.

### P4: Reduce Token Cost Per Item

**Problem**: 2923.8 tokens/item, target < 2000. item_relation consumes 61.5% of tokens (539,265).

**Actions** (ranked by savings/risk):
1. **Skip relation LLM for reject/content_signature items** (~150K savings, low risk) — reject+content_signature items don't form meaningful event relations
2. **Reduce item_relation batch size** (~80K savings) — also fixes P3 failure rate
3. **Trim item_card fields in relation prompts** (~60K savings, low risk) — send title + signature + key entities, not full summary
4. **Rule-based handling for same_thread/same_product_different_event** (~50K savings, medium risk) — 90 same_product + 11 same_thread don't need LLM
5. **Skip LLM for high-confidence deterministic releases** (~20K savings, low risk)

**Success criteria**: tokens_per_item < 2200 in initial pass, trending toward < 2000.

### P5: Review and Protect Effective Clusters

**Problem**: Only 2 effective clusters, both `likely_valid`. Need quality review before any real DB write.

**Findings** (from `phase1_3c_effective_cluster_review.md`):
1. **Codex Chrome extension cluster** (3 members, same source, 0-day window): Valid event cluster but members may be near_duplicates from same source — consider folding.
2. **DeepSeek V4 open-source cluster** (2 members, 2 sources, 0.28-day window): Valid event cluster but product field is garbage (`com 1Dl` → should be `DeepSeek-V4 Preview`).

**Actions**:
1. Fix DeepSeek product before DB write
2. Verify Codex cluster members are distinct (not near_duplicates of same tweet)
3. Do NOT relax cluster seed rules to inflate count
4. Run cluster quality checks from `phase1_3c_cluster_quality_recommendations.md`

## 4. New/Updated Tests

### Fixture Additions (from delta benchmark)

Add 30 delta benchmark rows to `tests/fixtures/semantic_signature_benchmark_phase1_3b.jsonl`:
- Chinese false negatives (4 items): Verify Chinese event triggers → event_signature
- Garbage product blockers (12 items): Verify URL/date/random/numeric products rejected
- Valid products (6 items): Verify OpenShell, LangSmith Fleet, GitHub Copilot Desktop, etc. survive
- Cluster members (5 items): Verify cluster member signatures stay correct

### New Test Cases

```python
# In test_semantic_signature_fixtures.py:
def test_chinese_event_triggers_produce_event_signature():
    """Chinese items with event triggers must not be rejected."""

def test_garbage_products_are_rejected():
    """URL fragments, random tokens, dates, numbers must not be products."""

def test_valid_products_survive_validator():
    """Known valid products must pass tightened validation."""

def test_relation_json_parse_errors_trigger_split_retry():
    """JSON parse failures in item_relation must trigger split retry."""
```

## 5. Live Evaluation Sequence

```
1. Run fixture tests:
   cd content_inbox && PYTHONPATH=. pytest tests/test_semantic_signature_fixtures.py tests/test_semantic_relation_fixtures.py tests/test_semantic_cluster_fixtures.py -q

2. Focused 80-item validation (after P0+P1+P2 fixes):
   python -m app.semantic evaluate --source-scope api.xgo.ing --max-items 80 --dry-run

3. Check 80-item gates:
   - chinese_event_detection_rate >= 0.5
   - accepted_garbage_product_count = 0
   - event_signature_valid_rate >= 0.6
   - final_failures < 5

4. If 80-item passes, run 300-item validation:
   python -m app.semantic evaluate --source-scope api.xgo.ing --max-items 300 --dry-run

5. If ALL gates pass on 300-item dry-run:
   - Run small scoped real-write rehearsal (5-10 items, verified clusters only)
   - Check DB integrity after write
   - Report final verdict
```

## 6. Readiness Gates (Codex Must Verify)

```json
{
  "hard_gates": {
    "chinese_event_detection_rate": ">= 0.5",
    "accepted_garbage_product_count": "= 0 (validated by rerun)",
    "event_signature_valid_rate": ">= 0.6",
    "effective_multi_item_clusters": ">= 1",
    "suspect_multi_item_clusters": "= 0",
    "must_run_skip_count": "= 0",
    "pair_conflicts": "= 0"
  },
  "soft_gates": {
    "tokens_per_item": "< 2200 (ideally < 2000)",
    "final_llm_failures": "< 10 (and categorized)",
    "benchmark_chinese_detection": ">= 0.75 (fixtures)",
    "benchmark_fnr": "< 0.15",
    "benchmark_fpr": "= 0.0"
  },
  "rehearsal_gate": {
    "small_scoped_real_write_rehearsal": "only if ALL hard gates + soft gates pass"
  }
}
```

## 7. Do-Not-Do List

Explicitly tell Codex:

- **Do NOT broad rewrite the pipeline.** This is a focused repair pass.
- **Do NOT change console UI.** No template/static changes.
- **Do NOT perform real semantic write unless ALL gates pass.**
- **Do NOT hard-code benchmark item IDs/titles.** Use semantic patterns and rules.
- **Do NOT optimize only for fixtures at expense of real 300-run quality.**
- **Do NOT relax cluster seed rules just to increase cluster count.** 2 good > 5 bad.
- **Do NOT change model/provider** unless JSON reliability is proven.
- **Do NOT add new prompt versions** — modify existing v1/v3 prompts only.
- **Do NOT change the semantic_level taxonomy** (event/thread/content/reject).
- **Do NOT remove the `extract_event_signature` deterministic fast path** — it handles 83% of items without LLM.

## 8. Key Diagnostic Artifacts to Reference

All in `content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep/`:

| File | Content |
|---|---|
| `phase1_3c_chinese_event_misses.md` | 50 Chinese items analyzed, 11 FN, trigger gaps |
| `phase1_3c_chinese_trigger_recommendations.md` | Specific trigger additions with risk assessment |
| `phase1_3c_garbage_product_audit.md` | 110 suspicious fields (36 blockers) |
| `phase1_3c_product_validator_rules.json` | 10 machine-readable product rules |
| `phase1_3c_actor_validator_rules.md` | 4 actor validation rules |
| `phase1_3c_llm_failure_breakdown.md` | 31 failures categorized by type |
| `phase1_3c_prompt_contract_repair_recommendations.md` | Specific JSON/protocol fixes |
| `phase1_3c_token_cost_attribution.md` | Per-stage token breakdown |
| `phase1_3c_token_reduction_recommendations.md` | 8 ranked reduction actions |
| `phase1_3c_effective_cluster_review.md` | 2 clusters reviewed, verdicts |
| `phase1_3c_delta_benchmark.jsonl` | 30-row delta benchmark |
| `phase1_3c_delta_fixture_recommendations.md` | Fixture integration guidance |

## 9. Expected Outputs from Codex

After focused repair:

1. **phase1_3c_focused_80_validation_report.md** — 80-item rerun results
2. **phase1_3c_300_rerun_report.md** — 300-item rerun (if 80 passes)
3. **phase1_3c_readiness_report.md** — All gates checked
4. **phase1_3c_scoped_write_rehearsal_report.md** — If gates pass and rehearsal runs
5. **Final verdict**: `READY_FOR_SCOPED_REAL_SEMANTIC_WRITE` or `NOT_READY`

## 10. Estimated Repair Scope

- **Files modified**: 6-8 Python files + 1-2 prompt files
- **New test code**: ~50 lines (Chinese detection + garbage product tests)
- **Fixture additions**: 20-30 rows
- **New production code**: 0 files
- **Risk of regression**: Low — all changes are additive or tightening existing behavior
