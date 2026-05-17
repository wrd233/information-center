# Codex Implementation Input — Phase 1.3b Step 3

**Purpose**: Provide a detailed, actionable implementation brief for the next Codex pass.
**Source**: 50-row benchmark, Phase 1.3 evidence, taxonomy analysis
**Target**: `content_inbox/app/semantic/` pipeline

---

## A. Recommended Approach: Hybrid Extraction

### Architecture

```
Item → content_role classifier (existing)
     → language detection (new, lightweight)
     → deterministic fast path (expanded)
         ├─ versioned release pattern: "ProductName vX.Y.Z"
         ├─ YC launch pattern: "Congrats on the launch, @..."
         ├─ paper link pattern: "paper: https://..."
         ├─ explicit release: "announces|launches|releases|ships ProductName"
         └─ Chinese release: "发布|推出|上线|开源 ProductName"
     → LLM-backed extraction (for items that pass fast-path confidence < 0.7)
         ├─ structured prompt with few-shot examples
         ├─ outputs: semantic_level, actor, product, action, object, date_bucket, confidence
         └─ validator post-processing
     → validator (strict rules from signature_taxonomy_rules.json)
         ├─ reject URL fragments as products
         ├─ reject number/date fragments as products
         ├─ reject sentence fragments > 8 words as products
         ├─ reject former-employer-as-actor
         ├─ reject integration-target-as-actor
         └─ apply accept/reject rules from taxonomy
     → final semantic_level assignment
```

### When to use LLM vs deterministic

**Deterministic only** (skip LLM):
- Versioned release matched by regex (e.g., "OpenShell v0.0.40")
- Y Combinator launch format ("Congrats on the launch, @X & @Y!")
- "paper:" format link posts (assign thread_signature, research_paper action)
- Items with content_role=low_signal or title < 4 words (reject immediately)

**LLM-backed** (deterministic uncertain or high-potential):
- Chinese-language items
- Items with concreteness_score 0.4-0.7
- Items where deterministic gives action=other but entities exist
- Items where deterministic product is a phrase fragment > 3 words
- Candidate-bearing items (selected_for_relation=True)

**LLM must NOT**:
- Create clusters directly (cluster policy stays deterministic/gated)
- Modify content_role or entities (those come from separate passes)
- Make fold decisions (fold policy stays deterministic)

---

## B. LLM Prompt Design

### Input to LLM

```json
{
  "title": "string",
  "short_summary": "string (from item_card)",
  "source_name": "string",
  "published_at": "ISO8601",
  "content_role": "source_material|firsthand|commentary|aggregator|analysis|report",
  "entities": ["array of extracted named entities"],
  "event_hint": "string (from item_card)",
  "language": "en|zh|mixed"
}
```

### Output from LLM (structured JSON)

```json
{
  "semantic_level": "event_signature|thread_signature|content_signature|reject",
  "actor": "string (empty if none)",
  "product_or_model": "string (empty if none)",
  "action": "release|feature_update|availability|pricing|benchmark|ranking|adoption_metric|case_study|integration|partnership|funding|company_launch|research_paper|technical_blog|security|event|tutorial|opinion_analysis|other",
  "object": "string (additional details, empty if none)",
  "date_bucket": "YYYY-MM-DD",
  "confidence": 0.0-1.0,
  "is_event_like": true|false,
  "is_thread_like": true|false,
  "reject_reason": "string (if semantic_level=reject)",
  "extraction_notes": "string (optional, for diagnostics)"
}
```

### Few-shot examples to include in prompt

**Example 1 — Chinese release (event_signature)**:
```
Input: { "title": "Google 刚刚发布了一个新东西：Googlebook", "source_name": "小互(@imxiaohu)", "content_role": "analysis", "entities": ["Google", "Googlebook", "Gemini"], "language": "zh" }
Output: { "semantic_level": "event_signature", "actor": "Google", "product_or_model": "Googlebook", "action": "release", "object": "Gemini-powered AI Laptop platform", "date_bucket": "2026-05-12", "confidence": 0.9, "is_event_like": true, "is_thread_like": false }
```

**Example 2 — Same-source paper feed (thread_signature)**:
```
Input: { "title": "paper: https://t.co/fkR2wVD129", "source_name": "AK(@_akhaliq)", "content_role": "source_material", "entities": ["paper", "HuggingFace"], "language": "en" }
Output: { "semantic_level": "thread_signature", "actor": "", "product_or_model": "HuggingFace paper", "action": "research_paper", "object": "", "date_bucket": "2026-05-13", "confidence": 0.6, "is_event_like": false, "is_thread_like": true, "extraction_notes": "Link-only paper post. Product is URL fragment. Thread-like for same-source paper feed." }
```

**Example 3 — Low-signal social (reject)**:
```
Input: { "title": "Great advice", "source_name": "Lenny Rachitsky(@lennysan)", "content_role": "report", "entities": ["Great", "Grant", "Lee"], "language": "en" }
Output: { "semantic_level": "reject", "actor": "", "product_or_model": "", "action": "other", "object": "", "date_bucket": "2026-05-12", "confidence": 0.95, "is_event_like": false, "is_thread_like": false, "reject_reason": "Generic social engagement with no concrete actor, product, or event." }
```

**Example 4 — Chinese pricing (event_signature, critical false-negative fix)**:
```
Input: { "title": "上海电信直接把 Token 做成话费套餐了。1块钱25万token", "source_name": "orange.ai(@oran_ge)", "content_role": "report", "entities": ["上海电信", "Token", "话费套餐"], "language": "zh" }
Output: { "semantic_level": "event_signature", "actor": "China Telecom Shanghai", "product_or_model": "Token calling plan", "action": "pricing", "object": "1 RMB per 250K tokens", "date_bucket": "2026-05-16", "confidence": 0.7, "is_event_like": true, "is_thread_like": false }
```

### Prompt construction rules

1. Include 6-8 few-shot examples covering: English release, Chinese release, Chinese pricing, paper feed, low-signal reject, YC launch, versioned release, integration
2. System prompt: "You are extracting structured event signatures from social media content about AI/tech. Classify into event_signature, thread_signature, content_signature, or reject. Be precise about actor (who made/did this), product (what was released/changed), and action (what happened). Never use URL fragments, version numbers alone, or sentence fragments as product names."
3. Temperature: 0.1 (low — this is extraction, not generation)
4. Max tokens: 300 (output is compact JSON)
5. Model: deepseek-v4-flash (cost-efficient for extraction)

---

## C. Candidate Lane Changes

### Current problem

Phase 1.3 candidate generation treated all items equally. This produced 307 low-priority candidates from generic token overlap.

### Proposed lane assignment based on semantic_level

| Semantic Level | Candidate Lanes | Rationale |
|---|---|---|
| `event_signature` | `precision_event`, `same_event_recall` | Can match with other event_signatures for same-event clustering |
| `thread_signature` | `same_thread`, `same_product_different_event` | Can match with related thread_signatures for thread construction |
| `content_signature` | (none — no relation lanes) | Only search/source profile indexing |
| `reject` | (none — skip all relation processing) | Only deterministic exact-duplicate check |

### Lane definitions

- **precision_event**: High-confidence same-event matching. Requires matching actor + product + action. Used for event cluster seeds.
- **same_event_recall**: Broader same-event recall. Requires matching actor + product. Allows different actions if same timestamp window.
- **same_thread**: Thread construction. Same source, same product family, same company. Does NOT create event clusters.
- **same_product_different_event**: Different events for same product. Informational relation only.

### Budget allocation

- `precision_event` lane: protected budget (must-run candidates)
- `same_event_recall` lane: standard budget
- `same_thread` lane: lower priority budget
- Items with `semantic_level=reject`: consume zero relation budget

---

## D. Readiness Gate Changes

### Proposed gates (replacing Phase 1.3 gates)

| Gate | Threshold | Measures |
|---|---|---|
| `event_signature_valid_rate` | >= 0.6 | Fraction of event_signature items with valid (actor + product + non-other action) |
| `event_signature_benchmark_fnr` | < 0.2 | False negative rate on benchmark event_signature rows |
| `event_signature_benchmark_fpr` | < 0.1 | False positive rate (reject classified as event_signature) |
| `thread_signature_precision` | >= 0.7 | Fraction of thread_signature items that are correctly not event_signature |
| `near_duplicate_precision` | >= 0.8 | Fraction of near_duplicate pairs that are true duplicates |
| `related_with_new_info_precision` | >= 0.7 | Fraction of related_with_new_info pairs that are same event |
| `effective_multi_item_clusters` | >= 1 | At least one useful multi-item event cluster formed |
| `suspect_multi_item_clusters` | = 0 | No broad-topic clusters from generic tokens |
| `must_run_skip_count` | = 0 | Zero must-run candidates skipped |
| `item_card_fallback_rate` | < 0.05 | LLM extraction fallback rate stays low |
| `tokens_per_item` | < 2000 | Cost efficiency |
| `chinese_event_detection_rate` | >= 0.5 | Fraction of Chinese event items correctly classified |
| `small_scoped_real_write_rehearsal` | True | Scoped write rehearsal completed successfully |

### Benchmark integration

Before any live run, the fixture regression suite must pass:

```bash
PYTHONPATH=. python3 -m pytest tests/test_semantic_signature_fixtures.py -q
PYTHONPATH=. python3 -m pytest tests/test_semantic_relation_fixtures.py -q
PYTHONPATH=. python3 -m pytest tests/test_semantic_cluster_fixtures.py -q
```

---

## E. Live Evaluation Sequence

```
1. Fixture-only test (no API calls)
   └─ Validate signature extraction against 33 signature fixtures
   └─ Validate relation classification against 17 relation fixtures
   └─ Validate cluster formation against 6 cluster fixtures
   └─ MUST PASS before any live run

2. 20-item live smoke test
   └─ Run on final 20 items from Phase 1.3 evidence
   └─ Verify: event_signature_valid_rate > 0, no must-run skips
   └─ Verify: no Chinese events classified as reject

3. 80-item live run
   └─ Run on full round_c_80_live_tuned dataset
   └─ Compare semantic_level distribution against benchmark expectations
   └─ Verify: at least one Notion-like event cluster appears

4. 300-item api.xgo.ing event_hotspots run
   └─ Full scale test with real event_hotspots sampling
   └─ Verify: no broad-topic clusters from generic AI tokens
   └─ Verify: Chinese event detection rate >= 0.5

5. Readiness report
   └─ Generate all gates and metrics
   └─ Compare against Phase 1.3 baseline

6. Scoped real-write rehearsal (ONLY if all gates pass)
   └─ Small scope (1-2 sources, 20 items)
   └─ Write to test DB, verify, rollback
   └─ Confirm no data corruption
```

---

## F. Files to Modify (NOT in this step — for Codex)

These are the files Codex should target, listed for planning:

| File | Change |
|---|---|
| `app/semantic/signatures.py` | Replace `extract_event_signature()` with hybrid approach. Add `deterministic_fast_path()`, `llm_signature_pass()`, `validate_signature()`. Add `assign_semantic_level()`. |
| `app/semantic/evidence.py` | Add `semantic_level` field to output schemas. |
| `app/semantic/relations.py` | Update candidate lane assignment based on `semantic_level`. Add `thread_signature` lane. |
| `app/semantic/clusters.py` | Update cluster seed rules. Prevent thread_signature from seeding event clusters. |
| `app/semantic/prompts.py` or new file | Add LLM signature extraction prompt with few-shot examples. |
| `config/` | Add `signature_taxonomy_rules.json` reference. Add Chinese trigger lists. |
| `tests/fixtures/` | Add `semantic_signature_benchmark_phase1_3b.jsonl`, `semantic_relation_benchmark_phase1_3b.jsonl`, `semantic_cluster_benchmark_phase1_3b.jsonl`. |
| `tests/test_semantic_signature_fixtures.py` | New test: validate signature extraction against fixtures. |
| `tests/test_semantic_relation_fixtures.py` | New test: validate relation classification against fixtures. |
| `tests/test_semantic_cluster_fixtures.py` | New test: validate cluster formation against fixtures. |

---

## G. Expected Success Criteria

After Codex implementation:

1. **Benchmark event signature false negative rate < 0.2**: Shanghai Telecom, Stelline Dev Kit, LangSmith Fleet, LangChain Interrupt must all be event_signature
2. **Accepted signatures are no longer garbage**: No URL fragments, number fragments, or 60+ character phrases as product names
3. **Chinese release/pricing/availability detected**: Googlebook (发布), Shanghai Telecom (套餐), GitHub Copilot (技术预览) all accepted
4. **must_run_skip_count = 0**: No protected candidates skipped due to budget
5. **pair_conflicts = 0**: No conflicting relation verdicts
6. **At least one Notion-like event cluster appears**: Coordinated same-source launch detected
7. **No broad-topic cluster**: No cluster formed from generic AI/agent/API/research/paper token overlap
8. **YC launches threaded, not clustered**: Recurring format correctly identified as thread_signature
9. **AK paper feed threaded, not clustered**: Same-source paper format correctly identified as thread_signature
10. **Phase 1.3 over-rejection fixed**: At least 5 of the 8 false negative items now correctly classified
