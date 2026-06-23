from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from typing import Any

from app.adapters.base import FeedEntry
from app.config import AppConfig, settings
from app.models.schemas import FetchRunResponse
from app.services.source_service import SourceService
from app.utils.text import excerpt, normalize_title, sha256_text
from app.utils.url_normalize import normalize_url


class FetchService:
    def __init__(self, source_service: SourceService, config: AppConfig | None = None):
        self.source_service = source_service
        self.config = config or settings
        self._locks: dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    def _lock_for(self, source_id: str) -> threading.Lock:
        with self._locks_guard:
            self._locks.setdefault(source_id, threading.Lock())
            return self._locks[source_id]

    def identity_key(self, source_id: str, entry: FeedEntry) -> str:
        normalized_url = normalize_url(entry.url)
        if normalized_url:
            return normalized_url
        if entry.guid:
            return str(entry.guid)
        published_date = (entry.published_at or "")[:10]
        fallback = f"{source_id}:{normalize_title(entry.title)}:{published_date}"
        return sha256(fallback.encode("utf-8")).hexdigest()

    def entry_record(self, source_id: str, entry: FeedEntry) -> dict[str, Any]:
        summary_excerpt = excerpt(entry.summary, self.config.summary_excerpt_max_chars)
        return {
            "source_id": source_id,
            "guid": entry.guid,
            "url": entry.url,
            "normalized_url": normalize_url(entry.url) or None,
            "identity_key": self.identity_key(source_id, entry),
            "title": entry.title,
            "published_at": entry.published_at,
            "summary_excerpt": summary_excerpt,
            "content_hash": sha256_text(entry.title or ""),
            "summary_hash": sha256_text(summary_excerpt),
        }

    def fetch_one(self, source_id: str, *, include_raw: bool = False) -> dict[str, Any] | None:
        source = self.source_service.sources.get(source_id)
        if not source:
            return None
        lock = self._lock_for(source_id)
        if not lock.acquire(blocking=False):
            raise RuntimeError(f"fetch already running for {source_id}")
        run_id = self.source_service.runs.start_fetch_run(source_id, include_raw)
        try:
            result = self.source_service.adapter_for(source).fetch(source, include_raw=include_raw)
            scanned = 0
            new_count = 0
            existing_count = 0
            existing_streak = 0
            stopped_reason = "feed_exhausted"
            raw_entries = []
            for position, entry in enumerate(result.entries):
                if scanned >= self.config.fetch_scan_limit:
                    stopped_reason = "scan_limit_reached"
                    break
                record = self.entry_record(source_id, entry)
                stored, seen_status = self.source_service.entries.upsert_seen(record)
                self.source_service.runs.add_run_entry(
                    run_id, stored["entry_id"], source_id, position, seen_status, record["identity_key"]
                )
                scanned += 1
                if seen_status == "new":
                    new_count += 1
                    existing_streak = 0
                else:
                    existing_count += 1
                    existing_streak += 1
                if include_raw and entry.raw is not None:
                    raw_entries.append(entry.raw)
                if existing_streak >= self.config.stop_after_existing_streak:
                    stopped_reason = "existing_streak_reached"
                    break
            self.source_service.sources.update_fetch_success(
                source_id, new_count=new_count, existing_count=existing_count, scanned_count=scanned
            )
            run = self.source_service.runs.finish_fetch_run(
                run_id,
                {
                    "status": "ok",
                    "fetched_count": len(result.entries),
                    "scanned_count": scanned,
                    "new_count": new_count,
                    "existing_count": existing_count,
                    "stopped_reason": stopped_reason,
                    "error_message": None,
                },
            )
            response: dict[str, Any] = {"ok": True, "fetch_run": FetchRunResponse(**run).model_dump()}
            if include_raw:
                response["raw_entries"] = raw_entries
            return response
        except Exception as exc:
            error = str(exc)
            self.source_service.sources.update_fetch_failure(source_id, error=error, threshold=self.config.health_threshold)
            run = self.source_service.runs.finish_fetch_run(
                run_id,
                {
                    "status": "failed",
                    "fetched_count": 0,
                    "scanned_count": 0,
                    "new_count": 0,
                    "existing_count": 0,
                    "stopped_reason": "fetch_failed",
                    "error_message": error,
                },
            )
            return {"ok": False, "fetch_run": FetchRunResponse(**run).model_dump(), "error": error}
        finally:
            lock.release()

    def fetch_batch(
        self,
        *,
        source_ids: list[str] | None = None,
        statuses: list[str] | None = None,
        include_raw: bool = False,
        max_concurrent_sources: int | None = None,
    ) -> dict[str, Any]:
        statuses = statuses or ["active"]
        if source_ids:
            candidates = [self.source_service.sources.get(source_id) for source_id in source_ids]
            sources = [source for source in candidates if source and source.get("status") != "disabled"]
        else:
            sources, _total, _stats = self.source_service.sources.list(status=None, include_disabled=False, limit=10000)
            sources = [source for source in sources if source.get("status") in statuses]
        max_workers = max_concurrent_sources or self.config.default_max_concurrent_sources
        max_workers = max(1, min(max_workers, self.config.hard_concurrency_limit, max(1, len(sources))))
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.fetch_one, source["source_id"], include_raw=include_raw): source["source_id"]
                for source in sources
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        return {"ok": all(item.get("ok") for item in results), "total": len(results), "results": results}

