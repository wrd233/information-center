from __future__ import annotations

import time
from email.utils import parsedate_to_datetime
from typing import Any
import urllib.request

import feedparser

from app.config import settings
from app.models import ContentAnalyzeRequest
from app.profiler import profiler
from app.utils import clean_text


def fetch_feed(feed_url: str) -> bytes:
    req = urllib.request.Request(
        feed_url,
        headers={
            "user-agent": "content-inbox/0.1 (+local)",
            "accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        },
    )
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=settings.request_timeout_seconds) as response:
        raw = response.read()
    profiler.record("fetch_feed_seconds", time.monotonic() - t0)
    return raw


def parse_feed(
    feed_url: str,
    source_id: str | None = None,
    source_name: str | None = None,
    source_category: str | None = None,
    limit: int | None = None,
) -> tuple[dict[str, Any], list[ContentAnalyzeRequest]]:
    parsed = feedparser.parse(fetch_feed(feed_url))
    if parsed.bozo and not parsed.entries:
        raise ValueError(f"failed to parse feed: {parsed.bozo_exception}")

    feed_title = clean_text(parsed.feed.get("title")) or source_name or feed_url
    items: list[ContentAnalyzeRequest] = []
    for entry in parsed.entries[: limit or None]:
        summary = (
            entry.get("summary")
            or entry.get("description")
            or first_content_value(entry.get("content"))
        )
        items.append(
            ContentAnalyzeRequest(
                url=entry.get("link"),
                source_id=source_id,
                feed_url=feed_url,
                title=entry.get("title"),
                source_name=source_name or feed_title,
                source_category=source_category,
                content_type="article",
                summary=summary,
                content_text=first_content_value(entry.get("content")) or summary,
                published_at=parse_entry_datetime(entry),
                author=entry.get("author"),
                guid=entry.get("id") or entry.get("guid"),
                screen=True,
            )
        )
    meta = {
        "feed_url": feed_url,
        "source_name": source_name or feed_title,
        "feed_title": feed_title,
        "total_items_found": len(parsed.entries),
    }
    return meta, items


def first_content_value(content: Any) -> str | None:
    if isinstance(content, list) and content:
        first = content[0]
        if isinstance(first, dict):
            return first.get("value")
    return None


def parse_entry_datetime(entry: dict[str, Any]) -> str | None:
    value = entry.get("published") or entry.get("updated") or entry.get("created")
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError, IndexError, OverflowError):
        return value
