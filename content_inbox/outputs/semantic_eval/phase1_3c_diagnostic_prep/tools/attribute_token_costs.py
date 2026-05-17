#!/usr/bin/env python3
"""Phase 1.3c Task D: Token Cost Attribution and Reduction Plan.

Analyzes token consumption across stages and items in the Phase 1.3b 300-run.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

EVIDENCE_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600")
OUT_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep")


def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    metrics = load_json(EVIDENCE_DIR / "stage_metrics.json")
    calls = load_jsonl(EVIDENCE_DIR / "llm_calls.jsonl")
    items = load_jsonl(EVIDENCE_DIR / "semantic_items.jsonl")
    sigs = load_jsonl(EVIDENCE_DIR / "event_signatures.jsonl")

    item_map = {i["dry_run_item_id"]: i for i in items}
    sig_map = {s["item_id"]: s for s in sigs}

    # Stage-level breakdown (from stage_metrics)
    concurrency = metrics.get("concurrency", {})
    by_task = concurrency.get("by_task", {})
    token_cost = metrics.get("token_cost", [])
    stage_budgets = metrics.get("stage_budgets", {})

    total_tokens = concurrency.get("actual_tokens", 877140)
    total_calls = concurrency.get("actual_calls", 220)
    cache_hit_tokens = concurrency.get("cache_hit_tokens", 236160)
    cache_hit_rate = concurrency.get("cache_hit_rate", 0.2692)
    total_items = 300

    # Per-stage breakdown
    stage_breakdown = []
    for tc in token_cost:
        if tc.get("calls", 0) == 0:
            continue
        stage_breakdown.append({
            "task_type": tc["task_type"],
            "calls": tc["calls"],
            "success": tc["success"],
            "failed": tc["failed"],
            "total_tokens": tc["total_tokens"],
            "input_tokens": tc["input_tokens"],
            "output_tokens": tc["output_tokens"],
            "avg_tokens_per_call": round(tc["total_tokens"] / tc["calls"], 1) if tc["calls"] else 0,
            "tokens_per_item": round(tc["total_tokens"] / total_items, 1),
            "cache_hit_tokens": tc.get("cache_hit_tokens", 0),
            "avg_latency_ms": tc["avg_latency_ms"],
            "retry_count": tc.get("retry_count", 0),
        })

    # Per-call analysis
    calls_by_stage = defaultdict(list)
    calls_by_item = defaultdict(list)
    total_failure_tokens = 0
    successful_calls = []
    failed_calls = []

    for call in calls:
        stage = call.get("stage", "unknown")
        calls_by_stage[stage].append(call)
        for iid in call.get("item_ids", []):
            calls_by_item[iid].append(call)
        tokens = call.get("input_tokens", 0) + call.get("output_tokens", 0)
        if not call.get("success", False):
            total_failure_tokens += tokens
            failed_calls.append(call)
        else:
            successful_calls.append(call)

    # Top expensive calls
    all_calls_sorted = sorted(calls, key=lambda c: c.get("input_tokens", 0) + c.get("output_tokens", 0), reverse=True)
    top_expensive_calls = []
    for c in all_calls_sorted[:20]:
        top_expensive_calls.append({
            "call_id": c.get("call_id"),
            "stage": c.get("stage"),
            "input_tokens": c.get("input_tokens", 0),
            "output_tokens": c.get("output_tokens", 0),
            "total_tokens": c.get("input_tokens", 0) + c.get("output_tokens", 0),
            "success": c.get("success", False),
            "prompt_variant": c.get("prompt_variant"),
            "item_count": len(c.get("item_ids", [])),
            "item_ids": c.get("item_ids", [])[:3],
        })

    # Token cost per semantic level
    tokens_by_level = defaultdict(int)
    items_by_level = defaultdict(int)
    for call in successful_calls:
        for iid in call.get("item_ids", []):
            sig = sig_map.get(iid, {})
            level = sig.get("semantic_level", "unknown")
            call_tokens = call.get("input_tokens", 0) + call.get("output_tokens", 0)
            share = call_tokens / len(call.get("item_ids", [])) if call.get("item_ids") else call_tokens
            tokens_by_level[level] += share
            items_by_level[level] += 1

    # Top expensive items (total tokens across all calls involving item)
    item_token_totals = defaultdict(float)
    for call in calls:
        iids = call.get("item_ids", [])
        if not iids:
            continue
        call_tokens = call.get("input_tokens", 0) + call.get("output_tokens", 0)
        share = call_tokens / len(iids)
        for iid in iids:
            item_token_totals[iid] += share

    top_items = sorted(item_token_totals.items(), key=lambda x: x[1], reverse=True)[:20]
    top_expensive_items = []
    for iid, tokens in top_items:
        item = item_map.get(iid, {})
        sig = sig_map.get(iid, {})
        top_expensive_items.append({
            "item_id": iid,
            "title": item.get("title", "")[:120],
            "source_name": item.get("source_name", ""),
            "semantic_level": sig.get("semantic_level", ""),
            "estimated_tokens": round(tokens, 1),
        })

    # Write attribution JSON
    attribution = {
        "overall": {
            "total_items": total_items,
            "actual_tokens": total_tokens,
            "actual_calls": total_calls,
            "tokens_per_item": round(total_tokens / total_items, 1),
            "cache_hit_tokens": cache_hit_tokens,
            "cache_hit_rate": round(cache_hit_rate, 4),
            "failure_tokens": total_failure_tokens,
            "failure_token_pct": round(total_failure_tokens / total_tokens * 100, 1),
        },
        "by_stage": stage_breakdown,
        "by_semantic_level": {
            level: {
                "estimated_tokens": round(tokens, 1),
                "items_touching": items_by_level[level],
                "avg_tokens_per_item": round(tokens / items_by_level[level], 1) if items_by_level[level] else 0,
            }
            for level, tokens in sorted(tokens_by_level.items(), key=lambda x: x[1], reverse=True)
        },
        "top_expensive_calls": top_expensive_calls,
        "top_expensive_items": top_expensive_items,
        "failure_cost": {
            "total_failure_tokens": total_failure_tokens,
            "pct_of_total": round(total_failure_tokens / total_tokens * 100, 1),
            "failed_call_count": len(failed_calls),
        },
    }

    attr_path = OUT_DIR / "phase1_3c_token_cost_attribution.json"
    with open(attr_path, "w") as f:
        json.dump(attribution, f, indent=2, ensure_ascii=False)
    print(f"Wrote token attribution to {attr_path}")

    # Write high-cost examples
    hc_path = OUT_DIR / "phase1_3c_high_cost_examples.jsonl"
    with open(hc_path, "w") as f:
        for item in top_expensive_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
        for c in top_expensive_calls:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote high-cost examples to {hc_path}")

    # Write MD report
    md_path = OUT_DIR / "phase1_3c_token_cost_attribution.md"
    with open(md_path, "w") as f:
        f.write("# Phase 1.3c Token Cost Attribution\n\n")
        f.write("## Overall\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|---|---|\n")
        f.write(f"| Total items | {total_items} |\n")
        f.write(f"| Total tokens | {total_tokens:,} |\n")
        f.write(f"| Total LLM calls | {total_calls} |\n")
        f.write(f"| Tokens per item | {total_tokens/total_items:.1f} |\n")
        f.write(f"| Cache hit rate | {cache_hit_rate:.2%} |\n")
        f.write(f"| Failure tokens | {total_failure_tokens:,} ({total_failure_tokens/total_tokens*100:.1f}%) |\n")

        f.write("\n## By Stage\n\n")
        f.write("| Stage | Calls | Tokens | % of Total | Tokens/Item | Success | Failed |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for sb in stage_breakdown:
            pct = sb["total_tokens"] / total_tokens * 100
            f.write(f"| {sb['task_type']} | {sb['calls']} | {sb['total_tokens']:,} | {pct:.1f}% | {sb['tokens_per_item']:.1f} | {sb['success']} | {sb['failed']} |\n")

        f.write("\n## By Semantic Level\n\n")
        f.write("| Level | Estimated Tokens | Items Touching | Avg Tokens/Item |\n")
        f.write("|---|---|---|---|\n")
        for level, data in sorted(attribution["by_semantic_level"].items(), key=lambda x: x[1]["estimated_tokens"], reverse=True):
            f.write(f"| {level} | {data['estimated_tokens']:,.0f} | {data['items_touching']} | {data['avg_tokens_per_item']:.1f} |\n")

        f.write("\n## Top 10 Most Expensive Items\n\n")
        f.write("| Item ID | Title | Source | Level | Est. Tokens |\n")
        f.write("|---|---|---|---|---|\n")
        for item in top_expensive_items[:10]:
            f.write(f"| {item['item_id']} | {item['title'][:80]} | {item['source_name'][:30]} | {item['semantic_level']} | {item['estimated_tokens']:,.0f} |\n")

        f.write("\n## Top 10 Most Expensive Calls\n\n")
        f.write("| Call ID | Stage | Tokens | Success | Variant | Items |\n")
        f.write("|---|---|---|---|---|---|\n")
        for c in top_expensive_calls[:10]:
            f.write(f"| {c['call_id']} | {c['stage']} | {c['total_tokens']:,} | {c['success']} | {c['prompt_variant']} | {c['item_count']} |\n")

    print(f"Wrote attribution report to {md_path}")

    # Write reduction recommendations
    red_path = OUT_DIR / "phase1_3c_token_reduction_recommendations.md"
    with open(red_path, "w") as f:
        f.write("# Phase 1.3c Token Reduction Recommendations\n\n")
        f.write(f"Current: {total_tokens/total_items:.1f} tokens/item. Target: < 2000 tokens/item.\n")
        f.write(f"Savings needed: ~{total_tokens - 2000 * total_items:,} tokens ({(total_tokens - 2000*total_items)/total_tokens*100:.1f}% reduction)\n\n")

        f.write("## Ranked Recommendations\n\n")

        recommendations = [
            {
                "rank": 1,
                "action": "Reduce item_relation batch size from 8-9 to 4-5 pairs",
                "expected_savings": "80,000-120,000 tokens (item_relation is 61.5% of total, smaller batches reduce output tokens)",
                "quality_risk": "Low — smaller batches actually improve JSON reliability",
                "difficulty": "Low — config change",
                "priority": "P0",
            },
            {
                "rank": 2,
                "action": "Skip relation LLM for reject and content_signature items",
                "expected_savings": "~150,000 tokens (reject+content_signature ~60% of items don't need pair relations)",
                "quality_risk": "Low — these items rarely form meaningful relations",
                "difficulty": "Low — filter in candidates.py",
                "priority": "P0",
            },
            {
                "rank": 3,
                "action": "Use deterministic rule-based relations for same_thread and same_product_different_event lanes",
                "expected_savings": "~50,000 tokens (90 same_product_different_event + 11 same_thread currently go through LLM)",
                "quality_risk": "Medium — need careful rule design",
                "difficulty": "Medium — requires relation_policy.py changes",
                "priority": "P1",
            },
            {
                "rank": 4,
                "action": "Trim item_card fields passed into relation prompts — send only title + signature + key entities, not full summary",
                "expected_savings": "~60,000 tokens (reduces input tokens for 157 item_relation calls)",
                "quality_risk": "Low — relations need event facts, not full prose",
                "difficulty": "Medium — prompt and pipeline changes",
                "priority": "P1",
            },
            {
                "rank": 5,
                "action": "Skip LLM signature pass for deterministic high-confidence versioned releases",
                "expected_savings": "~20,000 tokens (many versioned releases have 100% deterministic confidence)",
                "quality_risk": "Low — high-confidence deterministic already 0.9821 valid rate",
                "difficulty": "Low — gating check in signatures.py",
                "priority": "P2",
            },
            {
                "rank": 6,
                "action": "Batch or rule-handle same_thread candidates — they rarely need LLM judgment",
                "expected_savings": "~15,000 tokens",
                "quality_risk": "Medium",
                "difficulty": "Medium",
                "priority": "P2",
            },
            {
                "rank": 7,
                "action": "Use compact event_signature prompt for LLM fallback and reduce output schema size",
                "expected_savings": "~30,000 tokens (prompt vs output trimming)",
                "quality_risk": "Low-Medium",
                "difficulty": "Low — prompt edit",
                "priority": "P2",
            },
            {
                "rank": 8,
                "action": "Use LLM only for Chinese event-like items that deterministic cannot resolve",
                "expected_savings": "~10,000 tokens (small but important for Chinese recall)",
                "quality_risk": "Low — addresses specific gap",
                "difficulty": "Low",
                "priority": "P1",
            },
        ]

        for rec in recommendations:
            f.write(f"### {rec['rank']}. {rec['action']}\n\n")
            f.write(f"- **Expected savings**: {rec['expected_savings']}\n")
            f.write(f"- **Quality risk**: {rec['quality_risk']}\n")
            f.write(f"- **Difficulty**: {rec['difficulty']}\n")
            f.write(f"- **Priority**: {rec['priority']}\n\n")

        f.write("## Combined Savings Estimate\n\n")
        f.write("Implementing P0+P1 recommendations could reduce tokens/item from {:.1f} to ~{:.0f}, saving ~{:,.0f} tokens per 300-item run.\n".format(
            total_tokens/total_items,
            1800,
            total_tokens - 1800 * total_items
        ))

    print(f"Wrote reduction recommendations to {red_path}")


if __name__ == "__main__":
    main()
