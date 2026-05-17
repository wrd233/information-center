from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from app.utils import normalize_url, stable_hash


PROXY_NOISE_TOKENS = {
    "api.xgo.ing",
    "xgo.ing",
    "xgoing",
    "rss",
    "feed",
    "feeds",
    "twitter",
    "x.com",
    "t.co",
    "powered",
    "view",
    "quoted",
    "tweet",
    "browser",
    "support",
    "video",
    "https",
    "http",
    "www",
    "com",
    "co",
    "link",
    "links",
    "get",
    "started",
    "does",
    "your",
    "you",
    "not",
    "tag",
    "utm_source",
    "utm_medium",
}

GENERIC_ENTITY_TOKENS = {
    "about",
    "again",
    "agent",
    "agents",
    "ai",
    "aiautomation",
    "aiworkflow",
    "app",
    "apps",
    "api",
    "across",
    "all",
    "also",
    "already",
    "actually",
    "any",
    "access",
    "available",
    "benchmark",
    "blog",
    "build",
    "business",
    "but",
    "character",
    "create",
    "data",
    "demo",
    "download",
    "female",
    "feature",
    "general",
    "github",
    "gpt",
    "home",
    "idea",
    "ideas",
    "inside",
    "launch",
    "learn",
    "like",
    "llm",
    "model",
    "models",
    "more",
    "new",
    "open",
    "open-source",
    "paper",
    "platform",
    "preview",
    "product",
    "prompt",
    "real",
    "release",
    "research",
    "source",
    "start",
    "thread",
    "today",
    "tool",
    "tools",
    "tour",
    "update",
    "users",
    "walk",
    "workflow",
    "workflows",
    "your",
    "around",
    "early",
    "best",
    "faster",
    "tip",
    "tips",
}

STOPWORDS = {
    "the",
    "and",
    "with",
    "from",
    "that",
    "this",
    "for",
    "about",
    "after",
    "before",
    "using",
    "into",
    "have",
    "has",
    "was",
    "were",
    "are",
    "will",
    "can",
    "all",
    "also",
    "already",
    "across",
    "actually",
    "better",
    "available",
    "around",
    "access",
    "build",
    "get",
    "started",
    "https",
    "http",
    "how",
    "what",
    "why",
    "now",
    "new",
}

EVENT_PHRASES = {
    "launch",
    "launched",
    "release",
    "released",
    "rollout",
    "update",
    "benchmark",
    "partnership",
    "acquisition",
    "funding",
    "open-source",
    "opensourced",
    "paper",
    "research",
    "incident",
    "availability",
    "preview",
    "pricing",
    "integration",
    "api",
    "agent",
}

GENERIC_EVENT_PHRASES = {"agent", "api", "research", "paper", "update", "release", "launch", "preview", "benchmark"}

EVENT_ACTION_ALIASES = {
    "announc": "release",
    "available": "availability",
    "availability": "availability",
    "benchmark": "benchmark",
    "dataset": "dataset",
    "funding": "funding",
    "incident": "security_issue",
    "integration": "integration",
    "launch": "launch",
    "launched": "launch",
    "opensourced": "release",
    "open-source": "release",
    "outage": "outage",
    "paper": "paper",
    "partnership": "partnership",
    "preview": "availability",
    "pricing": "pricing",
    "release": "release",
    "released": "release",
    "rollout": "availability",
    "security": "security_issue",
    "update": "feature_update",
}

AI_ENTITY_RE = re.compile(
    r"\b(?:OpenAI|ChatGPT|Codex|GPT[-\w.]*|o[134](?:-mini)?|Anthropic|Claude|Google|Gemini|DeepMind|xAI|Grok|DeepSeek|Qwen[\w.-]*|Alibaba|Cursor|Windsurf|Cognition|Devin|LangChain|LlamaIndex|Perplexity|Hugging\s+Face|NVIDIA|Replit|Runway|Pika|Redis|Weaviate|Kimi|Manus|Mem0|Meta|Microsoft|GitHub|arXiv|Cohere|Aleph\s+Alpha|Notion|Oracle|ElevenLabs|Monica|Skywork|Fireworks|Mistral|v\d+(?:\.\d+)?|V\d+(?:\.\d+)?|R1)\b",
    re.IGNORECASE,
)

VERSION_OR_PRODUCT_RE = re.compile(
    r"\b(?:[A-Z][A-Za-z]+(?:[-\s][A-Z0-9][A-Za-z0-9.]+){0,4}\s(?:Agent|Agents|API|SDK|Computer|Transcribe|Realtime|Whisper|Translate|Search|Operator|Database|Characters)|[A-Za-z]+[-\s]?\d+(?:\.\d+)*(?:[-\w.]*)?|GPT[-\s]?[A-Za-z0-9.:-]+|Grok[-\s]?[A-Za-z0-9.:-]+|Qwen[\w.-]*|Kimi[-\s]?[A-Za-z0-9.:-]+|Claude[-\s]?[A-Za-z0-9.:-]+|Gemini[-\s]?[A-Za-z0-9.:-]+|Parallel\s+Agents|GPT-Realtime-2|Realtime\s+API|Agent\s+API|Finance\s+Search)\b",
    re.IGNORECASE,
)

BOILERPLATE_PATTERNS = [
    re.compile(r"\bi break down stories like this every day\b", re.IGNORECASE),
    re.compile(r"\bsubscribe\b.*\bnewsletter\b", re.IGNORECASE),
    re.compile(r"\bclick here\b|\bread more\b|\bfull story\b", re.IGNORECASE),
    re.compile(r"\bfollow me\b|\bjoin \d+[km]?\+?\b", re.IGNORECASE),
]


@dataclass
class CandidateAssessment:
    candidate_score: float
    candidate_priority: str
    candidate_score_components: dict[str, float] = field(default_factory=dict)
    candidate_suppression_reason: str | None = None
    shared_entities: list[str] = field(default_factory=list)
    shared_entities_weighted: list[str] = field(default_factory=list)
    boilerplate_detected: bool = False
    generic_entity_overlap: bool = False
    same_event_evidence: list[str] = field(default_factory=list)
    new_info_evidence: list[str] = field(default_factory=list)
    disqualifiers: list[str] = field(default_factory=list)
    positive_features: list[str] = field(default_factory=list)
    negative_features: list[str] = field(default_factory=list)
    event_signature_key: str | None = None
    event_signature_match: bool = False
    generic_only: bool = False
    time_window_hours: float | None = None
    generic_overlap: list[str] = field(default_factory=list)

    @property
    def suppressed(self) -> bool:
        return self.candidate_priority == "suppress"

    def model_dump(self) -> dict[str, Any]:
        return {
            "candidate_score": round(self.candidate_score, 3),
            "candidate_priority": self.candidate_priority,
            "candidate_score_components": self.candidate_score_components,
            "candidate_suppression_reason": self.candidate_suppression_reason,
            "shared_entities": self.shared_entities,
            "shared_entities_weighted": self.shared_entities_weighted,
            "boilerplate_detected": self.boilerplate_detected,
            "generic_entity_overlap": self.generic_entity_overlap,
            "same_event_evidence": self.same_event_evidence,
            "new_info_evidence": self.new_info_evidence,
            "disqualifiers": self.disqualifiers,
            "positive_features": self.positive_features,
            "negative_features": self.negative_features,
            "event_signature_key": self.event_signature_key,
            "event_signature_match": self.event_signature_match,
            "generic_only": self.generic_only,
            "time_window_hours": round(self.time_window_hours, 3) if self.time_window_hours is not None else None,
            "generic_overlap": self.generic_overlap,
            "reason": "; ".join(self.positive_features + self.negative_features + self.disqualifiers),
        }


def parse_json_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if not value:
        return {}
    try:
        parsed = json.loads(str(value))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not value:
        return []
    try:
        parsed = json.loads(str(value))
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def semantic_tokens(text: str) -> set[str]:
    raw = re.findall(r"[A-Za-z][A-Za-z0-9_.+-]{1,}|[\u4e00-\u9fff]{2,8}", (text or "").lower())
    return {
        token.strip("._-")
        for token in raw
        if len(token.strip("._-")) >= 2 and token not in STOPWORDS
    }


def normalized_entity_terms(values: list[str]) -> set[str]:
    terms: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        lowered = text.lower()
        terms.add(lowered)
        compact = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", lowered)
        if compact:
            terms.add(compact)
    return terms


def is_proxy_noise_token(token: str) -> bool:
    lowered = (token or "").strip().lower()
    if lowered in PROXY_NOISE_TOKENS or lowered in STOPWORDS:
        return True
    if lowered.startswith("api.xgo.ing") or lowered.endswith(".xgo.ing"):
        return True
    return False


def filtered_semantic_tokens(text: str) -> list[str]:
    tokens = []
    for token in semantic_tokens(text):
        if is_proxy_noise_token(token):
            continue
        if len(token) < 3 and not re.search(r"\d", token):
            continue
        tokens.append(token)
    return sorted(set(tokens))


def ai_entities(text: str) -> list[str]:
    found: list[str] = []
    for match in AI_ENTITY_RE.finditer(text or ""):
        value = " ".join(match.group(0).split())
        if value and value.lower() not in {item.lower() for item in found}:
            found.append(value)
    return found


def event_phrases(text: str) -> list[str]:
    lowered = (text or "").lower()
    return sorted({phrase for phrase in EVENT_PHRASES if phrase in lowered})


def event_action(text: str) -> str | None:
    lowered = (text or "").lower()
    ordered = [
        ("launches", "launch"),
        ("launched", "launch"),
        ("launch", "launch"),
        ("announc", "release"),
        ("released", "release"),
        ("release", "release"),
        ("rollout", "availability"),
        ("available", "availability"),
        ("availability", "availability"),
    ]
    for needle, action in ordered:
        if needle in lowered:
            return action
    for needle, action in EVENT_ACTION_ALIASES.items():
        if needle in lowered:
            return action
    return None


def concrete_products(text: str, entities: list[str] | None = None) -> list[str]:
    found: list[str] = []
    entity_lowers = {entity.lower() for entity in (entities or [])}
    for match in VERSION_OR_PRODUCT_RE.finditer(text or ""):
        value = " ".join(match.group(0).replace("_", " ").split()).strip(" .,:;")
        lowered = value.lower()
        if not value or lowered in GENERIC_ENTITY_TOKENS or lowered in entity_lowers:
            continue
        if lowered not in {item.lower() for item in found}:
            found.append(value)
    return found[:8]


def published_day_bucket(item: dict[str, Any]) -> str | None:
    parsed = parse_time(item.get("published_at") or item.get("created_at"))
    return parsed.date().isoformat() if parsed else None


def event_signature(item: dict[str, Any], card: dict[str, Any] | None = None) -> dict[str, Any]:
    text = item_text(item, card)
    actors = ai_entities(text)
    products = concrete_products(text, actors)
    action = event_action(text)
    bucket = published_day_bucket(item)
    generic_tokens = sorted(token for token in semantic_tokens(text) if token in GENERIC_ENTITY_TOKENS)[:20]
    confidence = 0.0
    if actors and products and action:
        confidence = 0.86
    elif actors and products:
        confidence = 0.62
    elif actors and action:
        confidence = 0.46
    elif products and action:
        confidence = 0.42
    key = None
    if confidence >= 0.8 and action and bucket:
        actor_key = normalized_entity_terms([actors[0]]).pop() if actors else "unknown"
        product_key = normalized_entity_terms([products[0]]).pop() if products else "unknown"
        action_key = action or "event"
        key = f"{actor_key}|{product_key}|{action_key}|{bucket}"
    return {
        "signature_key": key,
        "actors": actors[:6],
        "products": products[:6],
        "event_type": action,
        "time_bucket": bucket,
        "generic_tokens": generic_tokens,
        "confidence": round(confidence, 3),
        "is_concrete": bool(key),
    }


def non_proxy_domain(url: str | None) -> str | None:
    if not url:
        return None
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return None
    host = host.removeprefix("www.")
    if not host or host in {"api.xgo.ing", "xgo.ing", "twitter.com", "x.com", "t.co"}:
        return None
    return host


def item_text(item: dict[str, Any], card: dict[str, Any] | None = None) -> str:
    parts = [
        item.get("title"),
        item.get("summary"),
        item.get("content_text"),
    ]
    if card:
        parts.extend([card.get("canonical_title"), card.get("event_hint"), card.get("short_summary")])
        parts.extend(parse_json_list(card.get("entities_json")))
    return " ".join(str(part or "") for part in parts)


def item_entities(item: dict[str, Any], card: dict[str, Any] | None = None) -> set[str]:
    values = ai_entities(item_text(item, card))
    if card:
        values.extend(str(v) for v in parse_json_list(card.get("entities_json")))
    values.extend(filtered_semantic_tokens(f"{item.get('title') or ''} {item.get('summary') or ''}")[:12])
    return normalized_entity_terms(values)


def original_item_id(item: dict[str, Any]) -> str:
    raw = parse_json_dict(item.get("raw_json")) or parse_json_dict(item.get("latest_raw_json"))
    return str(raw.get("source_item_id") or item.get("original_item_id") or item.get("item_id") or "")


def stable_item_key(item: dict[str, Any], dry_run_item_id: str | None = None) -> str:
    original = original_item_id(item)
    if original:
        return f"orig:{original}"
    if item.get("dedupe_key"):
        return f"dedupe:{item['dedupe_key']}"
    if item.get("source_id") and item.get("guid"):
        return f"guid:{item['source_id']}:{item['guid']}"
    if item.get("source_id") and item.get("url"):
        return f"url:{item['source_id']}:{normalize_url(item['url'])}"
    return f"item:{dry_run_item_id or item.get('item_id') or ''}"


def relation_pair_key(left: dict[str, Any], right: dict[str, Any]) -> str:
    keys = sorted([stable_item_key(left), stable_item_key(right)])
    return stable_hash("|".join(keys))


def title_similarity(left: str, right: str) -> float:
    a = semantic_tokens(left or "")
    b = semantic_tokens(right or "")
    if not a or not b:
        return 0.0
    return len(a & b) / max(1.0, math.sqrt(len(a) * len(b)))


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def hours_apart(left: str | None, right: str | None) -> float | None:
    a = parse_time(left)
    b = parse_time(right)
    if not a or not b:
        return None
    return abs((a - b).total_seconds()) / 3600


def time_proximity_score(left: dict[str, Any], right: dict[str, Any]) -> float:
    gap = hours_apart(left.get("published_at") or left.get("created_at"), right.get("published_at") or right.get("created_at"))
    if gap is None:
        return 0.0
    if gap <= 24:
        return 1.0
    if gap <= 72:
        return 0.65
    if gap <= 168:
        return 0.25
    return 0.0


def detect_boilerplate(text: str) -> bool:
    lowered = text or ""
    return any(pattern.search(lowered) for pattern in BOILERPLATE_PATTERNS)


def deterministic_duplicate(left: dict[str, Any], right: dict[str, Any]) -> tuple[str, list[str]] | None:
    roles: list[str] = []
    if left.get("url") and right.get("url") and normalize_url(left["url"]) == normalize_url(right["url"]):
        roles.append("same_url")
    if left.get("guid") and right.get("guid") and left["guid"] == right["guid"]:
        roles.append("same_guid")
    if roles:
        return "duplicate", roles
    if stable_hash((left.get("title") or "").strip().lower()) == stable_hash((right.get("title") or "").strip().lower()):
        return "near_duplicate", ["same_title_hash"]
    return None


def assess_candidate(
    left_item: dict[str, Any],
    right_item: dict[str, Any],
    left_card: dict[str, Any] | None = None,
    right_card: dict[str, Any] | None = None,
) -> CandidateAssessment:
    left_text = item_text(left_item, left_card)
    right_text = item_text(right_item, right_card)
    left_entities = item_entities(left_item, left_card)
    right_entities = item_entities(right_item, right_card)
    shared = sorted(left_entities & right_entities)
    weighted = [entity for entity in shared if entity not in GENERIC_ENTITY_TOKENS and not is_proxy_noise_token(entity)]
    title_score = title_similarity(left_item.get("title") or "", right_item.get("title") or "")
    event_left = set(event_phrases(left_text))
    event_right = set(event_phrases(right_text))
    concrete_event_phrase_overlap = (event_left & event_right) - GENERIC_EVENT_PHRASES
    event_overlap = len(event_left & event_right) / max(1, min(len(event_left) or 1, len(event_right) or 1))
    time_score = time_proximity_score(left_item, right_item)
    time_gap = hours_apart(left_item.get("published_at") or left_item.get("created_at"), right_item.get("published_at") or right_item.get("created_at"))
    cross_source = (left_item.get("source_id") or left_item.get("source_name") or "") != (right_item.get("source_id") or right_item.get("source_name") or "")
    boilerplate = detect_boilerplate(left_text) or detect_boilerplate(right_text)
    shared_generic = sorted(entity for entity in shared if entity in GENERIC_ENTITY_TOKENS or is_proxy_noise_token(entity))
    generic_overlap = bool(shared) and not weighted
    left_sig = event_signature(left_item, left_card)
    right_sig = event_signature(right_item, right_card)
    signature_match = bool(left_sig.get("signature_key") and left_sig.get("signature_key") == right_sig.get("signature_key"))
    shared_actors = sorted(normalized_entity_terms(left_sig.get("actors", [])) & normalized_entity_terms(right_sig.get("actors", [])))
    shared_products = sorted(normalized_entity_terms(left_sig.get("products", [])) & normalized_entity_terms(right_sig.get("products", [])))
    same_action = bool(left_sig.get("event_type") and left_sig.get("event_type") == right_sig.get("event_type"))
    concrete_event_match = signature_match or (
        bool(shared_actors and shared_products and same_action and (time_gap is None or time_gap <= 72))
        or bool(len(weighted) >= 2 and concrete_event_phrase_overlap and (time_gap is not None and time_gap <= 72))
        or bool(shared_actors and len(weighted) >= 2 and title_score >= 0.55 and (time_gap is not None and time_gap <= 72))
    )
    same_source_penalty = -0.45 if not cross_source else 0.0
    boilerplate_penalty = -1.2 if boilerplate else 0.0
    proxy_penalty = -1.0 if any(is_proxy_noise_token(token) for token in shared) else 0.0
    generic_penalty = -1.4 if generic_overlap else 0.0
    score = (
        title_score * 3.0
        + min(len(weighted), 4) * 0.9
        + event_overlap * 0.45
        + time_score * 0.45
        + (0.45 if cross_source and concrete_event_match else 0.0)
        + (4.0 if signature_match else 0.0)
        + (2.5 if concrete_event_match and not signature_match else 0.0)
        + (0.8 if shared_products else 0.0)
        + same_source_penalty
        + boilerplate_penalty
        + proxy_penalty
        + generic_penalty
    )
    disqualifiers: list[str] = []
    suppression_reason: str | None = None
    if boilerplate:
        disqualifiers.append("same_account_boilerplate")
    if generic_overlap:
        disqualifiers.append("generic_entity_overlap")
    if not weighted and not title_score and any(is_proxy_noise_token(token) for token in shared):
        disqualifiers.append("proxy_domain_only")
    hard = deterministic_duplicate(left_item, right_item)
    generic_only = bool(shared_generic) and not weighted and not concrete_event_match and title_score < 0.55
    if generic_only and "generic_only_overlap" not in disqualifiers:
        disqualifiers.append("generic_only_overlap")
    if time_gap is not None and time_gap > 168 and not hard and not signature_match:
        disqualifiers.append("wide_time_window")
    if hard:
        priority = "must_run"
    elif "proxy_domain_only" in disqualifiers:
        priority = "suppress"
        suppression_reason = "suppressed_proxy_domain"
    elif generic_only:
        priority = "suppress"
        suppression_reason = "suppressed_generic_only"
    elif boilerplate and title_score < 0.45 and len(weighted) < 2:
        priority = "suppress"
        suppression_reason = "suppressed_boilerplate"
    elif generic_overlap and title_score < 0.4 and event_overlap <= 0:
        priority = "suppress"
        suppression_reason = "suppressed_generic_entity"
    elif title_score >= 0.82 and time_score >= 0.65:
        priority = "must_run"
    elif concrete_event_match and score >= 5.0:
        priority = "must_run"
    elif concrete_event_match and score >= 3.4:
        priority = "high"
    elif (shared_products and (shared_actors or same_action) and time_score >= 0.25) or score >= 2.2:
        priority = "medium"
    elif score > 0:
        priority = "low"
    else:
        priority = "suppress"
        suppression_reason = "weak_same_topic"
    same_event_evidence = []
    if title_score >= 0.55:
        same_event_evidence.append("high_title_similarity")
    if weighted:
        same_event_evidence.append(f"shared_weighted_entities:{', '.join(weighted[:5])}")
    if signature_match:
        same_event_evidence.append(f"event_signature_match:{left_sig.get('signature_key')}")
    elif concrete_event_match:
        same_event_evidence.append("same_actor_product_action_72h")
    if event_left & event_right:
        same_event_evidence.append(f"shared_event_phrases:{', '.join(sorted(event_left & event_right))}")
    if concrete_event_phrase_overlap:
        same_event_evidence.append(f"shared_concrete_event_phrases:{', '.join(sorted(concrete_event_phrase_overlap))}")
    if time_score >= 0.65:
        same_event_evidence.append("close_time_window")
    positive_features = list(same_event_evidence)
    if shared_products:
        positive_features.append(f"shared_products:{', '.join(shared_products[:5])}")
    if shared_actors:
        positive_features.append(f"shared_actors:{', '.join(shared_actors[:5])}")
    negative_features = []
    if shared_generic:
        negative_features.append(f"generic_overlap:{', '.join(shared_generic[:8])}")
    if time_gap is not None and time_gap > 168:
        negative_features.append(f"wide_time_window_hours:{round(time_gap, 1)}")
    return CandidateAssessment(
        candidate_score=max(0.0, round(score, 3)),
        candidate_priority=priority,
        candidate_score_components={
            "title_similarity": round(title_score, 3),
            "entity_overlap_weighted": float(len(weighted)),
            "event_signature_match": 1.0 if signature_match else 0.0,
            "concrete_event_match": 1.0 if concrete_event_match else 0.0,
            "product_overlap": float(len(shared_products)),
            "actor_overlap": float(len(shared_actors)),
            "event_action_overlap": 1.0 if same_action else 0.0,
            "event_phrase_overlap": round(event_overlap, 3),
            "time_proximity": round(time_score, 3),
            "source_diversity": 1.0 if cross_source else 0.0,
            "same_source_penalty": same_source_penalty,
            "boilerplate_penalty": boilerplate_penalty,
            "proxy_domain_penalty": proxy_penalty,
            "generic_entity_penalty": generic_penalty,
        },
        candidate_suppression_reason=suppression_reason,
        shared_entities=shared[:20],
        shared_entities_weighted=weighted[:20],
        boilerplate_detected=boilerplate,
        generic_entity_overlap=generic_overlap,
        same_event_evidence=same_event_evidence,
        new_info_evidence=[],
        disqualifiers=disqualifiers,
        positive_features=positive_features,
        negative_features=negative_features,
        event_signature_key=left_sig.get("signature_key") if signature_match else None,
        event_signature_match=signature_match,
        generic_only=generic_only,
        time_window_hours=time_gap,
        generic_overlap=shared_generic[:20],
    )


def infer_event_relation_type(
    relation_label: str,
    assessment: CandidateAssessment,
    *,
    reason: str = "",
    evidence: list[str] | None = None,
    new_information: list[str] | None = None,
) -> str:
    evidence = evidence or []
    new_information = new_information or []
    if relation_label in {"duplicate", "near_duplicate"}:
        return "same_event"
    reason_text = " ".join([reason, " ".join(evidence), " ".join(new_information)]).lower()
    if assessment.boilerplate_detected or "boilerplate" in reason_text or "newsletter" in reason_text:
        return "same_account_boilerplate"
    if assessment.generic_entity_overlap and not assessment.shared_entities_weighted:
        return "entity_overlap_only"
    if relation_label != "related_with_new_info" and "same product" in reason_text and "same event" not in reason_text:
        return "same_product_different_event"
    if "same_thread" in reason_text or "follow-up" in reason_text or "follow up" in reason_text:
        return "same_thread"
    if relation_label == "related_with_new_info":
        if (
            (assessment.event_signature_match or any("same_actor_product_action_72h" in item for item in assessment.same_event_evidence))
            and new_information
            and not any(d in assessment.disqualifiers for d in {"generic_entity_overlap", "generic_only_overlap", "same_account_boilerplate", "wide_time_window"})
        ):
            return "same_event"
        if (
            "same" in reason_text
            and any(token in reason_text for token in ["rollout", "launch", "release", "announcement", "support"])
            and assessment.shared_entities_weighted
            and new_information
            and not any(d in assessment.disqualifiers for d in {"generic_only_overlap", "same_account_boilerplate", "wide_time_window"})
        ):
            return "same_event"
        if assessment.shared_entities_weighted:
            return "same_product_different_event"
        return "same_topic_only"
    if relation_label == "uncertain":
        if assessment.shared_entities_weighted:
            return "same_topic_only"
        return "different"
    if assessment.shared_entities_weighted and assessment.candidate_score >= 2:
        return "same_topic_only"
    return "different"


def relation_cluster_eligible(relation_label: str, event_relation_type: str) -> bool:
    return relation_label in {"duplicate", "near_duplicate", "related_with_new_info"} and event_relation_type == "same_event"


def normalize_relation_label(
    relation_label: str,
    assessment: CandidateAssessment,
    *,
    reason: str = "",
    evidence: list[str] | None = None,
    new_information: list[str] | None = None,
) -> tuple[str, str, bool, list[str]]:
    event_type = infer_event_relation_type(
        relation_label,
        assessment,
        reason=reason,
        evidence=evidence,
        new_information=new_information,
    )
    disqualifiers = list(assessment.disqualifiers)
    if relation_label == "related_with_new_info" and event_type != "same_event":
        relation_label = "different"
        if event_type not in disqualifiers:
            disqualifiers.append(event_type)
    eligible = relation_cluster_eligible(relation_label, event_type)
    return relation_label, event_type, eligible, disqualifiers


def hotspot_key_candidates(item: dict[str, Any]) -> dict[str, Any]:
    text = item_text(item)
    raw = sorted(semantic_tokens(text))
    filtered = [token for token in raw if not is_proxy_noise_token(token) and token not in GENERIC_ENTITY_TOKENS]
    entities = ai_entities(text)
    phrases = event_phrases(text)
    domain = non_proxy_domain(item.get("url"))
    signature = event_signature(item)
    selected = ""
    key_source = "fallback"
    if signature.get("signature_key"):
        selected = str(signature["signature_key"])
        key_source = "event_signature"
    elif entities and filtered and not set(filtered).issubset(GENERIC_ENTITY_TOKENS):
        product = concrete_products(text, entities)
        if product:
            selected = f"{entities[0].lower()}|{product[0].lower()}"
            key_source = "entity_product"
        else:
            selected = entities[0].lower()
            key_source = "entity"
    elif phrases and filtered:
        selected = f"{filtered[0]}:{phrases[0]}"
        key_source = "event_phrase"
    elif domain:
        selected = domain
        key_source = "target_domain"
    elif filtered:
        selected = filtered[0]
        key_source = "fallback"
    else:
        selected = "misc"
    return {
        "raw_candidate_keys": raw[:50],
        "filtered_keys": filtered[:50],
        "selected_hotspot_key": selected,
        "key_source": key_source,
        "proxy_domain_filtered": any(is_proxy_noise_token(token) for token in raw),
        "dominant_entities": entities[:10],
        "dominant_event_phrases": phrases[:10],
        "target_domain": domain,
        "event_signature": signature,
        "signature_key": signature.get("signature_key"),
        "generic_tokens": signature.get("generic_tokens", []),
        "signature_confidence": signature.get("confidence", 0.0),
    }
