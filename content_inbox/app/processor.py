from __future__ import annotations

import threading
import time
from typing import Any

from app.config import settings
from app.clusterer import cluster_content
from app.models import ClusteringResult, ContentAnalyzeRequest, NormalizedContent, ProcessResult
from app.profiler import profiler
from app.screener import gated_screening, screen_content
from app.storage import InboxStore
from app.utils import clean_text, normalize_url, stable_hash, truncate

CONTENT_STATE_LOCK = threading.RLock()


def normalize_content(payload: ContentAnalyzeRequest) -> NormalizedContent:
    title = clean_text(payload.title) or clean_text(payload.summary) or payload.url or "Untitled"
    content_text = clean_text(payload.content_text)
    summary = clean_text(payload.summary)
    return NormalizedContent(
        title=truncate(title, 500) or "Untitled",
        url=normalize_url(payload.url),
        source_name=clean_text(payload.source_name) or "Unknown",
        source_category=clean_text(payload.source_category),
        content_type=(payload.content_type or "unknown").strip() or "unknown",
        published_at=payload.published_at,
        author=clean_text(payload.author),
        summary=truncate(summary, 2000),
        content_text=truncate(content_text, settings.max_content_chars),
        guid=clean_text(payload.guid),
    )


def build_dedupe_key(content: NormalizedContent) -> str:
    if content.url:
        return stable_hash(f"url:{content.url}")
    if content.guid:
        return stable_hash(f"guid:{content.source_name}:{content.guid}")
    return stable_hash(f"title-source:{content.source_name}:{content.title.lower()}")


def pre_llm_gate(normalized: NormalizedContent) -> tuple[bool, str, list[str]]:
    title = (normalized.title or "").strip()
    summary = (normalized.summary or "").strip()
    content_text = (normalized.content_text or "").strip()
    combined_text = f"{title}\n{summary}\n{content_text}".strip()

    if not combined_text:
        return False, "empty_content", []

    if len(combined_text) < 20:
        return False, "too_short", []

    hints = _collect_hints(title)
    return True, "", hints


def _collect_hints(title: str) -> list[str]:
    hints = []
    title_lower = title.lower()
    if any(kw in title_lower for kw in ["限时优惠", "免费领取", "扫码", "加群", "到手价", "促销", "秒杀"]):
        hints.append("possible_ad")
    if any(kw in title_lower for kw in ["招聘", "求职", "内推", "急招", "招人", "校招", "社招"]):
        hints.append("possible_job")
    if any(kw in title_lower for kw in ["周报", "日报", "月报", "季报", "简报", "newsletter"]):
        hints.append("possible_digest")
    if any(kw in title_lower for kw in ["导航", "目录", "链接汇总", "资源汇总"]):
        hints.append("possible_navigation")
    return hints


def process_content(
    store: InboxStore, payload: ContentAnalyzeRequest, raw: dict[str, Any] | None = None
) -> ProcessResult:
    normalized = normalize_content(payload)
    dedupe_key = build_dedupe_key(normalized)
    existing = store.get_by_dedupe_key(dedupe_key)
    if existing:
        updated = store.mark_seen(existing["item_id"])
        return ProcessResult(
            item_id=updated["item_id"],
            is_duplicate=True,
            normalized=NormalizedContent(
                title=updated["title"],
                url=updated["url"],
                source_name=updated["source_name"],
                source_category=updated["source_category"],
                content_type=updated["content_type"],
                published_at=updated["published_at"],
                author=updated["author"],
                summary=updated["summary"],
                content_text=updated["content_text"],
                guid=updated["guid"],
            ),
            screening=updated["screening"],
            clustering=updated.get("clustering") or ClusteringResult(),
            notification_decision=(updated.get("clustering") or {}).get(
                "notification_decision", "manual_review"
            ),
            cluster_relation=(updated.get("clustering") or {}).get("cluster_relation", "disabled"),
            incremental_summary=(updated.get("clustering") or {}).get("incremental_summary", ""),
        )

    should_call, gate_reason, gate_hints = pre_llm_gate(normalized)
    if not should_call:
        if not payload.screen:
            screening = screen_content(normalized, use_ai=False)
        else:
            screening = gated_screening(normalized, gate_reason, gate_hints)
    else:
        screening = screen_content(normalized, use_ai=payload.screen)
        if gate_hints:
            screening.gate_hints = gate_hints

    inserted = store.insert(dedupe_key, normalized, screening, raw=raw)
    clustering = cluster_content(
        store,
        item_id=inserted["item_id"],
        normalized=normalized,
        screening=screening,
    )
    updated = store.update_item_clustering(inserted["item_id"], clustering)
    return ProcessResult(
        item_id=updated["item_id"],
        is_duplicate=False,
        normalized=normalized,
        screening=screening,
        clustering=clustering,
        notification_decision=clustering.notification_decision,
        cluster_relation=clustering.cluster_relation,
        incremental_summary=clustering.incremental_summary,
    )


def process_content_thread_safe(
    store: InboxStore, payload: ContentAnalyzeRequest, raw: dict[str, Any] | None = None
) -> ProcessResult:
    t_wait = time.monotonic()
    with CONTENT_STATE_LOCK:
        t_acquired = time.monotonic()
        result = process_content(store, payload, raw=raw)
        t_done = time.monotonic()
        profiler.record("lock_wait_seconds", t_acquired - t_wait)
        profiler.record("lock_held_seconds", t_done - t_acquired)
        return result
