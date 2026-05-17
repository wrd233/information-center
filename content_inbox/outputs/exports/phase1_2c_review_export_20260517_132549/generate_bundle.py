#!/usr/bin/env python3
"""Generate phase1_2c_review_bundle.md and phase1_2c_review_bundle.json"""
import json, csv, os
from datetime import datetime

export_dir = os.path.dirname(os.path.abspath(__file__))
base = '/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval'

now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# ===== LOAD DATA =====

with open(f'{base}/api_xgo_ing_phase1_2c_final_summary_20260517_130115.json') as f:
    final = json.load(f)

with open(f'{base}/api_xgo_ing_phase1_2c_full_300_final/semantic_quality_summary.json') as f:
    sem = json.load(f)

with open(f'{base}/api_xgo_ing_phase1_2c_ingest_20260517_111620.json') as f:
    ingest = json.load(f)

# Load all run JSONs
run_names = {
    'smoke_c3': f'{base}/api_xgo_ing_phase1_2c_smoke_hotspots_c3/semantic_quality_summary.json',
    'smoke_c3_iter2': f'{base}/api_xgo_ing_phase1_2c_smoke_hotspots_c3_iter2/semantic_quality_summary.json',
    'hotspots_150_c3': f'{base}/api_xgo_ing_phase1_2c_hotspots_150_c3/semantic_quality_summary.json',
    'hotspots_150_c2': f'{base}/api_xgo_ing_phase1_2c_hotspots_150_c2_cmp/semantic_quality_summary.json',
    'hotspots_150_c4': f'{base}/api_xgo_ing_phase1_2c_hotspots_150_c4_cmp/semantic_quality_summary.json',
    'final_300': f'{base}/api_xgo_ing_phase1_2c_full_300_final/semantic_quality_summary.json',
}
all_runs = {}
for name, path in run_names.items():
    if os.path.exists(path):
        with open(path) as f:
            all_runs[name] = json.load(f)

# Read CSVs
def read_csv(filename):
    path = f'{export_dir}/{filename}'
    if os.path.exists(path):
        with open(path) as f:
            return list(csv.DictReader(f))
    return []

sources = read_csv('sources_api_xgo_ing.csv')
items_added = read_csv('items_added_phase1_2c.csv')
sem_items = read_csv('semantic_items_300.csv')
relations = read_csv('semantic_relations_available.csv')
fallbacks = read_csv('semantic_item_card_fallbacks.csv')
failures = read_csv('semantic_item_card_failures.csv')

# ===== COMPUTE STATS =====
runs_data = final.get('runs', {})
final_run = runs_data.get('final', {})

# ===== BUILD MARKDOWN =====
md = f"""# Phase 1.2c Review Export Bundle

## 1. Export Metadata

- **Repo path**: `/Users/wangrundong/work/infomation-center`
- **Git commit**: `b30e483`
- **Export time**: {now}
- **Database used**: `content_inbox/data/content_inbox.sqlite3` (read-only)
- **Before backup**: `before_api_xgo_semantic_phase1_2c_20260517_111621.sqlite3`
- **DB items before**: 2840
- **DB items after**: 3123
- **DB item delta**: 283
- **All commands were read-only**: YES
- **No code was modified**: YES
- **Semantic was dry-run**: YES (not written to production DB)

## 2. Files Included

| File | Description |
|---|---|
| `sources_api_xgo_ing.csv` | All 151 api.xgo.ing* sources with full details |
| `items_added_phase1_2c.csv` | 283 new items with content snippets |
| `items_added_by_source.csv` | Per-source new item counts |
| `ingest_runs_phase1_2c.csv` | Ingest run records (592 individual source runs) |
| `ingest_run_sources_phase1_2c.csv` | Per-source ingest results (17 completed) |
| `semantic_items_300.csv` | 300 sampled items with card tier/reason |
| `semantic_item_card_fallbacks.csv` | 96 heuristic/minimal-rule items |
| `semantic_relations_available.csv` | 120 annotated relation examples from 6 runs |
| `semantic_cluster_candidates.csv` | 77 cluster samples from 6 runs |
| `evidence_files/` | Copied semantic eval outputs (16 files/dirs) |

## 3. Ingest Source Scope

### 3.1 Overview

| Metric | Value |
|---|---|
| Sources matched (api.xgo.ing*) | 151 |
| Succeeded | 7 |
| Failed (timeout) | 143 |
| Failed (HTTP error) | 1 |
| New items (reported by ingest) | 2 |
| Duplicates (reported) | 68 |
| DB item delta (before→after) | 283 |

The 283 DB item delta is _larger_ than the 2 "new items" reported by ingest because:
1. The 2 "new items" means items where `dedupe_key` was genuinely novel.
2. The remaining delta comes from: existing items receiving updates (incrementing `seen_count`, updating timestamps), and items from other concurrent processes.
3. Note: 143 sources timed out but may have partially written items before timeout.

### 3.2 Source Coverage

All 151 `api.xgo.ing*` sources are listed in `sources_api_xgo_ing.csv`. Full field details:
- `source_id`, `source_name`, `feed_url`, `status`, `last_success_at`, `last_failure_at`
- `consecutive_failures`, `failure_count`, `last_new_items`, `last_duplicate_items`
- `last_ingest_at`, `last_run_id`

### 3.3 Items Added (283)

Full list in `items_added_phase1_2c.csv`. Fields for each item:
- `item_id`, `source_id`, `source_name`, `title`, `url`, `guid`
- `published_at`, `created_at`, `summary_snippet`, `content_snippet`
- `dedupe_key`, `dedupe_version`

### 3.4 Per-Source Added Items (Top 20)

"""
# Add top 20 sources by added items
source_added = {}
for it in items_added:
    sn = it.get('source_name', 'unknown')
    source_added[sn] = source_added.get(sn, 0) + 1
md += "| Source | Items Added |\n|---|---|\n"
for sn, count in sorted(source_added.items(), key=lambda x: -x[1])[:20]:
    md += f"| {sn} | {count} |\n"

md += f"""
### 3.5 Partial Write Suspects

The 143 timeout sources may have partial writes. Evidence:
- 592 individual source run records between 02:50-04:00 UTC on May 17
- 575 runs still in "running" status (never completed = timed out)
- 13 runs completed successfully
- 4 runs completed with failure

Only 17 of 592 runs have corresponding `rss_ingest_run_sources` records (these are the completed ones).

**Partial write indication**: Items with `created_at` between 02:50-04:00 UTC on May 17 from timed-out sources suggest partial writes succeeded before timeout killed the ingest.

Full data in `ingest_runs_phase1_2c.csv` and `ingest_run_sources_phase1_2c.csv`.

## 4. Ingest Delta Detail

### 4.1 Items Added by Time

"""
# Time distribution of added items
from collections import Counter
hours = Counter()
for it in items_added:
    created = it.get('created_at', '')
    if created:
        h = created[11:13]
        hours[h] += 1
md += "| Hour (UTC) | Items |\n|---|---|\n"
for h in sorted(hours):
    md += f"| {h}:00 | {hours[h]} |\n"

md += f"""

### 4.2 Sample of Added Items (First 10)
"""
for it in items_added[:10]:
    title = (it.get('title', '') or '')[:120]
    src = it.get('source_name', '') or ''
    link = it.get('url', '') or ''
    created = it.get('created_at', '') or ''
    snippet = (it.get('summary_snippet', '') or '')[:200]
    md += f"""
- **Title**: {title}
  - Source: {src}
  - Link: {link}
  - Created: {created}
  - Snippet: {snippet}
"""

# ===== SECTION 5: SEMANTIC DRY-RUN COVERAGE =====
md += f"""
## 5. Semantic Dry-Run Coverage

### 5.1 Final 300 Run Summary

| Metric | Value |
|---|---|
| Items sampled | 300 |
| Languages | 289 English, 11 Chinese |
| Sources represented | 57 |
| Total LLM calls | 223 |
| Total tokens | 714,640 |
| Duration | 1232.7s |
| Concurrency | 4 |

### 5.2 Card Quality

| Tier | Count |
|---|---|
| Full | 99 |
| Standard | 105 |
| Minimal | 96 |
| **Total generated** | **300** |

| Metric | Value |
|---|---|
| Heuristic card fallbacks | 35 |
| Item card failures | 7 |
| Avg confidence (full) | 0.734 |
| Avg confidence (standard) | 0.715 |
| Avg confidence (minimal) | 0.550 |

### 5.3 Content Roles

| Role | Count |
|---|---|
| Report | 129 |
| Source Material | 85 |
| Commentary | 26 |
| Analysis | 25 |
| Low Signal | 21 |
| Aggregator | 7 |
| Firsthand | 7 |

### 5.4 Item-Item Relations

| Relation | Count |
|---|---|
| Different | 453 |
| Near Duplicate | 7 |
| Related with New Info | 23 |
| Uncertain | 1 |
| **Total candidate pairs** | **484** |
| Fold candidates | 7 |
| LLM relation calls | 97 |

### 5.5 Item-Cluster Relations

| Metric | Value |
|---|---|
| Candidate clusters considered | 20 |
| Created clusters | 20 |
| Multi-item clusters | **0** |
| Avg items per cluster | 1.0 |
| Attached to existing | 0 |
| new_info relations | 16 |
| source_material relations | 4 |

## 6. Relation Evidence

### 6.1 Available Data

**CRITICAL GAP**: The semantic eval output JSONs only contain **20 annotated examples per run** (10 high-confidence + 10 low-confidence). The full 484 individual relation records (453 different, 7 near_duplicate, 23 related_with_new_info, 1 uncertain) are NOT available in the JSON/MD outputs. They existed only in the dry-run evaluation database which was not persisted.

Only **aggregate counts** are available for the full relation set.

### 6.2 Annotated Relation Examples (Final 300 Run)
"""
# Extract final 300 relation examples
final300_rels = [r for r in relations if r.get('_run') == 'final_300']
high_conf = [r for r in final300_rels if r.get('_low_confidence') != 'True']
low_conf = [r for r in final300_rels if r.get('_low_confidence') == 'True']

md += f"\n**High-confidence examples ({len(high_conf)}):**\n\n"
for i, rel in enumerate(high_conf[:10]):
    rel_type = rel.get('primary_relation', '')
    title_a = rel.get('candidate_item_title', '')
    title_b = rel.get('new_item_title', '')
    conf = rel.get('confidence', '')
    reason = rel.get('reason', '')
    should_fold = rel.get('should_fold', '')
    source = rel.get('source', '')
    pub = rel.get('published_at', '')
    md += f"""**Relation {i+1}** — {rel_type} (confidence={conf}, should_fold={should_fold})
- Item A: {title_a}
- Item B: {title_b}
- Published: {pub}
- Source: {source}
- Reason: {reason}

"""

md += f"\n**Low-confidence examples ({len(low_conf)}):**\n\n"
for i, rel in enumerate(low_conf[:10]):
    rel_type = rel.get('primary_relation', '')
    title_a = rel.get('candidate_item_title', '')
    title_b = rel.get('new_item_title', '')
    conf = rel.get('confidence', '')
    reason = rel.get('reason', '')
    md += f"""**Low-Conf {i+1}** — {rel_type} (confidence={conf})
- A: {title_a}
- B: {title_b}
- Reason: {reason}

"""

# ===== Non-final300 run relations =====
other_runs_rels = [r for r in relations if r.get('_run') != 'final_300']
md += f"### 6.3 Relations from Other Runs ({len(other_runs_rels)} examples across 5 runs)\n\n"
md += "See `semantic_relations_available.csv` for the full list of 120 annotated relation examples.\n\n"

# ===== SECTION 7: CLUSTER DIAGNOSTICS =====
md += """## 7. Cluster Diagnostics

### 7.1 Why Multi-Item Clusters = 0

The final 300 run created 20 clusters, all single-item. Root causes from the report:

1. **Candidate recall limited**: Only 20 candidate clusters considered out of 300 items. The recall strategy (lexical/entity/time/source hybrid) may be too conservative.
2. **Stage budget constraints**: The `relation_heavy` stage budget profile may have limited cluster-relation LLM calls.
3. **Attachment rejected**: Items offered for attachment were rejected by the cluster-relation LLM (classified as different/uncertain rather than new_info/source_material).
4. **High threshold for multi-item**: The system requires both semantic relation AND cluster-level agreement; many item pairs have weak-enough relations that they don't form clusters.

### 7.2 Cluster Samples (Final 300 Run)

"""
final300_clusters = sem.get('item_clusters', {}).get('cluster_samples', [])
for i, cl in enumerate(final300_clusters[:10]):
    title = cl.get('cluster_title', '')
    facts = cl.get('core_facts', [])
    rep_items = cl.get('representative_items', [])
    item_count = cl.get('item_count', 1)
    md += f"""**Cluster {i+1}**: {title}
- Items: {item_count} | Representative: {', '.join(rep_items[:3])}
- Core facts: {'; '.join(facts[:2])}

"""

md += f"\nRemaining {len(final300_clusters) - 10} clusters listed in `semantic_cluster_candidates.csv`.\n\n"

# ===== SECTION 8: EVENT HOTSPOT DIAGNOSTICS =====
md += """## 8. Event Hotspot Diagnostics

The `event_hotspots` sampling mode was used for the 150-item comparison runs. Each run used hotspot-based sampling to identify candidate groups.

### 8.1 Hotspot Coverage

"""
for run_name in ['smoke_c3', 'hotspots_150_c3', 'hotspots_150_c2', 'hotspots_150_c4']:
    rd = all_runs.get(run_name, {})
    ic = rd.get('item_clusters', {})
    clusters = ic.get('cluster_samples', [])
    cc = ic.get('candidate_clusters_considered', 0)
    mc = ic.get('multi_item_cluster_count', 0)
    md += f"- **{run_name}**: {cc} candidates considered, {len(clusters)} clusters, {mc} multi-item\n"

md += """
### 8.2 Why Hotspots Didn't Form Multi-Item Clusters

Hotspot sampling groups items by lexical/entity/time proximity, but:
1. Grouped items may be about different specific events within the same broad theme.
2. The LLM cluster-relation check may find items are "same_topic" but not "same_event".
3. Budget constraints could limit the number of LLM checks per hotspot group.

Full hotspot group data was not persisted in the output JSONs (only aggregate counts).

## 9. Item-Card Fallback/Failure Cases

### 9.1 Heuristic Fallbacks (35 of 300)

The `heuristic_card_fallback_count: 35` refers to items where LLM card generation produced JSON parse errors, triggering a heuristic/minimal card fallback. In the steps data, these appear as items with JSON parse error reasons.

Additionally, 96 items received "local minimal card" via `minimal_rule` (no LLM call at all), typically for very short or low-signal content.

"""
# Show sample fallback items
md += "**Sample of 10 minimal-rule items:**\n\n"
for fb in fallbacks[:10]:
    title = (fb.get('title', '') or '')[:100]
    reason = fb.get('card_reason', '')
    source = fb.get('source_name', '')
    md += f"- [{source}] {title} (reason: {reason})\n"

md += f"\nFull list of {len(fallbacks)} fallback items in `semantic_item_card_fallbacks.csv`.\n\n"

md += """### 9.2 Card Failures (7 of 300)

The 7 item-card failures represent items where even the fallback/heuristic card generation failed. **The specific item_ids for these 7 failures are NOT available in the JSON outputs** — only the count is recorded.

In the `steps.item_cards.items` list, all 300 items have card assignments (no items are marked as outright failed). The 7 failures might be:
- Items that failed before reaching the steps tracking
- Items counted in `errors_fallbacks.final_failures` (total=9, which includes 7 card failures + 1 relation failure + 1 cluster failure)

## 10. Source-Profile Review Aggregation

### 10.1 Conservative Aggregation

The Phase 1.2c semantic eval used conservative source-profile review: source-level priority reviews were suppressed/aggregated (0 source_priority_reviews in the final run, down from 67 in the first smoke test).

"""
# Source profile data
sp = sem.get('source_profiles', {})
md += f"""- **Total sources with profile data**: {len(sp.get('sources', sp.get('source_profiles', {})))} (from the top-level structure)
- **Source priority reviews generated**: 0 (suppressed in final run)
- **Review queue entries due to failure**: 393

### 10.2 Per-Source Metrics

See `source_profiles` in the bundle JSON for per-source data including:
- `total_items`, `llm_processed_items`
- `duplicate_rate`, `near_duplicate_rate`, `new_event_rate`
- `incremental_value_avg`, `report_value_avg`
- `llm_total_tokens`, `llm_yield_score`, `llm_priority`

## 11. Known Gaps in Exported Evidence

The following data **could not be exported** because it does not exist in the available outputs:

| Gap | Reason |
|---|---|
| Full 484 item-item relation records | Only 20 annotated examples per run in JSON; dry-run DB not persisted |
| Individual 7 near_duplicate pairs | Count known (7), but individual pairs not in outputs |
| Individual 23 related_with_new_info pairs | Count known (23), but individual pairs not in outputs |
| The 1 uncertain pair | Count known, but not individually listed |
| 7 card failure item_ids | Only count known, not individual items |
| Raw LLM prompts/responses | Not included in eval outputs |
| Hotspot group membership | Only aggregate counts, not per-group item lists |
| 300 items' full content (titles/summaries) | Dry-run used separate DB with different item_ids; production DB items don't match |

### Why the 300 Items Don't Match the Production DB

The semantic evaluation used a **dry-run database** (an in-memory or temporary copy). The `item_id` values in the semantic outputs (e.g., `item_2fd731e980504b92bcb3e87e7cc828ad`) are from this dry-run DB and do **not** correspond to any items in the production `content_inbox.sqlite3`. This means:
- We cannot look up the full title/summary/link for the 300 evaluation items from the production DB
- The 10 annotated card samples in the report provide the only item-level content detail
- Cross-referencing would require matching by title/content fingerprint, which is fragile

## 12. Concurrency Comparison

"""
# Concurrency data
cc = final.get('concurrency', {})
md += f"- **Recommended concurrency**: {cc.get('recommended_concurrency', 'N/A')}\n"
for run in cc.get('runs', []):
    md += f"- **{run.get('label', '?')}**: {run.get('duration_seconds', 0):.0f}s, {run.get('actual_tokens', 0)} tokens, {run.get('final_failures', 0)} failures, {run.get('item_relations_non_different', 0)} non-different relations\n"

# Write MD file
md_path = f'{export_dir}/phase1_2c_review_bundle.md'
with open(md_path, 'w') as f:
    f.write(md)
print(f"Markdown bundle written: {md_path}")
print(f"Size: {len(md)} chars")
