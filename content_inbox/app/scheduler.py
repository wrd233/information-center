from __future__ import annotations

import threading
import time
from datetime import datetime, time as dt_time, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from app.config import settings
from app.inbox_run import PostProcessCallback, start_inbox_run
from app.storage import InboxStore
from app.utils import utc_now


SCHEDULER_META_KEY = "inbox_loop_scheduler_state"


def scheduler_timezone() -> ZoneInfo:
    try:
        return ZoneInfo(settings.daily_run_tz)
    except Exception:
        return ZoneInfo("Asia/Shanghai")


def parse_daily_time(value: str | None = None) -> dt_time:
    raw = value or settings.daily_run_time or "06:00"
    hour_text, minute_text = raw.split(":", 1)
    return dt_time(hour=int(hour_text), minute=int(minute_text[:2]))


def next_daily_run(now: datetime | None = None) -> datetime:
    tz = scheduler_timezone()
    local_now = (now or datetime.now(timezone.utc)).astimezone(tz)
    daily = parse_daily_time()
    candidate = local_now.replace(hour=daily.hour, minute=daily.minute, second=0, microsecond=0)
    if candidate <= local_now:
        candidate = candidate + timedelta(days=1)
    return candidate


def local_day_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    tz = scheduler_timezone()
    local_now = (now or datetime.now(timezone.utc)).astimezone(tz)
    start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return start.astimezone(timezone.utc), end.astimezone(timezone.utc)


def has_successful_full_run_today(store: InboxStore, now: datetime | None = None) -> bool:
    start, end = local_day_window(now)
    with store.connect() as conn:
        row = conn.execute(
            """
            SELECT 1
            FROM rss_ingest_runs
            WHERE source_mode = 'registry_full'
              AND trigger_type IN ('manual', 'scheduled')
              AND status IN ('success', 'partial_success')
              AND finished_at >= ?
              AND finished_at < ?
            LIMIT 1
            """,
            (start.isoformat(), end.isoformat()),
        ).fetchone()
    return row is not None


def should_recover_missed_run(store: InboxStore, now: datetime | None = None) -> bool:
    if not settings.scheduler_enabled or not settings.daily_run_recover_missed:
        return False
    tz = scheduler_timezone()
    local_now = (now or datetime.now(timezone.utc)).astimezone(tz)
    daily = parse_daily_time()
    scheduled_today = local_now.replace(hour=daily.hour, minute=daily.minute, second=0, microsecond=0)
    if local_now < scheduled_today:
        return False
    return not has_successful_full_run_today(store, now)


def scheduler_state(store: InboxStore) -> dict[str, Any]:
    state = store.get_metadata_json(SCHEDULER_META_KEY, {}) or {}
    return {
        "enabled": bool(settings.scheduler_enabled),
        "daily_time": settings.daily_run_time,
        "timezone": settings.daily_run_tz,
        "recover_missed": bool(settings.daily_run_recover_missed),
        "next_run": next_daily_run().isoformat(),
        "last_attempt_at": state.get("last_attempt_at"),
        "last_run_id": state.get("last_run_id"),
        "last_status": state.get("last_status"),
        "last_error": state.get("last_error"),
    }


def record_scheduler_attempt(
    store: InboxStore,
    *,
    status: str,
    run_id: str | None = None,
    error: str | None = None,
) -> None:
    store.set_metadata_value(
        SCHEDULER_META_KEY,
        {
            "last_attempt_at": utc_now(),
            "last_run_id": run_id,
            "last_status": status,
            "last_error": error,
        },
    )


class InboxLoopScheduler:
    def __init__(
        self,
        store: InboxStore,
        *,
        post_process: PostProcessCallback | None = None,
        poll_seconds: int = 60,
    ) -> None:
        self.store = store
        self.post_process = post_process
        self.poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if not settings.scheduler_enabled:
            record_scheduler_attempt(self.store, status="disabled")
            return
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._loop, name="inbox-loop-scheduler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def _loop(self) -> None:
        self._attempt_recovery()
        while not self._stop.is_set():
            now = datetime.now(timezone.utc)
            if now >= next_daily_run(now) - timedelta(seconds=self.poll_seconds):
                self._trigger_scheduled()
            self._stop.wait(self.poll_seconds)

    def _attempt_recovery(self) -> None:
        if should_recover_missed_run(self.store):
            self._trigger_scheduled(recovery=True)
        else:
            record_scheduler_attempt(self.store, status="idle")

    def _trigger_scheduled(self, *, recovery: bool = False) -> None:
        if has_successful_full_run_today(self.store):
            record_scheduler_attempt(self.store, status="skipped_already_ran")
            return
        if not self.store.list_active_rss_sources(limit=1):
            record_scheduler_attempt(self.store, status="no_active_sources")
            return
        if not settings.enable_real_runs:
            record_scheduler_attempt(self.store, status="real_runs_disabled")
            return
        try:
            result = start_inbox_run(
                self.store,
                {
                    "force": True,
                    "run_synchronously": False,
                    "scheduler_recovery": recovery,
                    "limits": {"max_items_per_source": 20, "probe_limit": 20},
                },
                trigger_type="scheduled",
                post_process=self.post_process,
            )
            record_scheduler_attempt(
                self.store,
                status=result.get("status", "unknown"),
                run_id=result.get("run_id"),
                error=None if result.get("accepted") else result.get("message"),
            )
        except Exception as exc:
            record_scheduler_attempt(self.store, status="error", error=str(exc))
