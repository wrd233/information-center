from __future__ import annotations

from dataclasses import dataclass
from typing import Final


PRIORITIES: Final[tuple[str, ...]] = ("must_run", "high", "medium", "low", "suppress")
PRIORITY_ORDER: Final[dict[str, int]] = {name: index for index, name in enumerate(reversed(PRIORITIES), start=1)}

GENERIC_ENTITY_TOKENS: Final[set[str]] = {
    "about",
    "agent",
    "agents",
    "ai",
    "api",
    "app",
    "apps",
    "article",
    "available",
    "benchmark",
    "blog",
    "build",
    "case",
    "data",
    "demo",
    "feature",
    "general",
    "github",
    "gpt",
    "home",
    "idea",
    "ideas",
    "launch",
    "llm",
    "model",
    "models",
    "new",
    "open",
    "open-source",
    "paper",
    "platform",
    "preview",
    "product",
    "prompt",
    "read",
    "release",
    "research",
    "source",
    "thread",
    "today",
    "tool",
    "tools",
    "tweet",
    "update",
    "users",
    "workflow",
    "workflows",
}

PROXY_NOISE_TOKENS: Final[set[str]] = {
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
    "https",
    "http",
    "www",
    "com",
    "co",
    "link",
    "links",
    "utm_source",
    "utm_medium",
}

STOPWORDS: Final[set[str]] = {
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

EVENT_ACTION_ALIASES: Final[dict[str, str]] = {
    "announc": "release",
    "available": "availability",
    "availability": "availability",
    "benchmark": "benchmark",
    "case study": "case_study",
    "customer": "case_study",
    "dataset": "dataset",
    "funding": "funding",
    "incident": "security",
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
    "security": "security",
    "ships": "release",
    "shipped": "release",
    "update": "feature_update",
}

EVENT_ACTIONS: Final[set[str]] = set(EVENT_ACTION_ALIASES.values()) | {"event", "opinion", "other"}


@dataclass(frozen=True)
class CandidateThresholds:
    near_title_must_run: float = 0.86
    near_title_high: float = 0.72
    signature_high: float = 5.0
    signature_must_run: float = 6.0
    actor_product_high: float = 4.2
    actor_product_medium: float = 3.0
    exploratory_medium: float = 2.4
    max_low_per_item_ratio: float = 0.33


@dataclass(frozen=True)
class ClusterThresholds:
    near_duplicate_seed_confidence: float = 0.75
    related_new_info_seed_confidence: float = 0.80
    attach_confidence: float = 0.75
    tight_time_window_hours: float = 72.0
    max_seed_time_window_hours: float = 168.0


@dataclass(frozen=True)
class CardPolicyConfig:
    minimal_summary_chars: int = 420
    standard_summary_chars: int = 900
    full_summary_chars: int = 1400
    minimal_content_chars: int = 0
    standard_content_chars: int = 900
    full_content_chars: int = 2200
    deterministic_minimal_chars: int = 520
    long_item_chars: int = 1800


@dataclass(frozen=True)
class ReadinessThresholds:
    heuristic_fallback_max_rate: float = 0.10
    parse_failure_fallback_max_rate: float = 0.03
    budget_skip_fallback_max_rate: float = 0.05
    event_signature_valid_min_rate: float = 0.70
    max_pair_conflicts: int = 0
    max_skipped_must_run: int = 0
    max_db_lock_errors: int = 0
    effective_cluster_min_count: int = 1


CANDIDATE_THRESHOLDS: Final = CandidateThresholds()
CLUSTER_THRESHOLDS: Final = ClusterThresholds()
CARD_POLICY: Final = CardPolicyConfig()
READINESS_THRESHOLDS: Final = ReadinessThresholds()

STAGE_BUDGET_PROFILES: Final[dict[str, dict[str, float]]] = {
    "balanced": {
        "item_card": 0.40,
        "item_relation": 0.25,
        "item_cluster_relation": 0.25,
        "cluster_card_patch": 0.07,
        "source_profile": 0.03,
    },
    "relation_heavy": {
        "item_card": 0.32,
        "item_relation": 0.34,
        "item_cluster_relation": 0.24,
        "cluster_card_patch": 0.07,
        "source_profile": 0.03,
    },
    "cluster_heavy": {
        "item_card": 0.32,
        "item_relation": 0.22,
        "item_cluster_relation": 0.36,
        "cluster_card_patch": 0.07,
        "source_profile": 0.03,
    },
    "card_heavy": {
        "item_card": 0.55,
        "item_relation": 0.18,
        "item_cluster_relation": 0.17,
        "cluster_card_patch": 0.07,
        "source_profile": 0.03,
    },
    "phase1_2e_profile": {
        "item_card": 0.30,
        "item_relation": 0.30,
        "item_cluster_relation": 0.27,
        "cluster_card_patch": 0.08,
        "source_profile": 0.05,
    },
    "phase1_3_advisory": {
        "item_card": 0.34,
        "item_relation": 0.31,
        "item_cluster_relation": 0.25,
        "cluster_card_patch": 0.07,
        "source_profile": 0.03,
    },
}

