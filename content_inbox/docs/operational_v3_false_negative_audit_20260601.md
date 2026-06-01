# Operational v3 False Negative Audit

**Generated:** 2026-06-01
**Data sources:** Synthetic eval (86 items) + Real scoped run test_cp2_72a8069c (133 items, 12 AI sources)

---

## FN Taxonomy

### Category 1: Same-Source Repeat Post (same_source_repeat)

Same source posts multiple items about the same event. Signature matches but priority capped at `medium` due to conservative scoring.

**Real Examples (from scoped run):**

| # | Score | Source | Title A | Title B | Why Missed |
|---|-------|--------|---------|---------|------------|
| 1 | 6.02 | ChatGPT | GPT-5.5 Instant is starting to roll out to everyone... | GPT-5.5 Instant is rolling out starting today... | priority=medium, lane=same_event_recall |
| 2 | 5.72 | DeepSeek | DeepSeek-V4-Pro discount extended until May 31... | DeepSeek-V4-Pro API 75% OFF until May 5th... | priority=medium, lane=same_event_recall |
| 3 | 3.56 | Meta AI | Today we're introducing TRIBE v2... | Without any retraining, TRIBE v2 can reliably predict... | priority=medium, lane=exploratory_recall |
| 4 | 3.22 | Mistral | Start experimenting with Voxtral Mini Transcribe 2... | Available now. Mini Transcribe 2 via API at $0.003/min... | priority=medium, lane=exploratory_recall |
| 5 | 2.81 | Meta AI | CHMv2 is already supporting public sector efforts... | We're announcing Canopy Height Maps v2... | priority=medium, lane=same_event_recall |
| 6 | 3.63 | OpenAI Devs | Learn about Codex pets... | Show us the Codex pets you hatched... | priority=medium, lane=same_event_recall |

**Root cause:** `assess_candidate` assigns `priority=medium` when same-source + close_time_window + shared_signature but differences in entity overlap or title similarity. The `_relation_from_candidate` only auto-merges `must_run` and `high`.

**Suggested fix:** Upgrade same_source + same_signature + close_time_window (≤72h) to `high` priority. Add `same_source_repeat` lane.

### Category 2: Cross-Source Same Product Release (cross_source_same_product)

Different sources (or different official accounts) report the same product release. Gets `wide_time_window` disqualifier if days differ.

**Real Examples:**

| # | Score | Sources | Description | Why Missed |
|---|-------|---------|-------------|------------|
| 1 | 5.50 | Perplexity + ChatGPT | GPT-5.5 now available on Perplexity vs GPT-5.5 Instant rolling out to ChatGPT | wide_time_window_hours:262.3, priority=medium |
| 2 | 4.26 | Perplexity + ChatGPT | Same pair, different item combination | wide_time_window_hours:262.3, priority=medium |
| 3 | 3.24 | OpenAI Devs + OpenAI | Codex can now help you build AI apps... vs Codex now works directly in Chrome... | generic_overlap:apps, priority=medium |

**Synthetic Examples:**

| # | Pair | Description |
|---|------|-------------|
| 1 | openai_variant_a, openai_variant_b | Title rewrite: "launches GPT-5.5" vs "rolls out new model" |
| 2 | openai_variant_a, url_tracking_a | URL tracking variant |
| 3 | openai_punctuation_variant, openai_variant_a | Punctuation variant |

**Root cause:** Cross-source pairs face more disqualifiers (wide_time_window, generic_overlap). Even when they share product/actor, the priority drops to `medium`.

**Suggested fix:** When same_actor AND same_product AND related_action AND time_window ≤ 7 days, upgrade to `high_uncertain` (goes to DeepSeek or review, not auto-merge).

### Category 3: Pricing/Promotion Event (same_actor_different_pricing)

Same actor announces multiple pricing-related items. May be same pricing event with different aspects or different events.

**Real Examples:**

| # | Score | Source | Title A | Title B | Why Missed |
|---|-------|--------|---------|---------|------------|
| 1 | 4.69 | DeepSeek | Input Cache Price Drop! | V4-Pro discount extended until May 31... | generic_overlap:api, priority=medium |

**Suggested fix:** When same_actor + pricing_action + close_time_window, upgrade to `high_uncertain` lane. Send to DeepSeek with structured evidence.

### Category 4: Cross-Language Same Event (cross_language)

Chinese + English descriptions of the same event. Not present in real scoped data (all English), only in synthetic.

**Synthetic Examples:**

| # | Pair | Description |
|---|------|-------------|
| 1 | deepseek_cn_a, deepseek_cn_b | CN: "深度求索发布面向代码智能体的 V4.1 模型" vs EN: "DeepSeek launches V4.1 model for coding agents" |
| 2 | deepseek_cn_a, guid_a | CN DeepSeek vs EN DeepSeek (GUID variant) |
| 3 | policy_a, policy_b | CN: "欧盟发布 AI 法案实施指南" vs EN: "European Commission publishes AI Act implementation guidance" |

**Root cause:** Alias registry needs expansion for CN↔EN mappings. Current alias hits: 17 (synthetic), 64 (real). But cross-language signatures don't match exactly.

**Suggested fix:** Expand alias registry with CN↔EN actor, product, and action mappings.

### Category 5: Funding Rewrite (funding_event)

Different phrasings for the same funding event. Synthetic only.

**Synthetic Example:**

| # | Pair | Description |
|---|------|-------------|
| 1 | anthropic_funding_a, anthropic_funding_b | "Anthropic raises $X billion" vs "Claude maker secures fresh financing" |

**Root cause:** Action aliases needed: raises↔financing↔funding. Actor alias: Anthropic↔Claude maker.

**Suggested fix:** Expand funding action aliases and actor aliases.

### Category 6: Policy Event (policy_event)

Policy/regulation announcements with different phrasing.

**Synthetic Example:**

| # | Pair | Description |
|---|------|-------------|
| 1 | policy_a, policy_b | "European Commission publishes AI Act guidance" vs "EU发布 AI 法案实施指南" |

**Suggested fix:** Policy actor aliases (European Commission↔EU↔欧盟) and action aliases.

---

## Combined FN Count

| Source | Pairs | Likely Same-Event | Definitely Same-Event |
|--------|-------|-------------------|----------------------|
| Synthetic eval | 8 | 8 | 8 |
| Real scoped run (review only) | 639 | ~15-20 | ~6-10 |

**Conservative estimate:** At least 14-18 false negatives across synthetic + real combined.

---

## Recommended Fix Priority

1. **Fix auto-merge precision bug** (Checkpoint 2 finding): `_relation_from_candidate` must respect `assessment.reason_code == "different_event"`

2. **Upgrade same_source_repeat priority**: same source + same signature + ≤72h → `high` priority → auto-merge or DeepSeek

3. **Expand alias registry**: CN↔EN mappings, Anthropic↔Claude maker, EU↔European Commission↔欧盟

4. **Add cross_source_same_product lane**: same actor + same product + related action + ≤7 days → `high_uncertain` → DeepSeek

5. **Add funding/policy action aliases**: raises↔financing↔funding, publishes↔releases↔announces

6. **Relax time bucket for follow-ups**: ≤7 days for same_source follow-up angles → `high_uncertain`

---

## Files To Modify (for Checkpoint 4)

- `app/semantic/operational_pipeline.py`: Fix `_relation_from_candidate` precision bug; add new lanes
- `app/semantic/signatures.py`: Expand alias registry
- `app/semantic/candidates.py`: Add new lanes and scoring adjustments
- `tests/test_semantic_phase1.py`: Add FN fixture tests
