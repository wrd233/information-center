from __future__ import annotations

import json
import random
import socket
import time
import urllib.error
import urllib.request

from app.config import settings
from app.profiler import profiler
from app.utils import truncate


_EMBEDDING_RETRY_MAX_ATTEMPTS = 3
_EMBEDDING_RETRY_BASE_DELAY = 2.0
_EMBEDDING_RETRY_MAX_DELAY = 30.0


def _is_retryable_embedding_error(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in (429, 503)
    if isinstance(exc, (urllib.error.URLError, socket.timeout)):
        return True
    return False


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
    t0 = time.monotonic()
    timeout = float(settings.embedding.get("timeout_seconds", 60))
    api_url = f"{settings.embedding['base_url'].rstrip('/')}/embeddings"

    last_exc: Exception | None = None
    for attempt in range(1, _EMBEDDING_RETRY_MAX_ATTEMPTS + 1):
        try:
            req = urllib.request.Request(
                api_url,
                data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                headers={
                    "content-type": "application/json",
                    "authorization": f"Bearer {api_key}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
                content_type = response.headers.get("content-type", "")
                if "json" not in content_type.lower():
                    raise RuntimeError(
                        f"embedding API returned non-JSON content-type {content_type}: {raw[:200]}"
                    )
                payload = json.loads(raw)
                break
        except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout) as exc:
            last_exc = exc
            if attempt < _EMBEDDING_RETRY_MAX_ATTEMPTS and _is_retryable_embedding_error(exc):
                delay = min(_EMBEDDING_RETRY_BASE_DELAY * (2 ** (attempt - 1)), _EMBEDDING_RETRY_MAX_DELAY)
                jitter = random.uniform(0, 0.1 * delay)
                total_delay = delay + jitter
                code = getattr(exc, "code", None)
                print(
                    f"[EMBEDDING_RETRY] attempt {attempt}/{_EMBEDDING_RETRY_MAX_ATTEMPTS} "
                    f"after {code or type(exc).__name__}, "
                    f"sleeping {total_delay:.1f}s",
                    flush=True,
                )
                time.sleep(total_delay)
                continue
            if isinstance(last_exc, urllib.error.HTTPError):
                detail = last_exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"embedding API returned {last_exc.code}: {detail}") from last_exc
            raise
    profiler.record("embedding_seconds", time.monotonic() - t0)
    return [float(value) for value in payload["data"][0]["embedding"]]
