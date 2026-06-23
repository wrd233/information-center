from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.services.result_envelope import error_from_check_result, finish_timing, source_summary, start_timing
from app.services.source_service import SourceService


class CheckService:
    def __init__(self, source_service: SourceService):
        self.source_service = source_service

    def check_one(self, source_id: str) -> dict[str, Any] | None:
        source = self.source_service.sources.get(source_id)
        if not source:
            return None
        started_at, started_perf = start_timing()
        with self.source_service.source_operation(source_id) as acquired:
            if not acquired:
                timing = finish_timing(started_at, started_perf)
                error = {
                    "error_type": "source_busy",
                    "message": f"check/fetch already running for {source_id}",
                    "http_status": None,
                    "retryable": True,
                    "failure_stage": "unknown",
                }
                return {
                    "ok": False,
                    "source": source_summary(source),
                    "timing": timing,
                    "counts": {"scanned": 0, "new": 0, "existing": 0, "failed": 1},
                    "result": None,
                    "error": error,
                    "feed_url": self.source_service.resolved_url(source),
                    "status": "failed",
                    "entry_count": 0,
                    "checked_at": timing["finished_at"],
                }
            result = self.source_service.adapter_for(source).check(source)
        self.source_service.sources.update_check(source_id, ok=result.ok, error=result.error)
        timing = finish_timing(started_at, started_perf)
        error = error_from_check_result(result)
        return {
            "ok": result.ok,
            "source": source_summary(source),
            "timing": timing,
            "counts": {"scanned": result.entry_count, "new": 0, "existing": 0, "failed": 0 if result.ok else 1},
            "result": {"feed_url": result.feed_url, "entry_count": result.entry_count} if result.ok else None,
            "error": error,
            "feed_url": result.feed_url,
            "status": "ok" if result.ok else "failed",
            "entry_count": result.entry_count,
            "checked_at": result.checked_at,
        }

    def check_batch(self, statuses: list[str] | None = None, source_ids: list[str] | None = None) -> dict:
        statuses = statuses or ["active", "broken"]
        if source_ids:
            candidates = [self.source_service.sources.get(source_id) for source_id in source_ids]
            sources = [source for source in candidates if source and source.get("status") != "disabled"]
        else:
            sources, _total, _stats = self.source_service.sources.list(status=None, include_disabled=False, limit=10000)
            sources = [source for source in sources if source.get("status") in statuses]
        results = []
        with ThreadPoolExecutor(max_workers=min(7, max(1, len(sources)))) as executor:
            futures = {executor.submit(self.check_one, source["source_id"]): source["source_id"] for source in sources}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        return {"ok": all(item["ok"] for item in results), "total": len(results), "results": results}
