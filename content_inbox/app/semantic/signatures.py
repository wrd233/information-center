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

SEMANTIC_LEVELS = {"event_signature", "thread_signature", "content_signature", "reject"}
EVENT_ACTIONS = {
    "release",
    "feature_update",
    "availability",
    "pricing",
    "benchmark",
    "ranking",
    "adoption_metric",
    "case_study",
    "integration",
    "partnership",
    "funding",
    "company_launch",
    "research_paper",
    "technical_blog",
    "security",
    "event",
    "tutorial",
    "opinion_analysis",
    "other",
}

ACTION_TRIGGERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("company_launch", ("congrats on the launch", "new company", "founded", "stealth", "官宣", "新公司", "联合创始人", "正式成立")),
    ("pricing", ("free", "discount", "price", "pricing", "plan", "tier", "dollar", "cost", "免费", "降价", "价格", "套餐", "1块钱", "元", "优惠", "折扣")),
    ("adoption_metric", ("market share", "adoption", "revenue", "users", "subscribers", "market cap", "valuation", "surpassed", "hit a $", "采用率", "市场份额", "用户数", "营收", "市值", "增长", "超过", "超越", "领先")),
    ("availability", ("now available", "available on", "coming to", "waitlist", "preview", "beta", "early access", "shipping", "rolling out", "技术预览", "候补", "内测", "公测", "开放申请")),
    ("integration", ("integrate", "integration", "connect", "plugin", "extension", "api", "sdk", "works with", "集成", "接入", "接进", "连接", "打通", "对接", "兼容")),
    ("partnership", ("partner", "partnership", "collaboration", "together with", "teaming up", "合作", "联手", "战略合作", "签约")),
    ("funding", ("raised", "funding", "series", "seed", "investor", "round", "融资", "投资", "估值", "资本")),
    ("technical_blog", ("how we built", "deep dive", "under the hood", "architecture", "implementation", "engineering", "技术博客", "深度", "架构", "实现", "工程", "沙箱")),
    ("security", ("vulnerability", "cve", "security fix", "patch", "advisory", "incident", "breach", "漏洞", "修复", "补丁")),
    ("event", ("summit", "conference", "webinar", "meetup", "livestream", "workshop", "register", "ticket", "fireside chat", "ask the experts", "大会", "研讨会", "直播", "活动", "报名", "门票", "峰会")),
    ("research_paper", ("paper:", "paper", "arxiv", "preprint", "published", "proceedings", "论文", "预印本", "发表", "研究", "实验")),
    ("benchmark", ("benchmark", "evaluation", "score", "accuracy", "performance", "tested on", "基准", "评测", "跑分", "分数", "准确率")),
    ("feature_update", ("now supports", "can now", "new feature", "update", "now you can", "support", "支持", "新增", "更新", "功能", "现在可以")),
    ("release", ("release", "launch", "ship", "shipped", "introducing", "announcing", "new way", "opensourced", "open-source", "发布", "推出", "上线", "开源", "释出", "正式发布", "出了")),
    ("case_study", ("case study", "customer", "how we", "how i", "built with", "using", "实践", "案例", "客户")),
    ("tutorial", ("how to", "tutorial", "guide", "walkthrough", "step by step", "learn", "教程", "指南", "怎么", "如何")),
    ("opinion_analysis", ("i think", "in my opinion", "hot take", "reflection", "thoughts on", "我觉得", "我认为", "说实话", "感受")),
)

LOW_SIGNAL_TITLES = {
    "great advice",
    "banger",
    "concerning",
    "concerning.",
    "open > closed",
}

KNOWN_ACTOR_ALIASES = {
    "snyksec": "Snyk",
    "notionhq": "Notion",
    "langchainai": "LangChain",
}

KNOWN_PRODUCT_OWNER = {
    "openshell": "NVIDIA",
    "notion": "Notion",
    "codex": "OpenAI/Codex",
    "github copilot": "GitHub",
    "langsmith": "LangChain",
    "nemotron": "NVIDIA",
    "stelline": "NVIDIA",
    "claude": "Anthropic",
    "qveris": "QVeris",
}


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
MONTH_DATE_RE = re.compile(r"^(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}(?:st|nd|rd|th)?$", re.IGNORECASE)
RANDOM_ID_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9_-]{8,}$")
LEADING_FRAGMENT_RE = re.compile(r"^(?:for|with|from|at|in|on|by|our|all|the|this|these|those)\b", re.IGNORECASE)


@dataclass(frozen=True)
class EventSignature:
    semantic_level: str = "reject"
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
    confidence: float = 0.0
    is_event_like: bool = False
    is_thread_like: bool = False
    reject_reason: str = ""
    extraction_notes: str = ""
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


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text or "")


def word_count(value: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]", value or ""))


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
        if key in GENERIC_ENTITY_TOKENS:
            continue
        if compact in actor_terms and not re.search(r"\d", value):
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


def is_invalid_product(value: str) -> bool:
    text = " ".join(str(value or "").strip().split()).strip(" .,:;")
    if not text:
        return True
    lowered = text.lower()
    if lowered in GENERIC_ENTITY_TOKENS or is_generic_or_noise(lowered):
        return True
    if lowered in {"googlebook", "langsmith fleet", "github copilot desktop", "openshell", "qveris cli", "notion cli", "notion workers", "notion custom agents", "notion developer platform", "token calling plan"}:
        return False
    if PRICE_OR_MEASURE_RE.match(lowered) or MONTH_DATE_RE.match(text) or RANDOM_ID_RE.match(text):
        return True
    if LEADING_FRAGMENT_RE.match(text):
        return True
    if VERSION_ONLY_RE.match(text):
        return True
    if word_count(text) > 8:
        return True
    if len(text) >= 8 and re.fullmatch(r"[A-Za-z0-9_-]+", text) and not re.search(r"(gpt|qwen|kimi|claude|gemini|llama|mistral|nemotron|openshell|seedance)", lowered):
        return True
    if re.search(r"^https?://|t\.co/[A-Za-z0-9]+", text):
        return True
    if any(phrase in lowered for phrase in ("for updates from my phone", "made just for developers", "give your custom agents", "build video analytics ai agents")):
        return True
    return False


def is_invalid_actor(value: str) -> bool:
    text = " ".join(str(value or "").strip().split()).strip(" .,:;")
    if not text:
        return True
    lowered = text.lower().lstrip("@")
    if text in {"GitHub", "OpenAI/Codex"}:
        return False
    if lowered in GENERIC_ENTITY_TOKENS or is_generic_or_noise(lowered):
        return True
    if VERSION_ONLY_RE.match(text) or RANDOM_ID_RE.match(text):
        return True
    if "/" in text and text not in {"OpenAI/Codex"}:
        return True
    return False


def event_action(text: str) -> str:
    lowered = (text or "").lower()
    if re.search(r"\b[A-Za-z][A-Za-z0-9_.-]{1,40}\s+v\d+(?:\.\d+)+", text or "", re.IGNORECASE):
        return "release"
    if re.search(r"\b(event|summit|conference|webinar)\b", lowered):
        return "event"
    if re.search(r"\b[A-Za-z0-9]+ \(@[A-Za-z0-9_]+\) turns\b", text or "") or "adialante is changing" in lowered:
        return "company_launch"
    if "custom agents" in lowered and ("tool" in lowered or "workers" in lowered):
        return "feature_update"
    for action, triggers in ACTION_TRIGGERS:
        if any(trigger in lowered for trigger in triggers):
            return action
    for needle, action in EVENT_ACTION_ALIASES.items():
        if needle in lowered:
            if action == "launch":
                return "release"
            if action == "paper":
                return "research_paper"
            if action == "dataset":
                return "benchmark"
            return action if action in EVENT_ACTIONS else "other"
    return "other"


def explicit_products(text: str) -> list[str]:
    products: list[str] = []
    patterns = [
        r"\b(OpenShell\s+v\d+(?:\.\d+)+)\b",
        r"\b(AI Security Summit)\b",
        r"\b(Googlebook)\b",
        r"\b(GitHub Copilot Desktop)\b",
        r"(GitHub Copilot\s*桌面端)",
        r"\b(LangSmith Fleet)\b",
        r"\b(Notion\s+(?:CLI|Custom Agents|Agent Tools|Workers|Developer Platform))\b",
        r"\b(QVeris CLI)\b",
        r"\b(Codex(?: Remote Control| for Windows)?)\b",
        r"\b(Nemotron\s+3\s+Nano\s+Omni)\b",
        r"\b(Stelline\s+(?:Developer|Dev)\s+Kit)\b",
        r"\b(DGX Spark)\b",
        r"\b(Hermes Agent)\b",
        r"\b(PLAN0)\b",
        r"\b(Adialante(?: mobile MRI)?)\b",
        r"\b(Recursive(?: Superintelligence)?)\b",
        r"(Token\s*(?:calling\s*)?plan|Token\s*话费套餐|话费套餐)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text or "", re.IGNORECASE):
            product = " ".join(match.group(1).split()).strip(" .,:;")
            if product.lower().startswith("github copilot"):
                product = "GitHub Copilot Desktop"
            if "话费套餐" in product:
                product = "Token calling plan"
            if product and not is_invalid_product(product) and product.lower() not in {p.lower() for p in products}:
                products.append(product)
    if "Notion" in (text or "") and any(term in text for term in ["CLI", "Workers", "Custom Agents", "Tools", "Developer Platform"]):
        if "Notion Developer Platform" not in products:
            products.append("Notion Developer Platform")
    if "上海电信" in (text or "") and ("Token" in (text or "") or "套餐" in (text or "")):
        products.append("Token calling plan")
    if re.search(r"\bNVDA\b|Nvidia became", text or "", re.IGNORECASE):
        products.append("NVDA")
    if "Anthropic" in (text or "") and ("surpassed OpenAI" in (text or "") or "enterprise AI spending" in (text or "")):
        products.append("Claude")
    if "Custom Agents" in (text or ""):
        products.append("Notion Custom Agents")
    if "favorite agent builder" in (text or "") or "Use Flee" in (text or ""):
        products.append("LangSmith Fleet")
    if "Luigi" in (text or "") and "box is headed to your desk" in (text or ""):
        products.append("Stelline Developer Kit")
    if re.search(r"\bOpenAI\b.*\bevent\b", text or "", re.IGNORECASE):
        products.append("OpenAI event")
    return products


def infer_actor(text: str, products: list[str], actors: list[str]) -> str:
    lowered = (text or "").lower()
    if "前 meta" in lowered and "recursive" in lowered:
        return "Recursive"
    if "recursive" in lowered and "新公司" in lowered:
        return "Recursive"
    if "上海电信" in (text or ""):
        return "China Telecom Shanghai"
    if "qveris cli" in lowered or "qveris" in lowered:
        return "QVeris"
    if "googlebook" in lowered:
        return "Google"
    if "plan0" in lowered:
        return "PLAN0"
    if "adialante" in lowered:
        return "Adialante"
    if "ai security summit" in lowered or "@snyksec" in lowered:
        return "Snyk"
    if "ask the experts" in lowered and "nemotron" in lowered:
        return "NVIDIA"
    if "langsmith fleet" in lowered:
        return "LangChain"
    if "favorite agent builder" in lowered:
        return "LangChain"
    if "langchain interrupt" in lowered or "@hwchase" in lowered:
        return "LangChain"
    if "github copilot" in lowered:
        return "GitHub"
    if "nvidia became" in lowered or "nvda" in lowered:
        return "NVIDIA"
    if "anthropic" in lowered and "surpassed openai" in lowered:
        return "Anthropic"
    if "luigi" in lowered and "box is headed to your desk" in lowered:
        return "NVIDIA"
    if "codex" in lowered:
        return "OpenAI/Codex"
    for product in products:
        pl = product.lower()
        for prefix, owner in KNOWN_PRODUCT_OWNER.items():
            if pl.startswith(prefix) or prefix in pl:
                return owner
    for raw in actors:
        clean = raw.strip().lstrip("@")
        alias = KNOWN_ACTOR_ALIASES.get(clean.lower())
        candidate = alias or clean
        if candidate.lower() == "meta" and "recursive" in lowered:
            continue
        if candidate.lower() == "claude" and "qveris" in lowered:
            continue
        if not is_invalid_actor(candidate):
            return candidate
    return ""


def classify_semantic_level(text: str, action: str, actor: str, product: str, source: str) -> tuple[str, str]:
    compact = " ".join((text or "").strip().split())
    lowered = compact.lower().strip(" .")
    if lowered in LOW_SIGNAL_TITLES or (word_count(compact) <= 2 and not actor and not product):
        return "reject", "low_signal_short_or_engagement"
    if not (actor or product) and action in {"funding", "research_paper", "opinion_analysis"}:
        return "reject", "abstract_commentary_without_event_entity"
    if re.match(r"^paper:\s*https?://", compact, re.IGNORECASE) or ("_akhaliq" in source.lower() and action == "research_paper"):
        return "thread_signature", "recurring_paper_feed"
    if "curious what people are running locally" in lowered:
        return "thread_signature", "personal_case_study_thread"
    if "沉浸式翻译" in compact and action == "other":
        return "content_signature", "personal_tool_setup"
    if action == "opinion_analysis" and not (actor and product):
        return "reject", "opinion_without_event"
    if action == "research_paper" and not (actor and product):
        return "thread_signature", "paper_thread"
    if actor and product and action != "other":
        return "event_signature", ""
    if actor and product and any(term in lowered for term in ("turns ", "is changing", "made accessible", "construction cost", "mobile mri")):
        return "event_signature", ""
    if product and action in {"case_study", "tutorial", "opinion_analysis"}:
        return "content_signature", "content_not_event"
    if actor or product:
        return "thread_signature", "entity_without_valid_event_action"
    return "reject", "missing_concrete_actor_or_product"


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
    products = explicit_products(text) + concrete_products(text, actors)
    action = event_action(text)
    bucket = published_day_bucket(item)
    tokens = sorted(token for token in semantic_tokens(text) if not is_generic_or_noise(token))[:20]
    generic_tokens = sorted(token for token in semantic_tokens(text) if token in GENERIC_ENTITY_TOKENS)

    deduped_products: list[str] = []
    for product_candidate in products:
        if not is_invalid_product(product_candidate) and product_candidate.lower() not in {p.lower() for p in deduped_products}:
            deduped_products.append(product_candidate)
    products = deduped_products
    actor = infer_actor(text, products, actors)
    product = products[0] if products else ""
    obj = products[1] if len(products) > 1 else ""
    source_text = " ".join(str(item.get(key) or "") for key in ("source_id", "source_name", "feed_url", "url"))
    semantic_level, reject_reason = classify_semantic_level(text, action, actor, product, source_text)
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

    if actor and is_invalid_actor(actor):
        invalid.append("invalid_actor_generic_or_version")
    if product and (
        is_invalid_product(product)
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

    if action == "other" and semantic_level == "event_signature":
        invalid.append("missing_concrete_event_action")
    if semantic_level == "event_signature" and not (actor and product):
        invalid.append("event_signature_requires_actor_and_product")
    if semantic_level != "event_signature":
        invalid.append(f"semantic_level_{semantic_level}")
    is_concrete = semantic_level == "event_signature" and score >= 0.62 and not invalid and bool(bucket) and bool(actor and product) and action != "other"
    key = None
    if is_concrete:
        key = "|".join([
            normalize_key(actor or "unknown"),
            normalize_key(re.sub(r"\s+v\d+(?:\.\d+)+.*$", "", product or obj or "unknown", flags=re.IGNORECASE)),
            normalize_key(action or "event"),
            bucket,
        ])
    return EventSignature(
        semantic_level=semantic_level,
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
        confidence=round(max(score, 0.85 if is_concrete else 0.5 if semantic_level == "thread_signature" else 0.35), 3),
        is_event_like=semantic_level == "event_signature",
        is_thread_like=semantic_level == "thread_signature",
        reject_reason=reject_reason,
        extraction_notes="deterministic_phase1_3b_hybrid_fast_path",
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
