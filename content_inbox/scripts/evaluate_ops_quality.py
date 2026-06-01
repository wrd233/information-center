from __future__ import annotations

import json
import re
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from app.models import ContentAnalyzeRequest
from app.ops_api import (
    api_report_generate,
    api_run_report,
    ensure_environment_metadata,
    generate_briefing,
    generate_information_objects,
    run_dedupe_stage,
)
from app.processor import process_content_thread_safe
from app.semantic.cards import generate_item_cards
from app.semantic.review import decide_review
from app.semantic.source_profiles import recompute_source_profiles
from app.storage import InboxStore
from app.utils import stable_hash, utc_now


@dataclass(frozen=True)
class QualityItem:
    case_id: str
    title: str
    url: str | None
    source_id: str
    source_name: str
    source_category: str
    published_at: str
    summary: str
    content_text: str
    gold_event: str
    gold_dedupe_group: str
    expected_duplicate_of: str | None = None
    expected_entities: tuple[str, ...] = ()
    should_form_event: bool = True


THRESHOLDS = {
    "process_dedupe_pair_f1": 0.95,
    "event_cluster_pair_f1": 0.80,
    "event_cluster_pair_recall": 0.75,
    "event_type_known_rate": 0.70,
    "event_summary_specific_rate": 0.80,
    "entity_recall": 0.70,
    "briefing_quality_score": 0.80,
    "report_quality_score": 0.75,
}


def build_quality_items() -> list[QualityItem]:
    items = [
        QualityItem(
            "url_tracking_a",
            "OpenAI launches GPT-5.5 for coding agents",
            "https://example.com/openai-gpt55?utm_source=rss&utm_campaign=test#section",
            "techcrunch",
            "TechCrunch",
            "AI",
            "2026-05-30T10:00:00+00:00",
            "OpenAI released GPT-5.5 for coding agent workflows.",
            "OpenAI released GPT-5.5 for coding agents, with stronger repository navigation and test repair.",
            "openai_gpt55_launch",
            "dup_openai_gpt55_url",
            expected_entities=("OpenAI", "GPT-5.5"),
        ),
        QualityItem(
            "url_tracking_b",
            "OpenAI launches GPT-5.5 for coding agents",
            "https://example.com/openai-gpt55?utm_medium=feed",
            "verge",
            "The Verge",
            "AI",
            "2026-05-30T10:05:00+00:00",
            "The same OpenAI GPT-5.5 launch story appears with tracking parameters removed.",
            "The same OpenAI GPT-5.5 launch story appears with tracking parameters removed.",
            "openai_gpt55_launch",
            "dup_openai_gpt55_url",
            expected_duplicate_of="url_tracking_a",
            expected_entities=("OpenAI", "GPT-5.5"),
        ),
        QualityItem(
            "http_https_a",
            "Nvidia unveils Rubin Ultra platform",
            "http://chips.example.com/nvidia-rubin-ultra",
            "semianalysis",
            "SemiAnalysis",
            "AI Hardware",
            "2026-05-30T11:00:00+00:00",
            "Nvidia announced its Rubin Ultra platform.",
            "Nvidia announced Rubin Ultra for AI accelerators.",
            "nvidia_rubin_ultra",
            "dup_nvidia_scheme",
            expected_entities=("Nvidia", "Rubin Ultra"),
        ),
        QualityItem(
            "http_https_b",
            "NVIDIA unveils Rubin Ultra platform",
            "https://chips.example.com/nvidia-rubin-ultra",
            "anandtech",
            "AnandTech",
            "AI Hardware",
            "2026-05-30T11:03:00+00:00",
            "NVIDIA announced Rubin Ultra for accelerators.",
            "NVIDIA announced Rubin Ultra for accelerators.",
            "nvidia_rubin_ultra",
            "dup_nvidia_scheme",
            expected_duplicate_of="http_https_a",
            expected_entities=("Nvidia", "Rubin Ultra"),
        ),
        QualityItem(
            "guid_a",
            "DeepSeek releases V4.1 model",
            None,
            "deepseek_blog",
            "DeepSeek Blog",
            "AI",
            "2026-05-30T12:00:00+00:00",
            "DeepSeek released V4.1.",
            "DeepSeek released V4.1 with better reasoning latency.",
            "deepseek_v41_release",
            "dup_deepseek_guid",
            expected_entities=("DeepSeek", "V4.1"),
        ),
        QualityItem(
            "guid_b",
            "DeepSeek releases V4.1 model",
            None,
            "deepseek_blog",
            "DeepSeek Blog",
            "AI",
            "2026-05-30T12:01:00+00:00",
            "DeepSeek released V4.1 again through the same guid.",
            "DeepSeek released V4.1 again through the same guid.",
            "deepseek_v41_release",
            "dup_deepseek_guid",
            expected_duplicate_of="guid_a",
            expected_entities=("DeepSeek", "V4.1"),
        ),
        QualityItem(
            "title_date_a",
            "AI safety institute publishes model evaluation results",
            None,
            "gov_ai",
            "Gov AI Feed",
            "Policy",
            "2026-05-30T13:00:00+00:00",
            "A safety institute published model evaluation results.",
            "The institute published model evaluation results.",
            "ai_safety_eval_results",
            "dup_title_date",
            expected_entities=("AI",),
        ),
        QualityItem(
            "title_date_b",
            "AI safety institute publishes model evaluation results",
            None,
            "gov_ai",
            "Gov AI Feed",
            "Policy",
            "2026-05-30T13:20:00+00:00",
            "Duplicate title and same date from the same source.",
            "Duplicate title and same date from the same source.",
            "ai_safety_eval_results",
            "dup_title_date",
            expected_duplicate_of="title_date_a",
            expected_entities=("AI",),
        ),
        QualityItem(
            "openai_variant_a",
            "OpenAI rolls out GPT-5.5 model aimed at coding agents",
            "https://news.example.com/ai/openai-gpt-55-rollout",
            "axios",
            "Axios",
            "AI",
            "2026-05-30T10:10:00+00:00",
            "OpenAI rolled out GPT-5.5 for coding agents.",
            "OpenAI rolled out GPT-5.5 for coding agents with enterprise controls.",
            "openai_gpt55_launch",
            "unique_openai_variant_a",
            expected_entities=("OpenAI", "GPT-5.5"),
        ),
        QualityItem(
            "openai_variant_b",
            "OpenAI GPT 5.5 model launches for software agents",
            "https://wire.example.com/openai-gpt-5-5-software-agents",
            "reuters",
            "Reuters",
            "AI",
            "2026-05-30T10:12:00+00:00",
            "OpenAI launched GPT 5.5 for software agents.",
            "OpenAI launched GPT 5.5 for software agents and IDE integrations.",
            "openai_gpt55_launch",
            "unique_openai_variant_b",
            expected_entities=("OpenAI", "GPT-5.5"),
        ),
        QualityItem(
            "openai_punctuation_variant",
            "OpenAI launches GPT 5.5 for coding agents",
            "https://wire.example.com/openai-gpt55-punctuation",
            "wired",
            "Wired",
            "AI",
            "2026-05-30T10:14:00+00:00",
            "OpenAI launches GPT 5.5 for coding agents.",
            "OpenAI launches GPT 5.5 for coding agents with punctuation-normalized wording.",
            "openai_gpt55_launch",
            "unique_openai_punctuation",
            expected_entities=("OpenAI", "GPT-5.5"),
        ),
        QualityItem(
            "deepseek_cn_a",
            "DeepSeek 发布 V4.1 模型，推理延迟下降",
            "https://cn.example.com/deepseek-v41-a",
            "36kr",
            "36氪",
            "AI",
            "2026-05-30T12:05:00+00:00",
            "DeepSeek 发布 V4.1 模型。",
            "DeepSeek 发布 V4.1 模型，降低推理延迟。",
            "deepseek_v41_release",
            "unique_deepseek_cn_a",
            expected_entities=("DeepSeek", "V4.1"),
        ),
        QualityItem(
            "deepseek_cn_b",
            "深度求索推出 DeepSeek V4.1，主打低延迟推理",
            "https://cn.example.com/deepseek-v41-b",
            "qbitai",
            "量子位",
            "AI",
            "2026-05-30T12:09:00+00:00",
            "深度求索推出 DeepSeek V4.1。",
            "深度求索推出 DeepSeek V4.1，主打低延迟推理。",
            "deepseek_v41_release",
            "unique_deepseek_cn_b",
            expected_entities=("DeepSeek", "V4.1"),
        ),
        QualityItem(
            "anthropic_funding_a",
            "Anthropic raises $2B at $60B valuation",
            "https://finance.example.com/anthropic-raises-2b",
            "bloomberg",
            "Bloomberg",
            "Startups",
            "2026-05-30T14:00:00+00:00",
            "Anthropic raised $2B at a $60B valuation.",
            "Anthropic raised $2B at a $60B valuation from strategic investors.",
            "anthropic_funding",
            "unique_anthropic_a",
            expected_entities=("Anthropic",),
        ),
        QualityItem(
            "anthropic_funding_b",
            "Anthropic closes new $2 billion financing round",
            "https://finance.example.com/anthropic-financing-round",
            "ft",
            "Financial Times",
            "Startups",
            "2026-05-30T14:08:00+00:00",
            "Anthropic closed a new financing round worth $2 billion.",
            "Anthropic closed a new financing round worth $2 billion.",
            "anthropic_funding",
            "unique_anthropic_b",
            expected_entities=("Anthropic",),
        ),
        QualityItem(
            "openai_cloud",
            "OpenAI signs new cloud capacity deal with Oracle",
            "https://business.example.com/openai-oracle-cloud",
            "wsj",
            "Wall Street Journal",
            "Business",
            "2026-05-30T15:00:00+00:00",
            "OpenAI signed a cloud capacity agreement with Oracle.",
            "OpenAI signed a new cloud capacity agreement with Oracle.",
            "openai_oracle_cloud",
            "unique_openai_cloud",
            expected_entities=("OpenAI", "Oracle"),
        ),
        QualityItem(
            "nvidia_earnings",
            "Nvidia beats revenue expectations on AI chip demand",
            "https://markets.example.com/nvidia-earnings",
            "cnbc",
            "CNBC",
            "Markets",
            "2026-05-30T16:00:00+00:00",
            "Nvidia beat expectations because of AI chip demand.",
            "Nvidia beat revenue expectations because of AI chip demand.",
            "nvidia_earnings",
            "unique_nvidia_earnings",
            expected_entities=("Nvidia",),
        ),
        QualityItem(
            "generic_title_a",
            "Breaking: Major update announced",
            "https://generic.example.com/openai-update",
            "site_a",
            "Site A",
            "AI",
            "2026-05-30T17:00:00+00:00",
            "OpenAI announced a major API update.",
            "OpenAI announced a major API update.",
            "openai_api_update",
            "unique_generic_a",
            expected_entities=("OpenAI",),
        ),
        QualityItem(
            "generic_title_b",
            "Breaking: Major update announced",
            "https://generic.example.com/nvidia-update",
            "site_b",
            "Site B",
            "AI Hardware",
            "2026-05-30T17:05:00+00:00",
            "Nvidia announced a major driver update.",
            "Nvidia announced a major driver update.",
            "nvidia_driver_update",
            "unique_generic_b",
            expected_entities=("Nvidia",),
        ),
        QualityItem(
            "daily_digest_a",
            "AI Daily Briefing: OpenAI, Anthropic, Nvidia updates",
            "https://digest.example.com/2026-05-30",
            "daily_digest",
            "AI Daily",
            "Digest",
            "2026-05-30T18:00:00+00:00",
            "A digest containing several unrelated updates.",
            "A digest containing OpenAI, Anthropic, and Nvidia snippets.",
            "digest_2026_05_30",
            "unique_digest_a",
            expected_entities=("OpenAI", "Anthropic", "Nvidia"),
            should_form_event=False,
        ),
        QualityItem(
            "daily_digest_b",
            "AI Daily Briefing: OpenAI, Anthropic, Nvidia updates",
            "https://digest.example.com/2026-05-31",
            "daily_digest",
            "AI Daily",
            "Digest",
            "2026-05-31T18:00:00+00:00",
            "A different daily digest with the same title pattern.",
            "A different daily digest with OpenAI, Anthropic, and Nvidia snippets.",
            "digest_2026_05_31",
            "unique_digest_b",
            expected_entities=("OpenAI", "Anthropic", "Nvidia"),
            should_form_event=False,
        ),
        QualityItem(
            "daily_digest_c",
            "AI Daily Briefing: OpenAI, Anthropic, Nvidia updates",
            "https://digest.example.com/2026-06-01",
            "daily_digest",
            "AI Daily",
            "Digest",
            "2026-06-01T18:00:00+00:00",
            "A third daily digest with the same title pattern.",
            "A third daily digest with OpenAI, Anthropic, and Nvidia snippets.",
            "digest_2026_06_01",
            "unique_digest_c",
            expected_entities=("OpenAI", "Anthropic", "Nvidia"),
            should_form_event=False,
        ),
        QualityItem(
            "market_wrap_a",
            "Market wrap: AI stocks rally",
            "https://digest.example.com/market-wrap-2026-05-30",
            "market_digest",
            "Market Digest",
            "Digest",
            "2026-05-30T20:00:00+00:00",
            "A market wrap that mentions Nvidia and Microsoft.",
            "A market wrap that mentions Nvidia and Microsoft stock moves.",
            "market_wrap_2026_05_30",
            "unique_market_wrap_a",
            expected_entities=("Nvidia", "Microsoft"),
            should_form_event=False,
        ),
        QualityItem(
            "market_wrap_b",
            "Market wrap: AI stocks rally",
            "https://digest.example.com/market-wrap-2026-05-31",
            "market_digest",
            "Market Digest",
            "Digest",
            "2026-05-31T20:00:00+00:00",
            "A different market wrap with the same title.",
            "A different market wrap with the same title but different underlying market moves.",
            "market_wrap_2026_05_31",
            "unique_market_wrap_b",
            expected_entities=("Nvidia", "Microsoft"),
            should_form_event=False,
        ),
        QualityItem(
            "policy_a",
            "EU publishes final AI Act implementation guidance",
            "https://policy.example.com/eu-ai-act-guidance",
            "euractiv",
            "Euractiv",
            "Policy",
            "2026-05-30T19:00:00+00:00",
            "The EU published final AI Act implementation guidance.",
            "The EU published final AI Act implementation guidance for model providers.",
            "eu_ai_act_guidance",
            "unique_policy_a",
            expected_entities=("EU", "AI Act"),
        ),
        QualityItem(
            "policy_b",
            "European Commission issues AI Act guidance for model providers",
            "https://policy.example.com/commission-ai-act-model-guidance",
            "politico",
            "Politico",
            "Policy",
            "2026-05-30T19:04:00+00:00",
            "The European Commission issued AI Act guidance.",
            "The European Commission issued AI Act guidance for model providers.",
            "eu_ai_act_guidance",
            "unique_policy_b",
            expected_entities=("European Commission", "AI Act"),
        ),
    ]

    for index in range(1, 61):
        company = ["OpenAI", "Anthropic", "Nvidia", "Google", "Meta", "Microsoft"][index % 6]
        topic = ["policy", "funding", "product", "security", "benchmark", "market"][index % 6]
        items.append(
            QualityItem(
                f"background_{index:02d}",
                f"{company} {topic} update {index}",
                f"https://background.example.com/{company.lower()}-{topic}-{index}",
                f"background_{index % 4}",
                f"Background Source {index % 4}",
                "Background",
                f"2026-05-{1 + index % 28:02d}T09:00:00+00:00",
                f"{company} had a {topic} update.",
                f"{company} had a {topic} update unrelated to the benchmark target events.",
                f"background_{index:02d}",
                f"unique_background_{index:02d}",
                expected_entities=(company,),
            )
        )
    return items


def request_for(item: QualityItem) -> ContentAnalyzeRequest:
    guid = item.gold_dedupe_group if item.case_id.startswith("guid_") else None
    return ContentAnalyzeRequest(
        url=item.url,
        source_id=item.source_id,
        feed_url=f"https://feeds.example.com/{item.source_id}.xml",
        title=item.title,
        source_name=item.source_name,
        source_category=item.source_category,
        summary=item.summary,
        content_text=item.content_text,
        published_at=item.published_at,
        guid=guid,
        screen=False,
    )


def pair_counts(expected_pairs: set[tuple[str, str]], actual_pairs: set[tuple[str, str]]) -> dict[str, Any]:
    tp = len(expected_pairs & actual_pairs)
    fp = len(actual_pairs - expected_pairs)
    fn = len(expected_pairs - actual_pairs)
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def expected_pairs_by_label(labels: dict[str, str], eligible: set[str] | None = None) -> set[tuple[str, str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for item_id, label in labels.items():
        if eligible is None or item_id in eligible:
            grouped[label].append(item_id)
    pairs: set[tuple[str, str]] = set()
    for members in grouped.values():
        if len(members) < 2:
            continue
        for a, b in combinations(sorted(members), 2):
            pairs.add((a, b))
    return pairs


def actual_pairs_by_group(groups: dict[str, list[str]]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for members in groups.values():
        if len(members) < 2:
            continue
        for a, b in combinations(sorted(set(members)), 2):
            pairs.add((a, b))
    return pairs


def contains_specific_summary(summary: str) -> bool:
    generic_patterns = [
        "自动生成的候选事件",
        "candidate event",
        "grouped by normalized title",
        "related item",
    ]
    lowered = summary.lower()
    return bool(summary.strip()) and not any(pattern in lowered for pattern in generic_patterns)


def language_cn_ratio(text: str) -> float:
    if not text:
        return 0.0
    cn = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return cn / (cn + latin) if (cn + latin) else 0.0


def score_markdown_output(text: str, required_terms: list[str], *, require_cn: bool) -> dict[str, Any]:
    english_scaffold = ["Generated at", "Object:", "Events", "Review Queue", "No matching items"]
    raw_status_labels = ["needs_review", "pending", "event_candidate"]
    checks = {
        "has_h1": text.lstrip().startswith("# "),
        "has_section": text.count("\n## ") >= 1,
        "has_list": "- " in text,
        "has_required_terms": all(term in text for term in required_terms),
        "has_actionable_counts": bool(re.search(r"\d+", text)),
        "has_object_context": ("关联对象" in text or "Object:" in text),
        "scaffold_localized": (not require_cn) or not any(label in text for label in english_scaffold),
        "status_labels_localized": (not require_cn) or not any(label in text for label in raw_status_labels),
        "not_too_thin": len(text.strip()) >= 240,
    }
    score = sum(1 for ok in checks.values() if ok) / len(checks)
    return {"score": score, "checks": checks}


def fetch_table(store: InboxStore, table: str) -> list[dict[str, Any]]:
    with store.connect() as conn:
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table}").fetchall()]


def parse_json_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not value:
        return {}
    try:
        parsed = json.loads(str(value))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def parse_json_array(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = json.loads(str(value))
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def compact_signature(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {"present": False}
    normalized = parse_json_object(row.get("normalized_output_json"))
    signature = parse_json_object(normalized.get("signature"))
    return {
        "present": True,
        "actor": signature.get("actor") or "",
        "product_or_model": signature.get("product_or_model") or "",
        "action": signature.get("action") or "",
        "semantic_level": signature.get("semantic_level") or "",
        "signature_key": signature.get("signature_key"),
        "is_concrete": bool(signature.get("is_concrete")),
        "alias_hits": signature.get("alias_hits") or [],
        "invalid_reasons": signature.get("invalid_reasons") or [],
    }


def compact_item_card(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {"present": False}
    return {
        "present": True,
        "canonical_title": row.get("canonical_title") or "",
        "language": row.get("language") or "unknown",
        "entities": parse_json_array(row.get("entities_json")),
        "event_hint": row.get("event_hint") or "",
        "content_role": row.get("content_role") or "unknown",
        "confidence": row.get("confidence"),
        "warnings": parse_json_array(row.get("warnings_json")),
    }


def compact_candidate(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {"present": False}
    features = parse_json_object(row.get("features_json"))
    return {
        "present": True,
        "candidate_priority": row.get("candidate_priority"),
        "lane": row.get("lane"),
        "relation_type": row.get("relation_type"),
        "decision_source": row.get("decision_source"),
        "confidence": row.get("confidence"),
        "reason_code": row.get("reason_code"),
        "status": row.get("status"),
        "same_actor": features.get("same_actor"),
        "same_product": features.get("same_product"),
        "same_action": features.get("same_action"),
        "event_signature_match": features.get("event_signature_match"),
        "positive_features": parse_json_array(row.get("positive_features_json")),
        "negative_features": parse_json_array(row.get("negative_features_json")),
        "disqualifiers": parse_json_array(row.get("disqualifiers_json")),
    }


def build_false_negative_traces(
    false_negative_pairs: list[tuple[str, str]],
    *,
    item_id_by_case: dict[str, str],
    cluster_members_by_cluster: dict[str, list[str]],
    stored_case_by_item: dict[str, str],
    inbox_items: list[dict[str, Any]],
    item_cards: list[dict[str, Any]],
    semantic_extractions: list[dict[str, Any]],
    event_candidate_pairs: list[dict[str, Any]],
    review_queue: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    inbox_by_id = {row["item_id"]: row for row in inbox_items}
    card_by_item = {row["item_id"]: row for row in item_cards if row.get("is_current", 1)}
    extraction_by_item = {row["item_id"]: row for row in semantic_extractions}
    candidate_by_pair: dict[frozenset[str], dict[str, Any]] = {}
    for row in event_candidate_pairs:
        if row.get("item_a_id") and row.get("item_b_id"):
            candidate_by_pair[frozenset([row["item_a_id"], row["item_b_id"]])] = row
    reviews_by_pair: dict[frozenset[str], list[dict[str, Any]]] = defaultdict(list)
    for row in review_queue:
        if row.get("target_type") != "item_pair":
            continue
        parts = str(row.get("target_id") or "").split(":", 1)
        if len(parts) == 2:
            reviews_by_pair[frozenset(parts)].append(row)
    clusters_by_item: dict[str, list[str]] = defaultdict(list)
    for cluster_id, case_ids in cluster_members_by_cluster.items():
        for case_id in set(case_ids):
            item_id = item_id_by_case.get(case_id)
            if item_id:
                clusters_by_item[item_id].append(cluster_id)

    traces: list[dict[str, Any]] = []
    for case_a, case_b in false_negative_pairs:
        item_a_id = item_id_by_case.get(case_a)
        item_b_id = item_id_by_case.get(case_b)
        pair_key = frozenset([item_a_id or "", item_b_id or ""])
        candidate = candidate_by_pair.get(pair_key)
        reviews = reviews_by_pair.get(pair_key, [])
        clusters_a = sorted(clusters_by_item.get(item_a_id or "", []))
        clusters_b = sorted(clusters_by_item.get(item_b_id or "", []))
        same_cluster = bool(set(clusters_a) & set(clusters_b))
        if not item_a_id or not item_b_id:
            failure_reason = "one_or_both_cases_missing_from_stored_items"
        elif not candidate:
            failure_reason = "no_candidate_pair_generated"
        elif reviews and not same_cluster:
            failure_reason = "candidate_went_to_review_but_not_clustered_before_eval"
        elif candidate.get("status") == "rejected":
            failure_reason = "candidate_rejected_by_rule"
        elif candidate.get("status") == "review":
            failure_reason = "candidate_requires_review_not_auto_merged"
        elif not same_cluster:
            failure_reason = "items_not_in_same_cluster_at_eval_time"
        else:
            failure_reason = "unexpected_trace_state"
        traces.append(
            {
                "pair": [case_a, case_b],
                "item_ids": [item_a_id, item_b_id],
                "items": [
                    {
                        "case_id": case_a,
                        "item_id": item_a_id,
                        "title": (inbox_by_id.get(item_a_id or "", {}).get("title") if item_a_id else None),
                        "item_card": compact_item_card(card_by_item.get(item_a_id or "")),
                        "signature": compact_signature(extraction_by_item.get(item_a_id or "")),
                        "clusters": clusters_a,
                    },
                    {
                        "case_id": case_b,
                        "item_id": item_b_id,
                        "title": (inbox_by_id.get(item_b_id or "", {}).get("title") if item_b_id else None),
                        "item_card": compact_item_card(card_by_item.get(item_b_id or "")),
                        "signature": compact_signature(extraction_by_item.get(item_b_id or "")),
                        "clusters": clusters_b,
                    },
                ],
                "candidate": compact_candidate(candidate),
                "relation": {
                    "judged_as": candidate.get("relation_type") if candidate else None,
                    "reason_code": candidate.get("reason_code") if candidate else None,
                    "status": candidate.get("status") if candidate else None,
                    "decision_source": candidate.get("decision_source") if candidate else None,
                },
                "review_queue": [
                    {
                        "id": row.get("id"),
                        "status": row.get("status"),
                        "review_type": row.get("review_type"),
                        "reason": row.get("reason"),
                    }
                    for row in reviews
                ],
                "cluster_eval": {
                    "same_cluster": same_cluster,
                    "cluster_ids_by_item": {case_a: clusters_a, case_b: clusters_b},
                    "counted_as_failure_because": failure_reason,
                },
            }
        )
    return traces


SEMANTIC_JUDGE_HARD_NEGATIVES = {
    "generic_entity_overlap",
    "generic_only_overlap",
    "same_account_boilerplate",
    "wide_time_window",
    "semantic_level_reject",
    "proxy_domain_only",
}


def build_semantic_judge_dry_run_proposals(
    event_candidate_pairs: list[dict[str, Any]],
    *,
    stored_case_by_item: dict[str, str],
) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for row in event_candidate_pairs:
        disqualifiers = parse_json_array(row.get("disqualifiers_json"))
        hard_negative = bool(set(disqualifiers) & SEMANTIC_JUDGE_HARD_NEGATIVES)
        eligible = (
            row.get("status") == "review"
            and row.get("candidate_priority") in {"medium", "high"}
            and not hard_negative
        )
        if not eligible:
            continue
        features = parse_json_object(row.get("features_json"))
        proposals.append(
            {
                "proposal_status": "dry_run_not_called",
                "task_type": "semantic_relation_judge",
                "item_pair": [
                    stored_case_by_item.get(row.get("item_a_id"), row.get("item_a_id")),
                    stored_case_by_item.get(row.get("item_b_id"), row.get("item_b_id")),
                ],
                "candidate_priority": row.get("candidate_priority"),
                "lane": row.get("lane"),
                "rule_relation_type": row.get("relation_type"),
                "rule_reason_code": row.get("reason_code"),
                "rule_status": row.get("status"),
                "judge_input_evidence": {
                    "same_actor": features.get("same_actor"),
                    "same_product": features.get("same_product"),
                    "same_action": features.get("same_action"),
                    "event_signature_match": features.get("event_signature_match"),
                    "positive_features": parse_json_array(row.get("positive_features_json"))[:5],
                    "negative_features": parse_json_array(row.get("negative_features_json"))[:5],
                    "disqualifiers": disqualifiers,
                },
                "proposal_policy": {
                    "proposal_only": True,
                    "should_auto_merge": False,
                    "review_queue_or_dry_run_report_only": True,
                },
            }
        )
    return proposals


def build_request(store: InboxStore) -> Any:
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=store)))


def run_evaluation() -> dict[str, Any]:
    tmp_dir = Path(tempfile.mkdtemp(prefix="content_inbox_quality_eval_"))
    store = InboxStore(tmp_dir / "quality_eval.db")
    ensure_environment_metadata(store, label="quality_eval", is_fresh=True)
    run_id = "run_quality_eval_" + stable_hash(utc_now())[:10]
    now = utc_now()
    store.create_ingest_run(
        {
            "run_id": run_id,
            "trigger_type": "quality_eval",
            "source_mode": "synthetic",
            "status": "success",
            "started_at": now,
            "finished_at": now,
            "selected_source_count": 1,
            "success_source_count": 1,
            "request": {"synthetic": True},
        }
    )

    items = build_quality_items()
    item_id_by_case: dict[str, str] = {}
    duplicate_results: dict[str, Any] = {}
    linked_item_ids: list[str] = []

    for item in items:
        result = process_content_thread_safe(store, request_for(item), raw={"case_id": item.case_id})
        duplicate_results[item.case_id] = {
            "item_id": result.item_id,
            "is_duplicate": result.is_duplicate,
            "expected_duplicate_of": item.expected_duplicate_of,
        }
        item_id_by_case[item.case_id] = result.item_id
        with store.connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO item_run_links(run_id, source_id, item_id, status, created_at) VALUES (?, ?, ?, ?, ?)",
                (run_id, item.source_id, result.item_id, "duplicate" if result.is_duplicate else "inserted", utc_now()),
            )
        linked_item_ids.append(result.item_id)

    unique_item_ids = sorted(set(linked_item_ids))
    run_dedupe_stage(store, run_id, unique_item_ids)
    generate_item_cards(store, limit=len(unique_item_ids), live=False)
    generate_information_objects(store, run_id, unique_item_ids)
    daily_briefing = generate_briefing(store, "daily")
    weekly_briefing = generate_briefing(store, "weekly")
    run_report = api_report_generate(build_request(store), {"report_type": "run", "object_type": "run", "object_id": run_id})["data"]
    run_endpoint_report = api_run_report(build_request(store), run_id)["data"]

    expected_duplicate_pairs: set[tuple[str, str]] = set()
    actual_duplicate_pairs: set[tuple[str, str]] = set()
    for item in items:
        if not item.expected_duplicate_of:
            continue
        expected_duplicate_pairs.add(tuple(sorted((item.expected_duplicate_of, item.case_id))))
        if duplicate_results[item.case_id]["is_duplicate"]:
            actual_duplicate_pairs.add(tuple(sorted((item.expected_duplicate_of, item.case_id))))
    process_dedupe_metrics = pair_counts(expected_duplicate_pairs, actual_duplicate_pairs)
    failed_duplicate_cases = [
        item.case_id
        for item in items
        if item.expected_duplicate_of and not duplicate_results[item.case_id]["is_duplicate"]
    ]

    dedupe_groups = fetch_table(store, "dedupe_groups")
    dedupe_group_items = fetch_table(store, "dedupe_group_items")
    dedupe_members_by_group: dict[str, list[str]] = defaultdict(list)
    for row in dedupe_group_items:
        dedupe_members_by_group[row["dedupe_group_id"]].append(row["item_id"])
    multi_item_dedupe_groups = {gid: members for gid, members in dedupe_members_by_group.items() if len(set(members)) > 1}

    stored_case_by_item: dict[str, str] = {}
    for case_id, item_id in item_id_by_case.items():
        stored_case_by_item.setdefault(item_id, case_id)
    stored_case_ids = set(stored_case_by_item.values())
    event_labels = {item.case_id: item.gold_event for item in items if item.case_id in stored_case_ids and item.should_form_event}
    non_event_case_ids = {item.case_id for item in items if item.case_id in stored_case_ids and not item.should_form_event}
    cluster_items = fetch_table(store, "cluster_items")
    cluster_members_by_cluster: dict[str, list[str]] = defaultdict(list)
    for row in cluster_items:
        case_id = stored_case_by_item.get(row["item_id"])
        if case_id:
            cluster_members_by_cluster[row["cluster_id"]].append(case_id)
    expected_event_pairs = expected_pairs_by_label(event_labels)
    actual_event_pairs = actual_pairs_by_group(cluster_members_by_cluster)
    event_cluster_metrics = pair_counts(expected_event_pairs, actual_event_pairs)
    false_positive_pairs = sorted(actual_event_pairs - expected_event_pairs)
    false_negative_pairs = sorted(expected_event_pairs - actual_event_pairs)

    events = fetch_table(store, "events")
    event_items = fetch_table(store, "event_items")
    inbox_items = fetch_table(store, "inbox_items")
    item_cards = fetch_table(store, "item_cards")
    review_queue = fetch_table(store, "review_queue")
    semantic_extractions = fetch_table(store, "semantic_extractions")
    event_candidate_pairs = fetch_table(store, "event_candidate_pairs")
    false_negative_traces = build_false_negative_traces(
        false_negative_pairs,
        item_id_by_case=item_id_by_case,
        cluster_members_by_cluster=cluster_members_by_cluster,
        stored_case_by_item=stored_case_by_item,
        inbox_items=inbox_items,
        item_cards=item_cards,
        semantic_extractions=semantic_extractions,
        event_candidate_pairs=event_candidate_pairs,
        review_queue=review_queue,
    )
    semantic_judge_dry_run_proposals = build_semantic_judge_dry_run_proposals(
        event_candidate_pairs,
        stored_case_by_item=stored_case_by_item,
    )
    review_apply_result = run_review_apply_sample(store, review_queue)
    source_profile_result = recompute_source_profiles(store)
    source_profiles = fetch_table(store, "source_profiles")
    source_signals = fetch_table(store, "source_signals")
    llm_call_logs = fetch_table(store, "llm_call_logs")

    event_item_case_ids = {stored_case_by_item.get(row["item_id"]) for row in event_items}
    event_item_case_ids.discard(None)
    non_event_candidate_rate = len(event_item_case_ids & non_event_case_ids) / len(non_event_case_ids) if non_event_case_ids else 0.0
    event_type_known_rate = sum(1 for row in events if row["event_type"] != "unknown") / len(events) if events else 0.0
    event_summary_specific_rate = sum(1 for row in events if contains_specific_summary(row["event_summary"])) / len(events) if events else 0.0
    event_review_coverage = len(review_queue) / len(events) if events else 0.0
    multi_item_event_rate = (
        sum(1 for members in cluster_members_by_cluster.values() if len(set(members)) > 1) / len(cluster_members_by_cluster)
        if cluster_members_by_cluster
        else 0.0
    )

    extracted_by_case: dict[str, set[str]] = defaultdict(set)
    alias_hit_count = 0
    for row in semantic_extractions:
        case_id = stored_case_by_item.get(row["item_id"])
        if not case_id:
            continue
        normalized = json.loads(row["normalized_output_json"] or "{}")
        extracted_by_case[case_id].update(str(value).lower() for value in normalized.get("entities", []))
        signature = normalized.get("signature") or {}
        alias_hit_count += len(signature.get("alias_hits") or [])
    expected_entity_total = 0
    matched_entity_total = 0
    for item in items:
        if item.case_id not in stored_case_ids:
            continue
        for entity in item.expected_entities:
            expected_entity_total += 1
            entity_lower = entity.lower()
            if any(entity_lower in extracted or extracted in entity_lower for extracted in extracted_by_case[item.case_id]):
                matched_entity_total += 1
    entity_recall = matched_entity_total / expected_entity_total if expected_entity_total else 1.0

    daily_body = daily_briefing["body_markdown"]
    weekly_body = weekly_briefing["body_markdown"]
    report_body = run_report["content"]
    run_endpoint_report_body = run_endpoint_report["content"]
    briefing_score = score_markdown_output(daily_body, ["事件", "待审核"], require_cn=True)
    weekly_briefing_score = score_markdown_output(weekly_body, ["事件", "待审核"], require_cn=True)
    report_score = score_markdown_output(report_body, ["生成时间", "关联对象"], require_cn=True)
    run_endpoint_report_score = score_markdown_output(run_endpoint_report_body, ["状态", "新增条目", "信息源数量"], require_cn=True)

    metrics = {
        "dataset": {
            "synthetic_items": len(items),
            "stored_unique_items": len(unique_item_ids),
            "gold_duplicate_pairs": len(expected_duplicate_pairs),
            "gold_same_event_pairs": len(expected_event_pairs),
            "gold_non_event_items": len(non_event_case_ids),
            "temp_db": str(store.database_path),
        },
        "process_dedupe": process_dedupe_metrics,
        "process_dedupe_failures": failed_duplicate_cases,
        "dedupe_stage": {
            "groups": len(dedupe_groups),
            "multi_item_groups": len(multi_item_dedupe_groups),
            "multi_item_group_rate": len(multi_item_dedupe_groups) / len(dedupe_groups) if dedupe_groups else 0.0,
        },
        "event_clustering": {
            **event_cluster_metrics,
            "auto_merge_precision": event_cluster_metrics["precision"],
            "clusters": len(cluster_members_by_cluster),
            "multi_item_event_rate": multi_item_event_rate,
            "false_positive_pairs": false_positive_pairs[:20],
            "false_negative_pairs": false_negative_pairs[:30],
            "false_negative_traces": false_negative_traces,
        },
        "event_extraction": {
            "events": len(events),
            "event_type_known_rate": event_type_known_rate,
            "event_summary_specific_rate": event_summary_specific_rate,
            "review_entries": len(review_queue),
            "review_coverage": event_review_coverage,
            "non_event_candidate_rate": non_event_candidate_rate,
            "entity_recall": entity_recall,
            "matched_entities": matched_entity_total,
            "expected_entities": expected_entity_total,
        },
        "candidate_diagnostics": {
            "total_candidates": len(event_candidate_pairs),
            "by_priority": dict(Counter(row["candidate_priority"] for row in event_candidate_pairs)),
            "by_lane": dict(Counter(row["lane"] for row in event_candidate_pairs)),
            "by_status": dict(Counter(row["status"] for row in event_candidate_pairs)),
            "medium_review_rate": (
                sum(1 for row in event_candidate_pairs if row["candidate_priority"] == "medium" and row["status"] == "review")
                / max(1, sum(1 for row in event_candidate_pairs if row["candidate_priority"] == "medium"))
            ),
            "disqualifiers": dict(
                Counter(
                    disqualifier
                    for row in event_candidate_pairs
                    for disqualifier in json.loads(row["disqualifiers_json"] or "[]")
                )
            ),
            "alias_hit_count": alias_hit_count,
        },
        "semantic_judge": {
            "dry_run_proposal_count": len(semantic_judge_dry_run_proposals),
            "dry_run_proposals": semantic_judge_dry_run_proposals,
            "live_calls": sum(1 for row in llm_call_logs if row.get("task_type") == "semantic_relation_judge"),
            "proposal_policy": "review_queue_or_dry_run_report_only",
        },
        "review_apply": review_apply_result,
        "source_scoring": {
            "recompute_ok": bool(source_profile_result.get("ok")),
            "profile_count": len(source_profiles),
            "signal_count": len(source_signals),
            "example_profile": source_scoring_example(source_profiles),
            "dimension_totals": source_signal_dimension_totals(source_signals),
        },
        "deepseek": {
            "operational_relation_calls": sum(1 for row in llm_call_logs if row.get("task_type") == "operational_relation"),
            "live_ok_calls": sum(1 for row in llm_call_logs if row.get("task_type") == "operational_relation" and row.get("status") == "ok"),
            "failed_or_skipped_calls": sum(1 for row in llm_call_logs if row.get("task_type") == "operational_relation" and row.get("status") in {"failed", "skipped"}),
            "total_tokens": sum(int(row.get("total_tokens") or 0) for row in llm_call_logs if row.get("task_type") == "operational_relation"),
        },
        "outputs": {
            "daily_briefing": briefing_score,
            "weekly_briefing": weekly_briefing_score,
            "run_report": report_score,
            "run_endpoint_report": run_endpoint_report_score,
            "daily_briefing_preview": daily_body[:1200],
            "run_report_preview": report_body[:1200],
            "run_endpoint_report_preview": run_endpoint_report_body[:1200],
        },
    }
    metrics["threshold_results"] = {
        "process_dedupe_pair_f1": metrics["process_dedupe"]["f1"] >= THRESHOLDS["process_dedupe_pair_f1"],
        "event_cluster_pair_f1": metrics["event_clustering"]["f1"] >= THRESHOLDS["event_cluster_pair_f1"],
        "event_cluster_pair_recall": metrics["event_clustering"]["recall"] >= THRESHOLDS["event_cluster_pair_recall"],
        "event_type_known_rate": event_type_known_rate >= THRESHOLDS["event_type_known_rate"],
        "event_summary_specific_rate": event_summary_specific_rate >= THRESHOLDS["event_summary_specific_rate"],
        "entity_recall": entity_recall >= THRESHOLDS["entity_recall"],
        "briefing_quality_score": briefing_score["score"] >= THRESHOLDS["briefing_quality_score"],
        "report_quality_score": report_score["score"] >= THRESHOLDS["report_quality_score"],
    }
    return metrics


def run_review_apply_sample(store: InboxStore, reviews: list[dict[str, Any]]) -> dict[str, Any]:
    relation_review = next((row for row in reviews if row["status"] == "pending" and row["review_type"] == "event_relation_review"), None)
    if not relation_review:
        return {"attempted": False, "reason": "no pending event_relation_review"}
    decided = decide_review(store, int(relation_review["id"]), "approved", reviewer="quality_eval", note="synthetic review apply sample")
    return {
        "attempted": True,
        "review_id": relation_review["id"],
        "ok": bool(decided.get("ok")),
        "apply_result": decided.get("apply_result"),
    }


def source_signal_dimension_totals(rows: list[dict[str, Any]]) -> dict[str, Any]:
    dimensions = [
        "discovery_value",
        "fact_value",
        "incremental_value",
        "interpretation_value",
        "duplicate_noise",
        "non_event_noise",
        "review_acceptance",
    ]
    return {name: sum(float(row.get(name) or 0) for row in rows) for name in dimensions}


def source_scoring_example(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    dimensions = [
        "discovery_value_avg",
        "fact_value_avg",
        "incremental_value_avg",
        "interpretation_value_avg",
        "duplicate_noise_rate",
        "non_event_noise_rate",
        "review_acceptance",
        "llm_yield_score",
        "priority_suggestion",
    ]
    scored = sorted(rows, key=lambda row: (row.get("llm_yield_score") or 0, row.get("review_acceptance") or 0), reverse=True)
    row = scored[0]
    return {"source_id": row.get("source_id"), **{name: row.get(name) for name in dimensions}}


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_report(metrics: dict[str, Any]) -> str:
    failed = [name for name, ok in metrics["threshold_results"].items() if not ok]
    status = "不通过" if failed else "通过"
    lines = [
        "# 作战台信息质量评估报告",
        "",
        f"生成时间: {utc_now()}",
        "",
        "## 结论",
        "",
        f"整体状态: **{status}**。本次离线评估使用合成样例，不读取真实运行数据。",
        "",
        "核心发现:",
        "",
        f"- 处理时去重 F1: {pct(metrics['process_dedupe']['f1'])}，召回 {pct(metrics['process_dedupe']['recall'])}。",
        f"- 事件聚合 F1: {pct(metrics['event_clustering']['f1'])}，召回 {pct(metrics['event_clustering']['recall'])}。",
        f"- 自动合并 precision: {pct(metrics['event_clustering']['auto_merge_precision'])}。",
        f"- medium review rate: {pct(metrics['candidate_diagnostics']['medium_review_rate'])}。",
        f"- alias hit count: {metrics['candidate_diagnostics']['alias_hit_count']}。",
        f"- review apply sample: {'ok' if metrics['review_apply'].get('ok') else metrics['review_apply'].get('reason', 'not ok')}。",
        f"- source scoring profiles/signals: {metrics['source_scoring']['profile_count']}/{metrics['source_scoring']['signal_count']}。",
        f"- operational DeepSeek relation calls: {metrics['deepseek']['operational_relation_calls']}。",
        f"- 事件类型识别率: {pct(metrics['event_extraction']['event_type_known_rate'])}。",
        f"- 事件摘要具体率: {pct(metrics['event_extraction']['event_summary_specific_rate'])}。",
        f"- 实体召回: {pct(metrics['event_extraction']['entity_recall'])}。",
        f"- 每日简报质量分: {pct(metrics['outputs']['daily_briefing']['score'])}。",
        f"- 运行报告质量分: {pct(metrics['outputs']['run_report']['score'])}。",
        f"- Run endpoint 报告质量分: {pct(metrics['outputs']['run_endpoint_report']['score'])}。",
        "",
        "## 指标标准",
        "",
        "| 模块 | 指标 | 合格线 | 说明 |",
        "|---|---:|---:|---|",
        "| 处理时去重 | duplicate pair F1 | 95% | URL tracking、GUID、同源标题日期应稳定识别；scheme 差异等应按产品策略纳入。 |",
        "| 去重阶段 | multi-item group rate | 视场景 | 阶段输出应能解释真实重复组；如果重复已在写入时折叠，阶段应明确展示 seen_count/重复来源。 |",
        "| 事件聚合 | same-event pair F1 | 80% | 同一事件多标题应合并，泛标题/日报/同主题不同事不能误合。 |",
        "| 事件聚合 | same-event recall | 75% | 不能只靠完全相同标题，否则跨来源新闻会大量漏合。 |",
        "| 事件提取 | known event_type rate | 70% | 至少应区分发布、融资、政策、财报、合作、安全等。 |",
        "| 事件提取 | specific summary rate | 80% | 摘要应描述发生了什么，而不是模板句。 |",
        "| 事件提取 | entity recall | 70% | 核心公司、模型、政策名需要进入实体/证据。 |",
        "| 简报 | structure+coverage score | 80% | 有标题、分区、事件/审核覆盖、数量/状态、中文一致性、足够信息密度。 |",
        "| 报告 | structure+context score | 75% | 有对象上下文、生成时间、统计、问题/结论，而不是只给占位信息。 |",
        "",
        "## 测试集",
        "",
        f"- 合成条目: {metrics['dataset']['synthetic_items']}",
        f"- 入库唯一条目: {metrics['dataset']['stored_unique_items']}",
        f"- Gold 重复 pair: {metrics['dataset']['gold_duplicate_pairs']}",
        f"- Gold 同事件 pair: {metrics['dataset']['gold_same_event_pairs']}",
        f"- Gold 非事件条目: {metrics['dataset']['gold_non_event_items']}",
        "",
        "样例覆盖 URL tracking 去重、HTTP/HTTPS 规范化、GUID 去重、同源标题日期去重、跨来源同事件变体、中英文标题变体、泛标题误合并、日报/聚合内容非事件、同主题不同事件。",
        "",
        "## 结果",
        "",
        "### 去重",
        "",
        f"- 处理时去重 precision/recall/F1: {pct(metrics['process_dedupe']['precision'])} / {pct(metrics['process_dedupe']['recall'])} / {pct(metrics['process_dedupe']['f1'])}",
        f"- 未识别重复样例: `{metrics['process_dedupe_failures']}`",
        f"- 去重阶段 groups: {metrics['dedupe_stage']['groups']}",
        f"- 去重阶段多成员 groups: {metrics['dedupe_stage']['multi_item_groups']} ({pct(metrics['dedupe_stage']['multi_item_group_rate'])})",
        "",
        "### 事件聚合",
        "",
        f"- precision/recall/F1: {pct(metrics['event_clustering']['precision'])} / {pct(metrics['event_clustering']['recall'])} / {pct(metrics['event_clustering']['f1'])}",
        f"- clusters: {metrics['event_clustering']['clusters']}",
        f"- 多条目 cluster 比率: {pct(metrics['event_clustering']['multi_item_event_rate'])}",
        f"- 误合并 pair 样例: `{metrics['event_clustering']['false_positive_pairs']}`",
        f"- 漏合并 pair 样例: `{metrics['event_clustering']['false_negative_pairs']}`",
        "",
        "### False Negative Trace",
        "",
    ]
    false_negative_traces = metrics["event_clustering"].get("false_negative_traces", [])
    if not false_negative_traces:
        lines.append("- No false negative pairs in this run.")
    for trace in false_negative_traces:
        pair = trace["pair"]
        candidate = trace["candidate"]
        relation = trace["relation"]
        item_lines = []
        for item in trace["items"]:
            signature = item["signature"]
            item_card = item["item_card"]
            card_entities = ", ".join(str(entity) for entity in (item_card.get("entities") or [])[:4])
            item_lines.append(
                f"  - {item['case_id']}: actor={signature.get('actor')!r}, product={signature.get('product_or_model')!r}, "
                f"action={signature.get('action')!r}, signature_key={signature.get('signature_key')!r}, "
                f"item_card_present={item_card.get('present')}, card_entities=[{card_entities}], "
                f"card_event_hint={item_card.get('event_hint')!r}, clusters={item['clusters']}"
            )
        lines.extend(
            [
                f"- Pair `{pair[0]}` / `{pair[1]}`:",
                *item_lines,
                f"  - candidate: present={candidate.get('present')}, priority={candidate.get('candidate_priority')}, lane={candidate.get('lane')}, status={candidate.get('status')}",
                f"  - relation: judged_as={relation.get('judged_as')}, reason_code={relation.get('reason_code')}, decision_source={relation.get('decision_source')}",
                f"  - review_queue: {len(trace['review_queue'])} entr{'y' if len(trace['review_queue']) == 1 else 'ies'}",
                f"  - eval_failure: {trace['cluster_eval']['counted_as_failure_because']}",
            ]
        )
    lines.extend(
        [
        "",
        "### Candidate 诊断",
        "",
        f"- candidate counts by priority: `{metrics['candidate_diagnostics']['by_priority']}`",
        f"- candidate counts by lane: `{metrics['candidate_diagnostics']['by_lane']}`",
        f"- candidate counts by status: `{metrics['candidate_diagnostics']['by_status']}`",
        f"- disqualifier counts: `{metrics['candidate_diagnostics']['disqualifiers']}`",
        f"- medium review rate: {pct(metrics['candidate_diagnostics']['medium_review_rate'])}",
        f"- alias hit count: {metrics['candidate_diagnostics']['alias_hit_count']}",
        "",
        "### Semantic Judge Dry-Run Proposals",
        "",
        f"- dry-run proposal count: {metrics['semantic_judge']['dry_run_proposal_count']}",
        f"- live semantic judge calls: {metrics['semantic_judge']['live_calls']}",
        f"- proposal policy: {metrics['semantic_judge']['proposal_policy']}",
        f"- proposals: `{metrics['semantic_judge']['dry_run_proposals'][:10]}`",
        "",
        "### Review Apply 与 Source Scoring",
        "",
        f"- review apply sample: `{metrics['review_apply']}`",
        f"- source scoring dimension totals: `{metrics['source_scoring']['dimension_totals']}`",
        f"- source scoring example profile: `{metrics['source_scoring']['example_profile']}`",
        f"- operational DeepSeek relation stats: `{metrics['deepseek']}`",
        "",
        "### 事件提取",
        "",
        f"- events: {metrics['event_extraction']['events']}",
        f"- event_type known rate: {pct(metrics['event_extraction']['event_type_known_rate'])}",
        f"- summary specific rate: {pct(metrics['event_extraction']['event_summary_specific_rate'])}",
        f"- review coverage: {pct(metrics['event_extraction']['review_coverage'])}",
        f"- 非事件条目被生成候选事件比率: {pct(metrics['event_extraction']['non_event_candidate_rate'])}",
        f"- entity recall: {pct(metrics['event_extraction']['entity_recall'])} ({metrics['event_extraction']['matched_entities']}/{metrics['event_extraction']['expected_entities']})",
        "",
        "### 简报和报告",
        "",
        f"- 每日简报质量分: {pct(metrics['outputs']['daily_briefing']['score'])}，检查项: `{metrics['outputs']['daily_briefing']['checks']}`",
        f"- 每周简报质量分: {pct(metrics['outputs']['weekly_briefing']['score'])}，检查项: `{metrics['outputs']['weekly_briefing']['checks']}`",
        f"- 运行报告质量分: {pct(metrics['outputs']['run_report']['score'])}，检查项: `{metrics['outputs']['run_report']['checks']}`",
        f"- Run endpoint 报告质量分: {pct(metrics['outputs']['run_endpoint_report']['score'])}，检查项: `{metrics['outputs']['run_endpoint_report']['checks']}`",
        "",
        "每日简报预览:",
        "",
        "```markdown",
        metrics["outputs"]["daily_briefing_preview"],
        "```",
        "",
        "运行报告预览:",
        "",
        "```markdown",
        metrics["outputs"]["run_report_preview"],
        "```",
        "",
        "Run endpoint 报告预览:",
        "",
        "```markdown",
        metrics["outputs"]["run_endpoint_report_preview"],
        "```",
        "",
        "## 问题追踪",
        "",
        "1. operational v3 已不使用规范化标题作为事件主键，但当前 rule-only 自动合并仍偏保守，跨语言、政策表述改写、融资改写等 false negative 仍多。",
        "2. 泛标题和日报类内容已被 eventness gate 挡住；后续风险主要是 review/LLM 放宽时误把同主题不同事件升为 same-event。",
        "3. 事件对象已具备类型、摘要和证据，但同一事件的新增事实仍主要等待 LLM/review apply 补足。",
        "4. 去重阶段在写入后重复已折叠的情况下几乎只产生单成员 group，不能解释重复来源和 seen_count。",
        "5. 实体抽取和 alias registry 对中文别名、政策名、产品名仍需从 false negative 样例继续扩充。",
        "6. Run endpoint 报告仍较薄；通用 report 生成已切到可信事件输入并通过质量门。",
        "",
        "## 建议修复顺序",
        "",
        "1. 先把评估脚本固化为回归命令，并把上述阈值作为非阻断质量门。",
        "2. 保持当前 high-confidence auto-merge precision，把 medium/high-uncertain 的召回增量交给 schema-bound LLM 与 review apply。",
        "3. 继续扩充 digest/newsletter/roundup/navigation hard negatives，并监控 hard-negative LLM 调用数保持 0。",
        "4. 从 false negative 样例补 alias/signature/action 规则，优先覆盖跨语言产品发布、政策 guidance、融资 round 改写。",
        "5. 去重报告需要从 `seen_count`、latest_raw、item_run_links 展示重复来源，而不是期待多个同 dedupe_key item 同时存在。",
        "6. Run endpoint 报告已切到可信事件输入；下一步补充 source scoring 明细和风险解释段落。",
        "",
        "## 原始指标 JSON",
        "",
        "```json",
        json.dumps(metrics, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    )
    return "\n".join(lines)


def main() -> None:
    metrics = run_evaluation()
    report = render_report(metrics)
    report_path = Path(__file__).resolve().parents[1] / "docs" / "ops_quality_eval_20260531.md"
    report_path.write_text(report, encoding="utf-8")
    print(json.dumps({"report_path": str(report_path), "threshold_results": metrics["threshold_results"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
