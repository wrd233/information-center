from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from app.semantic.config import (
    EVENT_ACTION_ALIASES,
    GENERIC_ENTITY_TOKENS,
    PROXY_NOISE_TOKENS,
    STOPWORDS,
)


AI_ENTITY_RE = re.compile(
    r"\b(?:OpenAI|ChatGPT|Codex|GPT[-\w.]*|Anthropic|Claude|Google|Gemini|DeepMind|xAI|Grok|DeepSeek|Qwen[\w.-]*|Alibaba|Cursor|Windsurf|Cognition|Devin|LangChain|LlamaIndex|LlamaCloud|Perplexity|Hugging\s+Face|NVIDIA|Replit|Runway|Pika|Redis|Weaviate|Kimi|Manus|Mem0|Meta|Microsoft|GitHub|arXiv|Cohere|Aleph\s+Alpha|Notion|Oracle|ElevenLabs|Monica|Skywork|Firecrawl|Fireworks|Mistral|MiniMax|Hailuo|Browser\s+Use|BrowserUse|Lovable|Vercel|Bun|YC|Y\s+Combinator|NASA)\b",
    re.IGNORECASE,
)

PRODUCT_RE = re.compile(
    r"\b(?:[A-Z][A-Za-z]+(?:[-\s][A-Z0-9][A-Za-z0-9.]+){0,5}\s(?:Agent|Agents|API|SDK|Computer|Transcribe|Realtime|Whisper|Translate|Search|Operator|Database|Characters|Connectors|Projects|Memory|Sources|Finance|Health|Harness|Arena)|[A-Za-z]+[-\s]?\d+(?:\.\d+)*(?:[-\w.]*)?|GPT[-\s]?[A-Za-z0-9.:-]+|Grok[-\s]?[A-Za-z0-9.:-]+|Qwen[\w.-]*|Kimi[-\s]?[A-Za-z0-9.:-]+|Claude[-\s]?[A-Za-z0-9.:-]+|Gemini[-\s]?[A-Za-z0-9.:-]+|Parallel\s+Agents|PHP\s+SDK|Laravel|GPT-Realtime-2|Realtime\s+API|Agent\s+API|Finance\s+Search|Professional\s+Finance|Health\s+Sources|Recommended\s+Connectors|Projects\s+memory|Hailuo\s+AI\s+App\s+v?\d+(?:\.\d+)*)\b",
    re.IGNORECASE,
)

VERSION_ONLY_RE = re.compile(r"^v?\d+(?:\.\d+)*(?:[-_\w]*)?$", re.IGNORECASE)
PRICE_OR_MEASURE_RE = re.compile(r"^(?:\$?\d+(?:\.\d+)?(?:m|k|b|%|x)?|at\s+\d+|effective\s+\d+[mkb]?)$", re.IGNORECASE)
MONTH_DATE_RE = re.compile(r"^(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}$", re.IGNORECASE)
RANDOM_ID_RE = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z0-9_-]{8,}$")
LEADING_FRAGMENT_RE = re.compile(r"^(?:for|with|from|at|in|on|by|our|all|the|this|these|those)\b", re.IGNORECASE)


@dataclass(frozen=True)
class EventSignature:
    actor: str = ""
    actor_type: str = "unknown"
    product_or_model: str = ""
    action: str = "other"
    object: str = ""
    date_bucket: str = ""
    time_window_hours: float = 72.0
    source_type: str = "unknown"
    signature_key: str | None = None
    supporting_tokens: list[str] = field(default_factory=list)
    source_item_ids: list[str] = field(default_factory=list)
    concreteness_score: float = 0.0
    is_concrete: bool = False
    invalid_reasons: list[str] = field(default_factory=list)

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


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


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def normalize_key(value: str) -> str:
    lowered = (value or "").lower().strip()
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", lowered)
    return lowered


def semantic_tokens(text: str) -> set[str]:
    raw = re.findall(r"[A-Za-z][A-Za-z0-9_.+-]{1,}|[\u4e00-\u9fff]{2,8}", (text or "").lower())
    return {
        token.strip("._-")
        for token in raw
        if len(token.strip("._-")) >= 2 and token.strip("._-") not in STOPWORDS
    }


def is_generic_or_noise(token: str) -> bool:
    lowered = (token or "").strip().lower()
    return (
        lowered in GENERIC_ENTITY_TOKENS
        or lowered in PROXY_NOISE_TOKENS
        or lowered.startswith("api.xgo.ing")
        or lowered.endswith(".xgo.ing")
    )


def normalized_terms(values: list[str]) -> set[str]:
    out: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        out.add(text.lower())
        compact = normalize_key(text)
        if compact:
            out.add(compact)
    return out


def item_text(item: dict[str, Any], card: dict[str, Any] | None = None) -> str:
    parts: list[Any] = [
        item.get("title"),
        item.get("summary"),
        item.get("content_text"),
    ]
    if card:
        parts.extend([card.get("canonical_title"), card.get("event_hint"), card.get("short_summary")])
        parts.extend(parse_json_list(card.get("entities_json") or card.get("entities")))
    return " ".join(str(part or "") for part in parts)


def ai_entities(text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for match in AI_ENTITY_RE.finditer(text or ""):
        value = " ".join(match.group(0).split()).strip()
        key = value.lower()
        if value and key not in seen and not is_generic_or_noise(key) and not VERSION_ONLY_RE.match(value):
            found.append(value)
            seen.add(key)
    return found


def concrete_products(text: str, actors: list[str] | None = None) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    actor_terms = normalized_terms(actors or [])
    for match in PRODUCT_RE.finditer(text or ""):
        value = " ".join(match.group(0).replace("_", " ").split()).strip(" .,:;")
        key = value.lower()
        compact = normalize_key(value)
        if not value:
            continue
        if key in GENERIC_ENTITY_TOKENS or compact in actor_terms:
            continue
        if PRICE_OR_MEASURE_RE.match(key):
            continue
        if MONTH_DATE_RE.match(value) or RANDOM_ID_RE.match(value) or LEADING_FRAGMENT_RE.match(value):
            continue
        if VERSION_ONLY_RE.match(value) and not re.search(r"[a-zA-Z]{2,}", value):
            continue
        if key not in seen:
            found.append(value)
            seen.add(key)
    return found[:8]


def event_action(text: str) -> str:
    lowered = (text or "").lower()
    ordered = [
        ("case study", "case_study"),
        ("customer", "case_study"),
        ("launches", "launch"),
        ("launched", "launch"),
        ("launch", "launch"),
        ("announc", "release"),
        ("shipped", "release"),
        ("ships", "release"),
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
    return "other"


def published_day_bucket(item: dict[str, Any]) -> str:
    parsed = parse_time(item.get("published_at") or item.get("created_at"))
    return parsed.date().isoformat() if parsed else ""


def source_type(item: dict[str, Any]) -> str:
    source = " ".join(str(item.get(key) or "") for key in ("source_id", "source_name", "feed_url", "url")).lower()
    if "socialmedia-" in source or "x.com" in source or "twitter" in source:
        return "social"
    if "arxiv" in source or "paper" in source:
        return "paper"
    if "blog" in source:
        return "blog"
    if any(domain in source for domain in ["openai.com", "anthropic.com", "google.com", "microsoft.com", "github.com"]):
        return "official"
    if source:
        return "media"
    return "unknown"


def target_domain(url: str | None) -> str:
    if not url:
        return ""
    try:
        host = urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""
    if host in {"api.xgo.ing", "xgo.ing", "twitter.com", "x.com", "t.co"}:
        return ""
    return host


def extract_event_signature(item: dict[str, Any], card: dict[str, Any] | None = None) -> EventSignature:
    text = item_text(item, card)
    actors = ai_entities(text)
    products = concrete_products(text, actors)
    action = event_action(text)
    bucket = published_day_bucket(item)
    tokens = sorted(token for token in semantic_tokens(text) if not is_generic_or_noise(token))[:20]
    generic_tokens = sorted(token for token in semantic_tokens(text) if token in GENERIC_ENTITY_TOKENS)

    actor = actors[0] if actors else ""
    product = products[0] if products else ""
    obj = products[1] if len(products) > 1 else ""
    invalid: list[str] = []
    score = 0.0
    if actor:
        score += 0.30
    if product:
        score += 0.32
    if action and action != "other":
        score += 0.20
    if bucket:
        score += 0.12
    if len(tokens) >= 2:
        score += 0.06

    if actor and (VERSION_ONLY_RE.match(actor) or is_generic_or_noise(actor)):
        invalid.append("invalid_actor_generic_or_version")
    if product and (
        PRICE_OR_MEASURE_RE.match(product.lower())
        or MONTH_DATE_RE.match(product)
        or RANDOM_ID_RE.match(product)
        or LEADING_FRAGMENT_RE.match(product)
        or product.lower() in GENERIC_ENTITY_TOKENS
    ):
        invalid.append("invalid_product_price_or_generic")
    if product and not actor and len(semantic_tokens(product)) > 4:
        invalid.append("invalid_product_fragment_without_actor")
    product_tokens = semantic_tokens(product)
    if product and product_tokens and all(token in GENERIC_ENTITY_TOKENS or is_generic_or_noise(token) for token in product_tokens):
        invalid.append("invalid_product_generic_phrase")
    if not actor and not product:
        invalid.append("missing_concrete_actor_or_product")
    if action in {"feature_update", "release", "other"} and not (actor or product):
        invalid.append("weak_action_without_entity")
    if set(normalize_key(t) for t in tokens).issubset({normalize_key(t) for t in GENERIC_ENTITY_TOKENS}) and not (actor or product):
        invalid.append("generic_tokens_only")
    if "powered" in generic_tokens and len(tokens) < 2 and not actor:
        invalid.append("xgo_boilerplate_dominated")

    if action == "other":
        invalid.append("missing_concrete_event_action")
    is_concrete = score >= 0.68 and not invalid and bool(bucket) and bool(actor or product)
    key = None
    if is_concrete:
        key = "|".join([
            normalize_key(actor or "unknown"),
            normalize_key(product or obj or "unknown"),
            normalize_key(action or "event"),
            bucket,
        ])
    return EventSignature(
        actor=actor,
        actor_type="organization" if actor else "unknown",
        product_or_model=product,
        action=action,
        object=obj,
        date_bucket=bucket,
        source_type=source_type(item),
        signature_key=key,
        supporting_tokens=tokens,
        source_item_ids=[str(item.get("item_id") or "")] if item.get("item_id") else [],
        concreteness_score=round(score, 3),
        is_concrete=is_concrete,
        invalid_reasons=invalid,
    )


def signature_match(left: EventSignature, right: EventSignature) -> bool:
    return bool(left.signature_key and left.signature_key == right.signature_key)


def compatible_actor_product_action(left: EventSignature, right: EventSignature, *, max_hours: float | None = None) -> bool:
    if not left.is_concrete or not right.is_concrete:
        return False
    actor_match = bool(left.actor and right.actor and normalize_key(left.actor) == normalize_key(right.actor))
    product_match = bool(
        left.product_or_model
        and right.product_or_model
        and normalize_key(left.product_or_model) == normalize_key(right.product_or_model)
    )
    action_match = bool(left.action and right.action and left.action == right.action)
    if not (actor_match and product_match and action_match):
        return False
    if max_hours is None:
        return True
    left_time = parse_time(left.date_bucket)
    right_time = parse_time(right.date_bucket)
    if not left_time or not right_time:
        return True
    return abs((left_time - right_time).total_seconds()) / 3600 <= max_hours
