from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter
from typing import Any

from app.config import AppConfig, settings
from app.models.schemas import BatchRunRequest, BatchSourceFilter
from app.services.check_service import CheckService
from app.services.fetch_service import FetchService
from app.services.source_service import SourceService
from app.utils.time import utc_now


TERMINAL_RUN_STATUSES = {"succeeded", "partial_success", "failed", "cancelled"}


class BatchRunService:
    def __init__(
        self,
        source_service: SourceService,
        check_service: CheckService,
        fetch_service: FetchService,
        config: AppConfig | None = None,
    ):
        self.source_service = source_service
        self.check_service = check_service
        self.fetch_service = fetch_service
        self.config = config or settings
        self._launcher = ThreadPoolExecutor(max_workers=2, thread_name_prefix="batch-run-launcher")
        self._adapter_semaphores: dict[str, threading.Semaphore] = {}
        self._adapter_guard = threading.Lock()

    def recover_incomplete(self) -> None:
        self.source_service.batch_runs.recover_incomplete()

    def create_run(self, action: str, payload: BatchRunRequest) -> dict[str, Any]:
        sources = self._snapshot_sources(action, payload)
        max_workers = self._max_workers(payload.max_concurrent_sources, len(sources))
        options = {
            "source_ids": payload.source_ids,
            "filter": payload.filter.model_dump() if payload.filter else None,
            "statuses": payload.statuses,
            "include_paused": payload.include_paused,
            "include_broken": payload.include_broken,
            "include_raw": payload.include_raw,
            "max_concurrent_sources": max_workers,
        }
        run = self.source_service.batch_runs.create(action=action, sources=sources, options=options)
        self._launcher.submit(self._execute_run, run["batch_run_id"], action, payload.include_raw, max_workers)
        return {
            "batch_run_id": run["batch_run_id"],
            "status": "running",
            "status_url": f"/api/v1/batch-runs/{run['batch_run_id']}",
            "items_url": f"/api/v1/batch-runs/{run['batch_run_id']}/items",
            "poll_interval_ms": 1000,
        }

    def get_run(self, batch_run_id: str) -> dict[str, Any] | None:
        return self.source_service.batch_runs.refresh_counts(batch_run_id)

    def list_items(self, batch_run_id: str) -> list[dict[str, Any]] | None:
        if not self.source_service.batch_runs.get(batch_run_id):
            return None
        return self.source_service.batch_runs.list_items(batch_run_id)

    def cancel(self, batch_run_id: str) -> dict[str, Any] | None:
        return self.source_service.batch_runs.request_cancel(batch_run_id)

    def _snapshot_sources(self, action: str, payload: BatchRunRequest) -> list[dict[str, Any]]:
        if payload.source_ids:
            candidates = [self.source_service.sources.get(source_id) for source_id in payload.source_ids]
            return [source for source in candidates if source and source.get("status") != "disabled"]

        source_filter = payload.filter or self._legacy_filter(action, payload)
        sources, _total, _stats = self.source_service.sources.list(
            search=source_filter.search,
            category=source_filter.category,
            include_disabled=False,
            limit=10000,
        )
        source_types = set(source_filter.source_types or [])
        statuses = set(source_filter.statuses or [])
        result = []
        for source in sources:
            if source_types and source.get("source_type") not in source_types:
                continue
            if statuses and source.get("status") not in statuses:
                continue
            result.append(source)
        return result

    def _legacy_filter(self, action: str, payload: BatchRunRequest) -> BatchSourceFilter:
        statuses = list(payload.statuses or (["active", "broken"] if action == "check" else ["active"]))
        if payload.include_broken and "broken" not in statuses:
            statuses.append("broken")
        if payload.include_paused and "paused" not in statuses:
            statuses.append("paused")
        return BatchSourceFilter(statuses=statuses)

    def _max_workers(self, requested: int | None, source_count: int) -> int:
        if source_count <= 0:
            return 1
        max_workers = requested or self.config.default_max_concurrent_sources
        return max(1, min(max_workers, self.config.hard_concurrency_limit, source_count))

    def _adapter_semaphore(self, source_type: str) -> threading.Semaphore:
        with self._adapter_guard:
            if source_type not in self._adapter_semaphores:
                limit = max(1, min(self.config.adapter_max_concurrent_sources(source_type), self.config.hard_concurrency_limit))
                self._adapter_semaphores[source_type] = threading.Semaphore(limit)
            return self._adapter_semaphores[source_type]

    def _execute_run(self, batch_run_id: str, action: str, include_raw: bool, max_workers: int) -> None:
        started_at = utc_now()
        started_perf = perf_counter()
        self.source_service.batch_runs.set_run_status(batch_run_id, "running", started_at=started_at)
        items = self.source_service.batch_runs.pending_items(batch_run_id)
        if not items:
            self.source_service.batch_runs.set_run_status(
                batch_run_id,
                "succeeded",
                finished_at=utc_now(),
                elapsed_ms=int((perf_counter() - started_perf) * 1000),
            )
            self.source_service.batch_runs.refresh_counts(batch_run_id)
            return

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=f"{action}-batch") as executor:
            futures = [executor.submit(self._execute_item, batch_run_id, action, item, include_raw) for item in items]
            for future in as_completed(futures):
                future.result()

        run = self.source_service.batch_runs.refresh_counts(batch_run_id) or {}
        if run.get("status") == "cancelling" or int(run.get("cancelled_count") or 0) > 0:
            final_status = "cancelled"
        elif int(run.get("failed_count") or 0) > 0 and int(run.get("success_count") or 0) > 0:
            final_status = "partial_success"
        elif int(run.get("failed_count") or 0) > 0:
            final_status = "failed"
        else:
            final_status = "succeeded"
        self.source_service.batch_runs.set_run_status(
            batch_run_id,
            final_status,
            finished_at=utc_now(),
            elapsed_ms=int((perf_counter() - started_perf) * 1000),
        )
        self.source_service.batch_runs.refresh_counts(batch_run_id)

    def _execute_item(self, batch_run_id: str, action: str, item: dict[str, Any], include_raw: bool) -> None:
        source_id = item["source_id"]
        if self.source_service.batch_runs.is_cancelling(batch_run_id):
            return
        current = [row for row in self.source_service.batch_runs.list_items(batch_run_id) if row["source_id"] == source_id]
        if not current or current[0].get("status") != "pending":
            return
        self.source_service.batch_runs.mark_item_running(batch_run_id, source_id)
        source = self.source_service.sources.get(source_id)
        source_type = str((source or item).get("source_type") or "native")
        semaphore = self._adapter_semaphore(source_type)
        with semaphore:
            result = self.check_service.check_one(source_id) if action == "check" else self.fetch_service.fetch_one(source_id, include_raw=include_raw)
        if result is None:
            self.source_service.batch_runs.finish_item(
                batch_run_id,
                source_id,
                status="skipped",
                updates={"error_type": "unknown_error", "error_message": "source not found", "failure_stage": "unknown"},
            )
            return
        self.source_service.batch_runs.finish_item(
            batch_run_id,
            source_id,
            status="succeeded" if result.get("ok") else "failed",
            updates=self._item_updates(action, result),
        )

    def _item_updates(self, action: str, result: dict[str, Any]) -> dict[str, Any]:
        timing = result.get("timing") or {}
        counts = result.get("counts") or {}
        error = result.get("error") or {}
        fetch_run = result.get("fetch_run") or {}
        stored_result = {key: value for key, value in result.items() if key != "raw_entries"}
        return {
            "elapsed_ms": timing.get("elapsed_ms"),
            "http_status": result.get("http_status") or error.get("http_status"),
            "content_type": result.get("content_type"),
            "error_type": error.get("error_type"),
            "error_message": error.get("message"),
            "failure_stage": error.get("failure_stage"),
            "entries_found": result.get("entries_found") or result.get("entry_count") or fetch_run.get("fetched_count") or counts.get("scanned") or 0,
            "entries_new": counts.get("new") or fetch_run.get("new_count") or 0,
            "entries_existing": counts.get("existing") or fetch_run.get("existing_count") or 0,
            "stopped_reason": fetch_run.get("stopped_reason") or ("check_failed" if action == "check" and not result.get("ok") else None),
            "result": stored_result,
        }
