from __future__ import annotations

import socket
import urllib.error
from typing import Any

from fastapi.responses import JSONResponse


RETRYABLE_ERRORS = {
    "rss_fetch_timeout",
    "rss_fetch_http_error",
    "rss_fetch_connection_error",
    "rss_fetch_rate_limited",
    "rss_fetch_server_error",
    "content_processing_error",
    "storage_error",
    "dedupe_error",
    "migration_error",
    "api_unreachable",
    "unknown_error",
}


def retryable_for(error_code: str) -> bool:
    return error_code in RETRYABLE_ERRORS


def error_payload(
    error_code: str,
    message: str,
    *,
    source_id: str | None = None,
    feed_url: str | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "error": {
            "error_code": error_code,
            "message": message,
            "retryable": retryable_for(error_code),
            "source_id": source_id,
            "feed_url": feed_url,
        },
    }


def error_response(
    error_code: str,
    message: str,
    *,
    status_code: int = 400,
    source_id: str | None = None,
    feed_url: str | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=error_payload(error_code, message, source_id=source_id, feed_url=feed_url),
    )


def classify_exception(exc: Exception) -> tuple[str, str]:
    message = str(exc)
    if isinstance(exc, TimeoutError) or isinstance(exc, socket.timeout):
        return "rss_fetch_timeout", message
    if isinstance(exc, urllib.error.HTTPError):
        if exc.code == 404:
            return "rss_fetch_not_found", message
        if exc.code == 429:
            return "rss_fetch_rate_limited", message
        if exc.code >= 500:
            return "rss_fetch_server_error", message
        return "rss_fetch_http_error", message
    if isinstance(exc, urllib.error.URLError):
        reason = str(getattr(exc, "reason", exc))
        lowered = reason.lower()
        if "timed out" in lowered or "timeout" in lowered:
            return "rss_fetch_timeout", reason
        return "rss_fetch_connection_error", reason
    lowered = message.lower()
    if "failed to parse feed" in lowered or "not well-formed" in lowered or "syntax error" in lowered:
        return "rss_parse_error", message
    if "empty feed" in lowered:
        return "rss_empty_feed", message
    if "content processing" in lowered:
        return "content_processing_error", message
    if "dedupe" in lowered:
        return "dedupe_error", message
    if "llm" in lowered or "screening" in lowered:
        return "llm_error", message
    if "embedding" in lowered:
        return "embedding_error", message
    if "sqlite" in lowered or "database" in lowered:
        return "storage_error", message
    return "unknown_error", message
