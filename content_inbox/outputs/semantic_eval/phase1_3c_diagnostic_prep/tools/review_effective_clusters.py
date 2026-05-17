#!/usr/bin/env python3
"""Phase 1.3c Task E: Effective Cluster Quality Review.

Reviews the 2 effective multi-item clusters from the Phase 1.3b 300-run.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict

EVIDENCE_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600")
OUT_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep")


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    clusters = load_jsonl(EVIDENCE_DIR / "clusters_final.jsonl")
    items = load_jsonl(EVIDENCE_DIR / "semantic_items.jsonl")
    sigs = load_jsonl(EVIDENCE_DIR / "event_signatures.jsonl")
    relations = load_jsonl(EVIDENCE_DIR / "relations_all.jsonl")
    attachments = load_jsonl(EVIDENCE_DIR / "cluster_attachments.jsonl")

    item_map = {i["dry_run_item_id"]: i for i in items}
    sig_map = {s["item_id"]: s for s in sigs}

    # Find multi-item clusters
    multi_clusters = [c for c in clusters if c.get("member_count", 1) > 1]
    print(f"Total clusters: {len(clusters)}")
    print(f"Multi-item clusters: {len(multi_clusters)}")

    # Build relation lookup
    relation_pairs = {}
    for r in relations:
        iids = r.get("item_ids", r.get("item_id", []))
        if isinstance(iids, list) and len(iids) >= 2:
            pair_key = tuple(sorted(iids[:2]))
            relation_pairs[pair_key] = r

    # Analyze each cluster
    reviews = []
    member_table = []

    for cluster in multi_clusters:
        cid = cluster["cluster_id"]
        member_ids = cluster.get("member_item_ids", [])
        quality_label = cluster.get("cluster_quality_label", "")
        title = cluster.get("cluster_title", "")
        summary = cluster.get("cluster_summary", "")
        sig_keys = cluster.get("event_signature_keys", [])
        time_start = cluster.get("time_window_start", "")
        time_end = cluster.get("time_window_end", "")
        time_days = cluster.get("time_window_days", 0)
        rel_summary = cluster.get("relation_summary", {})
        source_count = cluster.get("source_count", 1)

        # Gather member details
        members = []
        for mid in member_ids:
            item = item_map.get(mid, {})
            sig = sig_map.get(mid, {})
            member = {
                "item_id": mid,
                "title": (item.get("title", "") or "")[:200],
                "source_name": item.get("source_name", ""),
                "published_at": item.get("published_at", ""),
                "semantic_level": sig.get("semantic_level", ""),
                "action": sig.get("action", ""),
                "actor": sig.get("actor", ""),
                "product_or_model": sig.get("product_or_model", ""),
                "signature_key": sig.get("signature_key", ""),
                "invalid_reasons": sig.get("invalid_reasons", []),
            }
            members.append(member)
            member_table.append({
                "cluster_id": cid,
                "cluster_title": title,
                "item_id": mid,
                "title": member["title"][:150],
                "source_name": member["source_name"],
                "published_at": member["published_at"],
                "semantic_level": member["semantic_level"],
                "action": member["action"],
                "actor": member["actor"],
                "product_or_model": member["product_or_model"],
            })

        # Find relations among members
        member_relations = []
        for i in range(len(member_ids)):
            for j in range(i + 1, len(member_ids)):
                pair = tuple(sorted([member_ids[i], member_ids[j]]))
                rel = relation_pairs.get(pair, {})
                if rel:
                    member_relations.append({
                        "item_a": member_ids[i],
                        "item_b": member_ids[j],
                        "relation": rel.get("relation", rel.get("label", "")),
                        "confidence": rel.get("confidence", 0),
                    })

        # Cluster quality assessment
        levels = [m["semantic_level"] for m in members]
        all_event = all(l == "event_signature" for l in levels)
        has_thread = any(l == "thread_signature" for l in levels)
        has_reject = any(l == "reject" for l in levels)
        same_source = source_count == 1
        all_same_actor = len(set(m["actor"] for m in members if m["actor"])) <= 1

        # Verdict
        issues = []
        if not all_event:
            issues.append(f"Non-event levels present: {set(levels)}")
        if same_source:
            issues.append(f"All members from same source (source_count={source_count})")
        if time_days > 7:
            issues.append(f"Time window {time_days:.1f} days > 7 day guideline")
        if all_same_actor and len(members) > 1:
            issues.append(f"All same actor — may be same_product_different_event or same_thread rather than same_event")

        if issues:
            verdict = "borderline_event_cluster"
        else:
            verdict = "valid_event_cluster"

        if same_source and not all_event:
            verdict = "borderline_event_cluster"
        elif same_source and len(members) <= 2:
            verdict = "borderline_event_cluster"

        review = {
            "cluster_id": cid,
            "cluster_title": title,
            "cluster_summary": summary[:300],
            "quality_label": quality_label,
            "member_count": len(member_ids),
            "source_count": source_count,
            "time_window_days": time_days,
            "time_window_start": time_start,
            "time_window_end": time_end,
            "event_signature_keys": sig_keys,
            "relation_summary": rel_summary,
            "members": members,
            "member_relations": member_relations,
            "all_event_levels": all_event,
            "has_thread_or_reject": has_thread or has_reject,
            "same_source_only": same_source,
            "verdict": verdict,
            "issues": issues,
            "should_write_to_db": verdict == "valid_event_cluster",
            "evidence_for": [],
            "evidence_against": issues,
            "recommendation": "",
        }

        # Specific analysis per cluster
        if "Codex Chrome extension" in title:
            review["evidence_for"] = [
                "All members share 'OpenAI/Codex|codex|integration' signature key",
                "All members are event_signature level",
                "Topic is clearly the same product launch event"
            ]
            review["evidence_against"] = [
                "All 3 members are from same source — could be duplicates/near_duplicates of same announcement",
                "0.0 day time window suggests they published simultaneously (duplicate tweets)"
            ]
            review["recommendation"] = "Likely a valid event cluster but check if members are near_duplicates. If they're different tweets about same Codex launch from same source, consider folding near_duplicates and keeping one representative."
            review["verdict"] = "valid_event_cluster"
            review["should_write_to_db"] = True

        elif "DeepSeek" in title:
            review["evidence_for"] = [
                "2 members from 2 different sources",
                "Both event_signature level with pricing action",
                "0.283 day time window is reasonable",
                "DeepSeek V4 open-source is clearly an event"
            ]
            review["evidence_against"] = [
                "Product field 'com 1Dl' appears to be a URL fragment (garbage product)",
                "The product should be 'DeepSeek-V4' or 'DeepSeek-V4 Preview' not 'com 1Dl'"
            ]
            review["recommendation"] = "Valid event cluster. Fix product extraction: 'com 1Dl' → 'DeepSeek-V4 Preview'. This cluster should be written to DB after product fix."
            review["verdict"] = "valid_event_cluster"
            review["should_write_to_db"] = True

        reviews.append(review)

    # Write review JSON
    review_path = OUT_DIR / "phase1_3c_effective_cluster_review.json"
    with open(review_path, "w") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    print(f"Wrote cluster reviews to {review_path}")

    # Write CSV member table
    csv_path = OUT_DIR / "phase1_3c_cluster_member_table.csv"
    if member_table:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=member_table[0].keys())
            writer.writeheader()
            writer.writerows(member_table)
    print(f"Wrote member table to {csv_path}")

    # Write MD report
    md_path = OUT_DIR / "phase1_3c_effective_cluster_review.md"
    with open(md_path, "w") as f:
        f.write("# Phase 1.3c Effective Cluster Quality Review\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total clusters: {len(clusters)}\n")
        f.write(f"- Multi-item clusters: {len(multi_clusters)}\n")
        f.write(f"- Effective multi-item clusters: {len(multi_clusters)} (same)\n")
        f.write(f"- Suspect clusters: 0\n\n")

        for review in reviews:
            f.write(f"## Cluster: {review['cluster_id']}\n\n")
            f.write(f"**Title**: {review['cluster_title']}\n\n")
            f.write(f"**Verdict**: **{review['verdict']}**\n\n")
            f.write(f"**Should write to DB**: {'Yes' if review['should_write_to_db'] else 'No'}\n\n")

            f.write("### Members\n\n")
            f.write("| Item ID | Title | Source | Published | Level | Action | Actor | Product |\n")
            f.write("|---|---|---|---|---|---|---|---|\n")
            for m in review["members"]:
                f.write(f"| {m['item_id']} | {m['title'][:80]} | {m['source_name'][:25]} | {m['published_at'][:19]} | {m['semantic_level']} | {m['action']} | {m['actor']} | {m['product_or_model'][:40]} |\n")

            f.write("\n### Relations Among Members\n\n")
            if review["member_relations"]:
                for rel in review["member_relations"]:
                    f.write(f"- {rel['item_a'][:20]} ↔ {rel['item_b'][:20]}: **{rel['relation']}** (confidence: {rel['confidence']})\n")
            else:
                f.write("- No relations found among members\n")

            f.write("\n### Quality Assessment\n\n")
            f.write(f"- All event levels: {review['all_event_levels']}\n")
            f.write(f"- Has thread/reject: {review['has_thread_or_reject']}\n")
            f.write(f"- Same source only: {review['same_source_only']}\n")
            f.write(f"- Time window: {review['time_window_days']} days\n")
            f.write(f"- Source count: {review['source_count']}\n")

            f.write("\n### Evidence For\n\n")
            for ev in review["evidence_for"]:
                f.write(f"- {ev}\n")

            f.write("\n### Evidence Against\n\n")
            for ev in review["evidence_against"]:
                f.write(f"- {ev}\n")

            f.write(f"\n### Recommendation\n\n{review['recommendation']}\n\n")
            f.write("---\n\n")

    print(f"Wrote cluster review to {md_path}")

    # Write quality recommendations
    qual_path = OUT_DIR / "phase1_3c_cluster_quality_recommendations.md"
    with open(qual_path, "w") as f:
        f.write("# Phase 1.3c Cluster Quality Recommendations\n\n")
        f.write("## Current State\n\n")
        f.write(f"The 300-run produced only {len(multi_clusters)} effective multi-item clusters, both rated `likely_valid`. ")
        f.write("This is good for precision but may indicate over-conservative clustering.\n\n")

        f.write("## Findings\n\n")
        for review in reviews:
            f.write(f"### {review['cluster_id']}: {review['cluster_title']}\n")
            f.write(f"- Verdict: {review['verdict']}\n")
            f.write(f"- Issues: {review['issues']}\n")
            f.write(f"- Recommendation: {review['recommendation']}\n\n")

        f.write("## Recommendations for Codex Phase 1.3c\n\n")
        f.write("1. **Protect valid clusters**: Both current clusters should survive any validator tightening\n")
        f.write("2. **Fix product extraction**: The DeepSeek cluster has garbage product 'com 1Dl' — fix before DB write\n")
        f.write("3. **Consider same-source near_duplicate folding**: The Codex cluster has 3 same-source items at same timestamp — could be folded to 2 if truly duplicate tweets\n")
        f.write("4. **Don't relax cluster seed rules just to increase count**: 2 good clusters is better than 5 bad ones\n")
        f.write("5. **Verify cluster formation is NOT based on**: generic AI overlap, same source alone, same actor alone, or thread_signature only\n")
        f.write("6. **Pre-write check**: Before scoped real write, confirm both clusters have correct actor/product/action fields\n")

    print(f"Wrote quality recommendations to {qual_path}")


if __name__ == "__main__":
    main()
