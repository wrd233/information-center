from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.8 fallback only
    ZoneInfo = None  # type: ignore[assignment]


DEFAULT_API_BASE = "http://127.0.0.1:8787"


def str_to_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"expected boolean, got {value!r}")


def request_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    *,
    timeout: int = 30,
) -> tuple[int, dict[str, Any]]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method.upper(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(raw) if raw.strip() else {"ok": True}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"ok": False, "error": {"error_code": "unknown_error", "message": raw, "retryable": True}}
        return exc.code, data
    except Exception as exc:
        return 0, {
            "ok": False,
            "error": {
                "error_code": "api_unreachable",
                "message": str(exc),
                "retryable": True,
            },
        }


def write_json(data: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(data, ensure_ascii=False, sort_keys=True) + "\n")


def add_common_api_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON to stdout.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="content-inbox Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inbox = subparsers.add_parser("inbox", help="Query inbox items.")
    add_common_api_args(inbox)
    inbox.add_argument("--limit", type=int, default=20)
    inbox.add_argument("--offset", type=int, default=0)
    inbox.add_argument("--date")
    inbox.add_argument("--today", action="store_true")
    inbox.add_argument("--from", dest="from_time")
    inbox.add_argument("--to", dest="to_time")
    inbox.add_argument("--created-from")
    inbox.add_argument("--created-to")
    inbox.add_argument("--published-from")
    inbox.add_argument("--published-to")
    inbox.add_argument("--view", choices=["all", "readable", "recommended", "notifications"])
    inbox.add_argument("--keyword")
    inbox.add_argument("--source", dest="source_name")
    inbox.add_argument("--type", dest="content_type")
    inbox.add_argument("--include-silent", action="store_true")
    inbox.add_argument("--include-ignored", action="store_true")
    inbox.add_argument("--min-score", type=int)
    inbox.add_argument("--suggested-action")
    inbox.add_argument("--notification-decision")
    inbox.add_argument("--need-id")
    inbox.add_argument("--topic-id")
    inbox.add_argument("--min-need-score", type=int)
    inbox.add_argument("--min-topic-score", type=int)
    inbox.add_argument("--tz", default="")

    sources = subparsers.add_parser("sources", help="Manage registered RSS sources.")
    sources_sub = sources.add_subparsers(dest="sources_command", required=True)

    sources_list = sources_sub.add_parser("list")
    add_common_api_args(sources_list)
    sources_list.add_argument("--status")
    sources_list.add_argument("--category")
    sources_list.add_argument("--limit", type=int, default=100)
    sources_list.add_argument("--offset", type=int, default=0)

    sources_get = sources_sub.add_parser("get")
    add_common_api_args(sources_get)
    sources_get.add_argument("source_id")

    sources_register = sources_sub.add_parser("register")
    add_common_api_args(sources_register)
    sources_register.add_argument("--source-id")
    sources_register.add_argument("--name", required=True)
    sources_register.add_argument("--category")
    sources_register.add_argument("--feed-url", required=True)
    sources_register.add_argument("--status", default="active")
    sources_register.add_argument("--priority", type=int, default=3)
    sources_register.add_argument("--tag", dest="tags", action="append", default=[])
    sources_register.add_argument("--notes")
    sources_register.add_argument("--config-json", default="")

    sources_update = sources_sub.add_parser("update")
    add_common_api_args(sources_update)
    sources_update.add_argument("source_id")
    sources_update.add_argument("--name")
    sources_update.add_argument("--category")
    sources_update.add_argument("--feed-url")
    sources_update.add_argument("--status")
    sources_update.add_argument("--priority", type=int)
    sources_update.add_argument("--tag", dest="tags", action="append")
    sources_update.add_argument("--notes")
    sources_update.add_argument("--config-json", default="")

    sources_ingest = sources_sub.add_parser("ingest")
    add_common_api_args(sources_ingest)
    sources_ingest.add_argument("source_id")
    sources_ingest.add_argument("--limit", type=int)
    sources_ingest.add_argument("--screen", type=str_to_bool)
    sources_ingest.add_argument("--incremental-mode", choices=["fixed_limit", "until_existing"])
    sources_ingest.add_argument("--probe-limit", type=int)
    sources_ingest.add_argument("--new-source-initial-limit", type=int)
    sources_ingest.add_argument("--old-source-no-anchor-limit", type=int)
    sources_ingest.add_argument("--include-items", action="store_true")

    sources_test = sources_sub.add_parser("test")
    add_common_api_args(sources_test)
    sources_test.add_argument("source_id")
    sources_test.add_argument("--limit", type=int, default=5)

    sources_import = sources_sub.add_parser("import-csv")
    add_common_api_args(sources_import)
    sources_import.add_argument("--csv", required=True)
    sources_import.add_argument("--dry-run", action="store_true")
    sources_import.add_argument("--upsert", action="store_true")
    sources_import.add_argument("--skip-existing", action="store_true")
    sources_import.add_argument("--update-existing", action="store_true")
    sources_import.add_argument("--default-status", default="active")
    sources_import.add_argument("--default-category")
    sources_import.add_argument("--source-id-column")

    sources_backfill = sources_sub.add_parser("backfill-items")
    add_common_api_args(sources_backfill)
    sources_backfill.add_argument("--dry-run", action="store_true")
    sources_backfill.add_argument("--apply", action="store_true")

    sources_health = sources_sub.add_parser("health")
    add_common_api_args(sources_health)

    runs = subparsers.add_parser("runs", help="Inspect RSS ingest runs.")
    runs_sub = runs.add_subparsers(dest="runs_command", required=True)
    runs_list = runs_sub.add_parser("list")
    add_common_api_args(runs_list)
    runs_list.add_argument("--limit", type=int, default=20)
    runs_list.add_argument("--offset", type=int, default=0)
    runs_get = runs_sub.add_parser("get")
    add_common_api_args(runs_get)
    runs_get.add_argument("run_id")
    runs_sources = runs_sub.add_parser("sources")
    add_common_api_args(runs_sources)
    runs_sources.add_argument("run_id")

    return parser


def parse_config_json(raw: str) -> dict[str, Any]:
    if not raw:
        return {}
    loaded = json.loads(raw)
    if not isinstance(loaded, dict):
        raise ValueError("--config-json must decode to an object")
    return loaded


def local_today_range(tz_name: str) -> tuple[str, str]:
    if ZoneInfo is None:
        raise ValueError("timezone support is unavailable in this Python runtime")
    tz = ZoneInfo(tz_name)
    target = datetime.now(tz).date()
    start = datetime.combine(target, time.min, tzinfo=tz).astimezone(timezone.utc)
    end = datetime.combine(target, time.max, tzinfo=tz).astimezone(timezone.utc)
    return start.isoformat(), end.isoformat()


def run_inbox(args: argparse.Namespace) -> int:
    params: dict[str, str] = {
        "limit": str(args.limit),
        "offset": str(args.offset),
    }
    if args.today and args.tz:
        params["from"], params["to"] = local_today_range(args.tz)
    elif args.today:
        params["date"] = "today"
    elif args.date:
        params["date"] = args.date
    if args.from_time:
        params["from"] = args.from_time
    if args.to_time:
        params["to"] = args.to_time
    option_map = {
        "keyword": args.keyword,
        "source_name": args.source_name,
        "content_type": args.content_type,
        "min_score": args.min_score,
        "suggested_action": args.suggested_action,
        "notification_decision": args.notification_decision,
        "need_id": args.need_id,
        "topic_id": args.topic_id,
        "min_need_score": args.min_need_score,
        "min_topic_score": args.min_topic_score,
        "created_from": args.created_from,
        "created_to": args.created_to,
        "published_from": args.published_from,
        "published_to": args.published_to,
        "view": args.view,
    }
    for key, value in option_map.items():
        if value is not None:
            params[key] = str(value)
    if args.include_silent:
        params["include_silent"] = "true"
    if args.include_ignored:
        params["include_ignored"] = "true"
    url = f"{args.api_base.rstrip('/')}/api/inbox?{urllib.parse.urlencode(params)}"
    status, data = request_json("GET", url)
    write_json(data)
    if status == 0 or status >= 400 or data.get("ok") is False:
        print(f"content-inbox CLI error: {data.get('error', data)}", file=sys.stderr)
        return 1
    return 0


def run_sources(args: argparse.Namespace) -> int:
    base = args.api_base.rstrip("/")
    method = "GET"
    payload: dict[str, Any] | None = None
    if args.sources_command == "list":
        params = {"limit": str(args.limit), "offset": str(args.offset)}
        if args.status:
            params["status"] = args.status
        if args.category:
            params["category"] = args.category
        url = f"{base}/api/rss/sources?{urllib.parse.urlencode(params)}"
    elif args.sources_command == "get":
        url = f"{base}/api/rss/sources/{urllib.parse.quote(args.source_id)}"
    elif args.sources_command == "register":
        method = "POST"
        url = f"{base}/api/rss/sources"
        payload = {
            "source_id": args.source_id,
            "source_name": args.name,
            "source_category": args.category,
            "feed_url": args.feed_url,
            "status": args.status,
            "priority": args.priority,
            "tags": args.tags,
            "notes": args.notes,
            "config": parse_config_json(args.config_json),
        }
    elif args.sources_command == "update":
        method = "PATCH"
        url = f"{base}/api/rss/sources/{urllib.parse.quote(args.source_id)}"
        payload = {}
        updates = {
            "source_name": args.name,
            "source_category": args.category,
            "feed_url": args.feed_url,
            "status": args.status,
            "priority": args.priority,
            "tags": args.tags,
            "notes": args.notes,
        }
        payload.update({key: value for key, value in updates.items() if value is not None})
        if args.config_json:
            payload["config"] = parse_config_json(args.config_json)
    elif args.sources_command == "ingest":
        method = "POST"
        url = f"{base}/api/rss/sources/{urllib.parse.quote(args.source_id)}/ingest"
        payload = {
            key: value
            for key, value in {
                "limit": args.limit,
                "screen": args.screen,
                "incremental_mode": args.incremental_mode,
                "probe_limit": args.probe_limit,
                "new_source_initial_limit": args.new_source_initial_limit,
                "old_source_no_anchor_limit": args.old_source_no_anchor_limit,
                "include_items": args.include_items,
            }.items()
            if value is not None
        }
    elif args.sources_command == "test":
        method = "POST"
        url = f"{base}/api/rss/sources/{urllib.parse.quote(args.source_id)}/ingest"
        payload = {"test": True, "screen": False, "limit": args.limit}
    elif args.sources_command == "import-csv":
        from app.source_importer import read_source_csv

        sources = read_source_csv(
            Path(args.csv),
            default_status=args.default_status,
            default_category=args.default_category,
            source_id_column=args.source_id_column,
        )
        if args.dry_run:
            data = {
                "ok": True,
                "dry_run": True,
                "sources": sources,
                "stats": {"created": 0, "updated": 0, "skipped": len(sources), "failed": 0},
            }
            write_json(data)
            return 0
        stats = {"created": 0, "updated": 0, "skipped": 0, "failed": 0}
        results = []
        for source in sources:
            status, data = request_json("POST", f"{base}/api/rss/sources", source)
            if status == 409 and (args.upsert or args.update_existing or args.skip_existing):
                if args.skip_existing and not args.update_existing:
                    stats["skipped"] += 1
                    results.append(data)
                    continue
                source_id = source.get("source_id")
                if not source_id:
                    stats["failed"] += 1
                    results.append(data)
                    continue
                status, data = request_json("PATCH", f"{base}/api/rss/sources/{urllib.parse.quote(source_id)}", source)
                if status < 400 and data.get("ok") is not False:
                    stats["updated"] += 1
                else:
                    stats["failed"] += 1
                results.append(data)
                continue
            if status < 400 and data.get("ok") is not False:
                stats["created"] += 1
            else:
                stats["failed"] += 1
            results.append(data)
        data = {"ok": stats["failed"] == 0, "stats": stats, "results": results}
        write_json(data)
        return 0 if data["ok"] else 1
    elif args.sources_command == "backfill-items":
        method = "POST"
        apply_flag = bool(args.apply and not args.dry_run)
        url = f"{base}/api/rss/backfill-items?{urllib.parse.urlencode({'apply': str(apply_flag).lower()})}"
        payload = None
    elif args.sources_command == "health":
        url = f"{base}/api/rss/sources?limit=1"
    else:  # pragma: no cover - argparse prevents this.
        raise ValueError(f"unknown sources command: {args.sources_command}")

    status, data = request_json(method, url, payload)
    write_json(data)
    if status == 0 or status >= 400 or data.get("ok") is False:
        print(f"content-inbox CLI error: {data.get('error', data)}", file=sys.stderr)
        return 1
    return 0


def run_runs(args: argparse.Namespace) -> int:
    base = args.api_base.rstrip("/")
    if args.runs_command == "list":
        url = f"{base}/api/rss/runs?{urllib.parse.urlencode({'limit': args.limit, 'offset': args.offset})}"
    elif args.runs_command == "get":
        url = f"{base}/api/rss/runs/{urllib.parse.quote(args.run_id)}"
    elif args.runs_command == "sources":
        url = f"{base}/api/rss/runs/{urllib.parse.quote(args.run_id)}/sources"
    else:  # pragma: no cover
        raise ValueError(f"unknown runs command: {args.runs_command}")
    status, data = request_json("GET", url)
    write_json(data)
    if status == 0 or status >= 400 or data.get("ok") is False:
        print(f"content-inbox CLI error: {data.get('error', data)}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "inbox":
            return run_inbox(args)
        if args.command == "sources":
            return run_sources(args)
        if args.command == "runs":
            return run_runs(args)
    except Exception as exc:
        data = {
            "ok": False,
            "error": {
                "error_code": "cli_error",
                "message": str(exc),
                "retryable": False,
            },
        }
        write_json(data)
        print(f"content-inbox CLI error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
