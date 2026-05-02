from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG: dict[str, Any] = {
    "llm": {
        "provider": "deepseek",
        "base_url": "https://api.deepseek.com",
        "api_key_env": "CONTENT_INBOX_DEEPSEEK_API_KEY",
        "model": "deepseek-v4-flash",
        "temperature": 0.2,
        "max_tokens": 1200,
        "timeout_seconds": 60,
        "prompt_version": "screening_v1",
    },
    "screening": {
        "enabled": True,
        "max_input_chars": 4000,
        "categories": [
            "AI前沿",
            "AI工具",
            "信息管理",
            "技术学习",
            "工程实践",
            "社会观察",
            "人生经验",
            "商业产品",
            "娱乐内容",
            "新闻资讯",
            "低质营销",
            "其他",
        ],
    },
    "score_policy": {
        "ignore_below_value_score": 2,
        "read_min_value_score": 4,
        "read_min_personal_relevance": 3,
        "save_min_value_score": 4,
        "save_min_personal_relevance": 4,
        "transcribe_min_value_score": 4,
        "transcribe_min_personal_relevance": 3,
        "manual_review_confidence_below": 0.6,
    },
    "embedding": {
        "enabled": True,
        "provider": "yunwu",
        "base_url": "https://yunwu.apifox.cn/v1",
        "api_key_env": "CONTENT_INBOX_EMBEDDING_API_KEY",
        "model": "text-embedding-3-small",
        "dimensions": 1536,
        "timeout_seconds": 60,
        "max_input_chars": 3000,
    },
    "clustering": {
        "enabled": True,
        "top_k": 5,
        "new_event_threshold": 0.85,
        "duplicate_threshold": 0.97,
        "high_overlap_entity_ratio": 0.6,
        "cluster_min_value_score": 3,
        "cluster_min_personal_relevance": 3,
        "cluster_vector_strategy": "summary_embedding",
        "archive_after_days": 7,
    },
    "notification": {
        "full_push_for_new_event": True,
        "incremental_push_when_has_new_info": True,
        "silent_duplicates": True,
        "include_silent_in_default_inbox": False,
        "manual_review_when_uncertain": True,
    },
}


def load_yaml_config(base_dir: Path) -> dict[str, Any]:
    path = Path(os.getenv("CONTENT_INBOX_CONFIG", base_dir / "config" / "content_inbox.yaml"))
    config = copy.deepcopy(DEFAULT_CONFIG)
    if path.exists():
        with path.open(encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
        deep_merge(config, loaded)
    apply_env_overrides(config)
    return config


def deep_merge(target: dict[str, Any], source: dict[str, Any]) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_merge(target[key], value)
        else:
            target[key] = value


def apply_env_overrides(config: dict[str, Any]) -> None:
    llm = config["llm"]
    llm["base_url"] = os.getenv(
        "CONTENT_INBOX_OPENAI_BASE_URL",
        os.getenv("CONTENT_INBOX_DEEPSEEK_BASE_URL", llm["base_url"]),
    )
    llm["model"] = os.getenv(
        "CONTENT_INBOX_OPENAI_MODEL",
        os.getenv("CONTENT_INBOX_DEEPSEEK_MODEL", llm["model"]),
    )
    llm["timeout_seconds"] = float(
        os.getenv("CONTENT_INBOX_OPENAI_TIMEOUT", str(llm["timeout_seconds"]))
    )

    embedding = config["embedding"]
    embedding["base_url"] = os.getenv(
        "CONTENT_INBOX_EMBEDDING_BASE_URL", embedding["base_url"]
    )
    embedding["model"] = os.getenv("CONTENT_INBOX_EMBEDDING_MODEL", embedding["model"])
    embedding["timeout_seconds"] = float(
        os.getenv("CONTENT_INBOX_EMBEDDING_TIMEOUT", str(embedding["timeout_seconds"]))
    )

