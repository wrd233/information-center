from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "spm",
    "from",
    "share_source",
    "share_token",
}


def normalize_url(url: str | None) -> str:
    if not url:
        return ""
    text = url.strip()
    if not text:
        return ""
    parts = urlsplit(text)
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    query = urlencode([(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k not in TRACKING_PARAMS])
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, query, ""))


def route_from_rsshub_url(url: str, base_urls: list[str]) -> str | None:
    normalized = normalize_url(url)
    for base in base_urls:
        base_norm = normalize_url(base).rstrip("/")
        if normalized.startswith(base_norm + "/"):
            return normalized[len(base_norm) :]
    if "rsshub" in normalized:
        parts = urlsplit(normalized)
        return parts.path or None
    return None

