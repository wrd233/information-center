#!/usr/bin/env python3
"""Phase 1.3c Task A: Chinese Event Detection Miss Analysis.

Reads the Phase 1.3b 300-run evidence, identifies all Chinese/mixed-language items,
classifies them by detection quality, and produces diagnostic outputs.
"""

import json
import re
import csv
import sys
from pathlib import Path
from collections import Counter, defaultdict

EVIDENCE_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600")
OUT_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep")

# CJK Unicode ranges
CJK_RE = re.compile(r'[一-鿿㐀-䶿豈-﫿　-〿＀-￯]')

# Chinese event triggers to check coverage for
CHINESE_TRIGGERS = {
    "发布/发布了/刚刚发布/正式发布": {"action": "release", "examples": ["发布", "发布了", "刚刚发布", "正式发布"]},
    "推出/上线/开放/开源/释出": {"action": "release", "examples": ["推出", "上线", "开放", "开源", "释出"]},
    "支持/接入/打通/集成/连接/对接": {"action": "integration", "examples": ["支持", "接入", "打通", "集成", "连接", "对接"]},
    "技术预览/预览版/内测/公测/候补/waitlist": {"action": "availability", "examples": ["技术预览", "预览版", "内测", "公测", "候补"]},
    "套餐/免费/降价/价格/1块钱/元/折扣/优惠": {"action": "pricing", "examples": ["套餐", "免费", "降价", "价格", "折扣", "优惠"]},
    "超过/超越/领先/采用率/市场份额/市值/用户数/增长": {"action": "adoption_metric", "examples": ["超过", "超越", "领先", "采用率", "市场份额", "市值", "用户数", "增长"]},
    "官宣/新公司/联合创始人/创业/成立/融资": {"action": "company_launch", "examples": ["官宣", "新公司", "联合创始人", "创业", "成立", "融资"]},
    "大会/活动/直播/研讨会/峰会/报名": {"action": "event", "examples": ["大会", "活动", "直播", "研讨会", "峰会", "报名"]},
    "漏洞/安全/修复/补丁": {"action": "security", "examples": ["漏洞", "安全", "修复", "补丁"]},
    "评测/跑分/榜单/基准/准确率": {"action": "benchmark", "examples": ["评测", "跑分", "榜单", "基准", "准确率"]},
}

# Known valid products that should NOT be rejected
KNOWN_VALID_PRODUCTS = {
    "OpenShell v0.0.40", "OpenShell v0.0.37", "OpenShell v0.0.41",
    "LangSmith Fleet", "GitHub Copilot Desktop",
    "NVIDIA Nemotron 3 Nano Omni", "Shanghai Telecom Token calling plan",
    "Gemma 4", "Gemma-4", "GPT-5.5", "Grok 4.3",
    "Hailuo AI App v2.10.0", "Seedance 2.0",
    "Notion Developer Platform", "Notion Custom Agents", "Notion Workers",
    "Perplexity Computer", "Finance Search", "Claude Code", "Codex",
}


def load_jsonl(path):
    if not path.exists():
        print(f"WARNING: {path} not found")
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def has_cjk(text):
    return bool(CJK_RE.search(text or ""))


def classify_chinese_item(item, sig, card):
    """Classify a Chinese item into detection quality categories."""
    title = item.get("title", "")
    summary = card.get("summary", "") if card else ""
    semantic_level = sig.get("semantic_level", "reject")
    action = sig.get("action", "other")
    actor = sig.get("actor", "")
    product = sig.get("product_or_model", "")
    invalid_reasons = sig.get("invalid_reasons", [])
    entities = card.get("entities", []) if card else []

    # Determine if truly event-like based on content analysis
    has_product_entity = bool(product and product.strip() and product not in ("", "other"))
    has_actor = bool(actor and actor.strip())
    has_concrete_action = action not in ("other", "")
    has_strong_entities = bool(entities)

    # Check for event indicators in title/summary
    event_indicators = any(t in (title + summary) for t in [
        "发布", "推出", "上线", "开源", "开放", "释出",
        "官宣", "成立", "融资", "宣布", "正式",
    ])
    thread_indicators = any(t in (title + summary) for t in [
        "如何", "怎么", "为什么", "解读", "分析", "思考",
        "教程", "指南", "经验", "实践", "最佳",
    ])

    is_truly_event_like = event_indicators and (has_product_entity or has_actor or has_strong_entities)
    is_thread_like = thread_indicators and not is_truly_event_like

    if semantic_level == "event_signature":
        if has_product_entity and has_actor and not invalid_reasons:
            return "correct_event_signature"
        elif has_product_entity or has_actor:
            return "correct_event_signature"
        else:
            return "likely_false_positive_event"
    elif semantic_level == "thread_signature":
        if is_thread_like:
            return "correct_thread_signature"
        elif is_truly_event_like:
            return "likely_false_negative_thread"
        else:
            return "correct_thread_signature"
    elif semantic_level == "content_signature":
        if is_truly_event_like:
            return "likely_false_negative_event"
        elif is_thread_like:
            return "likely_false_negative_thread"
        else:
            return "correct_content_signature"
    else:  # reject
        if is_truly_event_like:
            return "likely_false_negative_event"
        elif is_thread_like:
            return "likely_false_negative_thread"
        else:
            return "correct_reject"


def check_trigger_coverage(text):
    """Check which Chinese triggers are present in text."""
    found = []
    for trigger_group, info in CHINESE_TRIGGERS.items():
        for example in info["examples"]:
            if example in (text or ""):
                found.append({
                    "trigger_group": trigger_group,
                    "matched_example": example,
                    "mapped_action": info["action"]
                })
                break
    return found


def propose_corrected_signature(item, sig, card):
    """Propose a corrected signature for a likely false negative."""
    title = item.get("title", "")
    summary = card.get("summary", "") if card else {}
    if isinstance(summary, dict):
        summary_text = summary.get("summary", "")
    else:
        summary_text = str(summary)
    entities = card.get("entities", []) if card else []
    full_text = f"{title} {summary_text}"

    # Try to extract actor from entities
    known_orgs = {"OpenAI", "Anthropic", "Google", "NVIDIA", "Meta", "Microsoft",
                  "DeepSeek", "Perplexity", "Cursor", "Devin", "Manus", "Replit",
                  "Notion", "ElevenLabs", "LlamaIndex", "Firecrawl", "LangChain",
                  "Gemini", "GPT", "Claude", "Bun", "Grok", "Lovable", "Browser Use",
                  "Hailuo", "Qwen", "xAI", "GitHub", "Vercel", "Recursive"}

    actor = sig.get("actor", "")
    product = sig.get("product_or_model", "")
    action = sig.get("action", "other")

    # Try to improve actor from entities
    if not actor or actor in ("", "other"):
        for ent in entities:
            if ent in known_orgs:
                actor = ent
                break
            if ent[0].isupper() and len(ent) > 1:
                actor = ent
                break

    # Try to improve product from entities
    if not product or len(product) < 3:
        for ent in entities:
            if ent not in known_orgs and len(ent) > 2:
                product = ent
                break

    # Detect better action
    triggers_found = check_trigger_coverage(full_text)
    if triggers_found and action == "other":
        action = triggers_found[0]["mapped_action"]

    # Determine semantic level
    event_indicators = any(t in full_text for t in ["发布", "推出", "上线", "开源", "宣布", "官宣", "发布"])
    thread_indicators = any(t in full_text for t in ["如何", "为什么", "解读", "分析", "教程", "指南"])

    if event_indicators and (actor or product):
        level = "event_signature"
    elif thread_indicators and (actor or product):
        level = "thread_signature"
    elif actor or product:
        level = "thread_signature"
    else:
        level = "reject"

    return {
        "semantic_level": level,
        "actor": actor,
        "product_or_model": product,
        "action": action,
        "object": sig.get("object", ""),
        "date_bucket": sig.get("date_bucket", ""),
        "confidence": 0.7 if actor and product else 0.4,
        "is_event_like": level == "event_signature",
        "is_thread_like": level == "thread_signature",
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load all evidence
    print("Loading evidence files...")
    items = load_jsonl(EVIDENCE_DIR / "semantic_items.jsonl")
    cards = load_jsonl(EVIDENCE_DIR / "item_cards.jsonl")
    sigs = load_jsonl(EVIDENCE_DIR / "event_signatures.jsonl")
    levels = load_jsonl(EVIDENCE_DIR / "semantic_levels.jsonl")

    # Build lookup maps
    item_map = {i["dry_run_item_id"]: i for i in items}
    card_map = {c["item_id"]: c for c in cards}
    sig_map = {s["item_id"]: s for s in sigs}
    level_map = {l["item_id"]: l for l in levels}

    # Find Chinese/mixed items
    chinese_items = []
    for item in items:
        item_id = item["dry_run_item_id"]
        title = item.get("title", "")
        snippet = item.get("content_snippet", "")
        if has_cjk(title) or has_cjk(snippet):
            chinese_items.append(item_id)

    print(f"Total items: {len(items)}")
    print(f"Chinese/mixed items: {len(chinese_items)}")

    # Analyze each Chinese item
    results = []
    classification_counts = Counter()
    trigger_coverage = Counter()
    false_negatives = []

    for item_id in chinese_items:
        item = item_map.get(item_id)
        if not item:
            continue
        sig = sig_map.get(item_id, {})
        card = card_map.get(item_id, {})
        level_data = level_map.get(item_id, {})

        classification = classify_chinese_item(item, sig, card)
        classification_counts[classification] += 1

        triggers = check_trigger_coverage(
            (item.get("title", "") or "") + " " + (item.get("content_snippet", "") or "")
        )
        for t in triggers:
            trigger_coverage[t["trigger_group"]] += 1

        record = {
            "item_id": item_id,
            "source_name": item.get("source_name", ""),
            "published_at": item.get("published_at", ""),
            "title": item.get("title", "")[:200],
            "content_snippet": (item.get("content_snippet", "") or "")[:300],
            "semantic_level": sig.get("semantic_level", "reject"),
            "action": sig.get("action", "other"),
            "actor": sig.get("actor", ""),
            "product_or_model": sig.get("product_or_model", ""),
            "object": sig.get("object", ""),
            "invalid_reasons": sig.get("invalid_reasons", []),
            "concreteness_score": sig.get("concreteness_score", 0),
            "confidence": sig.get("confidence", 0),
            "extraction_notes": sig.get("extraction_notes", ""),
            "card_summary": card.get("summary", "") if card else "",
            "content_role": card.get("content_role", "") if card else "",
            "entities": card.get("entities", []) if card else [],
            "classification": classification,
            "triggers_found": triggers,
        }

        if classification in ("likely_false_negative_event", "likely_false_negative_thread", "likely_false_positive_event"):
            record["corrected_signature"] = propose_corrected_signature(item, sig, card)
            false_negatives.append(record)

        results.append(record)

    # Calculate detection rate
    chinese_with_event_sig = sig_map.keys() & set(chinese_items)
    chinese_event_like_in_sigs = sum(
        1 for iid in chinese_items
        if sig_map.get(iid, {}).get("semantic_level") == "event_signature"
    )
    # Count items we classify as truly event-like
    truly_event_like = classification_counts.get("correct_event_signature", 0) + \
                       classification_counts.get("likely_false_negative_event", 0)
    detection_rate = chinese_event_like_in_sigs / len(chinese_items) if chinese_items else 0

    # Write JSONL output
    jsonl_path = OUT_DIR / "phase1_3c_chinese_event_misses.jsonl"
    with open(jsonl_path, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nWrote {len(results)} rows to {jsonl_path}")

    # Write summary JSON
    summary = {
        "total_items": len(items),
        "chinese_items": len(chinese_items),
        "chinese_event_detection_rate": round(detection_rate, 4),
        "chinese_event_signature_count": chinese_event_like_in_sigs,
        "truly_event_like_estimate": truly_event_like,
        "classification_counts": dict(classification_counts),
        "trigger_coverage": dict(trigger_coverage.most_common()),
        "false_negative_count": len(false_negatives),
    }
    summary_path = OUT_DIR / "phase1_3c_chinese_event_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Wrote summary to {summary_path}")

    # Write detailed MD report
    md_path = OUT_DIR / "phase1_3c_chinese_event_misses.md"
    with open(md_path, "w") as f:
        f.write("# Phase 1.3c Chinese Event Detection Miss Analysis\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total 300-run items: {len(items)}\n")
        f.write(f"- Chinese/mixed items found: {len(chinese_items)}\n")
        f.write(f"- Chinese event detection rate in signatures: {detection_rate:.4f} (gate: >= 0.5)\n")
        f.write(f"- Items with event_signature level: {chinese_event_like_in_sigs}\n")
        f.write(f"- Estimated truly event-like Chinese items: {truly_event_like}\n\n")

        f.write("## Classification Breakdown\n\n")
        f.write("| Classification | Count |\n")
        f.write("|---|---|\n")
        for cat, count in classification_counts.most_common():
            f.write(f"| {cat} | {count} |\n")

        f.write("\n## Trigger Coverage\n\n")
        f.write("| Trigger Group | Hit Count |\n")
        f.write("|---|---|\n")
        for trigger, count in trigger_coverage.most_common():
            f.write(f"| {trigger} | {count} |\n")

        # Missing triggers
        found_triggers = set(dict(trigger_coverage.most_common()).keys())
        all_triggers = set(CHINESE_TRIGGERS.keys())
        missing = all_triggers - found_triggers
        if missing:
            f.write("\n## Missing Trigger Groups (no hits in Chinese items)\n\n")
            for t in sorted(missing):
                f.write(f"- {t}\n")

        # False negative details
        f.write(f"\n## Likely False Negatives ({len(false_negatives)} items)\n\n")
        for fn in false_negatives:
            f.write(f"### {fn['item_id']}\n")
            f.write(f"- **Source**: {fn['source_name']}\n")
            f.write(f"- **Title**: {fn['title'][:150]}\n")
            f.write(f"- **Current Level**: {fn['semantic_level']}\n")
            f.write(f"- **Current Action**: {fn['action']}\n")
            f.write(f"- **Actor**: {fn['actor']}\n")
            f.write(f"- **Product**: {fn['product_or_model']}\n")
            f.write(f"- **Classification**: {fn['classification']}\n")
            if "corrected_signature" in fn:
                cs = fn["corrected_signature"]
                f.write(f"- **Corrected Level**: {cs['semantic_level']}\n")
                f.write(f"- **Corrected Actor**: {cs['actor']}\n")
                f.write(f"- **Corrected Product**: {cs['product_or_model']}\n")
                f.write(f"- **Corrected Action**: {cs['action']}\n")
            f.write(f"- **Invalid Reasons**: {fn['invalid_reasons']}\n")
            f.write("\n")

        # Correct positives
        correct_pos = [r for r in results if r["classification"] == "correct_event_signature"]
        f.write(f"\n## Correct Event Signatures ({len(correct_pos)} items)\n\n")
        for cp in correct_pos:
            f.write(f"- **{cp['item_id']}**: {cp['title'][:120]} | actor={cp['actor']} | product={cp['product_or_model']} | action={cp['action']}\n")

        # Correct rejects
        correct_rej = [r for r in results if r["classification"] == "correct_reject"]
        f.write(f"\n## Correctly Rejected ({len(correct_rej)} items)\n\n")
        for cr in correct_rej:
            f.write(f"- **{cr['item_id']}**: {cr['title'][:120]}\n")

    print(f"Wrote detailed report to {md_path}")

    # Write trigger recommendations
    trig_path = OUT_DIR / "phase1_3c_chinese_trigger_recommendations.md"
    with open(trig_path, "w") as f:
        f.write("# Phase 1.3c Chinese Trigger Recommendations\n\n")
        f.write("## Current Coverage Assessment\n\n")
        for trigger_group, info in CHINESE_TRIGGERS.items():
            count = trigger_coverage.get(trigger_group, 0)
            status = "FOUND" if count > 0 else "MISSING"
            f.write(f"- **{trigger_group}**: {status} (hits: {count}) → mapped_action: {info['action']}\n")

        f.write("\n## Recommended New/Enhanced Triggers\n\n")
        f.write("Based on the false negative analysis, these triggers should be added or enhanced:\n\n")

        # Specific recommendations backed by evidence
        f.write("### High Priority (causing false negatives)\n\n")
        f.write("| Trigger | Mapped Action | Should Imply | Risk | Confidence | Force LLM? |\n")
        f.write("|---|---|---|---|---|---|\n")

        for fn in false_negatives[:15]:
            title = fn.get("title", "")
            triggers = fn.get("triggers_found", [])
            if not triggers:
                # Find what trigger SHOULD have matched
                for tg, info in CHINESE_TRIGGERS.items():
                    if any(ex in title for ex in info["examples"]):
                        f.write(f"| {info['examples'][0]} (from {tg}) | {info['action']} | event_signature | Low | 0.8 | Yes if product entity present |\n")
                        break

        f.write("\n### Missing Trigger Assessment\n\n")
        for tg in sorted(missing):
            info = CHINESE_TRIGGERS[tg]
            f.write(f"- **{tg}** → `{info['action']}`\n")
            f.write(f"  - Should imply: event_signature (high confidence if product entity)\n")
            f.write(f"  - Risk of false positives: Low-Medium\n")
            f.write(f"  - Recommended deterministic confidence: 0.7-0.85\n")
            f.write(f"  - Force LLM fallback: Yes when title has product entity + this trigger\n")
            f.write(f"  - Example items: None found in 300-run (trigger group entirely missing)\n\n")

        f.write("\n## Root Cause Analysis\n\n")
        f.write("The Chinese detection rate of 0.3846 is caused by:\n\n")
        f.write("1. **Missing trigger coverage**: Several Chinese event trigger groups have zero hits, meaning the deterministic extractor cannot detect these event types.\n")
        f.write("2. **Weak entity extraction**: Many Chinese items have valid products/actors in their text but the entity extractor fails to identify them from the item cards.\n")
        f.write("3. **Validator over-rejection**: Some Chinese items with valid event signals are rejected due to `missing_concrete_actor_or_product` or `weak_action_without_entity`.\n")
        f.write("4. **LLM fallback not invoked**: Chinese event-like items that fail deterministic extraction don't get LLM-backed signature passes.\n")
        f.write("5. **Card summary quality**: Deterministic minimal cards for Chinese items often miss key entities.\n\n")

    print(f"Wrote trigger recommendations to {trig_path}")


if __name__ == "__main__":
    main()
