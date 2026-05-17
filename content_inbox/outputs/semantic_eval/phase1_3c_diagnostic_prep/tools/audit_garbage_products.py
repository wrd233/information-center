#!/usr/bin/env python3
"""Phase 1.3c Task B: Garbage Product/Actor Validator Audit.

Scans all accepted event/thread signatures in the 300-run for garbage
actor/product/object fields and produces validator rule recommendations.
"""

import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

EVIDENCE_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/api_xgo_ing_phase1_3b_full_300_20260517_234600")
OUT_DIR = Path("/Users/wangrundong/work/infomation-center/content_inbox/outputs/semantic_eval/phase1_3c_diagnostic_prep")

# Patterns for garbage detection
URL_PATTERN = re.compile(r'https?://|t\.co/|\.com|\.org|\.io|\.dev|\.ai|\.gg')
SHORTLINK_PATTERN = re.compile(r'^[a-zA-Z0-9]{5,8}$')  # shortlinks like t.co/xxxxx remnants
RANDOM_ALNUM_PATTERN = re.compile(r'^[a-z0-9]{6,10}$')  # like "sow0e7ym", "iobqd8a9", "ay4dy8o5"
DATE_PATTERN = re.compile(r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+(st|nd|rd|th)?', re.IGNORECASE)
MONTH_DAY_PATTERN = re.compile(r'^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(st|nd|rd|th)?$', re.IGNORECASE)
PURE_NUMBER_PATTERN = re.compile(r'^[\d,.]+\s*(million|billion|trillion|k|%|percent)?$', re.IGNORECASE)
NUMERIC_PHRASE_PATTERN = re.compile(r'^(a\s+|an\s+)?\d+[\d\s,.-]*\w*$')
PREPOSITION_START = re.compile(r'^(for|with|from|every|just|and|or|in|on|to|of|as|by|the|a|an|that|this|its|our|your|their)\s', re.IGNORECASE)
SENTENCE_PUNCTUATION = re.compile(r'[.!?;,]')
VERSION_ONLY = re.compile(r'^v?\d+\.\d+(\.\d+)?$')
PRICE_ONLY = re.compile(r'^[$€£¥]?\s*\d+[\d,.]*\s*(元|块|美元|美金|欧元)?$')
GENERIC_AI_TERMS = re.compile(r'^(AI|ML|LLM|agent|model|API|SDK|tool|framework|platform|system|solution|service|product|feature|update|release)$', re.IGNORECASE)

# Known valid product names
KNOWN_VALID = {
    "OpenShell v0.0.40", "OpenShell v0.0.37", "OpenShell v0.0.41",
    "LangSmith Fleet", "GitHub Copilot Desktop",
    "NVIDIA Nemotron 3 Nano Omni", "nemotron 3 nano omni",
    "Token calling plan",
    "Gemma 4", "Gemma-4", "GPT-5.5", "Grok 4.3", "Grok 4.3",
    "Hailuo AI App v2.10.0", "Seedance 2.0",
    "Notion Developer Platform", "Notion Custom Agents", "Notion Workers",
    "Perplexity Computer", "Finance Search",
    "Claude Code", "Claude Opus", "Codex", "codex",
    "GPT Image", "GPT Image 2",
    "ElevenAgents",
    "Hermes Agent", "Hermes agent",
    "QVeris CLI",
    "Adialante", "Recursive", "PLAN0",
    "Colossus 1",
    "ICML26",
    "AI Security Summit",
    "LangSmith Fleet",
    "Claude", "Claude w",
    "Gemini Intelligence",
    "Googlebook",
    "DGX Spark", "DGX spark",
    "Krea 2",
    "DeepSeek-V4",
    "Agent Harness",
    "Stelline Developer Kit",
    "Notion Workers",
    "OpenShell",
    "SF 2026",
}


def load_jsonl(path):
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def score_garbage_risk(field_value, field_name, item_title=""):
    """Score how suspicious a field value is. Returns (risk_category, reasons)."""
    v = (field_value or "").strip()
    if not v:
        return "acceptable", []

    reasons = []
    lower_v = v.lower()

    # Check against known valid products
    if v in KNOWN_VALID or lower_v in KNOWN_VALID:
        return "acceptable", []

    # URL fragments
    if URL_PATTERN.search(v):
        reasons.append("contains_url_fragment")

    # Short random alphanumeric tokens
    if RANDOM_ALNUM_PATTERN.match(v):
        reasons.append("random_alphanumeric_token")

    # Date patterns
    if DATE_PATTERN.search(v):
        reasons.append("contains_date_fragment")
    if MONTH_DAY_PATTERN.match(v):
        reasons.append("is_month_day_phrase")

    # Pure numbers
    if PURE_NUMBER_PATTERN.match(v):
        reasons.append("is_pure_number_or_numeric_phrase")

    # Numeric fragments embedded in irrelevant text
    if re.search(r'\b(around|about|of|up|to|a|over)\s+\d+', v, re.IGNORECASE) and len(v.split()) <= 3:
        reasons.append("numeric_preposition_fragment")

    # Starts with weak preposition
    if PREPOSITION_START.match(v) and len(v.split()) > 2:
        reasons.append("starts_with_weak_preposition")

    # Sentence fragments (contains punctuation + verbs)
    if SENTENCE_PUNCTUATION.search(v) and len(v.split()) > 3:
        reasons.append("contains_sentence_punctuation_in_long_phrase")

    # Long phrase (more than 6 words)
    if len(v.split()) > 6:
        reasons.append("long_phrase_gt_6_words")

    # Verb phrases (starts with verb-like word)
    verb_start = re.compile(r'^(build|create|make|use|get|run|try|learn|see|find|give|take|send|launch|release|announce|introduce|ship|add|fix|update|upgrade|improve|integrate|support)\s', re.IGNORECASE)
    if verb_start.match(v):
        reasons.append("starts_with_verb_phrase")

    # Generic AI terms used as standalone product
    if GENERIC_AI_TERMS.match(v):
        reasons.append("generic_ai_term_as_product")

    # Version only
    if VERSION_ONLY.match(v):
        reasons.append("isolated_version")

    # Price only
    if PRICE_ONLY.match(v):
        reasons.append("price_only_fragment")

    # Very short lowercase
    if len(v) <= 3 and v.islower() and not v.isalpha():
        reasons.append("short_lowercase_non_entity")

    # Product contains "for every" pattern
    if re.search(r'for\s+every|for\s+your|for\s+all', v, re.IGNORECASE):
        reasons.append("generic_for_every_pattern")

    # Determine severity
    blocker_reasons = {"random_alphanumeric_token", "is_month_day_phrase", "is_pure_number_or_numeric_phrase",
                       "contains_date_fragment", "price_only_fragment", "short_lowercase_non_entity",
                       "contains_url_fragment", "isolated_version"}
    warning_reasons = {"starts_with_weak_preposition", "contains_sentence_punctuation_in_long_phrase",
                       "starts_with_verb_phrase", "generic_ai_term_as_product",
                       "long_phrase_gt_6_words", "generic_for_every_pattern",
                       "numeric_preposition_fragment"}

    if any(r in blocker_reasons for r in reasons):
        return "blocker", reasons
    elif any(r in warning_reasons for r in reasons):
        return "warning", reasons
    return "acceptable", reasons


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading evidence...")
    sigs = load_jsonl(EVIDENCE_DIR / "event_signatures.jsonl")
    items = load_jsonl(EVIDENCE_DIR / "semantic_items.jsonl")
    item_map = {i["dry_run_item_id"]: i for i in items}

    print(f"Loaded {len(sigs)} signatures, {len(items)} items")

    # Analyze all non-reject signatures
    findings = []
    by_severity = Counter()
    by_suspicion_category = Counter()
    garbage_examples = []

    for sig in sigs:
        level = sig.get("semantic_level", "reject")
        if level == "reject":
            continue

        item_id = sig["item_id"]
        item = item_map.get(item_id, {})
        title = item.get("title", "")

        # Check product
        product = sig.get("product_or_model", "")
        prod_risk, prod_reasons = score_garbage_risk(product, "product_or_model", title)
        # Check actor
        actor = sig.get("actor", "")
        act_risk, act_reasons = score_garbage_risk(actor, "actor", title)
        # Check object
        obj = sig.get("object", "")
        obj_risk, obj_reasons = score_garbage_risk(obj, "object", title)

        for field_name, value, risk, reasons in [
            ("product_or_model", product, prod_risk, prod_reasons),
            ("actor", actor, act_risk, act_reasons),
            ("object", obj, obj_risk, obj_reasons),
        ]:
            if risk != "acceptable":
                by_severity[risk] += 1
                for r in reasons:
                    by_suspicion_category[r] += 1

                finding = {
                    "item_id": item_id,
                    "source_name": item.get("source_name", ""),
                    "title": title[:200],
                    "semantic_level": level,
                    "action": sig.get("action", ""),
                    "actor": actor,
                    "product_or_model": product,
                    "object": obj,
                    "suspicious_field": field_name,
                    "suspicious_value": value,
                    "suspicion_category": reasons,
                    "severity": risk,
                    "why_suspicious": ", ".join(reasons),
                    "recommended_correction": f"Re-extract {field_name} from title/entities or leave empty",
                    "recommended_validator_rule": f"Reject {field_name} if {' OR '.join(reasons)}",
                }
                findings.append(finding)
                if risk == "blocker":
                    garbage_examples.append(finding)

    # Write findings JSONL
    audit_path = OUT_DIR / "phase1_3c_garbage_product_audit.jsonl"
    with open(audit_path, "w") as f:
        for finding in findings:
            f.write(json.dumps(finding, ensure_ascii=False) + "\n")
    print(f"Wrote {len(findings)} suspicious field findings to {audit_path}")

    # Write detailed MD audit
    md_path = OUT_DIR / "phase1_3c_garbage_product_audit.md"
    with open(md_path, "w") as f:
        f.write("# Phase 1.3c Garbage Product/Actor Audit\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Total non-reject signatures analyzed: {sum(1 for s in sigs if s.get('semantic_level','reject')!='reject')}\n")
        f.write(f"- Suspicious field instances found: {len(findings)}\n")
        f.write(f"- Blockers: {by_severity['blocker']}\n")
        f.write(f"- Warnings: {by_severity['warning']}\n\n")

        f.write("## Suspicion Category Breakdown\n\n")
        f.write("| Category | Count |\n")
        f.write("|---|---|\n")
        for cat, count in by_suspicion_category.most_common():
            f.write(f"| {cat} | {count} |\n")

        f.write("\n## Blocker Garbage Examples\n\n")
        for ex in findings:
            if ex["severity"] != "blocker":
                continue
            f.write(f"### {ex['item_id']} — `{ex['suspicious_value'][:100]}`\n")
            f.write(f"- **Source**: {ex['source_name']}\n")
            f.write(f"- **Title**: {ex['title'][:150]}\n")
            f.write(f"- **Field**: {ex['suspicious_field']}\n")
            f.write(f"- **Level/Action**: {ex['semantic_level']}/{ex['action']}\n")
            f.write(f"- **Actor**: {ex['actor']}\n")
            f.write(f"- **Product**: {ex['product_or_model']}\n")
            f.write(f"- **Why**: {ex['why_suspicious']}\n\n")

        f.write("\n## Warning Examples\n\n")
        for ex in findings:
            if ex["severity"] != "warning":
                continue
            f.write(f"- **{ex['item_id']}**: `{ex['suspicious_value'][:80]}` ({ex['suspicious_field']}) — {ex['why_suspicious']}\n")

        f.write("\n## Known Valid Products (must not be over-rejected)\n\n")
        for p in sorted(KNOWN_VALID):
            f.write(f"- `{p}`\n")

    print(f"Wrote audit report to {md_path}")

    # Write product validator rules
    rules_path = OUT_DIR / "phase1_3c_product_validator_rules.json"
    rules = {
        "version": "1.3c-draft",
        "generated_from": "Phase 1.3b 300-run evidence audit",
        "rules": [
            {
                "id": "PV-001",
                "name": "reject_short_random_alphanumeric",
                "pattern": "^[a-z0-9]{6,10}$",
                "description": "Reject product if it is a short random alphanumeric token (e.g., sow0e7ym, iobqd8a9, ay4dy8o5)",
                "severity": "blocker",
                "examples": ["sow0e7ym", "iobqd8a9", "ay4dy8o5", "CERX3N35", "ns123abc", "trq212", "DeYA2K", "Yeuoly1"],
                "field": "product_or_model"
            },
            {
                "id": "PV-002",
                "name": "reject_month_day_phrase",
                "pattern": "^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\s+\\d{1,2}(st|nd|rd|th)?$",
                "description": "Reject product if it is a month+day phrase (e.g., May 4th, June 4th)",
                "severity": "blocker",
                "examples": ["May 4th", "June 4th"],
                "field": "product_or_model"
            },
            {
                "id": "PV-003",
                "name": "reject_pure_number_product",
                "pattern": r"^[\d,]+\s*(million|billion|trillion|k|%|percent)?$|^(a\s+|an\s+)?\d+[\d\s,.-]*\w*$",
                "description": "Reject product if it is a pure number or numeric phrase (e.g., around 1897, of 12M, a 24, up 130)",
                "severity": "blocker",
                "examples": ["around 1897", "of 12M", "a 24", "up 130", "to 100x", "to 55", "of 1", "a 0", "a 48-hour", "crossed 4", "top 12", "top 10", "under 35", "up 80"],
                "field": "product_or_model"
            },
            {
                "id": "PV-004",
                "name": "reject_date_fragment_product",
                "pattern": r"(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+",
                "description": "Reject product if it contains date-like fragments",
                "severity": "blocker",
                "examples": ["since 2018"],
                "field": "product_or_model"
            },
            {
                "id": "PV-005",
                "name": "reject_weak_preposition_start_product",
                "pattern": r"^(for|with|from|every|just|and|or|in|on|to|of|as|by|the|a|an|that|this|its|our|your|their)\s",
                "description": "Reject product if it starts with weak preposition/determiner unless in known product list",
                "severity": "warning",
                "examples": [],
                "field": "product_or_model",
                "exceptions": ["Notion Developer Platform", "Notion Custom Agents"]
            },
            {
                "id": "PV-006",
                "name": "reject_verb_phrase_product",
                "pattern": r"^(build|create|make|use|get|run|try|learn|see|find|give|take|send|launch|release|announce|introduce|ship|add|fix|update|upgrade|improve|integrate|support|meet)\s",
                "description": "Reject product if it starts with a verb (looks like a sentence fragment, not a product name)",
                "severity": "warning",
                "examples": ["Give Your Chat Agent", "Meet Replit Parallel Agents", "Try Parallel Agents"],
                "field": "product_or_model"
            },
            {
                "id": "PV-007",
                "name": "reject_long_phrase_product",
                "pattern": r"^\w+(\s+\w+){6,}$",
                "description": "Reject product if longer than 6 words and not a known valid product",
                "severity": "warning",
                "examples": ["data then skip the interface entirely Agents", "everything when you build products for Finance"],
                "field": "product_or_model"
            },
            {
                "id": "PV-008",
                "name": "reject_sentence_fragment_product",
                "pattern": r"[.!?;,].*\s+\w+\s+\w+",
                "description": "Reject product if contains sentence punctuation in a multi-word phrase",
                "severity": "warning",
                "examples": ["CI failures. Set up always-on agents", "just built issue was the initial characters"],
                "field": "product_or_model"
            },
            {
                "id": "PV-009",
                "name": "reject_generic_for_every_product",
                "pattern": r"for\s+every|for\s+your|for\s+all",
                "description": "Reject product containing 'for every/your/all' pattern — these are descriptive phrases not products",
                "severity": "blocker",
                "examples": ["Git semantics for every file your agent"],
                "field": "product_or_model"
            },
            {
                "id": "PV-010",
                "name": "reject_url_fragment_product",
                "pattern": r"https?://|t\.co/|\.com|\.org|\.io|\.dev|\.ai\b",
                "description": "Reject product if it contains URL fragments",
                "severity": "blocker",
                "examples": ["com 1Dl"],
                "field": "product_or_model"
            }
        ],
        "actor_rules": [
            {
                "id": "AV-001",
                "name": "former_employer_is_not_actor",
                "description": "Former employer mentioned in context (e.g., '前 Meta FAIR Director') is not the actor. The actor is the person or new company.",
                "severity": "warning",
                "examples": ["Meta mentioned as former employer, actor should be 田渊栋 or Recursive"]
            },
            {
                "id": "AV-002",
                "name": "product_is_not_organization_actor",
                "description": "Product/model name (e.g., GPT-5.5, Gemini) should not be used as actor unless the source is the official product account.",
                "severity": "warning",
                "examples": ["GPT-5.5 as actor → should be OpenAI", "Gemini as actor → should be Google"]
            },
            {
                "id": "AV-003",
                "name": "source_account_as_actor_only_if_official",
                "description": "Social media account name can be actor only if it's the official source making an announcement about itself.",
                "severity": "info"
            },
            {
                "id": "AV-004",
                "name": "prefer_empty_actor_over_wrong_actor",
                "description": "Leave actor empty rather than populating it with a wrong organization/product name.",
                "severity": "blocker",
                "examples": ["arxiv as actor for pricing → wrong, should be empty"]
            }
        ]
    }
    with open(rules_path, "w") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
    print(f"Wrote validator rules to {rules_path}")

    # Write rules markdown
    rules_md = OUT_DIR / "phase1_3c_product_validator_rules.md"
    with open(rules_md, "w") as f:
        f.write("# Phase 1.3c Product Validator Rules\n\n")
        f.write("## Product/Model Validation Rules\n\n")
        for rule in rules["rules"]:
            f.write(f"### {rule['id']}: {rule['name']}\n")
            f.write(f"- **Severity**: {rule['severity']}\n")
            f.write(f"- **Pattern**: `{rule['pattern']}`\n")
            f.write(f"- **Description**: {rule['description']}\n")
            if rule.get("examples"):
                f.write(f"- **Examples from 300-run**: {', '.join(f'`{ex}`' for ex in rule['examples'])}\n")
            if rule.get("exceptions"):
                f.write(f"- **Exceptions**: {', '.join(f'`{ex}`' for ex in rule['exceptions'])}\n")
            f.write(f"- **Field**: {rule['field']}\n\n")

        f.write("## Actor Validation Rules\n\n")
        for rule in rules["actor_rules"]:
            f.write(f"### {rule['id']}: {rule['name']}\n")
            f.write(f"- **Severity**: {rule['severity']}\n")
            f.write(f"- **Description**: {rule['description']}\n")
            if rule.get("examples"):
                f.write(f"- **Examples**: {', '.join(rule['examples'])}\n")
            f.write("\n")

    print(f"Wrote rules markdown to {rules_md}")

    # Actor validator rules
    actor_md = OUT_DIR / "phase1_3c_actor_validator_rules.md"
    with open(actor_md, "w") as f:
        f.write("# Phase 1.3c Actor Validator Rules\n\n")
        f.write("## Current Actor Extraction Issues\n\n")
        f.write("Based on the 300-run evidence, actor extraction has these issues:\n\n")

        # Find specific actor issues
        actor_issues = [f for f in findings if f["suspicious_field"] == "actor"]
        for ai in actor_issues:
            f.write(f"- **{ai['item_id']}**: actor=`{ai['suspicious_value']}` — {ai['why_suspicious']}\n")

        f.write("\n## Actor Validation Rules\n\n")
        for rule in rules["actor_rules"]:
            f.write(f"### {rule['id']}: {rule['name']}\n")
            f.write(f"- **Severity**: {rule['severity']}\n")
            f.write(f"- **{rule['description']}**\n")
            if rule.get("examples"):
                for ex in rule["examples"]:
                    f.write(f"  - {ex}\n")
            f.write("\n")

        f.write("\n## Recommendations\n\n")
        f.write("1. Never use a social media username/handle as actor unless verified as official source\n")
        f.write("2. Never use a product/model name as the actor — always use the organization\n")
        f.write("3. Cross-check actor against source_name — if the source is a personal account tweeting about a company, the company is the actor\n")
        f.write("4. Prefer empty actor over incorrect actor — missing actor is better than wrong attribution\n")
        f.write("5. For Chinese items, allow person names as actors when they are making official announcements\n")

    print(f"Wrote actor rules to {actor_md}")

    # Print summary
    print(f"\n=== Garbage Product Audit Summary ===")
    print(f"Total suspicious findings: {len(findings)}")
    print(f"  Blockers: {by_severity['blocker']}")
    print(f"  Warnings: {by_severity['warning']}")
    print(f"Top categories: {by_suspicion_category.most_common(10)}")


if __name__ == "__main__":
    main()
