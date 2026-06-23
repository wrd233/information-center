from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from app.models.schemas import CheckResult
from app.services.source_service import SourceService


class CheckService:
    def __init__(self, source_service: SourceService):
        self.source_service = source_service

    def check_one(self, source_id: str) -> CheckResult | None:
        source = self.source_service.sources.get(source_id)
        if not source:
            return None
        result = self.source_service.adapter_for(source).check(source)
        self.source_service.sources.update_check(source_id, ok=result.ok, error=result.error)
        return CheckResult(
            ok=result.ok,
            feed_url=result.feed_url,
            status="ok" if result.ok else "failed",
            entry_count=result.entry_count,
            error=result.error,
            checked_at=result.checked_at,
        )

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
                    results.append(result.model_dump())
        return {"ok": all(item["ok"] for item in results), "total": len(results), "results": results}

