from __future__ import annotations

from typing import Any

from app.config import settings
from app.models import ContentAnalyzeRequest, NormalizedContent, ProcessResult
from app.screener import screen_content
from app.storage import InboxStore
from app.utils import clean_text, normalize_url, stable_hash, truncate


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
        )

    screening = screen_content(normalized, use_ai=payload.screen)
    inserted = store.insert(dedupe_key, normalized, screening, raw=raw)
    return ProcessResult(
        item_id=inserted["item_id"],
        is_duplicate=False,
        normalized=normalized,
        screening=screening,
    )

