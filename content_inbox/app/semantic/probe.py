from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

from app.storage import InboxStore


def _backup_db(db_path: Path, *, reason: str = "backup") -> Path:
    backup_dir = db_path.parent / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if reason:
        backup = backup_dir / f"{db_path.name}.{reason}_{ts}.sqlite3"
    else:
        backup = backup_dir / f"{db_path.stem}.backup.{ts}.sqlite3"
    shutil.copy2(str(db_path), str(backup))
    return backup


def probe_source_scope(store: InboxStore, source_url_prefix: str) -> dict[str, Any]:
    search = f"%{source_url_prefix}%"
    clean = source_url_prefix.removeprefix("https://").removeprefix("http://")
    clean_search = f"%{clean}%"

    with store.connect() as conn:
        conn.row_factory = None
        # 1. Find matching rss_sources
        src_rows = conn.execute(
            """
            SELECT source_id, source_name, source_category, feed_url, status,
                   last_success_at, last_failure_at, failure_count, last_error_message,
                   last_ingest_at
            FROM rss_sources
            WHERE feed_url LIKE ?
               OR normalized_feed_url LIKE ?
               OR feed_url LIKE ?
               OR normalized_feed_url LIKE ?
               OR source_id LIKE ?
               OR source_name LIKE ?
            ORDER BY feed_url, source_id
            """,
            (search, search, clean_search, clean_search, search, search),
        ).fetchall()

        # 2. For each matched source, count items
        source_details = []
        total_items_via_join = 0
        total_items_via_direct = 0
        source_ids_matched = []

        for row in src_rows:
            src_id = row[0]
            src_name = row[1]
            src_cat = row[2]
            feed_url = row[3]
            status = row[4] or "unknown"

            source_ids_matched.append(src_id)

            # Count items via source_id join
            item_by_source_id = conn.execute(
                "SELECT COUNT(*) FROM inbox_items WHERE source_id = ?", (src_id,)
            ).fetchone()[0]

            # Count items via name+category fallback (for items with NULL source_id)
            if src_cat:
                item_by_name_cat = conn.execute(
                    "SELECT COUNT(*) FROM inbox_items WHERE source_name = ? AND source_category = ? AND (source_id IS NULL OR source_id = '')",
                    (src_name, src_cat),
                ).fetchone()[0]
            else:
                item_by_name_cat = conn.execute(
                    "SELECT COUNT(*) FROM inbox_items WHERE source_name = ? AND (source_category IS NULL OR source_category = '') AND (source_id IS NULL OR source_id = '')",
                    (src_name,),
                ).fetchone()[0]

            item_total = item_by_source_id + item_by_name_cat
            total_items_via_join += item_total
            latest_item_time = conn.execute(
                """
                SELECT MAX(COALESCE(published_at, created_at)) FROM inbox_items
                WHERE source_id = ?
                """,
                (src_id,),
            ).fetchone()[0]
            missing_source_id = conn.execute(
                """
                SELECT COUNT(*) FROM inbox_items
                WHERE source_name = ?
                  AND (? IS NULL OR source_category = ?)
                  AND (source_id IS NULL OR source_id = '')
                """,
                (src_name, src_cat, src_cat),
            ).fetchone()[0]
            missing_feed_url = conn.execute(
                """
                SELECT COUNT(*) FROM inbox_items
                WHERE source_name = ?
                  AND (? IS NULL OR source_category = ?)
                  AND (feed_url IS NULL OR feed_url = '')
                """,
                (src_name, src_cat, src_cat),
            ).fetchone()[0]

            source_details.append({
                "source_id": src_id,
                "source_name": src_name,
                "source_category": src_cat,
                "feed_url": feed_url,
                "source_name_has_html_entities": unescape(src_name or "") != (src_name or ""),
                "status": status,
                "last_success_at": row[5],
                "last_failure_at": row[6],
                "failure_count": row[7],
                "last_error_message": row[8],
                "last_ingest_at": row[9],
                "latest_item_time": latest_item_time,
                "item_count_by_source_id": item_by_source_id,
                "item_count_by_name_category": item_by_name_cat,
                "item_count_total": item_total,
                "missing_source_id_items": missing_source_id,
                "missing_feed_url_items": missing_feed_url,
            })

        # 3. Also count items via direct LIKE search (old behavior)
        if source_ids_matched:
            id_placeholders = ",".join("?" for _ in source_ids_matched)
            direct_count = conn.execute(
                f"""
                SELECT COUNT(*) FROM inbox_items
                WHERE source_id IN ({id_placeholders})
                   OR feed_url LIKE ?
                   OR url LIKE ?
                """,
                (*source_ids_matched, search, search),
            ).fetchone()[0]
        else:
            direct_count = conn.execute(
                "SELECT COUNT(*) FROM inbox_items WHERE feed_url LIKE ? OR url LIKE ? OR source_name LIKE ?",
                (search, search, search),
            ).fetchone()[0]
        total_items_via_direct = direct_count

        # 4. Global NULL stats
        total_items = conn.execute("SELECT COUNT(*) FROM inbox_items").fetchone()[0]
        null_source_id = conn.execute(
            "SELECT COUNT(*) FROM inbox_items WHERE source_id IS NULL OR source_id = ''"
        ).fetchone()[0]
        null_feed_url = conn.execute(
            "SELECT COUNT(*) FROM inbox_items WHERE feed_url IS NULL OR feed_url = ''"
        ).fetchone()[0]
        total_rss_sources = conn.execute("SELECT COUNT(*) FROM rss_sources").fetchone()[0]
        latest_scope_time = None
        if source_ids_matched:
            id_placeholders = ",".join("?" for _ in source_ids_matched)
            latest_scope_time = conn.execute(
                f"SELECT MAX(COALESCE(published_at, created_at)) FROM inbox_items WHERE source_id IN ({id_placeholders})",
                source_ids_matched,
            ).fetchone()[0]

        # 5. Diagnose
        diagnostics = []
        if len(source_details) == 0:
            diagnostics.append({
                "severity": "error",
                "case": "C",
                "message": (
                    f"No sources registered in rss_sources match '{source_url_prefix}'. "
                    f"Verify the prefix or register the source first."
                ),
            })
        elif total_items_via_join == 0:
            diagnostics.append({
                "severity": "warning",
                "case": "A",
                "message": (
                    f"{len(source_details)} source(s) matched but have zero items. "
                    f"Run ingest to fetch items."
                ),
            })
        else:
            if total_items_via_direct < total_items_via_join:
                diagnostics.append({
                    "severity": "info",
                    "case": "B",
                    "message": (
                        f"Items exist but direct LIKE search would miss "
                        f"{total_items_via_join - total_items_via_direct} items. "
                        f"Fix source linkage or use rss_sources join."
                    ),
                })
            if null_source_id > 0 or null_feed_url > 0:
                diagnostics.append({
                    "severity": "info",
                    "case": "D",
                    "message": (
                        f"{null_source_id} items have NULL source_id, "
                        f"{null_feed_url} have NULL feed_url. "
                        f"Run fix-source-linkage to repair."
                    ),
                })

        if not diagnostics:
            diagnostics.append({
                "severity": "info",
                "case": "nominal",
                "message": "Source scope filter should work correctly.",
            })

        return {
            "source_url_prefix": source_url_prefix,
            "diagnostics": diagnostics,
            "rss_sources_matched": source_details,
            "summary": {
                "total_rss_sources": total_rss_sources,
                "total_sources_matched": len(source_details),
                "total_items_via_rss_join": total_items_via_join,
                "total_items_via_direct_search": total_items_via_direct,
                "total_items": total_items,
                "total_items_with_null_source_id": null_source_id,
                "total_items_with_null_feed_url": null_feed_url,
                "latest_item_time": latest_scope_time,
                "sources_with_items": sum(1 for src in source_details if src["item_count_total"] > 0),
                "zero_item_sources": sum(1 for src in source_details if src["item_count_total"] == 0),
                "html_entity_source_name_issues": sum(1 for src in source_details if src["source_name_has_html_entities"]),
                "scope_missing_source_id_items": sum(src["missing_source_id_items"] for src in source_details),
                "scope_missing_feed_url_items": sum(src["missing_feed_url_items"] for src in source_details),
            },
        }


def probe_markdown_report(data: dict[str, Any]) -> str:
    summary = data.get("summary", {})
    sources = data.get("rss_sources_matched", [])
    lines = [
        f"# Source Scope Probe: {data.get('source_url_prefix')}",
        "",
        "## Summary",
        "",
        f"- rss_sources matched: {summary.get('total_sources_matched', 0)}",
        f"- sources with items: {summary.get('sources_with_items', 0)}",
        f"- zero-item sources: {summary.get('zero_item_sources', 0)}",
        f"- items via source linkage: {summary.get('total_items_via_rss_join', 0)}",
        f"- items via direct search: {summary.get('total_items_via_direct_search', 0)}",
        f"- latest_item_time: {summary.get('latest_item_time')}",
        f"- scope source_id missing items: {summary.get('scope_missing_source_id_items', 0)}",
        f"- scope feed_url missing items: {summary.get('scope_missing_feed_url_items', 0)}",
        f"- HTML entity source name issues: {summary.get('html_entity_source_name_issues', 0)}",
        "",
        "## Diagnostics",
        "",
    ]
    lines.extend(f"- [{d.get('severity')}] {d.get('case')}: {d.get('message')}" for d in data.get("diagnostics", []))
    lines.extend(["", "## Top Sources", "", "| source_id | items | latest | status | feed_url |", "|---|---:|---|---|---|"])
    for src in sorted(sources, key=lambda item: item.get("item_count_total", 0), reverse=True)[:60]:
        lines.append(
            f"| {src.get('source_id')} | {src.get('item_count_total', 0)} | {src.get('latest_item_time') or ''} | {src.get('status') or ''} | {src.get('feed_url') or ''} |"
        )
    zero = [src for src in sources if src.get("item_count_total", 0) == 0]
    if zero:
        lines.extend(["", "## Zero-Item Sources", ""])
        lines.extend(f"- {src.get('source_id')} - {src.get('feed_url')}" for src in zero[:100])
    entity_sources = [src for src in sources if src.get("source_name_has_html_entities")]
    if entity_sources:
        lines.extend(["", "## HTML Entity Source Names", ""])
        lines.extend(f"- {src.get('source_id')}: {src.get('source_name')}" for src in entity_sources[:100])
    lines.append("")
    return "\n".join(lines)


def fix_source_linkage(
    store: InboxStore,
    source_url_prefix: str,
    *,
    apply: bool = False,
    dry_run: bool = True,
) -> dict[str, Any]:
    search = f"%{source_url_prefix}%"
    clean = source_url_prefix.removeprefix("https://").removeprefix("http://")
    clean_search = f"%{clean}%"

    with store.connect() as conn:
        conn.row_factory = None
        # Find matching rss_sources
        src_rows = conn.execute(
            """
            SELECT source_id, source_name, source_category, feed_url
            FROM rss_sources
            WHERE feed_url LIKE ?
               OR normalized_feed_url LIKE ?
               OR feed_url LIKE ?
               OR normalized_feed_url LIKE ?
            ORDER BY feed_url, source_id
            """,
            (search, search, clean_search, clean_search),
        ).fetchall()

        items_scanned = 0
        items_fixed_source_id = 0
        items_fixed_feed_url = 0
        items_updated = 0
        errors = []
        backup_path = None

        for src_row in src_rows:
            src_id = src_row[0]
            src_name = src_row[1]
            src_cat = src_row[2]
            feed_url = src_row[3]

            # Find items with matching name+category but missing source_id or feed_url
            if src_cat:
                cur = conn.execute(
                    """
                    SELECT item_id FROM inbox_items
                    WHERE source_name = ? AND source_category = ?
                      AND (source_id IS NULL OR source_id = '' OR feed_url IS NULL OR feed_url = '')
                    """,
                    (src_name, src_cat),
                )
            else:
                cur = conn.execute(
                    """
                    SELECT item_id FROM inbox_items
                    WHERE source_name = ?
                      AND (source_category IS NULL OR source_category = '')
                      AND (source_id IS NULL OR source_id = '' OR feed_url IS NULL OR feed_url = '')
                    """,
                    (src_name,),
                )

            item_rows = cur.fetchall()
            if not item_rows:
                continue

            items_scanned += len(item_rows)
            needs_source_id = 0
            needs_feed_url = 0

            for (item_id,) in item_rows:
                # Check what needs fixing
                item = conn.execute(
                    "SELECT source_id, feed_url FROM inbox_items WHERE item_id = ?",
                    (item_id,),
                ).fetchone()
                if item:
                    cur_src = item[0]
                    cur_feed = item[1]
                    fix_src = not cur_src
                    fix_feed = not cur_feed
                    if fix_src:
                        needs_source_id += 1
                    if fix_feed:
                        needs_feed_url += 1

            if apply and not dry_run:
                if backup_path is None:
                    backup_path = str(_backup_db(Path(store.database_path)))
                if src_cat:
                    conn.execute(
                        """
                        UPDATE inbox_items
                        SET source_id = CASE WHEN (source_id IS NULL OR source_id = '') THEN ? ELSE source_id END,
                            feed_url = CASE WHEN (feed_url IS NULL OR feed_url = '') THEN ? ELSE feed_url END
                        WHERE source_name = ? AND source_category = ?
                          AND (source_id IS NULL OR source_id = '' OR feed_url IS NULL OR feed_url = '')
                        """,
                        (src_id, feed_url, src_name, src_cat),
                    )
                else:
                    conn.execute(
                        """
                        UPDATE inbox_items
                        SET source_id = CASE WHEN (source_id IS NULL OR source_id = '') THEN ? ELSE source_id END,
                            feed_url = CASE WHEN (feed_url IS NULL OR feed_url = '') THEN ? ELSE feed_url END
                        WHERE source_name = ?
                          AND (source_category IS NULL OR source_category = '')
                          AND (source_id IS NULL OR source_id = '' OR feed_url IS NULL OR feed_url = '')
                        """,
                        (src_id, feed_url, src_name),
                    )
                conn.commit()

            items_fixed_source_id += needs_source_id
            items_fixed_feed_url += needs_feed_url
            items_updated += len(item_rows)

    return {
        "ok": len(errors) == 0,
        "stats": {
            "sources_matched": len(src_rows),
            "items_scanned": items_scanned,
            "items_fixed_source_id": items_fixed_source_id,
            "items_fixed_feed_url": items_fixed_feed_url,
            "items_updated": items_updated,
            "errors": errors,
        },
        "dry_run": dry_run,
        "apply": apply,
        "backup_path": backup_path,
    }


def ingest_matching_sources(
    store: InboxStore,
    source_url_prefix: str,
    *,
    dry_run: bool = True,
    limit: int | None = None,
    concurrency: int = 8,
    per_source_timeout_seconds: int = 30,
    retry: int = 1,
) -> dict[str, Any]:
    search = f"%{source_url_prefix}%"
    clean = source_url_prefix.removeprefix("https://").removeprefix("http://")
    clean_search = f"%{clean}%"

    with store.connect() as conn:
        conn.row_factory = None
        src_rows = conn.execute(
            """
            SELECT source_id, source_name, feed_url, status
            FROM rss_sources
            WHERE (feed_url LIKE ? OR normalized_feed_url LIKE ?
                   OR feed_url LIKE ? OR normalized_feed_url LIKE ?)
              AND status != 'disabled'
            ORDER BY feed_url, source_id
            """,
            (search, search, clean_search, clean_search),
        ).fetchall()
        before_total_items = conn.execute("SELECT COUNT(*) FROM inbox_items").fetchone()[0]
        before_latest = conn.execute("SELECT MAX(COALESCE(published_at, created_at)) FROM inbox_items").fetchone()[0]

    sources_matched = [row[0] for row in src_rows]
    active_sources = [row[0] for row in src_rows if row[3] in ("active", "paused")]
    if limit:
        active_sources = active_sources[:limit]

    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "sources_matched": sources_matched,
            "active_sources": active_sources,
            "total_matched": len(sources_matched),
            "total_active": len(active_sources),
            "concurrency": concurrency,
            "per_source_timeout_seconds": per_source_timeout_seconds,
            "retry": retry,
        }

    # Non-dry-run: actually ingest
    results = []
    success_count = 0
    failure_count = 0
    new_items = 0
    duplicate_items = 0
    failures_by_reason: Counter[str] = Counter()
    backup_path = str(_backup_db(Path(store.database_path), reason="before_api_xgo_semantic_phase1_2c"))

    source_names = {row[0]: row[1] for row in src_rows}
    source_urls = {row[0]: row[2] for row in src_rows}

    for result in run_ingest_process_pool(
        store,
        active_sources,
        source_names=source_names,
        source_urls=source_urls,
        concurrency=concurrency,
        per_source_timeout_seconds=per_source_timeout_seconds,
        retry=retry,
    ):
        if result["ok"]:
            new_items += int(result.get("inserted_count", 0) or 0)
            duplicate_items += int(result.get("duplicate_count", 0) or 0)
            success_count += 1
        else:
            failure_count += 1
            failures_by_reason[result.get("failure_reason") or "unknown_error"] += 1
        results.append(result)

    with store.connect() as conn:
        after_total_items = conn.execute("SELECT COUNT(*) FROM inbox_items").fetchone()[0]
        after_latest = conn.execute("SELECT MAX(COALESCE(published_at, created_at)) FROM inbox_items").fetchone()[0]

    return {
        "ok": failure_count == 0,
        "dry_run": False,
        "backup_path": backup_path,
        "sources_matched": sources_matched,
        "active_sources": active_sources,
        "total_matched": len(sources_matched),
        "total_active": len(active_sources),
        "success_count": success_count,
        "failure_count": failure_count,
        "timeout_count": failures_by_reason.get("timeout", 0),
        "empty_feed_count": sum(1 for result in results if result.get("ok") and result.get("fetched_count") == 0),
        "duplicate_only_count": sum(1 for result in results if result.get("ok") and result.get("inserted_count") == 0 and result.get("duplicate_count", 0) > 0),
        "concurrency": concurrency,
        "per_source_timeout_seconds": per_source_timeout_seconds,
        "retry": retry,
        "items_before": before_total_items,
        "items_after": after_total_items,
        "new_items": new_items,
        "duplicates": duplicate_items,
        "db_item_delta": after_total_items - before_total_items,
        "latest_item_time_before": before_latest,
        "latest_item_time_after": after_latest,
        "failures_by_reason": dict(failures_by_reason),
        "sample_new_items": sample_recent_scope_items(store, source_url_prefix),
        "results": results,
    }


def classify_ingest_failure(status: int, result: dict[str, Any]) -> str:
    code = str(result.get("error_code") or result.get("code") or "").lower()
    message = str(result.get("message") or result.get("error_message") or result.get("error") or "").lower()
    text = f"{code} {message}"
    if status == 408 or "timeout" in text or "timed out" in text:
        return "timeout"
    if "http" in text or status in {401, 403, 404, 429, 500, 502, 503, 504}:
        return "http_error"
    if "parse" in text or "xml" in text or "feed" in text and "invalid" in text:
        return "parse_error"
    if "empty" in text:
        return "empty_feed"
    if status < 400:
        return "duplicate_only"
    return "unknown_error"


SOURCE_INGEST_SUBPROCESS_CODE = """
import json
import sys
from pathlib import Path
from app.models import RSSSourceIngestRequest
from app.rss_ingest import ingest_registered_source
from app.storage import InboxStore

store = InboxStore(Path(sys.argv[1]))
status, result = ingest_registered_source(store, sys.argv[2], RSSSourceIngestRequest(force=True))
print(json.dumps({"status": status, "result": result}, ensure_ascii=False))
"""


def run_ingest_process_pool(
    store: InboxStore,
    source_ids: list[str],
    *,
    source_names: dict[str, str],
    source_urls: dict[str, str],
    concurrency: int,
    per_source_timeout_seconds: int,
    retry: int,
) -> list[dict[str, Any]]:
    pending = [
        {
            "source_id": source_id,
            "attempt": 1,
            "started_at": datetime.now(),
        }
        for source_id in source_ids
    ]
    running: dict[subprocess.Popen[str], dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    max_attempts = max(1, retry + 1)

    while pending or running:
        while pending and len(running) < max(1, concurrency):
            job = pending.pop(0)
            proc = start_source_ingest_process(store, job["source_id"])
            job["attempt_started_at"] = datetime.now()
            job["attempt_started_monotonic"] = time.monotonic()
            running[proc] = job

        progressed = False
        for proc, job in list(running.items()):
            elapsed = time.monotonic() - job["attempt_started_monotonic"]
            if proc.poll() is None and per_source_timeout_seconds > 0 and elapsed > per_source_timeout_seconds:
                status, payload = finish_timed_out_source_process(proc, per_source_timeout_seconds)
            elif proc.poll() is None:
                continue
            else:
                status, payload = finish_source_process(proc)

            progressed = True
            del running[proc]
            ok = status < 400 and bool(payload.get("ok"))
            reason = classify_ingest_failure(status, payload)
            if not ok and job["attempt"] < max_attempts and reason in {"timeout", "http_error", "unknown_error"}:
                pending.append({
                    "source_id": job["source_id"],
                    "attempt": job["attempt"] + 1,
                    "started_at": job["started_at"],
                })
                continue
            results.append(format_source_ingest_result(
                job["source_id"],
                source_names=source_names,
                source_urls=source_urls,
                status=status,
                payload=payload,
                attempts=job["attempt"],
                started_at=job["started_at"],
            ))

        if not progressed:
            time.sleep(0.1)
    return results


def start_source_ingest_process(store: InboxStore, source_id: str) -> subprocess.Popen[str]:
    env = dict(os.environ)
    cwd = str(Path(__file__).resolve().parents[2])
    env["PYTHONPATH"] = cwd
    return subprocess.Popen(
        [sys.executable, "-c", SOURCE_INGEST_SUBPROCESS_CODE, str(store.database_path), source_id],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def finish_source_process(proc: subprocess.Popen[str]) -> tuple[int, dict[str, Any]]:
    stdout, stderr = proc.communicate(timeout=5)
    if proc.returncode != 0:
        return 500, {
            "ok": False,
            "error_code": "source_ingest_subprocess_failed",
            "message": (stderr or stdout or "").strip()[:1000],
        }
    try:
        payload = json.loads((stdout or "").strip().splitlines()[-1])
        return int(payload["status"]), dict(payload["result"])
    except Exception as exc:
        return 500, {
            "ok": False,
            "error_code": "source_ingest_subprocess_parse_failed",
            "message": f"{exc}: {(stdout or '')[:1000]}",
        }


def finish_timed_out_source_process(proc: subprocess.Popen[str], timeout_seconds: int) -> tuple[int, dict[str, Any]]:
    try:
        proc.kill()
        proc.communicate(timeout=5)
    except Exception:
        pass
    return 408, {
        "ok": False,
        "error_code": "source_ingest_timeout",
        "message": f"source ingest exceeded {timeout_seconds}s",
    }


def format_source_ingest_result(
    source_id: str,
    *,
    source_names: dict[str, str],
    source_urls: dict[str, str],
    status: int,
    payload: dict[str, Any],
    attempts: int,
    started_at: datetime,
) -> dict[str, Any]:
    run_stats = (payload.get("run") or {}).get("stats", {}) if isinstance(payload, dict) else {}
    ok = status < 400 and bool(payload.get("ok"))
    return {
        "source_id": source_id,
        "source_name": source_names.get(source_id),
        "feed_url": source_urls.get(source_id),
        "ok": ok,
        "status_code": status,
        "attempts": attempts,
        "failure_reason": None if ok else classify_ingest_failure(status, payload),
        "fetched_count": int(run_stats.get("fetched_entries", 0) or run_stats.get("feed_items_seen", 0) or 0),
        "inserted_count": int(run_stats.get("new_items", 0) or 0),
        "duplicate_count": int(run_stats.get("duplicate_items", 0) or 0),
        "failed_item_count": int(run_stats.get("failed_items", 0) or 0),
        "duration_seconds": round((datetime.now() - started_at).total_seconds(), 3),
        "error_message": payload.get("message") or payload.get("error_message") or ((payload.get("error") or {}).get("message") if isinstance(payload.get("error"), dict) else None),
        "result": payload,
    }


def ingest_one_source_subprocess(store: InboxStore, source_id: str, *, timeout_seconds: int) -> tuple[int, dict[str, Any]]:
    env = dict(os.environ)
    cwd = str(Path(__file__).resolve().parents[2])
    env["PYTHONPATH"] = cwd
    try:
        completed = subprocess.run(
            [sys.executable, "-c", SOURCE_INGEST_SUBPROCESS_CODE, str(store.database_path), source_id],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout_seconds if timeout_seconds > 0 else None,
        )
    except subprocess.TimeoutExpired:
        return 408, {"ok": False, "error_code": "source_ingest_timeout", "message": f"source ingest exceeded {timeout_seconds}s"}
    if completed.returncode != 0:
        return 500, {
            "ok": False,
            "error_code": "source_ingest_subprocess_failed",
            "message": (completed.stderr or completed.stdout or "").strip()[:1000],
        }
    try:
        payload = json.loads(completed.stdout.strip().splitlines()[-1])
        return int(payload["status"]), dict(payload["result"])
    except Exception as exc:
        return 500, {
            "ok": False,
            "error_code": "source_ingest_subprocess_parse_failed",
            "message": f"{exc}: {(completed.stdout or '')[:1000]}",
        }


def sample_recent_scope_items(store: InboxStore, source_url_prefix: str, limit: int = 10) -> list[dict[str, Any]]:
    search = f"%{source_url_prefix}%"
    clean = source_url_prefix.removeprefix("https://").removeprefix("http://")
    clean_search = f"%{clean}%"
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT item_id, title, source_id, source_name, feed_url, published_at, created_at
            FROM inbox_items
            WHERE source_id IN (
                SELECT source_id FROM rss_sources
                WHERE feed_url LIKE ? OR normalized_feed_url LIKE ? OR feed_url LIKE ? OR normalized_feed_url LIKE ?
            )
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (search, search, clean_search, clean_search, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def ingest_markdown_report(data: dict[str, Any]) -> str:
    lines = [
        "# api.xgo.ing Source Scope Ingest",
        "",
        "## Summary",
        "",
        f"- backup_path: {data.get('backup_path')}",
        f"- sources selected: {data.get('total_active', 0)}",
        f"- sources succeeded: {data.get('success_count', 0)}",
        f"- sources failed: {data.get('failure_count', 0)}",
        f"- timed out sources: {data.get('timeout_count', 0)}",
        f"- empty feeds: {data.get('empty_feed_count', 0)}",
        f"- duplicate-only feeds: {data.get('duplicate_only_count', 0)}",
        f"- concurrency: {data.get('concurrency')}",
        f"- per-source timeout: {data.get('per_source_timeout_seconds')}s",
        f"- retry: {data.get('retry')}",
        f"- items before: {data.get('items_before', 0)}",
        f"- items after: {data.get('items_after', 0)}",
        f"- DB item delta: {data.get('db_item_delta', 0)}",
        f"- new items reported: {data.get('new_items', 0)}",
        f"- duplicates reported: {data.get('duplicates', 0)}",
        f"- latest before: {data.get('latest_item_time_before')}",
        f"- latest after: {data.get('latest_item_time_after')}",
        "",
        "## Failures By Reason",
        "",
        "```json",
        __import__("json").dumps(data.get("failures_by_reason", {}), ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## Sample Recent Items",
        "",
    ]
    for item in data.get("sample_new_items", []):
        lines.append(f"- {item.get('published_at') or item.get('created_at')} | {item.get('source_name')} | {item.get('title')}")
    lines.extend(["", "## Failed Sources", ""])
    for result in data.get("results", []):
        if not result.get("ok"):
            payload = result.get("result") or {}
            lines.append(f"- {result.get('source_id')}: {result.get('failure_reason') or payload.get('error_code') or result.get('error')} {result.get('error_message') or payload.get('message') or ''}")
    lines.extend(["", "## Per-Source Results", "", "| source_id | ok | reason | fetched | inserted | duplicate | duration_s | attempts |", "|---|---:|---|---:|---:|---:|---:|---:|"])
    for result in sorted(data.get("results", []), key=lambda item: (not item.get("ok"), item.get("source_id") or "")):
        lines.append(
            f"| {result.get('source_id')} | {str(result.get('ok')).lower()} | {result.get('failure_reason') or ''} | {result.get('fetched_count', 0)} | {result.get('inserted_count', 0)} | {result.get('duplicate_count', 0)} | {result.get('duration_seconds', 0)} | {result.get('attempts', 1)} |"
        )
    lines.append("")
    return "\n".join(lines)
