from __future__ import annotations

import os
import threading


class _Profiler:
    """Thread-local timing accumulator. Enabled via CONTENT_INBOX_PROFILE=1 or per-request flag."""

    def __init__(self) -> None:
        self._local = threading.local()

    @property
    def enabled(self) -> bool:
        if os.getenv("CONTENT_INBOX_PROFILE") == "1":
            return True
        return getattr(self._local, "request_enabled", False)

    def enable_for_request(self) -> None:
        self._local.request_enabled = True

    def _ensure_store(self) -> dict[str, float]:
        if not hasattr(self._local, "store"):
            self._local.store: dict[str, float] = {}
        return self._local.store

    def record(self, key: str, value: float) -> None:
        if not self.enabled:
            return
        store = self._ensure_store()
        store[key] = round(store.get(key, 0.0) + value, 3)

    def collect(self) -> dict[str, float]:
        if not self.enabled:
            return {}
        store = self._ensure_store()
        return dict(store)

    def reset(self) -> None:
        self._local.store = {}


profiler = _Profiler()
