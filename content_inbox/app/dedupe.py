from __future__ import annotations

from datetime import datetime
from urllib.parse import urlparse, urlunparse

from app.models import NormalizedContent
from app.utils import stable_hash


def is_http_url(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def canonicalize_url_for_dedupe(url: str, *, canonicalize_http_https: bool = False) -> str:
    if not canonicalize_http_https:
        return url
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return urlunparse(parsed._replace(scheme="https"))
    return url


def source_key(content: NormalizedContent) -> str:
    return content.source_id or content.feed_url or content.source_name


def normalized_title(title: str) -> str:
    return " ".join(title.lower().split())


def published_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return value[:10] if len(value) >= 10 else None


def content_hash(content: NormalizedContent) -> str | None:
    text = content.content_text or content.summary
    if not text:
        return None
    return stable_hash(text)[:16]


def build_dedupe_key(content: NormalizedContent, *, canonicalize_http_https: bool = False) -> str:
    if is_http_url(content.url):
        url = canonicalize_url_for_dedupe(content.url or "", canonicalize_http_https=canonicalize_http_https)
        return stable_hash(f"url:{url}")
    skey = source_key(content)
    if content.guid:
        return stable_hash(f"guid:{skey}:{content.guid}")
    title = normalized_title(content.title)
    date = published_date(content.published_at)
    if date:
        return stable_hash(f"title-date:{skey}:{title}:{date}")
    chash = content_hash(content)
    if chash:
        return stable_hash(f"title-content:{skey}:{title}:{chash}")
    return stable_hash(f"title:{skey}:{title}")
