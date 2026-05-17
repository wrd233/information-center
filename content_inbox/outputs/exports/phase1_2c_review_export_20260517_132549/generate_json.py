#!/usr/bin/env python3
"""Generate phase1_2c_review_bundle.json"""
import json, csv, os
from datetime import datetime

export_dir = os.path.dirname(os.path.abspath(__file__))
base = '/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval'

now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Load data
with open(f'{base}/api_xgo_ing_phase1_2c_final_summary_20260517_130115.json') as f:
    final = json.load(f)

with open(f'{base}/api_xgo_ing_phase1_2c_full_300_final/semantic_quality_summary.json') as f:
    sem = json.load(f)

with open(f'{base}/api_xgo_ing_phase1_2c_ingest_20260517_111620.json') as f:
    ingest = json.load(f)

# Load all run JSONs
run_paths = {
    'smoke_c3': f'{base}/api_xgo_ing_phase1_2c_smoke_hotspots_c3/semantic_quality_summary.json',
    'smoke_c3_iter2': f'{base}/api_xgo_ing_phase1_2c_smoke_hotspots_c3_iter2/semantic_quality_summary.json',
    'hotspots_150_c3': f'{base}/api_xgo_ing_phase1_2c_hotspots_150_c3/semantic_quality_summary.json',
    'hotspots_150_c2': f'{base}/api_xgo_ing_phase1_2c_hotspots_150_c2_cmp/semantic_quality_summary.json',
    'hotspots_150_c4': f'{base}/api_xgo_ing_phase1_2c_hotspots_150_c4_cmp/semantic_quality_summary.json',
    'final_300': f'{base}/api_xgo_ing_phase1_2c_full_300_final/semantic_quality_summary.json',
}
all_runs = {}
for name, path in run_paths.items():
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

# Build sources list for JSON (limit fields)
sources_json = []
for s in sources:
    sources_json.append({
        'source_id': s.get('source_id', ''),
        'source_name': s.get('source_name', ''),
        'feed_url': s.get('feed_url', ''),
        'status': s.get('status', ''),
        'last_success_at': s.get('last_success_at', ''),
        'last_failure_at': s.get('last_failure_at', ''),
        'failure_count': s.get('failure_count', ''),
        'consecutive_failures': s.get('consecutive_failures', ''),
        'last_ingest_at': s.get('last_ingest_at', ''),
        'last_new_items_count': s.get('last_new_items_count', ''),
        'created_at': s.get('created_at', ''),
    })

# Build items_added JSON (with snippets)
items_added_json = []
for it in items_added:
    items_added_json.append({
        'item_id': it.get('item_id', ''),
        'source_id': it.get('source_id', ''),
        'source_name': it.get('source_name', ''),
        'title': (it.get('title', '') or '')[:200],
        'url': it.get('url', ''),
        'guid': it.get('guid', ''),
        'published_at': it.get('published_at', ''),
        'created_at': it.get('created_at', ''),
        'updated_at': it.get('updated_at', ''),
        'summary_snippet': (it.get('summary_snippet', '') or '')[:300],
        'content_snippet': (it.get('content_snippet', '') or '')[:300],
        'dedupe_key': it.get('dedupe_key', ''),
        'dedupe_version': it.get('dedupe_version', ''),
        'content_type': it.get('content_type', ''),
    })

# Build semantic items JSON
sem_items_json = []
for it in sem_items:
    sem_items_json.append({
        'seq_id': it.get('seq_id', ''),
        'item_id': it.get('item_id', ''),
        'card_reason': it.get('card_reason', ''),
        'card_source': it.get('card_source', ''),
        'source_name': it.get('source_name', ''),
        'title': (it.get('title', '') or '')[:200],
        'url': it.get('url', ''),
        'published_at': it.get('published_at', ''),
    })

# Extract relations from all runs
all_relations = []
for r in relations:
    all_relations.append({
        'run': r.get('_run', ''),
        'low_confidence': r.get('_low_confidence', '') == 'True',
        'primary_relation': r.get('primary_relation', ''),
        'candidate_item_title': r.get('candidate_item_title', ''),
        'new_item_title': r.get('new_item_title', ''),
        'confidence': r.get('confidence', ''),
        'should_fold': r.get('should_fold', ''),
        'reason': (r.get('reason', '') or '')[:300],
        'source': r.get('source', ''),
        'published_at': r.get('published_at', ''),
    })

# Extract relation type breakdown per run
relations_summary = {}
for run_name, rd in all_runs.items():
    ir = rd.get('item_relations', {})
    relations_summary[run_name] = {
        'candidate_pairs': ir.get('candidate_pairs_considered', 0),
        'different': ir.get('different', 0),
        'near_duplicate': ir.get('near_duplicate', 0),
        'related_with_new_info': ir.get('related_with_new_info', 0),
        'uncertain': ir.get('uncertain_count', 0),
        'avg_confidence': ir.get('avg_confidence', 0),
        'llm_calls': ir.get('llm_item_relation_calls', 0),
        'fold_candidates': ir.get('fold_candidates', 0),
    }

# Extract cluster data per run
clusters_summary = {}
all_cluster_samples = []
for run_name, rd in all_runs.items():
    ic = rd.get('item_clusters', {})
    clusters_summary[run_name] = {
        'candidate_clusters_considered': ic.get('candidate_clusters_considered', 0),
        'created_clusters': ic.get('created_clusters', 0),
        'multi_item_cluster_count': ic.get('multi_item_cluster_count', 0),
        'avg_items_per_cluster': ic.get('avg_items_per_cluster', 0),
        'avg_confidence': ic.get('avg_confidence', 0),
        'attached_existing_clusters': ic.get('attached_existing_clusters', 0),
        'actions': ic.get('actions', {}),
    }
    for cs in ic.get('cluster_samples', []):
        cs['_run'] = run_name
        all_cluster_samples.append(cs)

# Source profiles
source_profiles_data = sem.get('source_profiles', {})

# Card tier distribution
card_data = sem.get('item_cards', {})

# Fallback data
fallbacks_json = []
for fb in fallbacks:
    fallbacks_json.append({
        'seq_id': fb.get('seq_id', ''),
        'item_id': fb.get('item_id', ''),
        'card_reason': fb.get('card_reason', ''),
        'source_name': fb.get('source_name', ''),
        'title': (fb.get('title', '') or '')[:200],
        'url': fb.get('url', ''),
    })

# Build the complete bundle
bundle = {
    'export_metadata': {
        'repo_path': '/Users/wangrundong/work/infomation-center',
        'git_commit': 'b30e483',
        'export_time': now,
        'database_path': 'content_inbox/data/content_inbox.sqlite3',
        'db_items_before': 2840,
        'db_items_after': 3123,
        'db_item_delta': 283,
        'read_only': True,
        'code_modified': False,
        'semantic_dry_run': True,
        'phase1_2c_git_commit': final.get('git_commit', ''),
        'phase1_2c_generated_at': final.get('generated_at', ''),
    },
    'ingest': {
        'summary': final.get('ingest', {}),
        'probe_before': final.get('probe_before', {}),
        'probe_after': final.get('probe_after', {}),
        'sources': sources_json,
        'items_added': items_added_json,
        'items_added_count': len(items_added_json),
    },
    'semantic': {
        'summary': {
            'runs': final.get('runs', {}),
            'concurrency': final.get('concurrency', {}),
            'readiness': final.get('readiness', {}),
        },
        'final_300_card_quality': {
            'card_tier_distribution': card_data.get('card_tier_distribution', {}),
            'content_role_distribution': card_data.get('content_role_distribution', {}),
            'avg_confidence': card_data.get('avg_confidence', 0),
            'heuristic_fallback_count': card_data.get('heuristic_card_fallback_count', 0),
            'card_failures': card_data.get('item_cards_failed', 0),
            'annotated_samples': card_data.get('samples', []),
        },
        'items': sem_items_json,
        'item_card_fallbacks': fallbacks_json,
        'relations': {
            'per_run_summary': relations_summary,
            'all_annotated_examples': all_relations,
            'near_duplicate_count': sem.get('item_relations', {}).get('near_duplicate', 0),
            'related_with_new_info_count': sem.get('item_relations', {}).get('related_with_new_info', 0),
            'data_gap': 'Full 484 individual relations not available in output JSONs — only 120 annotated examples across 6 runs',
        },
        'clusters': {
            'per_run_summary': clusters_summary,
            'all_samples': all_cluster_samples,
            'multi_item_cluster_count': 0,
            'diagnosis': '20 candidate clusters considered, all single-item. Likely causes: conservative candidate recall, stage budget limits, LLM attachment rejection.',
        },
        'source_profiles': source_profiles_data,
        'errors': sem.get('errors_fallbacks', {}),
        'token_cost': sem.get('token_cost', {}),
    },
    'files_included': [
        'sources_api_xgo_ing.csv',
        'sources_item_counts.csv',
        'items_added_phase1_2c.csv',
        'items_added_by_source.csv',
        'ingest_runs_phase1_2c.csv',
        'ingest_run_sources_phase1_2c.csv',
        'semantic_items_300.csv',
        'semantic_item_card_fallbacks.csv',
        'semantic_item_card_failures.csv',
        'semantic_relations_available.csv',
        'semantic_cluster_candidates.csv',
        'evidence_files/',
        'phase1_2c_review_bundle.md',
        'phase1_2c_review_bundle.json',
    ],
    'known_gaps': [
        'Full 484 item-item relation records not available (only 120 annotated examples)',
        '7 near_duplicate pairs: count known, individual pairs NOT in outputs',
        '23 related_with_new_info pairs: count known, individual pairs NOT in outputs',
        '1 uncertain pair: count known, NOT individually listed',
        '7 card failure item_ids: only count known',
        'Raw LLM prompts/responses: not in eval outputs',
        'Hotspot group membership: only aggregate counts',
        '300 semantic items do not match production DB item_ids (separate dry-run DB)',
    ],
}

# Write JSON
json_path = f'{export_dir}/phase1_2c_review_bundle.json'
with open(json_path, 'w') as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)

print(f"JSON bundle written: {json_path}")
print(f"Size: {os.path.getsize(json_path)} bytes")
