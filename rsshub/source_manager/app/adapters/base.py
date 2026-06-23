from __future__ import annotations

from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from typing import Any

import feedparser
import httpx

from app.config import AppConfig, settings
from app.utils.text import clean_text
from app.utils.time import utc_now


@dataclass
class FeedEntry:
    guid: str | None
    url: str | None
    title: str | None
    published_at: str | None
    summary: str | None
    raw: dict[str, Any] | None = None


@dataclass
class FeedResult:
    feed_url: str
    feed_title: str
    entries: list[FeedEntry]
    raw_entries: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CheckResultData:
    ok: bool
    feed_url: str
    entry_count: int
    checked_at: str
    error: str | None = None


class BaseAdapter:
    def __init__(self, config: AppConfig | None = None):
        self.config = config or settings

    def resolve_url(self, source: dict[str, Any]) -> str:
        raise NotImplementedError

    def check(self, source: dict[str, Any]) -> CheckResultData:
        feed_url = self.resolve_url(source)
        try:
            result = self.fetch(source, include_raw=False)
            if not result.entries:
                raise ValueError("feed parsed but contains no entries")
            return CheckResultData(ok=True, feed_url=feed_url, entry_count=len(result.entries), checked_at=utc_now())
        except Exception as exc:
            return CheckResultData(ok=False, feed_url=feed_url, entry_count=0, checked_at=utc_now(), error=str(exc))

    def fetch(self, source: dict[str, Any], include_raw: bool = False) -> FeedResult:
        feed_url = self.resolve_url(source)
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            response = client.get(
                feed_url,
                headers={
                    "user-agent": "rss-source-manager/0.1 (+local)",
                    "accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
                },
            )
            response.raise_for_status()
        parsed = feedparser.parse(response.content)
        if parsed.bozo and not parsed.entries:
            raise ValueError(f"failed to parse feed: {parsed.bozo_exception}")
        feed_title = clean_text(parsed.feed.get("title")) or source.get("display_name") or feed_url
        entries = [entry_from_feedparser(item, include_raw=include_raw) for item in parsed.entries]
        return FeedResult(feed_url=feed_url, feed_title=feed_title, entries=entries)


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
        return str(value)


def entry_from_feedparser(entry: dict[str, Any], *, include_raw: bool) -> FeedEntry:
    summary = entry.get("summary") or entry.get("description") or first_content_value(entry.get("content"))
    return FeedEntry(
        guid=entry.get("id") or entry.get("guid"),
        url=entry.get("link"),
        title=entry.get("title"),
        published_at=parse_entry_datetime(entry),
        summary=summary,
        raw=dict(entry) if include_raw else None,
    )

