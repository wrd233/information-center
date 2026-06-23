from __future__ import annotations

from time import perf_counter
from typing import Any

from app.adapters.base import FeedFetchError
from app.utils.time import utc_now


def source_summary(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source.get("source_id"),
        "display_name": source.get("display_name"),
        "source_type": source.get("source_type"),
        "status": source.get("status"),
    }


def start_timing() -> tuple[str, float]:
    return utc_now(), perf_counter()


def finish_timing(started_at: str, started_perf: float) -> dict[str, Any]:
    elapsed_ms = int((perf_counter() - started_perf) * 1000)
    return {"started_at": started_at, "finished_at": utc_now(), "elapsed_ms": elapsed_ms}


def error_from_exception(exc: Exception) -> dict[str, Any]:
    if isinstance(exc, FeedFetchError):
        return {
            "error_type": exc.error_type,
            "message": exc.message,
            "http_status": exc.http_status,
            "retryable": exc.retryable,
            "failure_stage": exc.failure_stage,
        }
    message = str(exc) or exc.__class__.__name__
    if "already running" in message or "busy" in message:
        return {
            "error_type": "source_busy",
            "message": message,
            "http_status": None,
            "retryable": True,
            "failure_stage": "unknown",
        }
    return {
        "error_type": "unknown_error",
        "message": message,
        "http_status": None,
        "retryable": False,
        "failure_stage": "unknown",
    }


def error_from_check_result(result: Any) -> dict[str, Any] | None:
    if result.ok:
        return None
    return {
        "error_type": result.error_type or "unknown_error",
        "message": result.error or "check failed",
        "http_status": result.http_status,
        "retryable": bool(result.retryable),
        "failure_stage": result.failure_stage or "unknown",
    }
