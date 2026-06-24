from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import random


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "synthetic_materials_500.jsonl"
REPORT = ROOT / "REPORT.md"
GENERATED_BY = "codex_goal_04"

SOURCE_TYPES = ["rss", "web", "wechat", "upload", "document", "agent", "api", "unknown"]

PRIMARY_DOMAINS = [
    "AI agent workflow",
    "LLM evaluation",
    "RSS information system",
    "knowledge management",
    "Zabbix monitoring",
    "APM operations",
    "smart port logistics",
    "API-first architecture",
    "frontend experience",
    "software refactoring",
]

GENERAL_DOMAINS = [
    "urban transit",
    "public health",
    "education policy",
    "energy market",
    "local sports",
    "consumer technology",
]

GROUP_PURPOSES = {
    "basic_news": ["light_understanding", "search"],
    "long_article": ["light_understanding", "topic_structure"],
    "opinion_piece": ["light_understanding", "topic_structure"],
    "technical_article": ["light_understanding", "topic_structure"],
    "noise": ["light_understanding", "noise_handling"],
    "uncertain": ["light_understanding", "uncertainty"],
    "exact_duplicate": ["dedupe", "export"],
    "near_duplicate": ["similarity", "export"],
    "multi_source_same_event": ["event_candidate", "event_match"],
    "multi_day_event": ["event_candidate", "event_update"],
    "event_background": ["event_candidate", "topic_structure"],
    "conflicting_reports": ["event_update", "semantic_quality"],
    "weakly_related_event": ["event_candidate", "semantic_quality"],
    "topic_material": ["topic_structure", "search"],
    "topic_structure_refresh": ["topic_structure", "topic_local_refresh"],
    "no_url_material": ["material_detail", "export"],
    "missing_time_material": ["material_detail", "search"],
    "agent_submitted_material": ["upload_api", "run_detail"],
    "upload_material": ["frontend_upload", "api_smoke"],
    "export_evidence_pack": ["export", "topic_structure"],
}

CONTENT_TYPE_BY_GROUP = {
    "basic_news": "news",
    "long_article": "article",
    "opinion_piece": "opinion",
    "technical_article": "technical",
    "noise": "noise",
    "uncertain": "uncertain",
    "exact_duplicate": "news",
    "near_duplicate": "news",
    "multi_source_same_event": "news",
    "multi_day_event": "news",
    "event_background": "article",
    "conflicting_reports": "news",
    "weakly_related_event": "uncertain",
    "topic_material": "article",
    "topic_structure_refresh": "technical",
    "no_url_material": "article",
    "missing_time_material": "news",
    "agent_submitted_material": "technical",
    "upload_material": "article",
    "export_evidence_pack": "article",
}


def sentence(domain: str, group: str, index: int) -> str:
    return (
        f"This synthetic {group.replace('_', ' ')} item {index} describes {domain} work. "
        f"It is generated for information_workspace validation and must not be treated as real news. "
        f"The material includes enough detail for API ingestion, search snippets, LLM light understanding, "
        f"Event or Topic grouping, and Markdown evidence export checks. "
    )


def body(domain: str, group: str, index: int, content_type: str, event_key: str | None) -> str:
    base = sentence(domain, group, index)
    if content_type == "noise":
        return f"Synthetic ad fragment {index}: click now for unrelated coupons. No context."
    if content_type == "uncertain":
        return base + "The item intentionally says a claim is unconfirmed, timing is unclear, and the source lacks context."
    if content_type == "opinion":
        return base + "The author argues that teams should favor simpler workflows, but the claims require evidence from operational results. " * 3
    if content_type == "technical":
        return base + "It mentions API contracts, SQLite migration checks, APM routing, Zabbix alert quality, JSON schemas, and frontend smoke validation. " * 4
    if group in {"long_article", "topic_material", "topic_structure_refresh", "export_evidence_pack"}:
        return base + (
            "The article lays out background, tradeoffs, implementation constraints, user workflow implications, "
            "evidence gaps, and possible failure modes. It separates stable facts from interpretation and marks "
            "where future verification is needed. "
        ) * 7
    if event_key:
        return base + f"The shared synthetic event key is {event_key}, so related materials should cluster while still preserving source differences."
    return base + "The update includes a concrete change, a source perspective, and a limited uncertainty note."


def make_item(group: str, index: int, total_index: int) -> dict:
    content_type = CONTENT_TYPE_BY_GROUP[group]
    primary = total_index < 364
    domain_pool = PRIMARY_DOMAINS if primary else GENERAL_DOMAINS
    domain = domain_pool[total_index % len(domain_pool)]
    source_type = SOURCE_TYPES[total_index % len(SOURCE_TYPES)]
    event_key = None
    if group in {"multi_source_same_event", "multi_day_event", "conflicting_reports", "weakly_related_event", "near_duplicate", "event_background"}:
        event_key = f"{group}_cluster_{index // 5}"
    title = f"Synthetic {group.replace('_', ' ')} {index}: {domain}"
    text = body(domain, group, index, content_type, event_key)
    if group == "exact_duplicate":
        duplicate_bucket = index // 2
        duplicate_domain = PRIMARY_DOMAINS[duplicate_bucket % len(PRIMARY_DOMAINS)]
        title = f"Synthetic exact duplicate pair {duplicate_bucket}: {duplicate_domain}"
        text = body(duplicate_domain, group, duplicate_bucket, content_type, f"exact_duplicate_{duplicate_bucket}")
    if group == "near_duplicate":
        text = text + f" Variant angle {index % 3} adds a minor source emphasis without changing the core event."
    metadata = {
        "synthetic": True,
        "fixture_group": group,
        "test_purpose": GROUP_PURPOSES[group],
        "expected_behavior": expected_behavior(group),
        "generated_by": GENERATED_BY,
        "content_type": content_type,
        "domain_category": "primary" if primary else "general",
    }
    if event_key:
        metadata["event_key"] = event_key
    item = {
        "title": title,
        "content_text": text,
        "source_name": f"Synthetic Source {total_index % 17}",
        "source_type": source_type,
        "external_id": f"synthetic-{group}-{index}-{total_index}",
        "author": "Synthetic Fixture Generator",
        "published_at": f"2026-05-{(index % 28) + 1:02d}T08:00:00Z",
        "url": f"https://synthetic.example.invalid/{group}/{index}",
        "upstream_score": round(0.35 + (index % 60) / 100, 2),
        "upstream_reason": "Synthetic upstream score for validation only.",
        "metadata": metadata,
        "raw_payload": {"generator": GENERATED_BY, "group_index": index, "total_index": total_index},
    }
    if group == "no_url_material":
        item.pop("url")
    if group == "missing_time_material":
        item.pop("published_at")
    return item


def expected_behavior(group: str) -> str:
    if group == "exact_duplicate":
        return "should compress exact duplicate content to one primary material"
    if group == "near_duplicate":
        return "should retain full text but mark near-similar relation"
    if group in {"multi_source_same_event", "multi_day_event"}:
        return "should cluster into candidate Event with shared event_key"
    if group == "conflicting_reports":
        return "should preserve conflict as uncertainty or Event conflict note"
    if group == "weakly_related_event":
        return "should avoid polluting official Event without strong evidence"
    if group == "noise":
        return "should mark noise facet but not automatically ignored"
    if group == "uncertain":
        return "should include uncertain facet and uncertainty notes"
    if group == "no_url_material":
        return "should ingest and export with No original link marker"
    if group == "missing_time_material":
        return "should ingest with unknown published time"
    if group.startswith("topic") or group in {"long_article", "opinion_piece", "technical_article", "export_evidence_pack"}:
        return "should support Topic structure and export evidence checks"
    return "should ingest, search, and produce faithful light understanding"


def generate() -> list[dict]:
    random.seed(42)
    groups = list(GROUP_PURPOSES)
    counts = {group: 26 for group in groups}
    # 20 groups * 26 = 520
    items = []
    total_index = 0
    for group in groups:
        for index in range(counts[group]):
            items.append(make_item(group, index, total_index))
            total_index += 1
    return items


def write_report(items: list[dict]) -> None:
    group_counts = Counter(item["metadata"]["fixture_group"] for item in items)
    purpose_counts = Counter(purpose for item in items for purpose in item["metadata"]["test_purpose"])
    content_counts = Counter(item["metadata"]["content_type"] for item in items)
    domain_counts = Counter(item["metadata"]["domain_category"] for item in items)
    no_url = sum(1 for item in items if not item.get("url"))
    missing_time = sum(1 for item in items if not item.get("published_at"))
    lengths = [len(item["content_text"]) for item in items]
    lines = [
        "# Synthetic Corpus Report",
        "",
        f"- Total materials: {len(items)}",
        f"- No URL materials: {no_url}",
        f"- Missing time materials: {missing_time}",
        f"- Min length: {min(lengths)}",
        f"- Max length: {max(lengths)}",
        f"- Primary/general domain split: {dict(domain_counts)}",
        "",
        "## Fixture Groups",
        "",
    ]
    lines.extend(f"- {group}: {count}" for group, count in sorted(group_counts.items()))
    lines.extend(["", "## Test Purposes", ""])
    lines.extend(f"- {purpose}: {count}" for purpose, count in sorted(purpose_counts.items()))
    lines.extend(["", "## Content Types", ""])
    lines.extend(f"- {ctype}: {count}" for ctype, count in sorted(content_counts.items()))
    lines.extend(["", "## Sample Titles", ""])
    for group in sorted(group_counts):
        sample = next(item for item in items if item["metadata"]["fixture_group"] == group)
        lines.append(f"- {group}: {sample['title']}")
    lines.extend(
        [
            "",
            "## Quality Notes",
            "",
            "All materials are explicitly marked synthetic. They simulate realistic information-workbench scenarios without claiming to be real-world news.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    items = generate()
    OUT.write_text("\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in items) + "\n", encoding="utf-8")
    write_report(items)
    print(f"wrote {len(items)} materials to {OUT}")
    print(f"wrote report to {REPORT}")


if __name__ == "__main__":
    main()
