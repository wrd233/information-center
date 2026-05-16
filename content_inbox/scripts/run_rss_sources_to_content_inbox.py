#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch-submit RSS sources from rsshub/rss_opml/rss_sources.csv to content-inbox.

This script intentionally does not modify content-inbox code or the RSS source list.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml


TRUTHY = {"y", "yes", "true", "1", "on", "enable", "enabled", "启用", "是"}
FALSY = {"n", "no", "false", "0", "off", "disable", "disabled", "停用", "否"}
SKIP_STATUSES = {"disabled", "inactive", "broken", "error", "failed", "invalid", "dead", "paused", "停用", "失效", "错误"}
RUNS_DIRNAME = "runs"
RUN_PREFIX = "rss_run_"


@dataclass
class Source:
    row_index: int
    source_name: str
    source_category: str = ""
    local_xml_url: str = ""
    xml_url: str = ""
    status: str = ""
    enabled_raw: str = ""
    priority: str = ""
    raw: Dict[str, str] = field(default_factory=dict)


@dataclass
class SourcePlan:
    sequence: int
    source: Source
    feed_url: str
    url_mode: str
    url_source: str
    source_id: str
    screen: bool


class TeeStream(io.TextIOBase):
    def __init__(self, *streams: io.TextIOBase) -> None:
        self.streams = streams

    def write(self, s: str) -> int:
        for stream in self.streams:
            stream.write(s)
            stream.flush()
        return len(s)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()

    def isatty(self) -> bool:
        return any(getattr(stream, "isatty", lambda: False)() for stream in self.streams)


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def today_date() -> str:
    return dt.date.today().isoformat()


def normalize_key(name: str) -> str:
    return (name or "").strip().lower().replace("-", "_").replace(" ", "_")


def get_first(row: Dict[str, str], names: Iterable[str], default: str = "") -> str:
    normalized = {normalize_key(k): v for k, v in row.items()}
    for name in names:
        value = normalized.get(normalize_key(name))
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def is_enabled(row: Dict[str, str]) -> bool:
    enabled = get_first(row, ["enabled", "enable", "is_enabled", "启用"], default="")
    status = get_first(row, ["status", "状态"], default="").strip().lower()

    if status and status in SKIP_STATUSES:
        return False

    if enabled:
        v = enabled.strip().lower()
        if v in FALSY:
            return False
        if v in TRUTHY:
            return True

    return True


def priority_rank(priority: str) -> Tuple[int, str]:
    p = (priority or "").strip().lower()
    if not p:
        return (50, "")

    label_map = {
        "high": 0,
        "p0": 0,
        "urgent": 0,
        "medium": 10,
        "p1": 10,
        "normal": 20,
        "low": 30,
        "p2": 30,
    }
    if p in label_map:
        return (label_map[p], p)

    try:
        return (int(float(p)), p)
    except ValueError:
        return (40, p)


def status_rank(status: str) -> int:
    s = (status or "").strip().lower()
    if s in {"active", "ok", "valid", "正常"}:
        return 0
    if s in {"review", "待复核"}:
        return 1
    if s:
        return 2
    return 3


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / "rsshub" / "rss_opml" / "rss_sources.csv").exists():
            return candidate
        if (candidate / ".git").exists() and (candidate / "content_inbox").exists():
            return candidate
    return current


def read_sources(csv_path: Path) -> List[Source]:
    if not csv_path.exists():
        raise FileNotFoundError(f"RSS source CSV not found: {csv_path}")

    sources: List[Source] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            cleaned = {str(k).strip(): ("" if v is None else str(v).strip()) for k, v in row.items() if k is not None}
            if not is_enabled(cleaned):
                continue

            local_xml_url = get_first(cleaned, ["local_xml_url", "local_url", "local_feed_url"])
            xml_url = get_first(cleaned, ["xml_url", "feed_url", "rss_url", "url"])
            if not (local_xml_url or xml_url):
                continue

            sources.append(
                Source(
                    row_index=idx,
                    source_name=get_first(cleaned, ["title", "name", "source_name", "源名称"], default=f"source_row_{idx}"),
                    source_category=get_first(cleaned, ["category_path", "source_category", "category", "top_category", "分类"], default=""),
                    local_xml_url=local_xml_url,
                    xml_url=xml_url,
                    status=get_first(cleaned, ["status", "状态"], default=""),
                    enabled_raw=get_first(cleaned, ["enabled", "enable", "is_enabled", "启用"], default=""),
                    priority=get_first(cleaned, ["priority", "优先级"], default=""),
                    raw=cleaned,
                )
            )
    return sources


def select_sources(sources: List[Source], count: int) -> List[Source]:
    groups: Dict[str, List[Source]] = {}
    for src in sources:
        key = src.source_category or "Uncategorized"
        groups.setdefault(key, []).append(src)

    for key in groups:
        groups[key].sort(key=lambda s: (status_rank(s.status), priority_rank(s.priority), s.row_index))

    ordered_categories = sorted(
        groups.keys(),
        key=lambda k: (
            min(status_rank(s.status) for s in groups[k]),
            min(priority_rank(s.priority)[0] for s in groups[k]),
            k,
        ),
    )

    selected: List[Source] = []
    while len(selected) < count:
        added = False
        for category in ordered_categories:
            if groups[category]:
                selected.append(groups[category].pop(0))
                added = True
                if len(selected) >= count:
                    break
        if not added:
            break
    return selected


def replace_url_host(url: str, new_host: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url

    hostname = parsed.hostname or ""
    if hostname not in {"127.0.0.1", "localhost"}:
        return url

    auth = ""
    if parsed.username:
        auth = parsed.username
        if parsed.password:
            auth += f":{parsed.password}"
        auth += "@"

    host_port = new_host
    if ":" not in new_host and parsed.port:
        host_port = f"{new_host}:{parsed.port}"

    return urllib.parse.urlunparse(parsed._replace(netloc=f"{auth}{host_port}"))


def resolve_feed_url(source: Source, url_mode: str, rsshub_service_name: str) -> Tuple[str, str]:
    local_url = source.local_xml_url.strip()
    remote_url = source.xml_url.strip()

    if url_mode == "remote":
        return remote_url or local_url, "xml_url" if remote_url else "local_xml_url"

    feed_url = local_url or remote_url
    url_source = "local_xml_url" if local_url else "xml_url"

    if url_mode == "docker-host" and local_url:
        return replace_url_host(feed_url, "host.docker.internal"), url_source
    if url_mode == "compose-service" and local_url:
        return replace_url_host(feed_url, rsshub_service_name), url_source

    return feed_url, url_source


def build_source_id(source: Source, feed_url: str) -> str:
    return json.dumps(
        {
            "row_index": source.row_index,
            "source_name": source.source_name,
            "source_category": source.source_category,
            "local_xml_url": source.local_xml_url,
            "xml_url": source.xml_url,
            "feed_url": feed_url,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def build_headers(api_key: Optional[str]) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["X-API-Key"] = api_key
    return headers


def request_json(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 120,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url=url, data=body, method=method.upper(), headers=build_headers(api_key))

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            if not raw.strip():
                return {"ok": True, "_status": resp.status}
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = {"ok": False, "_raw": raw}
            data["_status"] = resp.status
            return data
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"detail": raw}
        return {"ok": False, "_status": e.code, "error": data}
    except Exception as e:
        return {"ok": False, "_status": None, "error": str(e)}


def set_llm_max_concurrency(
    api_base: str,
    max_concurrency: int,
    api_key: Optional[str],
    timeout: int = 30,
) -> Dict[str, Any]:
    """Call POST /api/runtime/llm-concurrency on the content-inbox service."""
    url = f"{api_base.rstrip('/')}/api/runtime/llm-concurrency"
    payload = {"max_concurrency": max_concurrency}
    return request_json("POST", url, payload, timeout=timeout, api_key=api_key)


def set_screening_mode(
    api_base: str,
    mode: str,
    api_key: Optional[str],
    timeout: int = 30,
) -> Dict[str, Any]:
    """Call POST /api/runtime/screening-mode on the content-inbox service."""
    url = f"{api_base.rstrip('/')}/api/runtime/screening-mode"
    payload = {"mode": mode}
    return request_json("POST", url, payload, timeout=timeout, api_key=api_key)


def analyze_rss_source(
    api_base: str,
    source: Source,
    feed_url: str,
    limit_per_source: int,
    screen: bool,
    timeout: int,
    api_key: Optional[str],
    profile: bool = False,
    audit_prompt: bool = False,
    dump_llm_prompt: bool = False,
    dump_llm_prompt_dir: str = "",
    incremental_mode: str = "fixed_limit",
    probe_limit: int = 20,
    new_source_initial_limit: int = 5,
    old_source_no_anchor_limit: int = 20,
    stop_on_first_existing: bool = True,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "feed_url": feed_url,
        "source_name": source.source_name,
        "source_category": source.source_category,
        "limit": limit_per_source,
        "screen": screen,
    }
    if profile:
        payload["profile"] = True
    if audit_prompt:
        payload["audit_prompt"] = True
    if dump_llm_prompt:
        payload["dump_llm_prompt"] = True
    if dump_llm_prompt_dir:
        payload["dump_llm_prompt_dir"] = dump_llm_prompt_dir
    if incremental_mode != "fixed_limit":
        payload["incremental_mode"] = incremental_mode
    payload["probe_limit"] = probe_limit
    payload["new_source_initial_limit"] = new_source_initial_limit
    payload["old_source_no_anchor_limit"] = old_source_no_anchor_limit
    payload["stop_on_first_existing"] = stop_on_first_existing
    return request_json("POST", f"{api_base.rstrip('/')}/api/rss/analyze", payload=payload, timeout=timeout, api_key=api_key)


def read_registry_sources(api_base: str, api_key: Optional[str], timeout: int, limit: int = 500) -> List[Source]:
    params = urllib.parse.urlencode({"status": "active", "limit": str(limit), "offset": "0"})
    response = request_json("GET", f"{api_base.rstrip('/')}/api/rss/sources?{params}", timeout=timeout, api_key=api_key)
    if response.get("ok") is False or (response.get("_status") is not None and int(response.get("_status")) >= 400):
        raise RuntimeError(json.dumps(response.get("error", response), ensure_ascii=False))
    rows = response.get("sources") or response.get("items") or []
    sources: List[Source] = []
    for idx, row in enumerate(rows, start=1):
        if str(row.get("status") or "").lower() != "active":
            continue
        feed_url = str(row.get("feed_url") or "").strip()
        if not feed_url:
            continue
        sources.append(
            Source(
                row_index=idx,
                source_name=str(row.get("source_name") or row.get("source_id") or f"registry_source_{idx}"),
                source_category=str(row.get("source_category") or ""),
                local_xml_url=str(row.get("local_feed_url") or ""),
                xml_url=feed_url,
                status=str(row.get("status") or "active"),
                enabled_raw="true",
                priority=str(row.get("priority") if row.get("priority") is not None else ""),
                raw={k: "" if v is None else str(v) for k, v in row.items()},
            )
        )
    return sources


def analyze_registered_source(
    api_base: str,
    source_id: str,
    limit_per_source: int,
    screen: bool,
    timeout: int,
    api_key: Optional[str],
    incremental_mode: str = "fixed_limit",
    probe_limit: int = 20,
    new_source_initial_limit: int = 5,
    old_source_no_anchor_limit: int = 20,
    stop_on_first_existing: bool = True,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "limit": limit_per_source,
        "screen": screen,
        "incremental_mode": incremental_mode,
        "probe_limit": probe_limit,
        "new_source_initial_limit": new_source_initial_limit,
        "old_source_no_anchor_limit": old_source_no_anchor_limit,
        "stop_on_first_existing": stop_on_first_existing,
    }
    return request_json(
        "POST",
        f"{api_base.rstrip('/')}/api/rss/sources/{urllib.parse.quote(source_id)}/ingest",
        payload=payload,
        timeout=timeout,
        api_key=api_key,
    )


def flatten_registered_ingest_response(response: Dict[str, Any]) -> Dict[str, Any]:
    run = response.get("run") or {}
    stats = run.get("stats") or {}
    incremental = run.get("incremental") or {}
    flattened = dict(response)
    flattened.setdefault("total_items", stats.get("fetched_entries", stats.get("feed_items_seen", 0)))
    flattened.setdefault("new_items", stats.get("new_items", 0))
    flattened.setdefault("duplicate_items", stats.get("duplicate_items", 0))
    flattened.setdefault("failed_items", stats.get("failed_items", 0))
    flattened.setdefault("screened_items", stats.get("processed_entries", stats.get("processed_items", 0)))
    flattened.setdefault("incremental_mode", incremental.get("mode") or incremental.get("incremental_mode", ""))
    flattened.setdefault("incremental_decision", incremental.get("decision") or incremental.get("incremental_decision", ""))
    flattened.setdefault("source_has_history", incremental.get("source_has_history", ""))
    flattened.setdefault("probe_limit", incremental.get("probe_limit", ""))
    flattened.setdefault("feed_items_seen", stats.get("fetched_entries", stats.get("feed_items_seen", "")))
    flattened.setdefault("anchor_found", incremental.get("anchor_found", ""))
    flattened.setdefault("anchor_index", incremental.get("anchor_index", ""))
    flattened.setdefault("selected_items_for_processing", stats.get("processed_entries", stats.get("selected_items_for_processing", "")))
    flattened.setdefault("warnings", incremental.get("warnings", []))
    return flattened


def run_one_plan(plan: SourcePlan, args: argparse.Namespace, api_key: Optional[str]) -> Dict[str, Any]:
    if getattr(args, "source_mode", "csv") == "registry":
        response = flatten_registered_ingest_response(
            analyze_registered_source(
                api_base=args.api_base,
                source_id=plan.source_id,
                limit_per_source=args.limit_per_source,
                screen=plan.screen,
                timeout=args.timeout,
                api_key=api_key,
                incremental_mode=args.incremental_mode,
                probe_limit=args.probe_limit,
                new_source_initial_limit=args.new_source_initial_limit,
                old_source_no_anchor_limit=args.old_source_no_anchor_limit,
                stop_on_first_existing=args.stop_on_first_existing,
            )
        )
    else:
        response = analyze_rss_source(
            api_base=args.api_base,
            source=plan.source,
            feed_url=plan.feed_url,
            limit_per_source=args.limit_per_source,
            screen=plan.screen,
            timeout=args.timeout,
            api_key=api_key,
            profile=args.profile,
            audit_prompt=args.audit_prompt,
            dump_llm_prompt=args.dump_llm_prompt,
            dump_llm_prompt_dir=getattr(args, 'dump_llm_prompt_dir', ''),
            incremental_mode=args.incremental_mode,
            probe_limit=args.probe_limit,
            new_source_initial_limit=args.new_source_initial_limit,
            old_source_no_anchor_limit=args.old_source_no_anchor_limit,
            stop_on_first_existing=args.stop_on_first_existing,
        )
    if args.audit_prompt:
        return summarize_audit_response(plan, response)
    return summarize_result_for_source(plan, response)


def query_inbox(
    api_base: str,
    api_key: Optional[str],
    timeout: int,
    limit: int = 100,
    from_time: str = "",
) -> Dict[str, Any]:
    base = f"{api_base.rstrip('/')}/api/inbox"
    preferred_params = {
        "notification_decision": "full_push,incremental_push",
        "include_silent": "false",
        "limit": str(limit),
    }
    if from_time:
        preferred_params["from"] = from_time
    else:
        preferred_params["date"] = "today"

    preferred_url = base + "?" + urllib.parse.urlencode(preferred_params)
    result = request_json("GET", preferred_url, timeout=timeout, api_key=api_key)
    result["_query_mode"] = "from" if from_time else "date"
    if result.get("ok") is not False and int(result.get("_status") or 0) < 400:
        return result

    fallback_params = {"notification_decision": "full_push,incremental_push", "include_silent": "false", "limit": str(limit), "date": "today"}
    fallback_url = base + "?" + urllib.parse.urlencode(fallback_params)
    fallback = request_json("GET", fallback_url, timeout=timeout, api_key=api_key)
    fallback["_fallback_used"] = True
    fallback["_preferred_error"] = result
    fallback["_query_mode"] = "date"
    return fallback


def query_inbox_view(
    api_base: str,
    api_key: Optional[str],
    timeout: int,
    *,
    need_id: str | None = None,
    topic_id: str | None = None,
    min_need_score: int | None = None,
    limit: int = 100,
    from_time: str = "",
    notification_mode: bool = False,
) -> Dict[str, Any]:
    base = f"{api_base.rstrip('/')}/api/inbox"
    params: Dict[str, str] = {"limit": str(limit)}
    if from_time:
        params["from"] = from_time
    else:
        params["date"] = "today"

    if notification_mode:
        params["notification_decision"] = "full_push,incremental_push"
        params["include_silent"] = "false"
    else:
        params["include_ignored"] = "true"
        params["include_silent"] = "true"
        if need_id:
            params["need_id"] = need_id
        if topic_id:
            params["topic_id"] = topic_id
        if min_need_score is not None:
            params["min_need_score"] = str(min_need_score)

    url = base + "?" + urllib.parse.urlencode(params)
    result = request_json("GET", url, timeout=timeout, api_key=api_key)
    result["_query_mode"] = "from" if from_time else "date"
    result["_query_url"] = url
    return result


def load_reading_need_min_scores(repo_root: Path) -> Dict[str, int]:
    path = repo_root / "content_inbox" / "config" / "reading_needs.yaml"
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    needs = loaded.get("needs") if isinstance(loaded, dict) else []
    result: Dict[str, int] = {}
    if not isinstance(needs, list):
        return result
    for need in needs:
        if not isinstance(need, dict):
            continue
        need_id = str(need.get("id") or "").strip()
        if not need_id:
            continue
        try:
            result[need_id] = int(need.get("min_score", 4))
        except (TypeError, ValueError):
            result[need_id] = 4
    return result


def get_nested(d: Dict[str, Any], *keys: str, default: Any = "") -> Any:
    current: Any = d
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return default if current is None else current


def extract_items(inbox: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(inbox.get("items"), list):
        return inbox["items"]
    items: List[Dict[str, Any]] = []
    sections = inbox.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict) and isinstance(section.get("items"), list):
                items.extend(section["items"])
    return items


def as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    return [str(value)]


def item_line(item: Dict[str, Any], *, need_id: str | None = None, topic_id: str | None = None) -> str:
    title = item.get("title") or get_nested(item, "normalized", "title") or "未命名"
    url = item.get("url") or get_nested(item, "normalized", "url")
    source = item.get("source_name") or get_nested(item, "normalized", "source_name") or ""
    screening = item.get("screening") or {}
    clustering = item.get("clustering") or {}
    summary = screening.get("summary") or item.get("summary") or ""
    reason = screening.get("reason") or ""
    score = screening.get("value_score") or item.get("value_score") or ""
    title_cn = screening.get("title_cn") or ""
    need_matches = screening.get("need_matches") or []
    topic_matches = screening.get("topic_matches") or []
    selected_need_match = next((match for match in need_matches if match.get("need_id") == need_id), None)
    selected_topic_match = next((match for match in topic_matches if match.get("topic_id") == topic_id), None)

    parts = [f"- **{md_escape(title)}**"]
    if title_cn:
        parts.append(f"  - 中文解释：{md_escape(title_cn)}")
    if source:
        parts.append(f"  - 来源：{md_escape(source)}")
    if url:
        parts.append(f"  - 链接：{url}")
    if score != "":
        parts.append(f"  - 评分：{md_escape(score)}")
    if summary:
        parts.append(f"  - 摘要：{md_escape(summary)}")
    if selected_need_match:
        parts.append(f"  - need_score：{md_escape(selected_need_match.get('score', ''))}")
        parts.append(f"  - priority：{md_escape(selected_need_match.get('priority', ''))}")
        parts.append(f"  - reason：{md_escape(selected_need_match.get('reason', ''))}")
        parts.append(f"  - evidence：{md_escape(', '.join(as_list(selected_need_match.get('evidence'))))}")
        parts.append(f"  - confidence：{md_escape(selected_need_match.get('confidence', ''))}")
        parts.append(f"  - needs_more_context：{md_escape(selected_need_match.get('needs_more_context', ''))}")
    elif selected_topic_match:
        parts.append(f"  - topic_score：{md_escape(selected_topic_match.get('score', ''))}")
        parts.append(f"  - reason：{md_escape(selected_topic_match.get('reason', ''))}")
        parts.append(f"  - confidence：{md_escape(selected_topic_match.get('confidence', ''))}")
        parts.append(f"  - needs_more_context：{md_escape(screening.get('needs_more_context'))}")
    else:
        if reason:
            parts.append(f"  - 理由：{md_escape(reason)}")
        if screening.get("confidence") != "":
            parts.append(f"  - confidence：{md_escape(screening.get('confidence'))}")
        if screening.get("needs_more_context") is not None:
            parts.append(f"  - needs_more_context：{md_escape(screening.get('needs_more_context'))}")
    parts.append(f"  - suggested_action：{md_escape(screening.get('suggested_action', ''))}")
    parts.append(f"  - notification_decision：{md_escape(clustering.get('notification_decision', ''))}")
    return "\n".join(parts)


def classify_error(result: Dict[str, Any]) -> str:
    message = (result.get("error_message") or "").lower()
    if not message:
        return ""
    if "429" in message:
        return "rate_limit"
    if "503" in message:
        return "rsshub_503"
    if "failed to parse feed" in message or "not well-formed" in message:
        return "feed_parse_error"
    if "timed out" in message or "timeout" in message:
        return "timeout"
    if "embedding" in message:
        return "embedding_error"
    if "deepseek" in message or "openai" in message or "screening" in message or "model" in message:
        return "model_error"
    if "connection refused" in message or "name or service not known" in message or "nodename nor servname" in message or "urlopen error" in message:
        return "network_error"
    if "400" in message or "500" in message or "api" in message:
        return "content_inbox_error"
    return "unknown"


def summarize_result_for_source(plan: SourcePlan, response: Dict[str, Any]) -> Dict[str, Any]:
    ok = response.get("ok")
    status_code = response.get("_status")
    failed_by_http = status_code is not None and int(status_code) >= 400

    profile = response.get("profile") or {}
    pre_dedupe_wait = profile.get("pre_dedupe_lock_wait_seconds", 0) or 0
    pre_dedupe_held = profile.get("pre_dedupe_lock_held_seconds", 0) or 0
    commit_wait = profile.get("commit_lock_wait_seconds", 0) or 0
    commit_held = profile.get("commit_lock_held_seconds", 0) or 0

    # Backwards-compatible roll-ups: sum of the two lock phases.
    # Direct old keys are kept for runs made before the lock split; when they
    # are missing we compute from the new split keys.
    lock_wait = profile.get("lock_wait_seconds")
    lock_held = profile.get("lock_held_seconds")
    if lock_wait is None:
        lock_wait = round(pre_dedupe_wait + commit_wait, 3)
    if lock_held is None:
        lock_held = round(pre_dedupe_held + commit_held, 3)

    profile_fields = {
        "fetch_feed_seconds": profile.get("fetch_feed_seconds", ""),
        "llm_basic_screening_seconds": profile.get("llm_basic_screening_seconds", ""),
        "llm_need_matching_seconds": profile.get("llm_need_matching_seconds", ""),
        "llm_screen_and_match_seconds": profile.get("llm_screen_and_match_seconds", ""),
        "screening_mode": response.get("screening_mode", ""),
        "llm_call_count": profile.get("llm_call_count", ""),
        "embedding_seconds": profile.get("embedding_seconds", ""),
        "lock_wait_seconds": lock_wait,
        "lock_held_seconds": lock_held,
        "pre_dedupe_lock_wait_seconds": pre_dedupe_wait,
        "pre_dedupe_lock_held_seconds": pre_dedupe_held,
        "commit_lock_wait_seconds": commit_wait,
        "commit_lock_held_seconds": commit_held,
        "source_total_seconds": profile.get("source_total_seconds", ""),
    }

    base = {
        "source_id": plan.source_id,
        "sequence": plan.sequence,
        "source_name": plan.source.source_name,
        "source_category": plan.source.source_category,
        "local_xml_url": plan.source.local_xml_url,
        "xml_url": plan.source.xml_url,
        "feed_url": plan.feed_url,
        "url_mode": plan.url_mode,
        "screen": plan.screen,
        **profile_fields,
    }

    if ok is False or failed_by_http:
        error_message = json.dumps(response.get("error", response), ensure_ascii=False)[:1000]
        result = {
            **base,
            "status": "failed",
            "total_items": 0,
            "new_items": 0,
            "duplicate_items": 0,
            "screened_items": 0,
            "recommended_items_from_api_response": 0,
            "new_items_recommended": "unknown",
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
            "incremental_mode": "",
            "incremental_decision": "",
            "source_has_history": "",
            "probe_limit": "",
            "feed_items_seen": "",
            "anchor_found": "",
            "anchor_index": "",
            "selected_items_for_processing": "",
            "incremental_warning": "",
            "error_message": error_message,
        }
        result["error_type"] = classify_error(result)
        return result

    return {
        **base,
        "status": "success",
        "total_items": response.get("total_items", 0),
        "new_items": response.get("new_items", 0),
        "duplicate_items": response.get("duplicate_items", 0),
        "screened_items": response.get("screened_items", 0),
        "recommended_items_from_api_response": response.get("recommended_items", 0),
        "new_items_recommended": "unknown",
        "new_event_items": response.get("new_event_items", 0),
        "incremental_items": response.get("incremental_items", 0),
        "silent_items": response.get("silent_items", 0),
        "failed_items": response.get("failed_items", 0),
        "incremental_mode": response.get("incremental_mode", ""),
        "incremental_decision": response.get("incremental_decision", ""),
        "source_has_history": str(response.get("source_has_history", "")),
        "probe_limit": response.get("probe_limit", ""),
        "feed_items_seen": response.get("feed_items_seen", ""),
        "anchor_found": str(response.get("anchor_found", "")),
        "anchor_index": response.get("anchor_index", ""),
        "selected_items_for_processing": response.get("selected_items_for_processing", ""),
        "incremental_warning": "; ".join(response.get("warnings", [])),
        "error_message": "",
        "error_type": "",
    }


def summarize_audit_response(plan: SourcePlan, response: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize an audit-mode API response into a result dict for the script pipeline."""
    ok = response.get("ok")
    status_code = response.get("_status")
    failed_by_http = status_code is not None and int(status_code) >= 400

    base = {
        "source_id": plan.source_id,
        "sequence": plan.sequence,
        "source_name": plan.source.source_name,
        "source_category": plan.source.source_category,
        "local_xml_url": plan.source.local_xml_url,
        "xml_url": plan.source.xml_url,
        "feed_url": plan.feed_url,
        "url_mode": plan.url_mode,
        "screen": plan.screen,
    }

    if ok is False or failed_by_http:
        error_message = json.dumps(response.get("error", response), ensure_ascii=False)[:1000]
        result = {
            **base,
            "status": "failed",
            "total_items": 0,
            "new_items": 0,
            "duplicate_items": 0,
            "screened_items": 0,
            "recommended_items_from_api_response": 0,
            "new_items_recommended": "unknown",
            "new_event_items": 0,
            "incremental_items": 0,
            "silent_items": 0,
            "failed_items": 0,
            "incremental_mode": "",
            "incremental_decision": "",
            "source_has_history": "",
            "probe_limit": "",
            "feed_items_seen": "",
            "anchor_found": "",
            "anchor_index": "",
            "selected_items_for_processing": "",
            "incremental_warning": "",
            "error_message": error_message,
            "_audit_records": [],
        }
        result["error_type"] = classify_error(result)
        return result

    audit_records = response.get("audit_records", [])
    return {
        **base,
        "status": "audited",
        "total_items": response.get("total_items", 0),
        "new_items": 0,
        "duplicate_items": 0,
        "screened_items": 0,
        "recommended_items_from_api_response": 0,
        "new_items_recommended": "unknown",
        "new_event_items": 0,
        "incremental_items": 0,
        "silent_items": 0,
        "failed_items": 0,
        "incremental_mode": "",
        "incremental_decision": "",
        "source_has_history": "",
        "probe_limit": "",
        "feed_items_seen": "",
        "anchor_found": "",
        "anchor_index": "",
        "selected_items_for_processing": "",
        "incremental_warning": "",
        "error_message": "",
        "error_type": "",
        "total_prompts": len(audit_records),
        "_audit_records": audit_records,
    }


def results_csv_headers() -> List[str]:
    return [
        "source_id",
        "sequence",
        "source_name",
        "source_category",
        "local_xml_url",
        "xml_url",
        "feed_url",
        "url_mode",
        "screen",
        "status",
        "incremental_mode",
        "incremental_decision",
        "source_has_history",
        "probe_limit",
        "feed_items_seen",
        "anchor_found",
        "anchor_index",
        "selected_items_for_processing",
        "incremental_warning",
        "total_items",
        "new_items",
        "duplicate_items",
        "screened_items",
        "recommended_items_from_api_response",
        "new_items_recommended",
        "new_event_items",
        "incremental_items",
        "silent_items",
        "failed_items",
        "error_type",
        "error_message",
        "fetch_feed_seconds",
        "llm_basic_screening_seconds",
        "llm_need_matching_seconds",
        "llm_screen_and_match_seconds",
        "screening_mode",
        "llm_call_count",
        "embedding_seconds",
        "lock_wait_seconds",
        "lock_held_seconds",
        "pre_dedupe_lock_wait_seconds",
        "pre_dedupe_lock_held_seconds",
        "commit_lock_wait_seconds",
        "commit_lock_held_seconds",
        "source_total_seconds",
    ]


def selected_csv_headers() -> List[str]:
    return [
        "sequence",
        "source_id",
        "source_name",
        "source_category",
        "local_xml_url",
        "xml_url",
        "feed_url",
        "url_mode",
        "url_source",
        "screen",
        "row_index",
        "status",
        "priority",
    ]


def write_csv_rows(path: Path, headers: List[str], rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def latest_run_dir(runs_dir: Path) -> Optional[Path]:
    candidates = sorted([p for p in runs_dir.glob(f"{RUN_PREFIX}*") if p.is_dir()], reverse=True)
    for candidate in candidates:
        if (candidate / "run_state.json").exists():
            return candidate
    return None


def load_run_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_selected_rows(plans: List[SourcePlan]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for plan in plans:
        rows.append(
            {
                "sequence": plan.sequence,
                "source_id": plan.source_id,
                "source_name": plan.source.source_name,
                "source_category": plan.source.source_category,
                "local_xml_url": plan.source.local_xml_url,
                "xml_url": plan.source.xml_url,
                "feed_url": plan.feed_url,
                "url_mode": plan.url_mode,
                "url_source": plan.url_source,
                "screen": plan.screen,
                "row_index": plan.source.row_index,
                "status": plan.source.status,
                "priority": plan.source.priority,
            }
        )
    return rows


def build_failed_rows(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "source_name": r.get("source_name", ""),
            "source_category": r.get("source_category", ""),
            "local_xml_url": r.get("local_xml_url", ""),
            "xml_url": r.get("xml_url", ""),
            "feed_url": r.get("feed_url", ""),
            "error_message": r.get("error_message", ""),
            "error_type": r.get("error_type", ""),
        }
        for r in results
        if r.get("status") == "failed"
    ]


def aggregate_stats(results: List[Dict[str, Any]], inbox: Dict[str, Any]) -> Dict[str, Any]:
    success = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") == "failed"]
    skipped = [r for r in results if r.get("status") == "skipped_known_failed"]
    inbox_items = extract_items(inbox)
    stats = inbox.get("stats") or {}
    incremental_mode = ""
    anchor_found_sources = 0
    new_source_baseline_sources = 0
    old_source_no_anchor_sources = 0
    selected_items_for_processing_total = 0
    for r in success:
        mode = r.get("incremental_mode", "")
        if mode:
            incremental_mode = mode
        dec = r.get("incremental_decision", "")
        if dec == "until_existing_anchor_found":
            anchor_found_sources += 1
        elif dec == "new_source_initial_baseline":
            new_source_baseline_sources += 1
        elif dec == "old_source_no_anchor":
            old_source_no_anchor_sources += 1
        selected_items_for_processing_total += int(r.get("selected_items_for_processing") or 0)
    return {
        "processed_sources": len(results),
        "successful_sources": len(success),
        "failed_sources": len(failed),
        "skipped_known_failed_sources": len(skipped),
        "total_items": sum(int(r.get("total_items") or 0) for r in success),
        "new_items": sum(int(r.get("new_items") or 0) for r in success),
        "duplicate_items": sum(int(r.get("duplicate_items") or 0) for r in success),
        "screened_items": sum(int(r.get("screened_items") or 0) for r in success),
        "recommended_items_from_api_response": sum(int(r.get("recommended_items_from_api_response") or 0) for r in success),
        "new_items_recommended": "unknown",
        "silent_items": sum(int(r.get("silent_items") or 0) for r in success),
        "failed_items": sum(int(r.get("failed_items") or 0) for r in success),
        "final_inbox_items_from_this_run": len(inbox_items),
        "full_push_items_from_this_run": int(stats.get("full_push", 0)),
        "incremental_push_items_from_this_run": int(stats.get("incremental_push", 0)),
        "inbox_query_mode": inbox.get("_query_mode", "unknown"),
        "inbox_query_fallback_used": bool(inbox.get("_fallback_used")),
        "incremental_mode": incremental_mode,
        "anchor_found_sources": anchor_found_sources,
        "new_source_baseline_sources": new_source_baseline_sources,
        "old_source_no_anchor_sources": old_source_no_anchor_sources,
        "selected_items_for_processing_total": selected_items_for_processing_total,
    }


def view_definitions(need_min_scores: Dict[str, int]) -> List[Dict[str, Any]]:
    return [
        {
            "title": "### 今天看什么娱乐\n",
            "key": "entertainment",
            "need_id": "entertainment",
            "min_need_score": need_min_scores.get("entertainment", 4),
        },
        {
            "title": "### 我关注的前沿咋样了\n",
            "key": "frontier",
            "need_id": "frontier",
            "min_need_score": need_min_scores.get("frontier", 4),
        },
        {
            "title": "### 我关心的话题议题有什么新的进展\n",
            "key": "watch_topic_update",
            "need_id": "watch_topic_update",
            "min_need_score": need_min_scores.get("watch_topic_update", 4),
        },
        {
            "title": "### 有什么是我值得看的\n",
            "key": "worth_reading",
            "need_id": "worth_reading",
            "min_need_score": need_min_scores.get("worth_reading", 4),
        },
    ]


def write_report(
    report_path: Path,
    selected: List[SourcePlan],
    results: List[Dict[str, Any]],
    notification_inbox: Dict[str, Any],
    reading_views: Dict[str, Dict[str, Any]],
    started_at: str,
    finished_at: str,
    url_mode: str,
    notes: List[str],
    need_min_scores: Dict[str, int],
) -> None:
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]
    stats = aggregate_stats(results, notification_inbox)

    lines: List[str] = []
    lines.append("# RSS 批量输入 content-inbox 运行报告\n")
    lines.append(f"- 开始时间：{started_at}")
    lines.append(f"- 结束时间：{finished_at}")
    lines.append(f"- 日期：{today_date()}")
    lines.append(f"- URL 模式：{url_mode}\n")

    lines.append("## 1. 总览\n")
    lines.append(f"- 选中 RSS 源数量：{len(selected)}")
    lines.append(f"- 已处理源数量：{stats['processed_sources']}")
    lines.append(f"- 成功源数量：{stats['successful_sources']}")
    lines.append(f"- 失败源数量：{stats['failed_sources']}")
    lines.append(f"- 已知失败跳过数量：{stats['skipped_known_failed_sources']}")
    lines.append(f"- total_items：{stats['total_items']}")
    lines.append(f"- new_items：{stats['new_items']}")
    lines.append(f"- duplicate_items：{stats['duplicate_items']}")
    lines.append(f"- screened_items：{stats['screened_items']}")
    lines.append(f"- recommended_items_from_api_response：{stats['recommended_items_from_api_response']}")
    lines.append(f"- new_items_recommended：{stats['new_items_recommended']}")
    lines.append(f"- final_inbox_items_from_this_run：{stats['final_inbox_items_from_this_run']}")
    lines.append(f"- full_push_items_from_this_run：{stats['full_push_items_from_this_run']}")
    lines.append(f"- incremental_push_items_from_this_run：{stats['incremental_push_items_from_this_run']}")
    lines.append(f"- silent_items：{stats['silent_items']}")
    lines.append(f"- failed_items：{stats['failed_items']}")
    lines.append(f"- inbox 查询模式：{stats['inbox_query_mode']}")
    lines.append(f"- inbox 是否回退到 date=today：{stats['inbox_query_fallback_used']}\n")

    # Incremental mode summary
    incremental_mode = stats.get("incremental_mode", "fixed_limit")
    lines.append("## 增量同步模式汇总\n")
    lines.append(f"- 同步模式：{incremental_mode}")
    if incremental_mode == "until_existing":
        lines.append(f"- 命中历史锚点的源数：{stats['anchor_found_sources']}")
        lines.append(f"- 新源基线同步数：{stats['new_source_baseline_sources']}")
        lines.append(f"- 老源未找到锚点数：{stats['old_source_no_anchor_sources']}")
        lines.append(f"- selected_items_for_processing 总计：{stats['selected_items_for_processing_total']}")
        old_source_no_anchor_list = [
            r for r in results
            if r.get("incremental_decision") == "old_source_no_anchor"
        ]
        if old_source_no_anchor_list:
            lines.append("\n**⚠️ 老源未找到锚点 (old_source_no_anchor) 的源列表：**\n")
            for r in old_source_no_anchor_list:
                lines.append(f"- **{md_escape(r.get('source_name'))}** ({md_escape(r.get('source_category'))}): {md_escape(r.get('incremental_warning', ''))}")
    lines.append("")

    lines.append("## 2. 统计口径说明\n")
    lines.append("- `recommended_items_from_api_response` 来自 `POST /api/rss/analyze` 聚合返回，可能受重复内容和服务端统计实现影响。")
    lines.append("- `new_items_recommended` 当前 API 没有稳定字段可精确区分“本次新增且被推荐”的数量，因此记为 `unknown`。")
    lines.append("- `final_inbox_items_from_this_run` / `full_push_items_from_this_run` / `incremental_push_items_from_this_run` 来自本次运行结束后 `GET /api/inbox?from=<run_started_at>` 的查询结果。")
    lines.append("- 四个阅读需求栏目使用独立的 `need_id` 查询，默认包含 silent / ignored 内容，不依赖通知决策。")
    if notes:
        for note in notes:
            lines.append(f"- {note}")
    lines.append("")

    lines.append("## 3. 各 RSS 源处理结果\n")
    lines.append("| # | 来源 | 分类 | 状态 | total | new | dup | screened | recommended_api | new_event | incremental | silent | failed | error_type |")
    lines.append("|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in results:
        lines.append(
            "| {sequence} | {source_name} | {source_category} | {status} | {total_items} | {new_items} | {duplicate_items} | {screened_items} | {recommended_items_from_api_response} | {new_event_items} | {incremental_items} | {silent_items} | {failed_items} | {error_type} |".format(
                sequence=r.get("sequence", ""),
                source_name=md_escape(r.get("source_name")),
                source_category=md_escape(r.get("source_category")),
                status=md_escape(r.get("status")),
                total_items=r.get("total_items", 0),
                new_items=r.get("new_items", 0),
                duplicate_items=r.get("duplicate_items", 0),
                screened_items=r.get("screened_items", 0),
                recommended_items_from_api_response=r.get("recommended_items_from_api_response", 0),
                new_event_items=r.get("new_event_items", 0),
                incremental_items=r.get("incremental_items", 0),
                silent_items=r.get("silent_items", 0),
                failed_items=r.get("failed_items", 0),
                error_type=md_escape(r.get("error_type", "")),
            )
        )
    lines.append("")

    lines.append("## 4. 阅读视图\n")
    for view in view_definitions(need_min_scores):
        lines.append(view["title"])
        view_items = extract_items(reading_views.get(view["key"], {}))
        if not view_items:
            lines.append("无\n")
            continue
        for item in view_items[:30]:
            lines.append(item_line(item, need_id=view["need_id"]))
            lines.append("")

    lines.append("### 系统通知推荐\n")
    notification_items = extract_items(notification_inbox)
    if not notification_items:
        lines.append("无\n")
    else:
        for item in notification_items[:30]:
            lines.append(item_line(item))
            lines.append("")

    lines.append("## 5. 失败源列表\n")
    if not failed:
        lines.append("无\n")
    else:
        for r in failed:
            lines.append(f"- **{md_escape(r.get('source_name'))}**")
            lines.append(f"  - 分类：{md_escape(r.get('source_category'))}")
            lines.append(f"  - local_xml_url：{r.get('local_xml_url') or '-'}")
            lines.append(f"  - xml_url：{r.get('xml_url') or '-'}")
            lines.append(f"  - final feed_url：{r.get('feed_url')}")
            lines.append(f"  - error_type：{md_escape(r.get('error_type'))}")
            lines.append(f"  - error_message：{md_escape(r.get('error_message'))}")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def save_run_artifacts(
    run_dir: Path,
    plans: List[SourcePlan],
    results: List[Dict[str, Any]],
    notification_inbox: Dict[str, Any],
    reading_views: Dict[str, Dict[str, Any]],
    started_at: str,
    url_mode: str,
    state_status: str,
    args_snapshot: Dict[str, Any],
    consecutive_failures: int,
    notes: List[str],
    need_min_scores: Dict[str, int],
) -> None:
    selected_rows = build_selected_rows(plans)
    source_results_path = run_dir / "source_results.csv"
    failed_sources_path = run_dir / "failed_sources.csv"
    report_path = run_dir / "report.md"
    run_state_path = run_dir / "run_state.json"

    write_csv_rows(run_dir / "selected_sources.csv", selected_csv_headers(), selected_rows)
    write_csv_rows(source_results_path, results_csv_headers(), results)
    write_csv_rows(
        failed_sources_path,
        ["source_name", "source_category", "local_xml_url", "xml_url", "feed_url", "error_message", "error_type"],
        build_failed_rows(results),
    )
    write_report(
        report_path=report_path,
        selected=plans,
        results=results,
        notification_inbox=notification_inbox,
        reading_views=reading_views,
        started_at=started_at,
        finished_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        url_mode=url_mode,
        notes=notes,
        need_min_scores=need_min_scores,
    )

    completed_source_ids = [r["source_id"] for r in results if r.get("status") in {"success", "failed", "skipped_known_failed"}]
    successful_source_ids = [r["source_id"] for r in results if r.get("status") == "success"]
    run_state = {
        "schema_version": 2,
        "status": state_status,
        "started_at": started_at,
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "args": args_snapshot,
        "url_mode": url_mode,
        "selected_count": len(plans),
        "completed_count": len(completed_source_ids),
        "successful_count": len(successful_source_ids),
        "failed_count": len([r for r in results if r.get("status") == "failed"]),
        "consecutive_failures": consecutive_failures,
        "completed_source_ids": completed_source_ids,
        "successful_source_ids": successful_source_ids,
        "notes": notes,
    }
    run_state_path.write_text(json.dumps(run_state, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = {
        "schema_version": 1,
        "source_mode": args_snapshot.get("source_mode", "csv"),
        "started_at": started_at,
        "updated_at": run_state["updated_at"],
        "selected_count": len(plans),
        "completed_count": len(completed_source_ids),
        "successful_count": len(successful_source_ids),
        "failed_count": run_state["failed_count"],
    }
    (run_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_count(value: str) -> Optional[int]:
    if value.lower() == "all":
        return None
    return int(value)


def load_known_failed_ids(runs_dir: Path, current_run_dir: Path) -> set[str]:
    failed_ids: set[str] = set()
    for path in sorted(runs_dir.glob(f"{RUN_PREFIX}*/failed_sources.csv")):
        rows = read_csv_rows(path)
        for row in rows:
            source_name = row.get("source_name", "")
            source_category = row.get("source_category", "")
            local_xml_url = row.get("local_xml_url", "")
            xml_url = row.get("xml_url", "")
            feed_url = row.get("feed_url", "")
            failed_ids.add(
                json.dumps(
                    {
                        "row_index": None,
                        "source_name": source_name,
                        "source_category": source_category,
                        "local_xml_url": local_xml_url,
                        "xml_url": xml_url,
                        "feed_url": feed_url,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
    current_failed = current_run_dir / "failed_sources.csv"
    for row in read_csv_rows(current_failed):
        failed_ids.add(
            json.dumps(
                {
                    "row_index": None,
                    "source_name": row.get("source_name", ""),
                    "source_category": row.get("source_category", ""),
                    "local_xml_url": row.get("local_xml_url", ""),
                    "xml_url": row.get("xml_url", ""),
                    "feed_url": row.get("feed_url", ""),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return failed_ids


def build_known_failed_aliases(source: Source, feed_url: str) -> set[str]:
    return {
        build_source_id(source, feed_url),
        json.dumps(
            {
                "row_index": None,
                "source_name": source.source_name,
                "source_category": source.source_category,
                "local_xml_url": source.local_xml_url,
                "xml_url": source.xml_url,
                "feed_url": feed_url,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Submit RSS sources to content-inbox and generate resumable reports.")
    parser.add_argument("--api-base", default=os.getenv("CONTENT_INBOX_API_BASE", "http://127.0.0.1:8787"))
    parser.add_argument("--api-key", default=os.getenv("CONTENT_INBOX_API_KEY", ""))
    parser.add_argument("--source-mode", choices=["csv", "registry"], default="csv", help="Read sources from CSV or the registered RSS source API.")
    parser.add_argument("--csv", default="", help="Path to rss_sources.csv. Default: rsshub/rss_opml/rss_sources.csv")
    parser.add_argument("--count", default="50", help="Number of enabled RSS sources to select, or 'all'.")
    parser.add_argument("--all", action="store_true", help="Process all enabled RSS sources.")
    parser.add_argument("--max-sources", type=int, default=None, help="Maximum number of selected sources to process.")
    parser.add_argument("--limit-per-source", type=int, default=20, help="Item limit for each RSS source.")
    parser.add_argument("--screen", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--profile", action="store_true", help="Enable per-source profiling in source_results.csv.")
    parser.add_argument("--audit-prompt", action="store_true", help="Enable prompt audit mode: assemble prompts without calling LLM and write prompt_audit.jsonl.")
    parser.add_argument("--dump-llm-prompt", action="store_true", help="Dump complete LLM request bodies to files. Real API calls are made.")
    parser.add_argument("--dump-llm-prompt-dir", default="", help="Output directory for LLM prompt dumps. Default: <run_dir>/llm_prompt_dumps/")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep seconds between sources.")
    parser.add_argument(
        "--concurrency",
        "--max-concurrent-sources",
        dest="concurrency",
        type=int,
        default=1,
        help="Maximum number of RSS sources to process concurrently. Default: 1.",
    )
    parser.add_argument(
        "--llm-max-concurrency",
        type=int,
        default=None,
        help="Set the content-inbox service LLM max concurrency at runtime via POST /api/runtime/llm-concurrency before processing sources. Default: leave unchanged.",
    )
    parser.add_argument(
        "--screening-mode",
        choices=["two_stage", "merged"],
        default=None,
        help="Set the content-inbox service screening mode at runtime via POST /api/runtime/screening-mode before processing sources. Default: leave unchanged.",
    )
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout seconds for each source.")
    parser.add_argument("--inbox-limit", type=int, default=100)
    parser.add_argument("--output-dir", default="", help="Default: content_inbox/outputs")
    parser.add_argument("--url-mode", choices=["auto", "remote", "docker-host", "compose-service"], default="docker-host")
    parser.add_argument("--rsshub-service-name", default="rsshub")
    parser.add_argument("--dry-run", action="store_true", help="Only print selected sources; do not call API.")
    parser.add_argument("--resume", action="store_true", help="Resume from the latest unfinished run.")
    parser.add_argument("--skip-known-failed", action="store_true", help="Skip sources that already failed in current/history runs.")
    parser.add_argument("--max-consecutive-failures", type=int, default=20)
    parser.add_argument(
        "--incremental-mode",
        choices=["fixed_limit", "until_existing"],
        default="fixed_limit",
        help="RSS incremental mode. fixed_limit=current behavior (process first N items). "
        "until_existing=scan until finding an existing anchor item.",
    )
    parser.add_argument(
        "--probe-limit",
        type=int,
        default=20,
        help="Max items to scan for an anchor in until_existing mode.",
    )
    parser.add_argument(
        "--new-source-initial-limit",
        type=int,
        default=5,
        help="Max items to process for a new source in until_existing mode.",
    )
    parser.add_argument(
        "--old-source-no-anchor-limit",
        type=int,
        default=20,
        help="Max items to process for an old source with no anchor found in until_existing mode.",
    )
    parser.add_argument(
        "--stop-on-first-existing",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Stop scanning when first existing item is found (until_existing mode).",
    )
    args = parser.parse_args()
    if args.concurrency < 1:
        parser.error("--concurrency must be >= 1")
    return args


def main() -> int:
    base_stdout = sys.stdout
    base_stderr = sys.stderr
    if hasattr(base_stdout, "reconfigure"):
        base_stdout.reconfigure(line_buffering=True)
    if hasattr(base_stderr, "reconfigure"):
        base_stderr.reconfigure(line_buffering=True)

    args = parse_args()
    if args.all and args.count.lower() != "50":
        print("[ERROR] --all and --count cannot be used together when --count is not the default 50.", file=base_stderr)
        return 2
    if args.all and args.max_sources is not None:
        print("[ERROR] --all and --max-sources cannot be used together.", file=base_stderr)
        return 2

    repo_root = find_repo_root(Path.cwd())
    csv_path = Path(args.csv).expanduser()
    if not args.csv:
        csv_path = repo_root / "rsshub" / "rss_opml" / "rss_sources.csv"
    elif not csv_path.is_absolute():
        csv_path = repo_root / csv_path

    output_dir = Path(args.output_dir).expanduser()
    if not args.output_dir:
        output_dir = repo_root / "content_inbox" / "outputs"
    elif not output_dir.is_absolute():
        output_dir = repo_root / output_dir
    runs_dir = output_dir / RUNS_DIRNAME
    runs_dir.mkdir(parents=True, exist_ok=True)

    run_dir: Path
    existing_state: Dict[str, Any] = {}
    if args.resume:
        latest = latest_run_dir(runs_dir)
        if latest is None:
            print("[ERROR] --resume requested but no prior run_state.json was found.", file=base_stderr)
            return 2
        run_dir = latest
        existing_state = load_run_state(run_dir / "run_state.json")
    else:
        run_dir = runs_dir / f"{RUN_PREFIX}{now_stamp()}"
        run_dir.mkdir(parents=True, exist_ok=True)

    log_path = run_dir / "stdout.log"
    log_file = log_path.open("a", encoding="utf-8")
    sys.stdout = TeeStream(base_stdout, log_file)
    sys.stderr = TeeStream(base_stderr, log_file)

    api_key = args.api_key or None
    count_value = None if args.all else parse_count(args.count)
    registry_limit = args.max_sources or count_value or 500
    try:
        if args.source_mode == "registry":
            sources = read_registry_sources(args.api_base, api_key, args.timeout, limit=int(registry_limit))
        else:
            sources = read_sources(csv_path)
    except Exception as e:
        print(f"[ERROR] Failed to read RSS sources: {e}", file=sys.stderr, flush=True)
        return 2

    selected_sources = sources if count_value is None else select_sources(sources, count_value)
    if args.max_sources is not None:
        selected_sources = selected_sources[: args.max_sources]

    plans: List[SourcePlan] = []
    for idx, source in enumerate(selected_sources, start=1):
        feed_url, url_source = resolve_feed_url(source, args.url_mode, args.rsshub_service_name)
        plans.append(
            SourcePlan(
                sequence=idx,
                source=source,
                feed_url=feed_url,
                url_mode=args.url_mode,
                url_source=url_source,
                source_id=source.raw.get("source_id") if args.source_mode == "registry" and source.raw.get("source_id") else build_source_id(source, feed_url),
                screen=args.screen,
            )
        )

    previous_results = read_csv_rows(run_dir / "source_results.csv") if args.resume else []
    results: List[Dict[str, Any]] = []
    results_by_id = {row.get("source_id", ""): row for row in previous_results if row.get("source_id")}
    completed_source_ids = set(existing_state.get("completed_source_ids", [])) if args.resume else set()

    known_failed_ids = load_known_failed_ids(runs_dir, run_dir) if args.skip_known_failed else set()
    skipped_known_failed = 0
    for plan in plans:
        if plan.source_id in results_by_id:
            results.append(results_by_id[plan.source_id])
            continue
        if args.skip_known_failed and any(alias in known_failed_ids for alias in build_known_failed_aliases(plan.source, plan.feed_url)):
            results.append(
                {
                    "source_id": plan.source_id,
                    "sequence": plan.sequence,
                    "source_name": plan.source.source_name,
                    "source_category": plan.source.source_category,
                    "local_xml_url": plan.source.local_xml_url,
                    "xml_url": plan.source.xml_url,
                    "feed_url": plan.feed_url,
                    "url_mode": plan.url_mode,
                    "screen": plan.screen,
                    "status": "skipped_known_failed",
                    "total_items": 0,
                    "new_items": 0,
                    "duplicate_items": 0,
                    "screened_items": 0,
                    "recommended_items_from_api_response": 0,
                    "new_items_recommended": "unknown",
                    "new_event_items": 0,
                    "incremental_items": 0,
                    "silent_items": 0,
                    "failed_items": 0,
                    "error_type": "skipped_known_failed",
                    "error_message": "Skipped because this source already failed in a prior run.",
                }
            )
            skipped_known_failed += 1

    seen_result_ids = {r["source_id"] for r in results if r.get("source_id")}
    pending_plans = [plan for plan in plans if plan.source_id not in seen_result_ids and plan.source_id not in completed_source_ids]
    results.extend([results_by_id[source_id] for source_id in completed_source_ids if source_id in results_by_id and source_id not in seen_result_ids])
    results.sort(key=lambda row: int(row.get("sequence") or 0))

    llm_max_concurrency_applied: Optional[int] = None
    runtime_config_set_ok: Optional[bool] = None

    args_snapshot = {
        "api_base": args.api_base,
        "source_mode": args.source_mode,
        "csv": str(csv_path),
        "count": args.count,
        "all": args.all,
        "max_sources": args.max_sources,
        "limit_per_source": args.limit_per_source,
        "screen": args.screen,
        "sleep": args.sleep,
        "concurrency": args.concurrency,
        "llm_max_concurrency_requested": args.llm_max_concurrency,
        "llm_max_concurrency_applied": llm_max_concurrency_applied,
        "runtime_config_set_ok": runtime_config_set_ok,
        "timeout": args.timeout,
        "inbox_limit": args.inbox_limit,
        "url_mode": args.url_mode,
        "rsshub_service_name": args.rsshub_service_name,
        "dry_run": args.dry_run,
        "resume": args.resume,
        "skip_known_failed": args.skip_known_failed,
        "max_consecutive_failures": args.max_consecutive_failures,
        "incremental_mode": args.incremental_mode,
        "probe_limit": args.probe_limit,
        "new_source_initial_limit": args.new_source_initial_limit,
        "old_source_no_anchor_limit": args.old_source_no_anchor_limit,
        "stop_on_first_existing": args.stop_on_first_existing,
    }
    started_at = existing_state.get("started_at") if args.resume and existing_state.get("started_at") else dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    notes: List[str] = []
    need_min_scores = load_reading_need_min_scores(repo_root)
    if skipped_known_failed:
        notes.append(f"本次因 --skip-known-failed 跳过 {skipped_known_failed} 个已知失败源。")
    if args.resume:
        notes.append(f"本次使用 --resume，继续运行目录：{run_dir}")

    health = request_json("GET", f"{args.api_base.rstrip('/')}/health", timeout=30, api_key=api_key)
    if health.get("ok") is False or (health.get("_status") is not None and int(health.get("_status")) >= 400):
        print(f"[ERROR] content-inbox health check failed: {json.dumps(health, ensure_ascii=False)}", file=sys.stderr, flush=True)
        return 3

    print(f"[INFO] Run dir: {run_dir}", flush=True)
    print(f"[INFO] Source mode: {args.source_mode}", flush=True)
    if args.source_mode == "csv":
        print(f"[INFO] CSV: {csv_path}", flush=True)
    print(f"[INFO] Enabled candidate sources: {len(sources)}", flush=True)
    print(f"[INFO] Selected sources: {len(plans)}", flush=True)
    print(f"[INFO] Pending sources this invocation: {len(pending_plans)}", flush=True)
    print(f"[INFO] URL mode: {args.url_mode}", flush=True)
    print(f"[INFO] Screen enabled: {args.screen}", flush=True)
    print(f"[INFO] Concurrency: {args.concurrency}", flush=True)
    print(f"[INFO] content-inbox health OK: {json.dumps(health, ensure_ascii=False)}", flush=True)

    # -- Runtime LLM concurrency configuration
    if args.llm_max_concurrency is not None:
        if args.dry_run:
            print(
                f"[INFO] Dry run: --llm-max-concurrency={args.llm_max_concurrency} would be applied, "
                "but not modifying runtime concurrency.",
                flush=True,
            )
            llm_max_concurrency_applied = None
            runtime_config_set_ok = None
        else:
            print(
                f"[INFO] Setting service LLM max concurrency to {args.llm_max_concurrency} ...",
                flush=True,
            )
            result = set_llm_max_concurrency(
                args.api_base, args.llm_max_concurrency, api_key, timeout=30
            )
            if result.get("ok") and result.get("_status") in (200, None):
                llm_max_concurrency_applied = result.get("llm_max_concurrency")
                runtime_config_set_ok = True
                print(
                    f"[INFO] Service LLM max concurrency set to {llm_max_concurrency_applied}",
                    flush=True,
                )
            else:
                runtime_config_set_ok = False
                err = result.get("error", result.get("detail", json.dumps(result, ensure_ascii=False)))
                print(
                    f"[ERROR] Failed to set service LLM max concurrency: {err}",
                    file=sys.stderr,
                    flush=True,
                )
                return 4

    # Update args_snapshot with actual runtime values (set after the runtime call)
    args_snapshot["llm_max_concurrency_applied"] = llm_max_concurrency_applied
    args_snapshot["runtime_config_set_ok"] = runtime_config_set_ok

    # -- Runtime screening mode configuration
    screening_mode_applied: Optional[str] = None
    runtime_screening_mode_set_ok: Optional[bool] = None
    if args.screening_mode is not None:
        if args.dry_run:
            print(
                f"[INFO] Dry run: --screening-mode={args.screening_mode} would be applied, "
                "but not modifying runtime screening mode.",
                flush=True,
            )
        else:
            print(
                f"[INFO] Setting service screening mode to {args.screening_mode} ...",
                flush=True,
            )
            result = set_screening_mode(
                args.api_base, args.screening_mode, api_key, timeout=30
            )
            if result.get("ok") and result.get("_status") in (200, None):
                screening_mode_applied = result.get("screening_mode")
                runtime_screening_mode_set_ok = True
                print(
                    f"[INFO] Service screening mode set to {screening_mode_applied}",
                    flush=True,
                )
            else:
                runtime_screening_mode_set_ok = False
                err = result.get("error", result.get("detail", json.dumps(result, ensure_ascii=False)))
                print(
                    f"[ERROR] Failed to set service screening mode: {err}",
                    file=sys.stderr,
                    flush=True,
                )
                return 4

    args_snapshot["screening_mode_requested"] = args.screening_mode
    args_snapshot["screening_mode_applied"] = screening_mode_applied
    args_snapshot["runtime_screening_mode_set_ok"] = runtime_screening_mode_set_ok

    notes.append(
        f"source concurrency={args.concurrency}, "
        f"llm_max_concurrency_requested={args.llm_max_concurrency}, "
        f"llm_max_concurrency_applied={llm_max_concurrency_applied}, "
        f"screening_mode_requested={args.screening_mode}, "
        f"screening_mode_applied={screening_mode_applied}, "
        f"timeout={args.timeout}, "
        f"sleep={args.sleep}, "
        f"limit_per_source={args.limit_per_source}"
    )

    if args.dump_llm_prompt:
        dump_dir = args.dump_llm_prompt_dir or str(run_dir / "llm_prompt_dumps")
        args.dump_llm_prompt_dir = dump_dir
        Path(dump_dir).mkdir(parents=True, exist_ok=True)
        print(f"[PROMPT_DUMP] Dump directory: {dump_dir}", flush=True)

    write_csv_rows(run_dir / "selected_sources.csv", selected_csv_headers(), build_selected_rows(plans))

    if args.dry_run:
        print("[INFO] Selected source preview:", flush=True)
        for plan in plans:
            print(
                f"  {plan.sequence:03d}. [{plan.source.source_category or 'Uncategorized'}] {plan.source.source_name} "
                f"({plan.url_source}) -> {plan.feed_url}",
                flush=True,
            )
        print(f"[INFO] Dry run concurrency: {args.concurrency}", flush=True)
        notification_inbox = {"ok": True, "items": [], "stats": {}, "_query_mode": "not_run"}
        reading_views = {
            view["key"]: {"ok": True, "items": [], "stats": {}, "_query_mode": "not_run"}
            for view in view_definitions(need_min_scores)
        }
        save_run_artifacts(
            run_dir,
            plans,
            results,
            notification_inbox,
            reading_views,
            started_at,
            args.url_mode,
            "dry_run",
            args_snapshot,
            0,
            notes,
            need_min_scores,
        )
        print(f"[INFO] Dry run finished. No API calls were made. Report path: {run_dir / 'report.md'}", flush=True)
        return 0

    notification_inbox: Dict[str, Any] = {"ok": True, "items": [], "stats": {}, "_query_mode": "pending"}
    reading_views: Dict[str, Dict[str, Any]] = {
        view["key"]: {"ok": True, "items": [], "stats": {}, "_query_mode": "pending"}
        for view in view_definitions(need_min_scores)
    }
    consecutive_failures = int(existing_state.get("consecutive_failures", 0)) if args.resume else 0
    save_run_artifacts(
        run_dir,
        plans,
        results,
        notification_inbox,
        reading_views,
        started_at,
        args.url_mode,
        "running",
        args_snapshot,
        consecutive_failures,
        notes,
        need_min_scores,
    )

    results_by_source_id = {row["source_id"]: row for row in results if row.get("source_id")}
    pending_queue = list(pending_plans)
    in_flight: Dict[Future[Dict[str, Any]], SourcePlan] = {}
    stop_submitting = False
    stop_reason_recorded = False

    def ordered_results() -> List[Dict[str, Any]]:
        return [results_by_source_id[p.source_id] for p in plans if p.source_id in results_by_source_id]

    def save_progress(state_status: str) -> None:
        save_run_artifacts(
            run_dir,
            plans,
            ordered_results(),
            notification_inbox,
            reading_views,
            started_at,
            args.url_mode,
            state_status,
            args_snapshot,
            consecutive_failures,
            notes,
            need_min_scores,
        )

    def submit_next(executor: ThreadPoolExecutor) -> bool:
        nonlocal stop_submitting
        if stop_submitting or not pending_queue:
            return False
        plan = pending_queue.pop(0)
        print(f"[SUBMIT] {plan.sequence:03d}/{len(plans):03d} {plan.source.source_name}", flush=True)
        print(f"         category={plan.source.source_category or '-'} feed_url={plan.feed_url}", flush=True)
        future = executor.submit(run_one_plan, plan, args, api_key)
        in_flight[future] = plan
        if args.sleep > 0 and pending_queue:
            time.sleep(args.sleep)
        return True

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        while len(in_flight) < args.concurrency and pending_queue and not stop_submitting:
            submit_next(executor)

        while in_flight:
            done, _ = wait(set(in_flight.keys()), return_when=FIRST_COMPLETED)
            for future in done:
                plan = in_flight.pop(future)
                try:
                    result = future.result()
                except Exception as exc:
                    result = {
                        "source_id": plan.source_id,
                        "sequence": plan.sequence,
                        "source_name": plan.source.source_name,
                        "source_category": plan.source.source_category,
                        "local_xml_url": plan.source.local_xml_url,
                        "xml_url": plan.source.xml_url,
                        "feed_url": plan.feed_url,
                        "url_mode": plan.url_mode,
                        "screen": plan.screen,
                        "status": "failed",
                        "total_items": 0,
                        "new_items": 0,
                        "duplicate_items": 0,
                        "screened_items": 0,
                        "recommended_items_from_api_response": 0,
                        "new_items_recommended": "unknown",
                        "new_event_items": 0,
                        "incremental_items": 0,
                        "silent_items": 0,
                        "failed_items": 0,
                        "error_type": "worker_error",
                        "error_message": str(exc),
                    }

                results_by_source_id[plan.source_id] = result

                if result["status"] == "failed":
                    consecutive_failures += 1
                    print(
                        f"[DONE] {plan.sequence:03d}/{len(plans):03d} {plan.source.source_name} "
                        f"status=failed error_type={result.get('error_type', '')} "
                        f"error_message={result.get('error_message', '')}",
                        flush=True,
                    )
                elif result["status"] == "audited":
                    print(
                        f"[DONE] {plan.sequence:03d}/{len(plans):03d} {plan.source.source_name} "
                        f"status=audited total_items={result.get('total_items', 0)} "
                        f"prompts_audited={result.get('total_prompts', 0)}",
                        flush=True,
                    )
                else:
                    consecutive_failures = 0
                    print(
                        f"[DONE] {plan.sequence:03d}/{len(plans):03d} {plan.source.source_name} "
                        f"status=success total_items={result.get('total_items', 0)} "
                        f"new_items={result.get('new_items', 0)} duplicate_items={result.get('duplicate_items', 0)}",
                        flush=True,
                    )

                save_progress("running")

                if consecutive_failures >= args.max_consecutive_failures:
                    stop_submitting = True
                    if not stop_reason_recorded:
                        notes.append(f"连续失败达到阈值 {args.max_consecutive_failures}，提前停止运行。")
                        stop_reason_recorded = True

            while len(in_flight) < args.concurrency and pending_queue and not stop_submitting:
                submit_next(executor)

    if stop_submitting and consecutive_failures >= args.max_consecutive_failures:
        save_progress("stopped_consecutive_failures")
        print(f"[ERROR] Consecutive failures reached {args.max_consecutive_failures}. Stopping new submissions.", file=sys.stderr, flush=True)
        return 4

    if args.audit_prompt:
        ordered = ordered_results()
        all_records: list[Dict[str, Any]] = []
        for result in ordered:
            records = result.pop("_audit_records", [])
            all_records.extend(records)
            status = result.get("status", "")
            source_name = result.get("source_name", "")
            feed_url = result.get("feed_url", "")
            seq = result.get("sequence", "")
            prompts = result.get("total_prompts", 0)
            print(
                f"[AUDIT] source={source_name} feed={feed_url} seq={seq} "
                f"status={status} prompts={prompts}",
                flush=True,
            )
        for record in all_records:
            print(f"[PROMPT_AUDIT] {json.dumps(record, ensure_ascii=False)}", flush=True)
        prompt_audit_path = run_dir / "prompt_audit.jsonl"
        with prompt_audit_path.open("w", encoding="utf-8") as f:
            for record in all_records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"[AUDIT] Total prompt audit records: {len(all_records)}", flush=True)
        print(f"[AUDIT] prompt_audit.jsonl written to {prompt_audit_path}", flush=True)
        print("[AUDIT] Audit mode complete. No LLM calls were made. No data was stored.", flush=True)
        return 0

    if args.dump_llm_prompt:
        dump_dir = args.dump_llm_prompt_dir
        dump_files = sorted(Path(dump_dir).glob("*.json"))
        print(f"[PROMPT_DUMP] {len(dump_files)} request body dumps written to {dump_dir}", flush=True)
        for f in dump_files:
            print(f"[PROMPT_DUMP]   {f.name}", flush=True)

    ordered_results = ordered_results()
    notification_inbox = query_inbox(
        args.api_base,
        api_key=api_key,
        timeout=args.timeout,
        limit=args.inbox_limit,
        from_time=started_at,
    )
    if notification_inbox.get("_query_mode") == "date":
        notes.append("`from=<run_started_at>` 查询未稳定生效，已回退到 `date=today`。")
    reading_views = {
        view["key"]: query_inbox_view(
            args.api_base,
            api_key,
            args.timeout,
            need_id=view["need_id"],
            min_need_score=view["min_need_score"],
            limit=args.inbox_limit,
            from_time=started_at,
        )
        for view in view_definitions(need_min_scores)
    }

    state_status = "completed"
    if any(r.get("status") == "failed" for r in ordered_results):
        state_status = "completed_with_failures"
    save_run_artifacts(
        run_dir,
        plans,
        ordered_results,
        notification_inbox,
        reading_views,
        started_at,
        args.url_mode,
        state_status,
        args_snapshot,
        consecutive_failures,
        notes,
        need_min_scores,
    )

    stats = aggregate_stats(ordered_results, notification_inbox)
    print("\n[SUMMARY]", flush=True)
    print(f"Processed sources: {stats['processed_sources']}", flush=True)
    print(f"Successful sources: {stats['successful_sources']}", flush=True)
    print(f"Failed sources: {stats['failed_sources']}", flush=True)
    print(f"Skipped known failed sources: {stats['skipped_known_failed_sources']}", flush=True)
    print(f"New items: {stats['new_items']}", flush=True)
    print(f"Recommended items from API responses: {stats['recommended_items_from_api_response']}", flush=True)
    print(f"Final inbox items from this run: {stats['final_inbox_items_from_this_run']}", flush=True)
    print(f"Report path: {run_dir / 'report.md'}", flush=True)
    print(f"Run state path: {run_dir / 'run_state.json'}", flush=True)

    if stats["failed_sources"]:
        print("\n[FAILED SOURCES]", flush=True)
        for r in ordered_results:
            if r.get("status") == "failed":
                print(f"- {r['source_name']} | {r['feed_url']} | {r['error_type']} | {r['error_message']}", flush=True)

    inbox_items = extract_items(notification_inbox)
    if inbox_items:
        print("\n[TOP INBOX ITEMS]", flush=True)
        for item in inbox_items[:10]:
            title = item.get("title") or get_nested(item, "normalized", "title") or "未命名"
            source = item.get("source_name") or get_nested(item, "normalized", "source_name") or ""
            screening = item.get("screening") or {}
            clustering = item.get("clustering") or {}
            score = screening.get("value_score", "")
            decision = clustering.get("notification_decision", item.get("notification_decision", ""))
            print(f"- [{score}] [{decision}] {title} — {source}", flush=True)

    return 0 if stats["failed_sources"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
