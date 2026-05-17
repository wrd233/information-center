#!/usr/bin/env python3
"""Phase 1.3c Task F: Phase 1.3c Delta Benchmark.

Builds a 20-30 row delta benchmark from the 300-run evidence,
supplementing the existing Step 1 / Step 3 50-row benchmark.
"""

import json
import csv
from pathlib import Path

EVIDENCE_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600")
OUT_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep")
STEP1_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3b_signature_benchmark_step1")


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load evidence
    items = load_jsonl(EVIDENCE_DIR / "semantic_items.jsonl")
    sigs = load_jsonl(EVIDENCE_DIR / "event_signatures.jsonl")
    errors = load_jsonl(EVIDENCE_DIR / "llm_errors.jsonl")

    item_map = {i["dry_run_item_id"]: i for i in items}
    sig_map = {s["item_id"]: s for s in sigs}

    # Load existing benchmark item IDs to avoid duplication
    existing_ids = set()
    bench_path = STEP1_DIR / "signature_benchmark_50.jsonl"
    if bench_path.exists():
        for row in load_jsonl(bench_path):
            for fid in ["item_id", "item_id_a", "item_id_b"]:
                if fid in row and row[fid]:
                    existing_ids.add(row[fid])

    # Load Chinese miss data
    chinese_misses = load_jsonl(OUT_DIR / "phase1_3c_chinese_event_misses.jsonl")
    garbage_findings = load_jsonl(OUT_DIR / "phase1_3c_garbage_product_audit.jsonl")
    failure_examples = load_jsonl(OUT_DIR / "phase1_3c_llm_failure_examples.jsonl")
    cr_path = OUT_DIR / "phase1_3c_effective_cluster_review.json"
    cluster_review = json.loads(cr_path.read_text()) if cr_path.exists() else []

    # Select benchmark rows
    benchmark_rows = []
    selected_item_ids = set()
    bid = 0

    def add_row(kind, item_id, candidate_id=None, cluster_id=None, current_level="", current_action="",
               current_actor="", current_product="", rec_level="", rec_action="", rec_actor="",
               rec_product="", should_cluster=False, should_thread=False, should_fold=False,
               failure_type="", cost_notes="", reason=""):
        nonlocal bid
        if item_id in selected_item_ids:
            return
        # Skip if in existing benchmark
        if item_id in existing_ids:
            return
        bid += 1
        item = item_map.get(item_id, {})
        row = {
            "benchmark_id": f"delta_{bid:03d}",
            "kind": kind,
            "item_id": item_id,
            "candidate_item_id": candidate_id or "",
            "cluster_id": cluster_id or "",
            "source_name": item.get("source_name", ""),
            "published_at": item.get("published_at", ""),
            "title": (item.get("title", "") or "")[:200],
            "current_semantic_level": current_level,
            "current_action": current_action,
            "current_actor": current_actor,
            "current_product_or_model": current_product,
            "current_relation": "",
            "current_cluster": "",
            "recommended_semantic_level": rec_level,
            "recommended_action": rec_action,
            "recommended_actor": rec_actor,
            "recommended_product_or_model": rec_product,
            "recommended_relation": "",
            "should_form_event_cluster": should_cluster,
            "should_form_thread_relation": should_thread,
            "should_fold": should_fold,
            "failure_type": failure_type,
            "cost_notes": cost_notes,
            "reason": reason,
            "human_label": "",
            "human_notes": "",
        }
        benchmark_rows.append(row)
        selected_item_ids.add(item_id)

    # Priority 1: Chinese false negatives (from Task A)
    for cm in chinese_misses:
        if len(benchmark_rows) >= 30:
            break
        if cm.get("classification") in ("likely_false_negative_event", "likely_false_negative_thread"):
            cs = cm.get("corrected_signature", {})
            add_row(
                kind="single_item_chinese_fn",
                item_id=cm["item_id"],
                current_level=cm.get("semantic_level", "reject"),
                current_action=cm.get("action", "other"),
                current_actor=cm.get("actor", ""),
                current_product=cm.get("product_or_model", ""),
                rec_level=cs.get("semantic_level", "event_signature"),
                rec_action=cs.get("action", "other"),
                rec_actor=cs.get("actor", ""),
                rec_product=cs.get("product_or_model", ""),
                reason=f"Chinese false negative: {cm.get('classification', '')}. {cm.get('invalid_reasons', [])}"
            )

    # Priority 2: Garbage products (blockers from Task B)
    for gf in garbage_findings:
        if len(benchmark_rows) >= 30:
            break
        if gf.get("severity") == "blocker":
            sig = sig_map.get(gf["item_id"], {})
            # Recommend cleaned product
            clean_product = ""
            if gf["suspicious_field"] == "product_or_model":
                clean_product = "[FIX: extract from title/entities]"
            elif gf["suspicious_field"] == "actor":
                clean_product = sig.get("product_or_model", "")

            add_row(
                kind="single_item_garbage_product",
                item_id=gf["item_id"],
                current_level=sig.get("semantic_level", ""),
                current_action=sig.get("action", ""),
                current_actor=sig.get("actor", ""),
                current_product=sig.get("product_or_model", ""),
                rec_level=sig.get("semantic_level", ""),
                rec_action=sig.get("action", ""),
                rec_actor="[FIX]" if gf["suspicious_field"] == "actor" else sig.get("actor", ""),
                rec_product=clean_product if gf["suspicious_field"] == "product_or_model" else sig.get("product_or_model", ""),
                reason=f"Garbage {gf['suspicious_field']}: '{gf['suspicious_value'][:80]}' — {gf['why_suspicious']}"
            )

    # Priority 3: Valid products that must not be over-rejected
    valid_products = {
        "item_445908ccd5234b7ba305d5cd8a7be275": "OpenShell v0.0.41",
        "item_9564c5e550d04eae8642a2117d5bdcdf": "GitHub Copilot Desktop",
        "item_2891159e43e84bc39c6995468481a874": "NVIDIA Nemotron 3 Nano Omni",
        "item_a7e9be5012784ce792fa7e4604ccff57": "Shanghai Telecom Token calling plan",
        "item_d14a2e59b1b444688d03152d2f0e059d": "LangSmith Fleet",
        "item_14b505e34c184cc28ffeaaa3d53efe99": "Grok 4.3",
    }
    for iid, prod_name in valid_products.items():
        if len(benchmark_rows) >= 30:
            break
        sig = sig_map.get(iid, {})
        if sig:
            add_row(
                kind="single_item_valid_product",
                item_id=iid,
                current_level=sig.get("semantic_level", ""),
                current_action=sig.get("action", ""),
                current_actor=sig.get("actor", ""),
                current_product=sig.get("product_or_model", ""),
                rec_level=sig.get("semantic_level", ""),
                rec_action=sig.get("action", ""),
                rec_actor=sig.get("actor", ""),
                rec_product=prod_name,
                reason=f"Valid product that must survive validator: {prod_name}"
            )

    # Priority 4: Cluster members
    for cr in cluster_review:
        if len(benchmark_rows) >= 30:
            break
        for member in cr.get("members", []):
            if len(benchmark_rows) >= 30:
                break
            add_row(
                kind="cluster_member",
                item_id=member["item_id"],
                cluster_id=cr["cluster_id"],
                current_level=member.get("semantic_level", ""),
                current_action=member.get("action", ""),
                current_actor=member.get("actor", ""),
                current_product=member.get("product_or_model", ""),
                rec_level=member.get("semantic_level", ""),
                rec_action=member.get("action", ""),
                rec_actor=member.get("actor", ""),
                rec_product=member.get("product_or_model", ""),
                should_cluster=True,
                reason=f"Member of {cr.get('verdict', '')} cluster: {cr.get('cluster_title', '')[:100]}"
            )

    print(f"Built {len(benchmark_rows)} delta benchmark rows (target: 20-30)")

    # Write JSONL
    jsonl_path = OUT_DIR / "phase1_3c_delta_benchmark.jsonl"
    with open(jsonl_path, "w") as f:
        for row in benchmark_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote to {jsonl_path}")

    # Write CSV
    csv_path = OUT_DIR / "phase1_3c_delta_benchmark.csv"
    if benchmark_rows:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=benchmark_rows[0].keys())
            writer.writeheader()
            writer.writerows(benchmark_rows)
    print(f"Wrote to {csv_path}")

    # Write MD report
    md_path = OUT_DIR / "phase1_3c_delta_benchmark.md"
    with open(md_path, "w") as f:
        f.write("# Phase 1.3c Delta Benchmark\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total rows: {len(benchmark_rows)}\n")
        f.write(f"- Complements existing 50-row Step 1 benchmark ({len(existing_ids)} existing IDs excluded)\n\n")

        by_kind = {}
        for row in benchmark_rows:
            kind = row["kind"]
            by_kind[kind] = by_kind.get(kind, 0) + 1

        f.write("## Distribution by Kind\n\n")
        f.write("| Kind | Count |\n")
        f.write("|---|---|\n")
        for kind, count in sorted(by_kind.items()):
            f.write(f"| {kind} | {count} |\n")

        f.write("\n## All Benchmark Rows\n\n")
        for row in benchmark_rows:
            f.write(f"### {row['benchmark_id']}: {row['kind']}\n")
            f.write(f"- **Item**: {row['item_id']}\n")
            f.write(f"- **Source**: {row['source_name']}\n")
            f.write(f"- **Title**: {row['title'][:150]}\n")
            f.write(f"- **Current**: level={row['current_semantic_level']}, action={row['current_action']}, actor={row['current_actor']}, product={row['current_product_or_model'][:80]}\n")
            f.write(f"- **Recommended**: level={row['recommended_semantic_level']}, action={row['recommended_action']}, actor={row['recommended_actor']}, product={row['recommended_product_or_model'][:80]}\n")
            f.write(f"- **Reason**: {row['reason']}\n")
            if row['should_form_event_cluster']:
                f.write(f"- **Should cluster**: Yes (cluster: {row['cluster_id']})\n")
            f.write("\n")

    print(f"Wrote to {md_path}")

    # Write fixture recommendations
    fix_path = OUT_DIR / "phase1_3c_delta_fixture_recommendations.md"
    with open(fix_path, "w") as f:
        f.write("# Phase 1.3c Delta Fixture Recommendations\n\n")
        f.write(f"The delta benchmark has {len(benchmark_rows)} rows. Recommended fixture additions:\n\n")

        f.write("## Signature Fixture Additions\n\n")
        single_items = [r for r in benchmark_rows if r["kind"].startswith("single_item")]
        f.write(f"Add {len(single_items)} rows to `tests/fixtures/semantic_signature_benchmark_phase1_3b.jsonl`:\n\n")
        for r in single_items[:15]:
            f.write(f"- **{r['benchmark_id']}**: {r['reason'][:120]}\n")

        f.write("\n## Integration Test Cases\n\n")
        f.write("1. **Chinese FN regression**: Verify Chinese items with event triggers get event_signature not reject\n")
        f.write("2. **Garbage product regression**: Verify URL fragments, random tokens, dates are rejected as products\n")
        f.write("3. **Valid product protection**: Verify known products survive validator tightening\n")
        f.write("4. **Cluster member regression**: Verify cluster members maintain correct signatures\n")

        f.write("\n## What NOT to Add\n\n")
        f.write("- Don't hard-code item IDs/titles — use semantic patterns\n")
        f.write("- Don't overfit to 300-run specific items\n")
        f.write("- Focus on rule-based tests: trigger coverage, validator patterns, level classification\n")

    print(f"Wrote to {fix_path}")


if __name__ == "__main__":
    main()
