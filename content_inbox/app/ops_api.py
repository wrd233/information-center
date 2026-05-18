from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from app.config import BASE_DIR, settings
from app.models import ContentAnalyzeRequest
from app.processor import build_dedupe_key, normalize_content, process_content_thread_safe
from app.rss import parse_feed
from app.rss_errors import classify_exception, retryable_for
from app.rss_runner import sort_entries_for_processing
from app.storage import InboxStore
from app.utils import normalize_url, stable_hash, utc_now


router = APIRouter()
_CANCELLED_RUNS: set[str] = set()


def ok(data: Any = None, *, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"ok": True, "data": data or {}, "error": None, "meta": meta or {}}


def fail(code: str, message: str, *, status_code: int = 400, details: dict[str, Any] | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"ok": False, "data": None, "error": {"code": code, "message": message, "details": details or {}}, "meta": {}},
    )


def get_ops_store(request: Request) -> InboxStore:
    store = getattr(request.app.state, "store", None)
    if store is None:
        store = InboxStore(settings.database_path)
        request.app.state.store = store
    ensure_environment_metadata(store)
    return store


def legacy_db_path() -> Path:
    return BASE_DIR / "data" / "content_inbox.sqlite3"


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_proof(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False, "size": None, "modified_at": None, "sha256": None}
    stat = path.stat()
    return {
        "path": str(path),
        "exists": True,
        "size": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "sha256": sha256_file(path),
    }


def metadata_get(conn, key: str) -> str | None:
    row = conn.execute("SELECT value FROM system_metadata WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def metadata_set(conn, key: str, value: Any) -> None:
    conn.execute(
        """
        INSERT INTO system_metadata(key, value, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
        """,
        (key, str(value), utc_now()),
    )


def ensure_environment_metadata(store: InboxStore, *, label: str | None = None, is_fresh: bool = True) -> dict[str, Any]:
    with store.connect() as conn:
        store.init_operational_schema(conn)
        database_id = metadata_get(conn, "database_id")
        if not database_id:
            database_id = f"db_{uuid.uuid4().hex[:12]}"
            metadata_set(conn, "database_id", database_id)
            metadata_set(conn, "created_at", utc_now())
        defaults = {
            "database_label": label or metadata_get(conn, "database_label") or store.database_path.parent.name,
            "database_path": str(store.database_path),
            "schema_version": "operational_v1",
            "app_version": "operational-console-v1",
            "environment_kind": settings.environment,
            "is_fresh_database": "true" if is_fresh else "false",
            "source_import_origin": metadata_get(conn, "source_import_origin") or "none",
            "last_migration_at": utc_now(),
        }
        for key, value in defaults.items():
            metadata_set(conn, key, value)
    return environment_snapshot(store)


def environment_snapshot(store: InboxStore) -> dict[str, Any]:
    with store.connect() as conn:
        meta_rows = conn.execute("SELECT key, value FROM system_metadata").fetchall()
        meta = {row["key"]: row["value"] for row in meta_rows}
        source_count = conn.execute("SELECT COUNT(*) AS n FROM rss_sources WHERE deleted_at IS NULL").fetchone()["n"]
        item_count = conn.execute("SELECT COUNT(*) AS n FROM inbox_items WHERE deleted_at IS NULL").fetchone()["n"]
        run_count = conn.execute("SELECT COUNT(*) AS n FROM rss_ingest_runs").fetchone()["n"]
    return {
        "database_id": meta.get("database_id"),
        "database_label": meta.get("database_label"),
        "database_path": meta.get("database_path", str(store.database_path)),
        "schema_version": meta.get("schema_version"),
        "created_at": meta.get("created_at"),
        "app_version": meta.get("app_version"),
        "environment_kind": meta.get("environment_kind"),
        "is_fresh_database": meta.get("is_fresh_database") == "true",
        "source_count": int(source_count or 0),
        "item_count": int(item_count or 0),
        "run_count": int(run_count or 0),
        "real_runs_enabled": bool(settings.enable_real_runs),
    }


def add_event(
    store: InboxStore,
    run_id: str,
    event_type: str,
    *,
    source_id: str | None = None,
    item_id: str | None = None,
    level: str = "info",
    message: str = "",
    payload: dict[str, Any] | None = None,
    object_type: str | None = None,
    object_id: str | None = None,
) -> dict[str, Any]:
    with store.connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO ingest_run_events(run_id, event_type, source_id, item_id, object_type, object_id, level, message, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (run_id, event_type, source_id, item_id, object_type, object_id, level, message, json.dumps(payload or {}, ensure_ascii=False), utc_now()),
        )
        row = conn.execute("SELECT * FROM ingest_run_events WHERE seq = ?", (cur.lastrowid,)).fetchone()
    return event_row(row)


def audit(
    store: InboxStore,
    action: str,
    *,
    operation_id: str | None = None,
    run_id: str | None = None,
    source_id: str | None = None,
    item_id: str | None = None,
    object_type: str | None = None,
    object_id: str | None = None,
    before: Any = None,
    after: Any = None,
    message: str = "",
    actor: str = "console",
) -> None:
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO audit_log(operation_id, run_id, source_id, item_id, object_type, object_id, action, actor, before_json, after_json, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                operation_id,
                run_id,
                source_id,
                item_id,
                object_type,
                object_id,
                action,
                actor,
                json.dumps(before, ensure_ascii=False) if before is not None else None,
                json.dumps(after, ensure_ascii=False) if after is not None else None,
                message,
                utc_now(),
            ),
        )


def event_row(row: Any) -> dict[str, Any]:
    return {
        "seq": row["seq"],
        "run_id": row["run_id"],
        "event_type": row["event_type"],
        "source_id": row["source_id"],
        "item_id": row["item_id"],
        "object_type": row["object_type"],
        "object_id": row["object_id"],
        "level": row["level"],
        "message": row["message"],
        "payload": json.loads(row["payload_json"] or "{}"),
        "created_at": row["created_at"],
    }


@router.get("/api/environment")
def api_environment(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    return ok({"environment": environment_snapshot(store), "legacy_database": file_proof(legacy_db_path())})


@router.post("/api/environment/init-fresh")
def api_init_fresh(request: Request, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    label = (payload or {}).get("database_label") or f"fresh_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    db_path = BASE_DIR / "data" / "environments" / label / "content_inbox.db"
    new_store = InboxStore(db_path)
    ensure_environment_metadata(new_store, label=label, is_fresh=True)
    request.app.state.store = new_store
    settings.database_path = db_path
    audit(new_store, "environment_initialized", message=f"Fresh database initialized at {db_path}")
    return ok({"environment": environment_snapshot(new_store), "legacy_database": file_proof(legacy_db_path())})


@router.get("/api/environment/health")
def api_environment_health(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    env = environment_snapshot(store)
    checks = [
        {"name": "database_exists", "ok": store.database_path.exists(), "message": str(store.database_path)},
        {"name": "fresh_database", "ok": env["is_fresh_database"], "message": env["database_label"] or ""},
        {"name": "not_legacy_default", "ok": store.database_path.resolve() != legacy_db_path().resolve(), "message": "Current DB is isolated from legacy path."},
        {"name": "real_runs_enabled", "ok": env["real_runs_enabled"], "message": "Set CONTENT_INBOX_ENABLE_REAL_RUNS=1 for real-write runs."},
    ]
    return ok({"environment": env, "checks": checks})


@router.get("/api/environment/report")
def api_environment_report(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    return ok({"environment": environment_snapshot(store), "legacy_database": file_proof(legacy_db_path()), "generated_at": utc_now()})


def parse_source_lines(text: str) -> list[dict[str, Any]]:
    sources = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split(",")]
        feed_url = parts[0]
        if not feed_url:
            continue
        sources.append({"feed_url": feed_url, "source_name": parts[1] if len(parts) > 1 and parts[1] else feed_url, "source_category": parts[2] if len(parts) > 2 else None})
    return sources


def parse_sources_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    fmt = (payload.get("format") or "urls").lower()
    content = payload.get("content") or payload.get("text") or ""
    if payload.get("sources"):
        return list(payload["sources"])
    if fmt == "json":
        loaded = json.loads(content)
        return loaded if isinstance(loaded, list) else loaded.get("sources", [])
    if fmt == "csv":
        reader = csv.DictReader(io.StringIO(content))
        rows = []
        for row in reader:
            feed_url = row.get("feed_url") or row.get("rss_url") or row.get("url")
            name = row.get("source_name") or row.get("name") or row.get("title") or feed_url
            if feed_url:
                rows.append({"source_id": row.get("source_id") or None, "feed_url": feed_url, "source_name": name, "source_category": row.get("source_category") or row.get("category")})
        return rows
    if fmt == "opml":
        root = ElementTree.fromstring(content)
        rows = []
        for node in root.findall(".//outline"):
            feed_url = node.attrib.get("xmlUrl") or node.attrib.get("xmlurl") or node.attrib.get("url")
            if feed_url:
                rows.append({"feed_url": feed_url, "source_name": node.attrib.get("title") or node.attrib.get("text") or feed_url, "source_category": node.attrib.get("category")})
        return rows
    return parse_source_lines(content)


def source_preview(store: InboxStore, payload: dict[str, Any]) -> dict[str, Any]:
    candidates = parse_sources_payload(payload)
    normalized = []
    seen = set()
    with store.connect() as conn:
        existing = {row["normalized_feed_url"] for row in conn.execute("SELECT normalized_feed_url FROM rss_sources").fetchall()}
    for candidate in candidates:
        feed_url = str(candidate.get("feed_url") or "").strip()
        if not feed_url:
            continue
        norm = normalize_url(feed_url) or feed_url
        status = "duplicate_in_file" if norm in seen else ("exists" if norm in existing else "new")
        seen.add(norm)
        normalized.append(
            {
                "source_id": candidate.get("source_id"),
                "source_name": candidate.get("source_name") or feed_url,
                "source_category": candidate.get("source_category"),
                "feed_url": feed_url,
                "normalized_feed_url": norm,
                "status": status,
                "priority": int(candidate.get("priority", 3) or 3),
                "tags": candidate.get("tags") or [],
                "notes": candidate.get("notes") or "",
                "config": candidate.get("config") or {"screen": False},
            }
        )
    return {
        "sources": normalized,
        "stats": {
            "total": len(normalized),
            "new": sum(1 for item in normalized if item["status"] == "new"),
            "exists": sum(1 for item in normalized if item["status"] == "exists"),
            "duplicate_in_file": sum(1 for item in normalized if item["status"] == "duplicate_in_file"),
        },
        "risk_level": "low",
        "requires_commit": True,
    }


@router.get("/api/sources")
def api_sources(request: Request, status: str | None = None, keyword: str | None = None, limit: int = 100, offset: int = 0) -> dict[str, Any]:
    store = get_ops_store(request)
    sources, stats = store.list_rss_sources({"status": status, "keyword": keyword, "limit": limit, "offset": offset})
    return ok({"sources": sources, "stats": stats})


@router.get("/api/sources/{source_id}")
def api_source_detail(request: Request, source_id: str) -> Any:
    store = get_ops_store(request)
    source = store.get_rss_source(source_id)
    if not source:
        return fail("SOURCE_NOT_FOUND", "Source not found.", status_code=404)
    items, _ = store.query({"source_id": source_id, "include_silent": True, "include_ignored": True, "limit": 10})
    with store.connect() as conn:
        audits = [dict(row) for row in conn.execute("SELECT * FROM audit_log WHERE source_id = ? ORDER BY id DESC LIMIT 20", (source_id,)).fetchall()]
    return ok({"source": source, "recent_items": items, "audit": audits})


@router.post("/api/sources")
def api_source_create(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    try:
        source, created = store.create_rss_source(payload)
    except ValueError as exc:
        return fail("SOURCE_DUPLICATE", str(exc), status_code=409)
    audit(store, "source_created", source_id=source["source_id"], after=source)
    return ok({"source": source, "created": created})


@router.patch("/api/sources/{source_id}")
def api_source_patch(request: Request, source_id: str, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    before = store.get_rss_source(source_id)
    if not before:
        return fail("SOURCE_NOT_FOUND", "Source not found.", status_code=404)
    try:
        source = store.update_rss_source(source_id, payload)
    except ValueError as exc:
        return fail("SOURCE_DUPLICATE", str(exc), status_code=409)
    audit(store, "source_updated", source_id=source_id, before=before, after=source)
    return ok({"source": source})


@router.delete("/api/sources/{source_id}")
def api_source_delete(request: Request, source_id: str) -> Any:
    store = get_ops_store(request)
    before = store.get_rss_source(source_id)
    if not before:
        return fail("SOURCE_NOT_FOUND", "Source not found.", status_code=404)
    source = store.update_rss_source(source_id, {"status": "archived"})
    audit(store, "source_archived", source_id=source_id, before=before, after=source)
    return ok({"source_id": source_id, "status": "archived"})


@router.post("/api/sources/import/preview")
def api_source_import_preview(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    preview = source_preview(store, payload)
    operation_id = f"op_{uuid.uuid4().hex}"
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO operation_previews(operation_id, operation_type, payload_json, preview_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (operation_id, "source_import", json.dumps(payload, ensure_ascii=False), json.dumps(preview, ensure_ascii=False), utc_now()),
        )
    preview["operation_id"] = operation_id
    return ok(preview)


@router.post("/api/sources/import/commit")
def api_source_import_commit(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    operation_id = payload.get("operation_id")
    if operation_id:
        with store.connect() as conn:
            row = conn.execute("SELECT * FROM operation_previews WHERE operation_id = ?", (operation_id,)).fetchone()
        if not row:
            return fail("OPERATION_NOT_FOUND", "Import preview operation was not found.", status_code=404)
        preview = json.loads(row["preview_json"])
    else:
        operation_id = f"op_{uuid.uuid4().hex}"
        preview = source_preview(store, payload)
    created = []
    skipped = []
    for source_payload in preview["sources"]:
        if source_payload["status"] != "new":
            skipped.append(source_payload)
            continue
        clean_payload = {key: source_payload.get(key) for key in ("source_id", "source_name", "source_category", "feed_url", "priority", "tags", "notes", "config")}
        clean_payload["status"] = "active"
        try:
            source, _ = store.create_rss_source(clean_payload)
            created.append(source)
            audit(store, "source_imported", operation_id=operation_id, source_id=source["source_id"], after=source)
        except ValueError:
            skipped.append({**source_payload, "status": "exists"})
    with store.connect() as conn:
        conn.execute("UPDATE operation_previews SET status = 'committed', committed_at = ? WHERE operation_id = ?", (utc_now(), operation_id))
        metadata_set(conn, "source_import_origin", "console_import")
    return ok({"operation_id": operation_id, "created": created, "skipped": skipped, "stats": {"created": len(created), "skipped": len(skipped)}})


@router.post("/api/sources/export")
def api_source_export(request: Request, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    fmt = ((payload or {}).get("format") or "json").lower()
    sources, _ = store.list_rss_sources({"limit": 10000, "offset": 0})
    if fmt == "csv":
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=["source_id", "source_name", "source_category", "feed_url", "status", "priority"])
        writer.writeheader()
        for source in sources:
            writer.writerow({key: source.get(key) for key in writer.fieldnames})
        content = out.getvalue()
    elif fmt == "opml":
        outlines = "\n".join(f'    <outline text="{s["source_name"]}" title="{s["source_name"]}" xmlUrl="{s["feed_url"]}" />' for s in sources)
        content = f'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><body>\n{outlines}\n</body></opml>'
    else:
        content = json.dumps({"sources": sources}, ensure_ascii=False, indent=2)
    return ok({"format": fmt, "content": content, "count": len(sources)})


def bulk_update_sources(request: Request, payload: dict[str, Any], status: str, action: str) -> dict[str, Any]:
    store = get_ops_store(request)
    operation_id = payload.get("operation_id") or f"op_{uuid.uuid4().hex}"
    updated = []
    for source_id in payload.get("source_ids") or []:
        before = store.get_rss_source(source_id)
        if not before:
            continue
        after = store.update_rss_source(source_id, {"status": status})
        updated.append(after)
        audit(store, action, operation_id=operation_id, source_id=source_id, before=before, after=after)
    return ok({"operation_id": operation_id, "updated": updated, "count": len(updated)})


@router.post("/api/sources/bulk-enable")
def api_bulk_enable(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    return bulk_update_sources(request, payload, "active", "source_enabled")


@router.post("/api/sources/bulk-disable")
def api_bulk_disable(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    return bulk_update_sources(request, payload, "disabled", "source_disabled")


@router.post("/api/sources/bulk-archive")
def api_bulk_archive(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    return bulk_update_sources(request, payload, "archived", "source_archived")


@router.post("/api/sources/bulk-delete")
def api_bulk_delete(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    return bulk_update_sources(request, payload, "archived", "source_soft_deleted")


@router.post("/api/sources/bulk-recheck")
def api_bulk_recheck(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    operation_id = f"op_{uuid.uuid4().hex}"
    for source_id in payload.get("source_ids") or []:
        audit(store, "source_recheck_requested", operation_id=operation_id, source_id=source_id)
    return ok({"operation_id": operation_id, "requested": payload.get("source_ids") or []})


@router.post("/api/sources/bulk-run")
def api_bulk_run(request: Request, payload: dict[str, Any]) -> Any:
    payload = {"mode": payload.get("mode", "dry_run"), "source_scope": {"type": "selected", "source_ids": payload.get("source_ids") or []}, "limits": payload.get("limits") or {}, "time_filter": payload.get("time_filter") or {}, "options": payload.get("options") or {}}
    return api_runs_create(request, payload)


def resolve_run_sources(store: InboxStore, config: dict[str, Any]) -> list[dict[str, Any]]:
    scope = config.get("source_scope") or {"type": "selected", "source_ids": []}
    scope_type = scope.get("type", "selected")
    if scope_type == "selected":
        return [source for sid in scope.get("source_ids") or [] if (source := store.get_rss_source(sid))]
    filters: dict[str, Any] = {"limit": int((config.get("limits") or {}).get("max_sources", 100)), "offset": 0}
    if scope_type == "all_active":
        filters["status"] = "active"
    elif scope_type == "failed":
        filters["has_error"] = True
    sources, _ = store.list_rss_sources(filters)
    return sources


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def within_time_range(entry: ContentAnalyzeRequest, time_filter: dict[str, Any]) -> tuple[bool, str | None]:
    published = parse_dt(entry.published_at)
    if published is None:
        return False, "missing_published_at"
    start = parse_dt(time_filter.get("published_from"))
    end = parse_dt(time_filter.get("published_to"))
    if start and published < start:
        return False, "before_range"
    if end and published > end:
        return False, "after_range"
    return True, None


@router.post("/api/runs/preview")
def api_runs_preview(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    sources = resolve_run_sources(store, payload)
    mode = payload.get("mode", "dry_run")
    if mode == "real_write" and not settings.enable_real_runs:
        return fail("UNSAFE_OPERATION_REQUIRES_CONFIRMATION", "Real-write runs require CONTENT_INBOX_ENABLE_REAL_RUNS=1.")
    preview = {
        "mode": mode,
        "source_count": len(sources),
        "sources": [{"source_id": s["source_id"], "source_name": s["source_name"], "status": s["status"]} for s in sources],
        "time_filter": payload.get("time_filter") or {},
        "limits": payload.get("limits") or {},
        "database": environment_snapshot(store),
        "will_write_items": mode == "real_write",
        "risk_level": "high" if mode == "real_write" else "low",
        "requires_confirmation": mode == "real_write" or (payload.get("source_scope") or {}).get("type") == "all_active",
    }
    return ok(preview)


@router.post("/api/runs")
def api_runs_create(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    mode = payload.get("mode", "dry_run")
    if mode not in {"dry_run", "real_write"}:
        return fail("INVALID_RUN_MODE", "mode must be dry_run or real_write")
    if mode == "real_write" and not settings.enable_real_runs:
        return fail("UNSAFE_OPERATION_REQUIRES_CONFIRMATION", "Real-write runs require CONTENT_INBOX_ENABLE_REAL_RUNS=1.")
    sources = resolve_run_sources(store, payload)
    if not sources:
        return fail("NO_SOURCES_SELECTED", "No sources matched the requested scope.")
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    started_at = utc_now()
    store.create_ingest_run(
        {
            "run_id": run_id,
            "trigger_type": "console",
            "source_mode": (payload.get("source_scope") or {}).get("type", "selected"),
            "status": "running",
            "started_at": started_at,
            "selected_source_count": len(sources),
            "request": payload,
        }
    )
    add_event(store, run_id, "run_created", message="Run created.", payload=payload)
    add_event(store, run_id, "run_started", message="Run started.", payload={"mode": mode, "source_count": len(sources)})
    audit(store, "run_created", run_id=run_id, after=payload)
    if payload.get("run_synchronously"):
        execute_run(store, run_id, sources, payload)
    else:
        thread = threading.Thread(target=execute_run, args=(store, run_id, sources, payload), daemon=True)
        thread.start()
    return ok({"run_id": run_id, "run": store.get_ingest_run(run_id)})


def execute_run(store: InboxStore, run_id: str, sources: list[dict[str, Any]], config: dict[str, Any]) -> None:
    mode = config.get("mode", "dry_run")
    limits = config.get("limits") or {}
    time_filter = config.get("time_filter") or {}
    max_items_per_source = int(limits.get("max_items_per_source", 50) or 50)
    max_total_items = int(limits.get("max_total_items", 5000) or 5000)
    total_new = total_dup = total_failed = total_processed = success_sources = failure_sources = 0
    linked_item_ids: list[str] = []
    started = time.monotonic()
    for source in sources[: int(limits.get("max_sources", len(sources)) or len(sources))]:
        if run_id in _CANCELLED_RUNS:
            add_event(store, run_id, "run_cancelled", level="warning", message="Run cancelled by user.")
            break
        source_started = utc_now()
        source_t0 = time.monotonic()
        add_event(store, run_id, "source_started", source_id=source["source_id"], message=f"Started {source['source_name']}")
        new_items = duplicate_items = failed_items = filtered_items = fetched = processed = 0
        try:
            add_event(store, run_id, "source_fetching", source_id=source["source_id"], message="Fetching feed.")
            meta, entries = parse_feed(source["feed_url"], source_id=source["source_id"], source_name=source["source_name"], source_category=source.get("source_category"), limit=max_items_per_source)
            fetched = len(entries)
            entries = sort_entries_for_processing(entries, (config.get("options") or {}).get("process_order", "oldest_first"))
            for entry in entries:
                if total_processed >= max_total_items:
                    add_event(store, run_id, "warning", source_id=source["source_id"], level="warning", message="Max total items reached.")
                    break
                ok_time, reason = within_time_range(entry, time_filter)
                if (time_filter.get("published_from") or time_filter.get("published_to")) and not ok_time:
                    filtered_items += 1
                    add_event(store, run_id, "item_filtered_by_time", source_id=source["source_id"], level="warning", message=reason or "filtered", payload={"title": entry.title, "published_at": entry.published_at})
                    continue
                entry.screen = bool((source.get("config") or {}).get("screen", False))
                add_event(store, run_id, "item_seen", source_id=source["source_id"], message=entry.title or "")
                if mode == "dry_run":
                    new_items += 1
                    processed += 1
                    total_processed += 1
                    add_event(store, run_id, "item_inserted" if False else "metric", source_id=source["source_id"], message="Dry-run candidate item.", payload={"title": entry.title})
                    continue
                result = process_content_thread_safe(store, entry, raw=entry.model_dump())
                status = "duplicate" if result.is_duplicate else "inserted"
                duplicate_items += 1 if result.is_duplicate else 0
                new_items += 0 if result.is_duplicate else 1
                processed += 1
                total_processed += 1
                with store.connect() as conn:
                    conn.execute(
                        "INSERT OR IGNORE INTO item_run_links(run_id, source_id, item_id, status, operation_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (run_id, source["source_id"], result.item_id, status, None, utc_now()),
                    )
                linked_item_ids.append(result.item_id)
                add_event(store, run_id, "item_duplicate" if result.is_duplicate else "item_inserted", source_id=source["source_id"], item_id=result.item_id, message=result.normalized.title)
                audit(store, f"item_{status}", run_id=run_id, source_id=source["source_id"], item_id=result.item_id)
            success_sources += 1
            status = "success"
            if mode == "real_write":
                store.record_rss_source_success(
                    source["source_id"],
                    run_id=run_id,
                    finished_at=utc_now(),
                    new_items=new_items,
                    duplicate_items=duplicate_items,
                    processed_items=processed,
                    feed_items_seen=fetched,
                    incremental_decision=None,
                    anchor_found=None,
                    duration_ms=int((time.monotonic() - source_t0) * 1000),
                )
            add_event(store, run_id, "source_completed", source_id=source["source_id"], message="Source completed.", payload={"new_items": new_items, "duplicate_items": duplicate_items, "filtered_items": filtered_items})
        except Exception as exc:
            failure_sources += 1
            status = "failed"
            code, message = classify_exception(exc)
            failed_items += 1
            if mode == "real_write":
                store.record_rss_source_failure(source["source_id"], run_id=run_id, finished_at=utc_now(), error_code=code, error_message=message, retryable=retryable_for(code), duration_ms=int((time.monotonic() - source_t0) * 1000))
            add_event(store, run_id, "source_failed", source_id=source["source_id"], level="error", message=message, payload={"error_code": code})
        total_new += new_items
        total_dup += duplicate_items
        total_failed += failed_items
        store.create_ingest_run_source(
            {
                "run_id": run_id,
                "source_id": source["source_id"],
                "feed_url": source["feed_url"],
                "source_name": source["source_name"],
                "source_category": source.get("source_category"),
                "status": status,
                "started_at": source_started,
                "finished_at": utc_now(),
                "duration_ms": int((time.monotonic() - source_t0) * 1000),
                "retryable": status == "failed",
                "fetched_entries_count": fetched,
                "processed_entries_count": processed,
                "new_items_count": new_items,
                "duplicate_items_count": duplicate_items,
                "failed_items_count": failed_items,
                "warnings": [{"filtered_items": filtered_items}],
                "result": {"filtered_items": filtered_items},
            }
        )
    if mode == "real_write" and linked_item_ids:
        add_event(store, run_id, "semantic_started", message="Generating lightweight semantic objects.")
        generate_information_objects(store, run_id, linked_item_ids)
        add_event(store, run_id, "semantic_completed", message="Semantic objects generated.")
    final_status = "cancelled" if run_id in _CANCELLED_RUNS else ("failed" if failure_sources and not success_sources else "success")
    duration_ms = int((time.monotonic() - started) * 1000)
    store.create_ingest_run(
        {
            "run_id": run_id,
            "trigger_type": "console",
            "source_mode": (config.get("source_scope") or {}).get("type", "selected"),
            "status": final_status,
            "started_at": store.get_ingest_run(run_id)["started_at"],
            "finished_at": utc_now(),
            "duration_ms": duration_ms,
            "selected_source_count": len(sources),
            "success_source_count": success_sources,
            "failure_source_count": failure_sources,
            "new_items_count": total_new,
            "duplicate_items_count": total_dup,
            "processed_items_count": total_processed,
            "failed_items_count": total_failed,
            "request": config,
            "summary": {"mode": mode, "duration_ms": duration_ms, "linked_item_count": len(set(linked_item_ids))},
        }
    )
    add_event(store, run_id, "run_completed" if final_status == "success" else f"run_{final_status}", message=f"Run {final_status}.", payload={"new_items": total_new, "duplicates": total_dup, "failed_items": total_failed})
    audit(store, f"run_{final_status}", run_id=run_id)


def normalized_title(value: str) -> str:
    return re.sub(r"\W+", " ", (value or "").lower()).strip()[:80] or "untitled"


def extract_terms(text: str) -> list[str]:
    words = re.findall(r"\b[A-Z][A-Za-z0-9][A-Za-z0-9_.-]{1,}\b", text or "")
    keywords = re.findall(r"\b(ai|openai|model|agent|security|funding|launch|release|policy|china|market)\b", (text or "").lower())
    terms = list(dict.fromkeys(words[:6] + [kw.title() for kw in keywords[:6]]))
    return terms[:8]


def generate_information_objects(store: InboxStore, run_id: str, item_ids: list[str]) -> None:
    now = utc_now()
    with store.connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM inbox_items WHERE item_id IN ({','.join('?' for _ in item_ids)})",
            item_ids,
        ).fetchall()
        for row in rows:
            item_id = row["item_id"]
            title = row["title"]
            body = f"{title}\n{row['summary'] or ''}"
            terms = extract_terms(body)
            extraction_id = f"se_{stable_hash(item_id)[:16]}"
            normalized = {"entities": terms, "topics": [row["source_category"] or "General"], "claims": [title] if title else []}
            conn.execute(
                "INSERT OR REPLACE INTO semantic_extractions(extraction_id, item_id, processor, confidence, needs_review, raw_output_json, normalized_output_json, evidence_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (extraction_id, item_id, "lightweight_rule", "low", 1, json.dumps({"title": title}, ensure_ascii=False), json.dumps(normalized, ensure_ascii=False), json.dumps([{"field": "title", "text": title}], ensure_ascii=False), now),
            )
            for term in terms:
                entity_id = "ent_" + stable_hash(term.lower())[:16]
                conn.execute(
                    "INSERT OR IGNORE INTO entities(entity_id, entity_name, entity_type, confidence, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (entity_id, term, "keyword", 0.45, now, now),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO item_entities(item_id, entity_id, confidence, evidence_json, created_at) VALUES (?, ?, ?, ?, ?)",
                    (item_id, entity_id, 0.45, json.dumps([{"title": title}], ensure_ascii=False), now),
                )
            topic_name = row["source_category"] or "General"
            topic_id = "topic_" + stable_hash(topic_name.lower())[:16]
            conn.execute(
                "INSERT OR IGNORE INTO topics(topic_id, topic_name, topic_summary, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (topic_id, topic_name, f"Items categorized as {topic_name}", now, now),
            )
            conn.execute("INSERT OR IGNORE INTO topic_items(topic_id, item_id, confidence, created_at) VALUES (?, ?, ?, ?)", (topic_id, item_id, 0.5, now))
        groups: dict[str, list[Any]] = {}
        for row in rows:
            groups.setdefault(normalized_title(row["title"]), []).append(row)
        for key, members in groups.items():
            first = members[0]
            cluster_id = "cluster_" + stable_hash(key)[:16]
            conn.execute(
                """
                INSERT OR IGNORE INTO event_clusters(cluster_id, cluster_title, cluster_summary, entities_json, representative_item_id, first_seen_at, last_seen_at, item_count, status, created_by, confidence, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (cluster_id, first["title"], f"{len(members)} related item(s) grouped by normalized title.", json.dumps(extract_terms(first["title"]), ensure_ascii=False), first["item_id"], now, now, len(members), "active", "lightweight_rule", 0.55 if len(members) > 1 else 0.35, now, now),
            )
            for member in members:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO cluster_items(cluster_id, item_id, primary_relation, same_event, same_topic, confidence, reason, evidence_json, decision_source, schema_version, input_fingerprint, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (cluster_id, member["item_id"], "same_topic" if len(members) == 1 else "same_event", 1 if len(members) > 1 else 0, 1, 0.55, "lightweight normalized title grouping", json.dumps([{"title": member["title"]}], ensure_ascii=False), "lightweight_rule", "operational_v1", stable_hash(cluster_id + member["item_id"]), now, now),
                )
                conn.execute("UPDATE inbox_items SET primary_cluster_id = ? WHERE item_id = ?", (cluster_id, member["item_id"]))
            event_id = "event_" + stable_hash(cluster_id)[:16]
            conn.execute(
                "INSERT OR IGNORE INTO events(event_id, event_title, event_summary, event_type, status, importance, confidence, primary_cluster_id, evidence_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (event_id, first["title"], f"Candidate event from cluster {cluster_id}.", "unknown", "needs_review", min(5, max(1, len(members))), 0.5 if len(members) > 1 else 0.3, cluster_id, json.dumps({"cluster_id": cluster_id, "method": "lightweight_rule"}, ensure_ascii=False), now, now),
            )
            for member in members:
                conn.execute("INSERT OR IGNORE INTO event_items(event_id, item_id, role, created_at) VALUES (?, ?, ?, ?)", (event_id, member["item_id"], "supporting", now))
            conn.execute(
                "INSERT INTO review_queue(review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ("event_candidate", "event", event_id, "pending", json.dumps({"action": "review_event"}, ensure_ascii=False), "Lightweight event candidate needs human review.", now, now),
            )


@router.get("/api/runs")
def api_runs(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    store = get_ops_store(request)
    runs, total = store.list_ingest_runs(limit=limit, offset=offset)
    return ok({"runs": runs, "stats": {"total": total, "returned": len(runs)}})


@router.get("/api/runs/{run_id}")
def api_run_detail(request: Request, run_id: str) -> Any:
    store = get_ops_store(request)
    run = store.get_ingest_run(run_id)
    if not run:
        return fail("RUN_NOT_FOUND", "Run not found.", status_code=404)
    return ok({"run": run})


@router.get("/api/runs/{run_id}/sources")
def api_run_sources(request: Request, run_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    return ok({"sources": store.list_ingest_run_sources(run_id)})


@router.get("/api/runs/{run_id}/events")
def api_run_events(request: Request, run_id: str, after_seq: int = 0, limit: int = 200) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = conn.execute("SELECT * FROM ingest_run_events WHERE run_id = ? AND seq > ? ORDER BY seq ASC LIMIT ?", (run_id, after_seq, limit)).fetchall()
    events = [event_row(row) for row in rows]
    return ok({"events": events, "last_seq": events[-1]["seq"] if events else after_seq})


@router.get("/api/runs/{run_id}/stream")
def api_run_stream(request: Request, run_id: str, after_seq: int = 0) -> StreamingResponse:
    def generate():
        seq = after_seq
        for _ in range(3600):
            store = get_ops_store(request)
            data = api_run_events(request, run_id, after_seq=seq, limit=100)["data"]
            for event in data["events"]:
                seq = event["seq"]
                yield f"event: run_event\ndata: {json.dumps(event, ensure_ascii=False)}\n\n"
            run = store.get_ingest_run(run_id)
            if run and run["status"] in {"success", "failed", "cancelled"} and not data["events"]:
                break
            time.sleep(1)
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/api/runs/{run_id}/items")
def api_run_items(request: Request, run_id: str, limit: int = 100, offset: int = 0) -> dict[str, Any]:
    return api_items(request, run_id=run_id, limit=limit, offset=offset)


@router.get("/api/runs/{run_id}/summary")
def api_run_summary(request: Request, run_id: str) -> Any:
    store = get_ops_store(request)
    run = store.get_ingest_run(run_id)
    if not run:
        return fail("RUN_NOT_FOUND", "Run not found.", status_code=404)
    sources = store.list_ingest_run_sources(run_id)
    events = api_run_events(request, run_id, limit=20)["data"]["events"]
    return ok({"run": run, "sources": sources, "recent_events": events})


@router.get("/api/runs/{run_id}/report")
def api_run_report(request: Request, run_id: str) -> Any:
    store = get_ops_store(request)
    run = store.get_ingest_run(run_id)
    if not run:
        return fail("RUN_NOT_FOUND", "Run not found.", status_code=404)
    sources = store.list_ingest_run_sources(run_id)
    body = f"# Run Report {run_id}\n\nStatus: {run['status']}\n\nNew items: {run['new_items_count']}\n\nSources: {len(sources)}\n"
    return ok({"format": "markdown", "content": body, "run": run, "sources": sources})


@router.post("/api/runs/{run_id}/cancel")
def api_run_cancel(request: Request, run_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    _CANCELLED_RUNS.add(run_id)
    add_event(store, run_id, "run_cancelled", level="warning", message="Cancellation requested.")
    audit(store, "run_cancelled", run_id=run_id)
    return ok({"run_id": run_id, "cancel_requested": True})


@router.post("/api/runs/{run_id}/rollback/preview")
def api_rollback_preview(request: Request, run_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = conn.execute("SELECT item_id, status FROM item_run_links WHERE run_id = ?", (run_id,)).fetchall()
    inserted = [row["item_id"] for row in rows if row["status"] == "inserted"]
    return ok({"run_id": run_id, "rollback_available": True, "soft_delete_item_count": len(inserted), "item_ids": inserted})


@router.post("/api/runs/{run_id}/rollback/commit")
def api_rollback_commit(request: Request, run_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    preview = api_rollback_preview(request, run_id)["data"]
    now = utc_now()
    with store.connect() as conn:
        for item_id in preview["item_ids"]:
            conn.execute("UPDATE inbox_items SET deleted_at = ?, rollback_run_id = ? WHERE item_id = ?", (now, run_id, item_id))
    add_event(store, run_id, "metric", level="warning", message="Soft rollback completed.", payload=preview)
    audit(store, "run_soft_rollback", run_id=run_id, after=preview)
    return ok({"run_id": run_id, "rolled_back": preview["soft_delete_item_count"]})


@router.get("/api/items")
def api_items(
    request: Request,
    run_id: str | None = None,
    source_id: str | None = None,
    published_from: str | None = None,
    published_to: str | None = None,
    keyword: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    store = get_ops_store(request)
    filters = {"source_id": source_id, "published_from": published_from, "published_to": published_to, "keyword": keyword, "include_silent": True, "include_ignored": True, "limit": limit, "offset": offset}
    if run_id:
        with store.connect() as conn:
            ids = [row["item_id"] for row in conn.execute("SELECT item_id FROM item_run_links WHERE run_id = ? ORDER BY id DESC LIMIT ? OFFSET ?", (run_id, limit, offset)).fetchall()]
            if not ids:
                return ok({"items": [], "stats": {"total": 0, "returned": 0}})
            rows = conn.execute(f"SELECT * FROM inbox_items WHERE item_id IN ({','.join('?' for _ in ids)}) AND deleted_at IS NULL", ids).fetchall()
        from app.storage import row_to_item
        items = [row_to_item(row) for row in rows]
        return ok({"items": items, "stats": {"total": len(items), "returned": len(items)}})
    items, total = store.query(filters)
    items = [item for item in items if not item.get("deleted_at")]
    return ok({"items": items, "stats": {"total": total, "returned": len(items)}})


@router.get("/api/items/{item_id}")
def api_item_detail(request: Request, item_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
        if not row:
            return fail("ITEM_NOT_FOUND", "Item not found.", status_code=404)
        from app.storage import row_to_item
        item = row_to_item(row)
        links = [dict(r) for r in conn.execute("SELECT * FROM item_run_links WHERE item_id = ? ORDER BY id DESC", (item_id,)).fetchall()]
        semantic = [dict(r) for r in conn.execute("SELECT * FROM semantic_extractions WHERE item_id = ? ORDER BY created_at DESC", (item_id,)).fetchall()]
        entities = [dict(r) for r in conn.execute("SELECT e.* FROM item_entities ie JOIN entities e ON e.entity_id = ie.entity_id WHERE ie.item_id = ?", (item_id,)).fetchall()]
    return ok({"item": item, "run_links": links, "semantic": semantic, "entities": entities})


@router.get("/api/items/{item_id}/raw")
def api_item_raw(request: Request, item_id: str) -> Any:
    detail = api_item_detail(request, item_id)
    if isinstance(detail, JSONResponse):
        return detail
    return ok({"raw": detail["data"]["item"].get("raw") or detail["data"]["item"].get("latest_raw") or {}})


@router.get("/api/items/{item_id}/dedupe")
def api_item_dedupe(request: Request, item_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT dg.* FROM dedupe_group_items dgi JOIN dedupe_groups dg ON dg.dedupe_group_id = dgi.dedupe_group_id WHERE dgi.item_id = ?", (item_id,)).fetchall()]
    return ok({"groups": rows})


@router.get("/api/items/{item_id}/semantic")
def api_item_semantic(request: Request, item_id: str) -> Any:
    detail = api_item_detail(request, item_id)
    if isinstance(detail, JSONResponse):
        return detail
    return ok({"semantic": detail["data"]["semantic"], "entities": detail["data"]["entities"]})


@router.get("/api/dedupe-groups")
def api_dedupe_groups(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM dedupe_groups ORDER BY updated_at DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()]
    return ok({"dedupe_groups": rows})


@router.get("/api/dedupe-groups/{group_id}")
def api_dedupe_group(request: Request, group_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        group = conn.execute("SELECT * FROM dedupe_groups WHERE dedupe_group_id = ?", (group_id,)).fetchone()
        if not group:
            return fail("DEDUPE_GROUP_NOT_FOUND", "Dedupe group not found.", status_code=404)
        members = [dict(r) for r in conn.execute("SELECT * FROM dedupe_group_items WHERE dedupe_group_id = ?", (group_id,)).fetchall()]
    return ok({"dedupe_group": dict(group), "members": members})


@router.post("/api/dedupe-groups/{group_id}/merge")
@router.post("/api/dedupe-groups/{group_id}/split")
@router.post("/api/dedupe-groups/{group_id}/review")
def api_dedupe_review(request: Request, group_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    audit(store, "dedupe_review", object_type="dedupe_group", object_id=group_id, after=payload or {})
    return ok({"dedupe_group_id": group_id, "accepted": True})


def list_table(request: Request, table: str, key: str, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute(f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()]
    return ok({key: rows})


@router.get("/api/clusters")
def api_clusters(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM event_clusters ORDER BY last_seen_at DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()]
    return ok({"clusters": rows})


@router.get("/api/clusters/{cluster_id}")
def api_cluster(request: Request, cluster_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        cluster = conn.execute("SELECT * FROM event_clusters WHERE cluster_id = ?", (cluster_id,)).fetchone()
        if not cluster:
            return fail("CLUSTER_NOT_FOUND", "Cluster not found.", status_code=404)
        items = [dict(r) for r in conn.execute("SELECT i.item_id, i.title, i.url, i.published_at FROM cluster_items ci JOIN inbox_items i ON i.item_id = ci.item_id WHERE ci.cluster_id = ?", (cluster_id,)).fetchall()]
    return ok({"cluster": dict(cluster), "items": items})


@router.post("/api/clusters/{cluster_id}/create-event")
def api_cluster_create_event(request: Request, cluster_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    event_id = "event_" + stable_hash(cluster_id + utc_now())[:16]
    now = utc_now()
    with store.connect() as conn:
        cluster = conn.execute("SELECT * FROM event_clusters WHERE cluster_id = ?", (cluster_id,)).fetchone()
        title = (payload or {}).get("title") or (cluster["cluster_title"] if cluster else cluster_id)
        conn.execute("INSERT OR REPLACE INTO events(event_id, event_title, event_summary, event_type, status, confidence, primary_cluster_id, evidence_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (event_id, title, (payload or {}).get("summary", ""), (payload or {}).get("event_type", "unknown"), "needs_review", 0.6, cluster_id, json.dumps({"manual": True}, ensure_ascii=False), now, now))
    audit(store, "event_created", object_type="event", object_id=event_id)
    return ok({"event_id": event_id})


@router.post("/api/clusters/{cluster_id}/review")
@router.post("/api/clusters/{cluster_id}/merge")
@router.post("/api/clusters/{cluster_id}/split")
@router.post("/api/clusters/{cluster_id}/dismiss")
def api_cluster_action(request: Request, cluster_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    audit(store, "cluster_action", object_type="cluster", object_id=cluster_id, after=payload or {})
    return ok({"cluster_id": cluster_id, "accepted": True})


@router.get("/api/events")
def api_events(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    return list_table(request, "events", "events", limit, offset)


@router.get("/api/events/{event_id}")
def api_event(request: Request, event_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        event = conn.execute("SELECT * FROM events WHERE event_id = ?", (event_id,)).fetchone()
        if not event:
            return fail("EVENT_NOT_FOUND", "Event not found.", status_code=404)
        items = [dict(r) for r in conn.execute("SELECT i.item_id, i.title, i.url, i.published_at FROM event_items ei JOIN inbox_items i ON i.item_id = ei.item_id WHERE ei.event_id = ?", (event_id,)).fetchall()]
    return ok({"event": dict(event), "items": items})


@router.post("/api/events/{event_id}/review")
@router.post("/api/events/{event_id}/merge")
@router.post("/api/events/{event_id}/split")
@router.post("/api/events/{event_id}/dismiss")
@router.post("/api/events/{event_id}/export")
def api_event_action(request: Request, event_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    audit(store, "event_action", object_type="event", object_id=event_id, after=payload or {})
    return ok({"event_id": event_id, "accepted": True})


@router.get("/api/entities")
def api_entities(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    return list_table(request, "entities", "entities", limit, offset)


@router.get("/api/entities/{entity_id}")
def api_entity(request: Request, entity_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        entity = conn.execute("SELECT * FROM entities WHERE entity_id = ?", (entity_id,)).fetchone()
        if not entity:
            return fail("ENTITY_NOT_FOUND", "Entity not found.", status_code=404)
        items = [dict(r) for r in conn.execute("SELECT i.item_id, i.title FROM item_entities ie JOIN inbox_items i ON i.item_id = ie.item_id WHERE ie.entity_id = ?", (entity_id,)).fetchall()]
    return ok({"entity": dict(entity), "items": items})


@router.post("/api/entities/{entity_id}/merge")
@router.post("/api/entities/{entity_id}/watch")
def api_entity_action(request: Request, entity_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    if request.url.path.endswith("/watch"):
        with store.connect() as conn:
            conn.execute("UPDATE entities SET watched = 1, updated_at = ? WHERE entity_id = ?", (utc_now(), entity_id))
    audit(store, "entity_action", object_type="entity", object_id=entity_id, after=payload or {})
    return ok({"entity_id": entity_id, "accepted": True})


@router.get("/api/relations")
def api_relations(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    return list_table(request, "relations", "relations", limit, offset)


@router.get("/api/claims")
def api_claims(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    return list_table(request, "claims", "claims", limit, offset)


@router.post("/api/relations/{relation_id}/review")
@router.post("/api/claims/{claim_id}/review")
def api_review_object(request: Request, relation_id: str | None = None, claim_id: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    object_id = relation_id or claim_id
    store = get_ops_store(request)
    audit(store, "semantic_object_review", object_id=object_id, after=payload or {})
    return ok({"object_id": object_id, "accepted": True})


@router.get("/api/topics")
def api_topics(request: Request, limit: int = 50, offset: int = 0) -> dict[str, Any]:
    return list_table(request, "topics", "topics", limit, offset)


@router.get("/api/topics/{topic_id}")
def api_topic(request: Request, topic_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        topic = conn.execute("SELECT * FROM topics WHERE topic_id = ?", (topic_id,)).fetchone()
        if not topic:
            return fail("TOPIC_NOT_FOUND", "Topic not found.", status_code=404)
        items = [dict(r) for r in conn.execute("SELECT i.item_id, i.title FROM topic_items ti JOIN inbox_items i ON i.item_id = ti.item_id WHERE ti.topic_id = ?", (topic_id,)).fetchall()]
    return ok({"topic": dict(topic), "items": items})


@router.get("/api/timeline")
def api_timeline(request: Request, limit: int = 100) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        events = [dict(r) for r in conn.execute("SELECT event_id, event_title, event_time, created_at, importance FROM events ORDER BY COALESCE(event_time, created_at) DESC LIMIT ?", (limit,)).fetchall()]
    return ok({"timeline": events})


@router.get("/api/review-queue")
def api_review_queue(request: Request, status: str = "pending", limit: int = 50, offset: int = 0) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM review_queue WHERE status = ? ORDER BY created_at DESC LIMIT ? OFFSET ?", (status, limit, offset)).fetchall()]
    return ok({"reviews": rows})


@router.post("/api/review-queue/{review_id}/resolve")
def api_review_resolve(request: Request, review_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        conn.execute("UPDATE review_queue SET status = ?, reviewed_at = ?, reviewer = ?, review_note = ?, updated_at = ? WHERE id = ?", ((payload or {}).get("status", "resolved"), utc_now(), (payload or {}).get("reviewer", "console"), (payload or {}).get("note", ""), utc_now(), review_id))
    audit(store, "review_resolved", object_type="review", object_id=str(review_id), after=payload or {})
    return ok({"review_id": review_id, "resolved": True})


@router.get("/api/evidence")
def api_evidence_list(request: Request, limit: int = 50) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT extraction_id, item_id, processor, confidence, evidence_json, created_at FROM semantic_extractions ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()]
    return ok({"evidence": rows})


@router.get("/api/evidence/{object_type}/{object_id}")
def api_evidence(request: Request, object_type: str, object_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        if object_type == "item":
            rows = [dict(r) for r in conn.execute("SELECT * FROM semantic_extractions WHERE item_id = ?", (object_id,)).fetchall()]
        else:
            rows = [dict(r) for r in conn.execute("SELECT * FROM audit_log WHERE object_type = ? AND object_id = ? ORDER BY id DESC", (object_type, object_id)).fetchall()]
    return ok({"object_type": object_type, "object_id": object_id, "evidence": rows})


def generate_briefing(store: InboxStore, briefing_type: str) -> dict[str, Any]:
    now = utc_now()
    with store.connect() as conn:
        events = [dict(r) for r in conn.execute("SELECT * FROM events ORDER BY created_at DESC LIMIT 10").fetchall()]
        reviews = [dict(r) for r in conn.execute("SELECT * FROM review_queue WHERE status = 'pending' ORDER BY created_at DESC LIMIT 10").fetchall()]
        title = f"{briefing_type.title()} Briefing {now[:10]}"
        body = "# " + title + "\n\n## Events\n" + "\n".join(f"- {e['event_title']} ({e['status']})" for e in events) + "\n\n## Review Queue\n" + "\n".join(f"- {r['review_type']} {r['target_type']}:{r['target_id']}" for r in reviews)
        briefing_id = f"brief_{briefing_type}_{stable_hash(now)[:12]}"
        conn.execute("INSERT OR REPLACE INTO briefings(briefing_id, briefing_type, title, body_markdown, payload_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)", (briefing_id, briefing_type, title, body, json.dumps({"events": events, "reviews": reviews}, ensure_ascii=False), now, now))
        row = conn.execute("SELECT * FROM briefings WHERE briefing_id = ?", (briefing_id,)).fetchone()
    return dict(row)


@router.get("/api/briefings/daily")
def api_daily_briefings(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM briefings WHERE briefing_type = 'daily' ORDER BY created_at DESC LIMIT 10").fetchall()]
    return ok({"briefings": rows})


@router.post("/api/briefings/daily/generate")
def api_generate_daily(request: Request) -> dict[str, Any]:
    return ok({"briefing": generate_briefing(get_ops_store(request), "daily")})


@router.get("/api/briefings/weekly")
def api_weekly_briefings(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM briefings WHERE briefing_type = 'weekly' ORDER BY created_at DESC LIMIT 10").fetchall()]
    return ok({"briefings": rows})


@router.post("/api/briefings/weekly/generate")
def api_generate_weekly(request: Request) -> dict[str, Any]:
    return ok({"briefing": generate_briefing(get_ops_store(request), "weekly")})


@router.get("/api/saved-views")
def api_saved_views(request: Request) -> dict[str, Any]:
    return list_table(request, "saved_views", "saved_views", 100, 0)


@router.post("/api/saved-views")
def api_saved_view_create(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    view_id = f"view_{uuid.uuid4().hex[:12]}"
    now = utc_now()
    with store.connect() as conn:
        conn.execute("INSERT INTO saved_views(saved_view_id, name, object_type, filters_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (view_id, payload.get("name", "Saved View"), payload.get("object_type", "items"), json.dumps(payload.get("filters") or {}, ensure_ascii=False), now, now))
    return ok({"saved_view_id": view_id})


@router.patch("/api/saved-views/{view_id}")
def api_saved_view_patch(request: Request, view_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        conn.execute("UPDATE saved_views SET name = COALESCE(?, name), filters_json = COALESCE(?, filters_json), updated_at = ? WHERE saved_view_id = ?", (payload.get("name"), json.dumps(payload.get("filters"), ensure_ascii=False) if "filters" in payload else None, utc_now(), view_id))
    return ok({"saved_view_id": view_id})


@router.delete("/api/saved-views/{view_id}")
def api_saved_view_delete(request: Request, view_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    with store.connect() as conn:
        conn.execute("DELETE FROM saved_views WHERE saved_view_id = ?", (view_id,))
    return ok({"saved_view_id": view_id, "deleted": True})


@router.post("/api/agent-query/preview")
def api_agent_query(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    items = api_items(request, keyword=payload.get("query"), limit=int(payload.get("limit", 10)))["data"]["items"]
    compact = [{"item_id": item["item_id"], "title": item["title"], "url": item["url"], "published_at": item["published_at"]} for item in items]
    markdown = "\n".join(f"- [{item['title']}]({item['url'] or '#'})" for item in items)
    return ok({"query": payload.get("query"), "format": payload.get("format", "compact"), "context_pack": compact, "markdown": markdown, "json": compact, "human": markdown or "No matching items."})


@router.get("/api/reports")
def api_reports(request: Request) -> dict[str, Any]:
    return list_table(request, "reports", "reports", 50, 0)


@router.post("/api/reports/generate")
def api_report_generate(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    now = utc_now()
    report_id = f"report_{stable_hash(now + json.dumps(payload, sort_keys=True))[:12]}"
    report_type = payload.get("report_type", "summary")
    title = f"{report_type.title()} Report"
    body = f"# {title}\n\nGenerated at {now}\n\nObject: {payload.get('object_type', 'environment')} {payload.get('object_id', '')}\n"
    with store.connect() as conn:
        conn.execute("INSERT OR REPLACE INTO reports(report_id, report_type, object_type, object_id, title, body_markdown, payload_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (report_id, report_type, payload.get("object_type"), payload.get("object_id"), title, body, json.dumps(payload, ensure_ascii=False), now, now))
    return ok({"report_id": report_id, "title": title, "content": body})


@router.get("/api/reports/{report_id}")
def api_report(request: Request, report_id: str) -> Any:
    store = get_ops_store(request)
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM reports WHERE report_id = ?", (report_id,)).fetchone()
    if not row:
        return fail("REPORT_NOT_FOUND", "Report not found.", status_code=404)
    return ok({"report": dict(row)})
