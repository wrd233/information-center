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
    http_status: int | None = None
    content_type: str | None = None


@dataclass
class CheckResultData:
    ok: bool
    feed_url: str
    entry_count: int
    checked_at: str
    error: str | None = None
    error_type: str | None = None
    http_status: int | None = None
    content_type: str | None = None
    failure_stage: str | None = None
    retryable: bool = False


class FeedFetchError(Exception):
    def __init__(
        self,
        message: str,
        *,
        error_type: str = "unknown_error",
        failure_stage: str = "unknown",
        http_status: int | None = None,
        content_type: str | None = None,
        retryable: bool = False,
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.failure_stage = failure_stage
        self.http_status = http_status
        self.content_type = content_type
        self.retryable = retryable


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
                raise FeedFetchError(
                    "feed parsed but contains no entries",
                    error_type="empty_feed",
                    failure_stage="parse_feed",
                    http_status=result.http_status,
                    content_type=result.content_type,
                )
            return CheckResultData(
                ok=True,
                feed_url=feed_url,
                entry_count=len(result.entries),
                checked_at=utc_now(),
                http_status=result.http_status,
                content_type=result.content_type,
            )
        except FeedFetchError as exc:
            return CheckResultData(
                ok=False,
                feed_url=feed_url,
                entry_count=0,
                checked_at=utc_now(),
                error=exc.message,
                error_type=exc.error_type,
                http_status=exc.http_status,
                content_type=exc.content_type,
                failure_stage=exc.failure_stage,
                retryable=exc.retryable,
            )
        except Exception as exc:
            return CheckResultData(
                ok=False,
                feed_url=feed_url,
                entry_count=0,
                checked_at=utc_now(),
                error=str(exc),
                error_type="unknown_error",
                failure_stage="unknown",
            )

    def fetch(self, source: dict[str, Any], include_raw: bool = False) -> FeedResult:
        try:
            feed_url = self.resolve_url(source)
        except Exception as exc:
            raise FeedFetchError(str(exc), error_type="unknown_error", failure_stage="resolve_url") from exc
        source_type = str(source.get("source_type") or "")
        timeout = self.config.timeout_config(source_type)
        request_timeout = httpx.Timeout(
            timeout["total_seconds"],
            connect=timeout["connect_seconds"],
            read=timeout["read_seconds"],
            write=timeout["read_seconds"],
            pool=timeout["connect_seconds"],
        )
        try:
            with httpx.Client(timeout=request_timeout, follow_redirects=True) as client:
                response = client.get(
                    feed_url,
                    headers={
                        "user-agent": "rss-source-manager/0.1 (+local)",
                        "accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
                    },
                )
                response.raise_for_status()
        except httpx.ConnectTimeout as exc:
            raise FeedFetchError(str(exc), error_type="connect_timeout", failure_stage="connect", retryable=True) from exc
        except httpx.ReadTimeout as exc:
            raise FeedFetchError(str(exc), error_type="read_timeout", failure_stage="read", retryable=True) from exc
        except httpx.TimeoutException as exc:
            raise FeedFetchError(str(exc), error_type="total_timeout", failure_stage="read", retryable=True) from exc
        except httpx.HTTPStatusError as exc:
            content_type = exc.response.headers.get("content-type")
            error_type = "rsshub_route_error" if source_type == "rsshub" else "http_error"
            raise FeedFetchError(
                f"HTTP {exc.response.status_code}",
                error_type=error_type,
                failure_stage="http_status",
                http_status=exc.response.status_code,
                content_type=content_type,
                retryable=exc.response.status_code >= 500,
            ) from exc
        except httpx.ConnectError as exc:
            message = str(exc)
            error_type = "dns_error" if "Name or service not known" in message or "nodename" in message else "connection_error"
            raise FeedFetchError(message, error_type=error_type, failure_stage="connect", retryable=True) from exc
        except httpx.RequestError as exc:
            raise FeedFetchError(str(exc), error_type="connection_error", failure_stage="connect", retryable=True) from exc
        parsed = feedparser.parse(response.content)
        if parsed.bozo and not parsed.entries:
            raise FeedFetchError(
                f"failed to parse feed: {parsed.bozo_exception}",
                error_type="parse_error",
                failure_stage="parse_feed",
                http_status=response.status_code,
                content_type=response.headers.get("content-type"),
            )
        feed_title = clean_text(parsed.feed.get("title")) or source.get("display_name") or feed_url
        entries = [entry_from_feedparser(item, include_raw=include_raw) for item in parsed.entries]
        return FeedResult(
            feed_url=feed_url,
            feed_title=feed_title,
            entries=entries,
            http_status=response.status_code,
            content_type=response.headers.get("content-type"),
        )


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
