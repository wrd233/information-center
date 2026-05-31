from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from html import unescape
from urllib.parse import parse_qsl, urldefrag, urlencode, urlparse, urlunparse


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean_text(value: str | None) -> str | None:
    if not value:
        return None
    text = unescape(TAG_RE.sub(" ", value))
    text = SPACE_RE.sub(" ", text).strip()
    return text or None


_TRACKING_PARAMS = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "fbclid",
        "gclid",
        "igshid",
        "mc_cid",
        "mc_eid",
        "ref",
        "ref_src",
        "source",
        "spm",
    }
)


def _clean_query(query: str) -> str:
    if not query:
        return query
    params = parse_qsl(query, keep_blank_values=True)
    cleaned = [(key, value) for key, value in params if key.lower() not in _TRACKING_PARAMS and not key.lower().startswith("utm_")]
    if not cleaned:
        return ""
    return urlencode(sorted(cleaned), doseq=True)


def normalize_url(value: str | None) -> str | None:
    if not value:
        return None
    url, _fragment = urldefrag(value.strip())
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    scheme = parsed.scheme.lower()
    if scheme in {"http", "https"}:
        scheme = "https"
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    query = _clean_query(parsed.query)
    return urlunparse((scheme, netloc, path, "", query, ""))


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def truncate(value: str | None, max_chars: int) -> str | None:
    if not value:
        return value
    value = value.strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 1].rstrip() + "…"
