from __future__ import annotations

from typing import Any
from urllib.parse import urlparse


def is_http_url(value: str | None) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def real_entry_link(entry: dict[str, Any]) -> str | None:
    link = entry.get("link")
    if is_http_url(link):
        return link
    links = entry.get("links")
    if isinstance(links, list):
        for candidate in links:
            if isinstance(candidate, dict) and is_http_url(candidate.get("href")):
                return candidate["href"]
    return None
