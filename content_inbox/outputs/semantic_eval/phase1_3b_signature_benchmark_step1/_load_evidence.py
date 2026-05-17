#!/usr/bin/env python3
"""Load and index all Phase 1.3 evidence for benchmark curation."""
import json
from pathlib import Path
from collections import defaultdict

ROUND_C = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3_round_c_80_live_tuned")

def load_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

# Load all files
items = load_jsonl(ROUND_C / "semantic_items.jsonl")
sigs = load_jsonl(ROUND_C / "event_signatures.jsonl")
cards = load_jsonl(ROUND_C / "item_cards.jsonl")
rels_interesting = load_jsonl(ROUND_C / "relations_interesting.jsonl")
rels_all = load_jsonl(ROUND_C / "relations_all.jsonl")
rejections = load_jsonl(ROUND_C / "cluster_seed_rejections.jsonl")

# Index
items_by_id = {r["dry_run_item_id"]: r for r in items}
sigs_by_id = {r["item_id"]: r for r in sigs}
cards_by_id = {r["item_id"]: r for r in cards}

print(f"Loaded: {len(items)} items, {len(sigs)} signatures, {len(cards)} cards")
print(f"Relations: {len(rels_interesting)} interesting, {len(rels_all)} all")
print(f"Cluster seed rejections: {len(rejections)}")
print()

# Count accepted vs rejected
accepted = [s for s in sigs if s.get("is_concrete")]
rejected = [s for s in sigs if not s.get("is_concrete")]
print(f"Accepted signatures: {len(accepted)}")
print(f"Rejected signatures: {len(rejected)}")
print()

# Group rejected by invalid reasons count
by_reason_count = defaultdict(list)
for s in rejected:
    reasons = s.get("invalid_reasons", [])
    by_reason_count[len(reasons)].append(s)
for k in sorted(by_reason_count):
    print(f"  {k} invalid reasons: {len(by_reason_count[k])} items")

# Print summary of all items
print("\n" + "="*80)
print("ALL 80 ITEMS WITH SIGNATURES")
print("="*80)

for i, sig in enumerate(sigs):
    item = items_by_id.get(sig["item_id"], {})
    card = cards_by_id.get(sig["item_id"], {})
    status = "ACCEPTED" if sig.get("is_concrete") else "REJECTED"

    print(f"\n--- Item {i+1}: {status} | {sig['item_id']} ---")
    print(f"Source: {item.get('source_name', 'N/A')}")
    print(f"Published: {item.get('published_at', 'N/A')}")
    print(f"Title: {item.get('title', 'N/A')[:120]}")
    if card:
        print(f"Card summary: {card.get('short_summary', 'N/A')[:200]}")
        print(f"Card role: {card.get('content_role', 'N/A')}")
        print(f"Card entities: {card.get('entities', [])}")
        print(f"Card event_hint: {card.get('event_hint', 'N/A')}")
    print(f"Action: {sig.get('action')} | Actor: {sig.get('actor')} | Actor type: {sig.get('actor_type')}")
    print(f"Product: {sig.get('product_or_model')} | Object: {sig.get('object')}")
    print(f"Concreteness: {sig.get('concreteness_score')} | Signature key: {sig.get('signature_key')}")
    print(f"Invalid reasons: {sig.get('invalid_reasons', [])}")
    print(f"Supporting tokens (first 10): {sig.get('supporting_tokens', [])[:10]}")

# Print relations summary
print("\n" + "="*80)
print("RELATIONS INTERESTING (32 pairs)")
print("="*80)

# Group by relation_label
by_label = defaultdict(list)
for r in rels_interesting:
    by_label[r.get("relation_label", "unknown")].append(r)
for label in sorted(by_label):
    print(f"\n  {label}: {len(by_label[label])} pairs")

# Print each relation
for i, r in enumerate(rels_interesting):
    print(f"\n--- Relation {i+1}: {r.get('relation_label')} ---")
    print(f"  Item A: {r.get('item_a_id')} | {r.get('item_a_source_name')}")
    print(f"    Title: {r.get('item_a_title', 'N/A')[:100]}")
    print(f"  Item B: {r.get('item_b_id')} | {r.get('item_b_source_name')}")
    print(f"    Title: {r.get('item_b_title', 'N/A')[:100]}")
    print(f"  Candidate score: {r.get('candidate_score', 'N/A')}")
    print(f"  Should fold: {r.get('should_fold')}")
    print(f"  Confidence: {r.get('confidence')}")
    print(f"  Reason: {r.get('reason', 'N/A')[:200]}")
    print(f"  Shared entities: {r.get('shared_entities', [])}")

# Print source distribution
print("\n" + "="*80)
print("SOURCE DISTRIBUTION")
print("="*80)
by_source = defaultdict(list)
for item in items:
    by_source[item.get("source_name", "unknown")].append(item["dry_run_item_id"])
for src in sorted(by_source):
    ids = by_source[src]
    accepted_count = sum(1 for iid in ids if iid in sigs_by_id and sigs_by_id[iid].get("is_concrete"))
    print(f"  {src}: {len(ids)} items, {accepted_count} accepted")
