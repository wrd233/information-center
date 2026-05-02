from __future__ import annotations

import json
import urllib.error
import urllib.request

from app.config import settings
from app.utils import truncate


def embed_text(text: str) -> list[float]:
    if not settings.embedding.get("enabled", True):
        raise RuntimeError("embedding is disabled")
    api_key = settings.embedding_api_key()
    if not api_key:
        raise RuntimeError(
            f"embedding requires API key env {settings.embedding.get('api_key_env')}"
        )
    text = truncate(text, int(settings.embedding.get("max_input_chars", 3000))) or ""
    if not text.strip():
        raise RuntimeError("embedding_text is empty")
    body = {
        "model": settings.embedding["model"],
        "input": text,
    }
    req = urllib.request.Request(
        f"{settings.embedding['base_url'].rstrip('/')}/embeddings",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(
            req, timeout=float(settings.embedding.get("timeout_seconds", 60))
        ) as response:
            raw = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("content-type", "")
            if "json" not in content_type.lower():
                raise RuntimeError(
                    f"embedding API returned non-JSON content-type {content_type}: {raw[:200]}"
                )
            payload = json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"embedding API returned {exc.code}: {detail}") from exc
    return [float(value) for value in payload["data"][0]["embedding"]]
