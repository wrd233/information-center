# Step 1 Summary: Phase 1.3b Event Signature Benchmark

## What Was Built

A 50-row curated benchmark from Phase 1.3 semantic evidence, designed to diagnose deterministic event signature extraction failures on social media content and serve as a foundation for Codex improvements.

**Output directory**: `content_inbox/outputs/semantic_eval/phase1_3b_signature_benchmark_step1/`

## Key Statistics

- **50 benchmark rows**: 33 single items, 15 pairs, 2 cluster candidates
- **16 source accounts** represented (100% coverage)
- **42 rows** have valid event signature recommendations
- **8 rows** are correctly rejected as non-event content
- **17 pair rows** with recommended relations (near_duplicate, same_product_different_event, same_thread, related_with_new_info, different)

## Top 10 Insights from the Evidence

1. **0% of accepted signatures are actually correct**: All 11 "accepted" signatures have at least one major flaw — wrong actor, gibberish product, incorrect action, or nonsense phrase fragments. The 0.7 concreteness threshold passes too much garbage.

2. **Action extraction is English-only and regex-dependent**: 66/80 items failed on `missing_concrete_event_action`. Chinese text (Googlebook launch: "刚刚发布") and nuanced English ("surpassed", "became the first company to hit") fail the same regex.

3. **Product tokenization is catastrophically wrong**: `product_or_model` values include URL fragments ("fkR2wVD129", "U4n62"), number fragments ("for 50", "just 0.3"), and sentence fragments ("for updates from my phone. hermes agent", "coordinated opposition campaigns around our Utah projects").

4. **Actor extraction conflates entities with actors**: "Meta" is identified as actor for Recursive launch (Meta is the founder's former employer). "Claude" is actor for QVeris CLI (Claude Code is the integration target, not the maker).

5. **Real events are false-negatived as triple-failure**: Shanghai Telecom Token plans, Stelline Developer Kit shipping, and LangSmith Fleet free tier were all classified as triple-failure low-signal content despite being real events.

6. **Cross-language near-duplicate detection works correctly**: The only near_duplicate pair (Anthropic adoption data in English and Chinese) was correctly identified with should_fold=True. This is a bright spot.

7. **CJK text fragments inflate candidate scores**: Chinese-language entity extraction produces multi-character substrings from quoting behavior that create false entity-overlap signals (candidate scores > 3.0 for unrelated content).

8. **Same-source same-format content is ignored by clustering**: AK's two "paper:" posts, Notion's four developer platform launch posts, and Y Combinator's four launch announcements all remained as single-item clusters despite obvious relationships.

9. **The pipeline is budget-starved, not computation-starved**: Only 17.6% of allocated budget was consumed. The pipeline stops early because all candidates are low-priority, not because it runs out of tokens.

10. **Social media content type matters for extraction**: Firsthand accounts, commentary, and aggregator content have fundamentally different extraction characteristics than source_material (press releases, product announcements).

## Top 5 Likely Changes Codex Should Make

1. **Replace deterministic regex extraction with LLM-based extraction**: The current regex approach cannot handle the linguistic variety of social media. An LLM call with few-shot examples for actor/product/action/object extraction would dramatically improve valid rate.

2. **Add content-type-aware extraction paths**: Source material (press releases, product pages) needs different extraction logic than commentary, firsthand accounts, or aggregator roundups. A single extraction strategy doesn't work across content types.

3. **Implement Chinese-language action detection**: The current action taxonomy and regex patterns are English-only. Chinese event language ("发布", "上线", "推出", "开源") needs its own detection pipeline.

4. **Fix product tokenization with proper noun phrase extraction**: Instead of tokenizing and joining adjacent tokens, extract product names using named entity recognition or LLM extraction. URL fragments, version numbers, and sentence fragments should never be product names.

5. **Add same-source thread detection**: When multiple posts from the same source share entities, timestamps, and topic domains, they should be considered for clustering even if individual event signatures are weak. This would catch the Notion platform launch and AK paper feed patterns.

## Benchmark Quality Concerns

1. **No human review yet**: All recommended labels and signatures are Claude's judgment. The `human_label` and `human_notes` fields are intentionally left empty for a future human review pass.

2. **Cluster candidate rows are speculative**: Since the run produced zero multi-item clusters, the 2 cluster candidate rows describe what SHOULD have happened based on manual analysis, not what DID happen.

3. **Chinese content analysis relies on machine understanding**: Chinese-language items were analyzed with Claude's understanding, which may miss cultural nuances or domain-specific terminology.

4. **Recommended signatures may be over-specific**: Some recommended signatures include details (object, date_bucket) that may be too specific for a general extraction system. These should be treated as aspirational targets, not hard requirements.

## Files Created

| File | Rows | Purpose |
|---|---|---|
| `signature_benchmark_50.jsonl` | 50 | Primary benchmark data (33 fields per row) |
| `signature_benchmark_50.csv` | 50 | CSV version for analysis |
| `signature_benchmark_50.md` | — | Human-readable review document |
| `signature_benchmark_sampling_notes.md` | — | Methodology and curation rationale |
| `signature_benchmark_evidence_index.json` | — | Traceability mapping |
| `step1_summary.md` | — | This file |
| `signature_benchmark_50_review_sheet.csv` | 50 | Simplified spreadsheet review |
| `signature_benchmark_50_review_sheet.md` | — | Simplified markdown review |

## Next Steps

1. Human review of benchmark labels, especially for Chinese-language items and cluster candidates
2. Implement LLM-based event signature extraction as a drop-in replacement for the deterministic extractor
3. Re-run the benchmark against the new extractor to measure improvement
4. Expand the benchmark to cover more content types and languages as the pipeline scales
