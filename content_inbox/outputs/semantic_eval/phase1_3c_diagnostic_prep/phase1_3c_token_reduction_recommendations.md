# Phase 1.3c Token Reduction Recommendations

Current: 2923.8 tokens/item. Target: < 2000 tokens/item.
Savings needed: ~277,140 tokens (31.6% reduction)

## Ranked Recommendations

### 1. Reduce item_relation batch size from 8-9 to 4-5 pairs

- **Expected savings**: 80,000-120,000 tokens (item_relation is 61.5% of total, smaller batches reduce output tokens)
- **Quality risk**: Low — smaller batches actually improve JSON reliability
- **Difficulty**: Low — config change
- **Priority**: P0

### 2. Skip relation LLM for reject and content_signature items

- **Expected savings**: ~150,000 tokens (reject+content_signature ~60% of items don't need pair relations)
- **Quality risk**: Low — these items rarely form meaningful relations
- **Difficulty**: Low — filter in candidates.py
- **Priority**: P0

### 3. Use deterministic rule-based relations for same_thread and same_product_different_event lanes

- **Expected savings**: ~50,000 tokens (90 same_product_different_event + 11 same_thread currently go through LLM)
- **Quality risk**: Medium — need careful rule design
- **Difficulty**: Medium — requires relation_policy.py changes
- **Priority**: P1

### 4. Trim item_card fields passed into relation prompts — send only title + signature + key entities, not full summary

- **Expected savings**: ~60,000 tokens (reduces input tokens for 157 item_relation calls)
- **Quality risk**: Low — relations need event facts, not full prose
- **Difficulty**: Medium — prompt and pipeline changes
- **Priority**: P1

### 5. Skip LLM signature pass for deterministic high-confidence versioned releases

- **Expected savings**: ~20,000 tokens (many versioned releases have 100% deterministic confidence)
- **Quality risk**: Low — high-confidence deterministic already 0.9821 valid rate
- **Difficulty**: Low — gating check in signatures.py
- **Priority**: P2

### 6. Batch or rule-handle same_thread candidates — they rarely need LLM judgment

- **Expected savings**: ~15,000 tokens
- **Quality risk**: Medium
- **Difficulty**: Medium
- **Priority**: P2

### 7. Use compact event_signature prompt for LLM fallback and reduce output schema size

- **Expected savings**: ~30,000 tokens (prompt vs output trimming)
- **Quality risk**: Low-Medium
- **Difficulty**: Low — prompt edit
- **Priority**: P2

### 8. Use LLM only for Chinese event-like items that deterministic cannot resolve

- **Expected savings**: ~10,000 tokens (small but important for Chinese recall)
- **Quality risk**: Low — addresses specific gap
- **Difficulty**: Low
- **Priority**: P1

## Combined Savings Estimate

Implementing P0+P1 recommendations could reduce tokens/item from 2923.8 to ~1800, saving ~337,140 tokens per 300-item run.
