from __future__ import annotations

from datetime import date, datetime, time, timezone
from typing import Any

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]


def resolve_date_filters(
    date_filter: str | None,
    from_filter: str | None,
    to_filter: str | None,
    *,
    tz: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
    published_from: str | None = None,
    published_to: str | None = None,
) -> dict[str, str | None]:
    filters: dict[str, str | None] = {
        "created_from": created_from or from_filter,
        "created_to": created_to or to_filter,
        "published_from": published_from,
        "published_to": published_to,
        "resolved_timezone": None,
    }
    if date_filter:
        if date_filter == "today":
            if tz:
                if ZoneInfo is None:
                    raise ValueError("timezone support is unavailable")
                zone = ZoneInfo(tz)
                target = datetime.now(zone).date()
                start = datetime.combine(target, time.min, tzinfo=zone).astimezone(timezone.utc)
                end = datetime.combine(target, time.max, tzinfo=zone).astimezone(timezone.utc)
                filters["resolved_timezone"] = tz
            else:
                target = date.today()
                start = datetime.combine(target, time.min, tzinfo=timezone.utc)
                end = datetime.combine(target, time.max, tzinfo=timezone.utc)
                filters["resolved_timezone"] = "UTC"
        else:
            target = date.fromisoformat(date_filter)
            start = datetime.combine(target, time.min, tzinfo=timezone.utc)
            end = datetime.combine(target, time.max, tzinfo=timezone.utc)
            filters["resolved_timezone"] = "UTC"
        filters["created_from"] = start.isoformat()
        filters["created_to"] = end.isoformat()
    filters["from"] = filters["created_from"]
    filters["to"] = filters["created_to"]
    return filters


def apply_view_defaults(filters: dict[str, Any], explicit_query_params: set[str]) -> dict[str, Any]:
    view = filters.get("view")
    if not view:
        return filters
    if view == "all":
        filters["include_ignored"] = True
        filters["include_silent"] = True
    elif view == "readable":
        filters["include_ignored"] = False
        if "include_silent" not in explicit_query_params:
            filters["include_silent"] = True
    elif view == "recommended":
        filters["include_ignored"] = False
        filters["include_silent"] = False
        if not filters.get("suggested_action"):
            filters["suggested_action"] = ["read", "save", "transcribe", "review"]
    elif view == "notifications":
        filters["include_ignored"] = False
        filters["include_silent"] = False
        if not filters.get("notification_decision"):
            filters["notification_decision"] = ["full_push", "incremental_push"]
    return filters
