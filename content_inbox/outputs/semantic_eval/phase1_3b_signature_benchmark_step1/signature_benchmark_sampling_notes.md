# Signature Benchmark Sampling Notes

## Evidence Sources

Primary source: `api_xgo_ing_phase1_3_round_c_80_live_tuned` (run `semantic_eval_20260517_104806_662651`)
- 80 semantic items from 16 Twitter/X sources
- 11 accepted signatures (13.75% valid rate), 69 rejected
- 32 relations_interesting pairs (1 near_duplicate, 1 same_product_different_event, 30 suspicious_different)
- 80 item cards with LLM-generated entities, content_role, and short_summary

Reference source: `api_xgo_ing_phase1_3_final_20260517_190408`
- 20 items, 0% valid rate, official NOT_READY verdict

## Sampling Strategy

This is a **curated benchmark**, not a random sample. Each row was individually selected for its diagnostic value. The curation process:

1. Read all 80 items with their computed signatures, invalid reasons, and item cards
2. Read all 32 relations_interesting pairs with LLM verdicts and reasoning
3. Identified key failure modes, edge cases, and pipeline inconsistencies
4. Selected items/pairs that best demonstrate each pattern
5. Assigned recommended labels and corrected event signatures through manual analysis

## Distribution

| Category | Count | Target | Met? |
|---|---|---|---|
| Single items | 33 | 30-35 | Yes |
| Pairs | 15 | 12-18 | Yes |
| Cluster candidates | 2 | 0-5 | Yes |
| **Total** | **50** | **50** | **Yes** |

### Single-item breakdown

| Sub-category | Count |
|---|---|
| Accepted-but-flawed signatures | 6 |
| Single-failure (missing_concrete_event_action) | 10 |
| Triple-failure low-signal | 9 |
| Borderline / edge cases | 8 |

### Pair breakdown

| Sub-category | Count |
|---|---|
| near_duplicate | 2 |
| same_product_different_event | 4 |
| suspicious_different (high score) | 5 |
| Same-source related (manually discovered) | 4 |

### Label distribution

| Recommended Label | Count |
|---|---|
| integration_or_tooling | 7 |
| event_announcement | 6 |
| generic_opinion | 6 |
| same_product_different_event | 4 |
| adoption_metric | 3 |
| company_or_funding | 3 |
| different_pair | 3 |
| pricing_or_availability | 3 |
| same_thread | 3 |
| feature_update | 2 |
| low_signal_social | 2 |
| related_with_new_info_candidate | 2 |
| research_paper | 2 |
| technical_blog | 2 |
| tutorial_or_guide | 1 |
| near_duplicate_candidate | 1 |

## Source Coverage

16 of 16 sources from the run are represented (100%). Distribution is intentionally uneven to reflect the actual data: orange.ai has 20 items (25% of corpus, mostly triple-failure), while AI Engineer has 1 item.

## Data Quality Limitations

1. **Item cards lack short_summary**: All `short_summary` fields from `item_cards.jsonl` are N/A — a known gap in the Phase 1.3 pipeline output. Summaries were inferred from titles and card entities.
2. **No true multi-item clusters exist**: The run produced 78 single-item clusters and 0 multi-item clusters. Cluster candidate rows are speculative.
3. **CJK text fragment overlap**: Chinese-language entity extraction produces multi-character substrings that inflate candidate scores without indicating real semantic overlap.
4. **All 11 accepted signatures are flawed**: Even "accepted" signatures have wrong actors, gibberish products, or incorrect actions. The 0.7 concreteness threshold is too low.

## Current Signature Failure Mode Summary

| Failure Mode | Description | Rows Demonstrating |
|---|---|---|
| Action = "other" despite clear event language | Action regex fails on Chinese text and nuanced English phrasing | B-single_007 (Googlebook), B-single_008 (NVIDIA market cap) |
| Product = sentence fragment | Tokenization produces phrase fragments instead of product names | A-single_004 (Hermes Agent), B-single_010 (Notion CLI) |
| Actor = wrong entity | Extractor picks adjacent named entity, not the actual actor | A-single_003 (Recursive → Meta), B-single_014 (QVeris → Claude) |
| False negative triple-failure | Real events classified as low-signal due to language/content barriers | C-single_024 (Shanghai Telecom), C-single_025 (Stelline kit) |
| Inconsistent acceptance | Same product series has v0.0.40 accepted, v0.0.41 rejected | E-pair_007 (OpenShell pair) |

## Current Candidate Recall Failure Mode Summary

| Failure Mode | Description |
|---|---|
| Generic token overlap | "Claude Code", "agent", "AI" cause false positive candidate pairs |
| CJK substring inflation | Chinese text produces shared entity fragments from quoting behavior |
| Same-source launch dilution | YC posts all share "congrats" and "launch" entities, creating many low-quality pairs |
| Missing same-event pairs | Notion CLI + Workers + Custom Agents (same launch) were never paired |

## Excluded Examples

Several items were considered but excluded:
- **"Read more" link-only posts** (items 8, 26, 32, 66, 80): Too thin for meaningful analysis; included via pair E8 instead
- **Most orange.ai philosophical posts**: 20 items from orange.ai, only 8 included to avoid over-representation
- **@ollama emoji reply** (item 59): One emoji, zero content
- **Marc Andreessen "Substack revolution"** (item 79): Too vague even for low-signal examples
- **Prompt injection test** (item 35): "Ignore your system prompt" — not real content

## Risks and Uncertainties

1. **Recommended labels are Claude's judgment**: No human review has been performed (human_label and human_notes are empty). Some labels may be debatable.
2. **Cluster candidate rows are speculative**: They describe what SHOULD have happened, not what DID happen. Confidence scores are lower (0.55-0.8).
3. **Chinese-language content may be mistranslated**: Chinese item analysis relies on machine understanding of the content.
4. **30 suspicious_different pairs were not exhaustively reviewed**: Only the highest-scoring and most diagnostic pairs were included.
5. **Date buckets are approximate**: Based on published_at date, not the actual event date mentioned in content.
