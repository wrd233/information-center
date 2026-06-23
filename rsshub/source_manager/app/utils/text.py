from __future__ import annotations

import hashlib
import re
from html import unescape


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def clean_text(value: object | None) -> str:
    if value is None:
        return ""
    text = unescape(str(value))
    text = TAG_RE.sub(" ", text)
    return SPACE_RE.sub(" ", text).strip()


def excerpt(value: object | None, max_chars: int) -> str:
    text = clean_text(value)
    return text[:max_chars]


def sha256_text(value: object | None) -> str:
    return hashlib.sha256(clean_text(value).encode("utf-8")).hexdigest()


def normalize_title(value: object | None) -> str:
    return clean_text(value).lower()

