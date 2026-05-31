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
from app.semantic.candidates import assess_candidate, deterministic_duplicate
from app.semantic.signatures import EventSignature, extract_event_signature
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


def discover_databases(current_path: str | None = None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    legacy = legacy_db_path().resolve()

    _add_db(results, legacy, label="content_inbox", is_legacy=False, current_path=current_path)

    for envs_dir in (
        BASE_DIR / "data" / "environments",
        Path("/data/environments"),
    ):
        if envs_dir.is_dir():
            for child in sorted(envs_dir.iterdir()):
                if not child.is_dir():
                    continue
                db_file = child / "content_inbox.db"
                if db_file.is_file():
                    _add_db(results, db_file.resolve(), label=child.name, is_legacy=False, current_path=current_path)

    if current_path:
        current_resolved = Path(current_path).resolve()
        for entry in results:
            entry["is_current"] = (Path(entry["path"]).resolve() == current_resolved)
    return results


def _add_db(
    results: list[dict[str, Any]],
    path: Path,
    label: str,
    is_legacy: bool = False,
    current_path: str | None = None,
) -> None:
    proof = file_proof(path)
    entry = {
        "label": label,
        "path": str(path),
        "size": proof.get("size"),
        "last_modified": proof.get("modified_at"),
        "is_current": False,
        "is_legacy": is_legacy,
        "exists": proof["exists"],
    }
    if current_path:
        entry["is_current"] = path.resolve() == Path(current_path).resolve()
    results.append(entry)


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
            "is_fresh_database": metadata_get(conn, "is_fresh_database") or ("true" if is_fresh else "false"),
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
        last_reset = conn.execute("SELECT * FROM audit_log WHERE action LIKE 'environment_reset%' ORDER BY id DESC LIMIT 1").fetchone()
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
        "legacy_business_fallback": False,
        "last_reset_at": last_reset["created_at"] if last_reset else None,
    }


OUTPUT_TABLES = [
    "reports",
    "briefings",
    "saved_views",
]

PIPELINE_OUTPUT_TABLES = [
    "review_queue",
    "topic_events",
    "topic_items",
    "topics",
    "claims",
    "relations",
    "item_entities",
    "entities",
    "event_items",
    "events",
    "semantic_extractions",
    "event_candidate_pairs",
    "dedupe_group_items",
    "dedupe_groups",
    "cluster_items",
    "cluster_cards",
    "cluster_relations",
    "source_signals",
    "source_profiles",
    "item_relations",
    "item_cards",
    "llm_call_logs",
    "event_clusters",
]

RUN_RESULT_TABLES = [
    "item_run_links",
    "ingest_run_events",
    "rss_ingest_run_sources",
    "rss_ingest_runs",
    "inbox_items",
]

RESET_TABLES_KEEP_SOURCES = [*OUTPUT_TABLES, *PIPELINE_OUTPUT_TABLES, *RUN_RESULT_TABLES]
RESET_TABLES_CLEAR_ALL = ["rss_sources", *RESET_TABLES_KEEP_SOURCES]
RESET_SCOPE_DETAILS = {
    "clear_runs_items_keep_sources": {
        "label": "清空运行结果，保留 Sources",
        "description": "回到“source 已准备好，但还没有 run/item/pipeline 输出”的状态。",
        "clears": ["runs", "run events", "item_run_links", "inbox_items", "dedupe", "semantic", "clusters/events", "review queue", "briefings/reports"],
        "keeps": ["source registry", "DB identity", "system metadata", "audit log"],
        "risk_level": "high",
        "confirmation": "RESET",
    },
    "clear_all_sources_and_content": {
        "label": "清空 Sources 和所有内容",
        "description": "回到空 Fresh DB，仅保留 schema、DB identity、system metadata 和 audit。",
        "clears": ["sources", "runs", "items", "pipeline outputs", "review queue", "briefings/reports"],
        "keeps": ["DB identity", "system metadata", "audit log"],
        "risk_level": "critical",
        "confirmation": "RESET",
    },
    "clear_pipeline_outputs_keep_items": {
        "label": "只清空 pipeline 派生数据，保留原始 items",
        "description": "用于重新跑 dedupe / semantic / clusters / events / review，不重新抓取 source。",
        "clears": ["dedupe", "semantic", "clusters/events", "entities/relations/claims/topics/timeline", "review queue", "briefings/reports"],
        "keeps": ["sources", "runs", "run events", "item_run_links", "inbox_items"],
        "risk_level": "medium",
        "confirmation": "RESET",
    },
    "clear_outputs_keep_events": {
        "label": "只清空 briefing/report/agent 输出",
        "description": "用于重新生成信息消费输出，不影响 events/review/items。",
        "clears": ["briefings", "reports", "saved views"],
        "keeps": ["sources", "runs", "items", "clusters/events", "review queue"],
        "risk_level": "medium",
        "confirmation": "RESET",
    },
    "clear_by_run_id": {
        "label": "清空指定 run 的结果",
        "description": "只移除所选 run 的 links/events/source progress；仅删除该 run 独占引入的 items。",
        "clears": ["selected run", "run events", "run source progress", "exclusive items", "exclusive item pipeline outputs"],
        "keeps": ["sources", "other runs", "items shared with other runs"],
        "risk_level": "high",
        "confirmation": "RESET <run_id>",
    },
    "clear_by_source_id": {
        "label": "清空指定 source 及下游内容",
        "description": "只移除所选 source 的 items/links/downstream outputs；可选择同时 archive source。",
        "clears": ["selected source items", "source run links", "exclusive run/source progress", "affected pipeline outputs"],
        "keeps": ["other sources", "other source items", "DB identity"],
        "risk_level": "high",
        "confirmation": "RESET <source_id>",
    },
    "create_new_fresh_db": {
        "label": "新建 Fresh DB 环境",
        "description": "创建并切换到新的 Fresh DB 文件，不修改 Legacy DB。",
        "clears": ["当前 UI 选择的工作 DB 会切换"],
        "keeps": ["Legacy DB", "旧 Fresh DB 文件"],
        "risk_level": "medium",
        "confirmation": "RESET",
    },
}


def table_counts(store: InboxStore, tables: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    with store.connect() as conn:
        existing = {row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        for table in tables:
            if table in existing:
                counts[table] = int(conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"] or 0)
    return counts


def existing_tables(conn, tables: list[str]) -> list[str]:
    known = {row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    return [table for table in tables if table in known]


def delete_all_from_tables(conn, tables: list[str]) -> None:
    for table in existing_tables(conn, tables):
        conn.execute(f"DELETE FROM {table}")


def qmarks(values: list[Any]) -> str:
    return ",".join("?" for _ in values)


def select_ids(conn, sql: str, params: list[Any] | tuple[Any, ...]) -> list[str]:
    return [str(row[0]) for row in conn.execute(sql, params).fetchall() if row[0] is not None]


def reset_tables_for_level(level: str) -> list[str]:
    if level == "clear_runs_items_keep_sources":
        return RESET_TABLES_KEEP_SOURCES
    if level == "clear_all_sources_and_content":
        return RESET_TABLES_CLEAR_ALL
    if level == "clear_pipeline_outputs_keep_items":
        return [*OUTPUT_TABLES, *PIPELINE_OUTPUT_TABLES]
    if level == "clear_outputs_keep_events":
        return OUTPUT_TABLES
    return []


def affected_downstream_ids(conn, item_ids: list[str]) -> dict[str, list[str]]:
    if not item_ids:
        return {"cluster_ids": [], "event_ids": [], "dedupe_group_ids": [], "entity_ids": [], "topic_ids": []}
    marks = qmarks(item_ids)
    cluster_ids = select_ids(conn, f"SELECT DISTINCT cluster_id FROM cluster_items WHERE item_id IN ({marks})", item_ids)
    dedupe_group_ids = select_ids(conn, f"SELECT DISTINCT dedupe_group_id FROM dedupe_group_items WHERE item_id IN ({marks})", item_ids)
    entity_ids = select_ids(conn, f"SELECT DISTINCT entity_id FROM item_entities WHERE item_id IN ({marks})", item_ids)
    topic_ids = select_ids(conn, f"SELECT DISTINCT topic_id FROM topic_items WHERE item_id IN ({marks})", item_ids)
    event_ids = select_ids(conn, f"SELECT DISTINCT event_id FROM event_items WHERE item_id IN ({marks})", item_ids)
    if cluster_ids:
        event_ids.extend(select_ids(conn, f"SELECT DISTINCT event_id FROM events WHERE primary_cluster_id IN ({qmarks(cluster_ids)})", cluster_ids))
    return {
        "cluster_ids": sorted(set(cluster_ids)),
        "event_ids": sorted(set(event_ids)),
        "dedupe_group_ids": sorted(set(dedupe_group_ids)),
        "entity_ids": sorted(set(entity_ids)),
        "topic_ids": sorted(set(topic_ids)),
    }


def run_reset_analysis(store: InboxStore, run_id: str) -> dict[str, Any]:
    with store.connect() as conn:
        run = conn.execute("SELECT run_id, status, started_at, new_items_count, duplicate_items_count FROM rss_ingest_runs WHERE run_id = ?", (run_id,)).fetchone()
        item_ids = select_ids(conn, "SELECT DISTINCT item_id FROM item_run_links WHERE run_id = ?", (run_id,))
        exclusive_item_ids = []
        shared_item_ids = []
        for item_id in item_ids:
            other_count = conn.execute("SELECT COUNT(DISTINCT run_id) AS n FROM item_run_links WHERE item_id = ? AND run_id != ?", (item_id, run_id)).fetchone()["n"]
            if int(other_count or 0) == 0:
                exclusive_item_ids.append(item_id)
            else:
                shared_item_ids.append(item_id)
        downstream = affected_downstream_ids(conn, exclusive_item_ids)
        source_rows = conn.execute("SELECT DISTINCT source_id FROM rss_ingest_run_sources WHERE run_id = ?", (run_id,)).fetchall()
    return {
        "run": dict(run) if run else None,
        "run_id": run_id,
        "item_ids": item_ids,
        "exclusive_item_ids": exclusive_item_ids,
        "shared_item_ids": shared_item_ids,
        "source_ids": [row["source_id"] for row in source_rows if row["source_id"]],
        **downstream,
    }


def source_reset_analysis(store: InboxStore, source_ids: list[str]) -> dict[str, Any]:
    source_ids = [sid for sid in source_ids if sid]
    if not source_ids:
        return {"source_ids": [], "sources": [], "item_ids": [], "run_ids": [], "exclusive_run_ids": [], "shared_run_ids": [], "archive_sources": False}
    with store.connect() as conn:
        marks = qmarks(source_ids)
        sources = [dict(row) for row in conn.execute(f"SELECT source_id, source_name, status FROM rss_sources WHERE source_id IN ({marks})", source_ids).fetchall()]
        item_ids = select_ids(conn, f"SELECT DISTINCT item_id FROM inbox_items WHERE source_id IN ({marks}) AND deleted_at IS NULL", source_ids)
        linked_item_ids = select_ids(conn, f"SELECT DISTINCT item_id FROM item_run_links WHERE source_id IN ({marks})", source_ids)
        item_ids = sorted(set(item_ids + linked_item_ids))
        run_ids = select_ids(conn, f"SELECT DISTINCT run_id FROM item_run_links WHERE source_id IN ({marks})", source_ids)
        run_ids.extend(select_ids(conn, f"SELECT DISTINCT run_id FROM rss_ingest_run_sources WHERE source_id IN ({marks})", source_ids))
        run_ids = sorted(set(run_ids))
        exclusive_run_ids = []
        shared_run_ids = []
        for run_id in run_ids:
            other_count = conn.execute(f"SELECT COUNT(DISTINCT source_id) AS n FROM rss_ingest_run_sources WHERE run_id = ? AND source_id NOT IN ({marks})", [run_id, *source_ids]).fetchone()["n"]
            if int(other_count or 0) == 0:
                exclusive_run_ids.append(run_id)
            else:
                shared_run_ids.append(run_id)
        downstream = affected_downstream_ids(conn, item_ids)
    return {
        "source_ids": source_ids,
        "sources": sources,
        "item_ids": item_ids,
        "run_ids": run_ids,
        "exclusive_run_ids": exclusive_run_ids,
        "shared_run_ids": shared_run_ids,
        **downstream,
    }


def delete_item_downstream(conn, item_ids: list[str], downstream: dict[str, list[str]]) -> None:
    if item_ids:
        marks = qmarks(item_ids)
        for table in ["semantic_extractions", "item_entities", "topic_items", "dedupe_group_items", "cluster_items", "event_items", "item_cards", "source_signals"]:
            if table in existing_tables(conn, [table]):
                conn.execute(f"DELETE FROM {table} WHERE item_id IN ({marks})", item_ids)
        if "event_candidate_pairs" in existing_tables(conn, ["event_candidate_pairs"]):
            conn.execute(f"DELETE FROM event_candidate_pairs WHERE item_a_id IN ({marks}) OR item_b_id IN ({marks})", [*item_ids, *item_ids])
        if "item_relations" in existing_tables(conn, ["item_relations"]):
            conn.execute(f"DELETE FROM item_relations WHERE item_a_id IN ({marks}) OR item_b_id IN ({marks})", [*item_ids, *item_ids])
        if "llm_call_logs" in existing_tables(conn, ["llm_call_logs"]):
            conn.execute(f"DELETE FROM llm_call_logs WHERE item_id IN ({marks})", item_ids)
    cluster_ids = downstream.get("cluster_ids", [])
    event_ids = downstream.get("event_ids", [])
    dedupe_group_ids = downstream.get("dedupe_group_ids", [])
    entity_ids = downstream.get("entity_ids", [])
    topic_ids = downstream.get("topic_ids", [])
    if dedupe_group_ids:
        conn.execute(f"DELETE FROM dedupe_groups WHERE dedupe_group_id IN ({qmarks(dedupe_group_ids)})", dedupe_group_ids)
    if cluster_ids:
        marks = qmarks(cluster_ids)
        for table, column in [("cluster_cards", "cluster_id"), ("cluster_relations", "from_cluster_id"), ("source_signals", "cluster_id")]:
            if table in existing_tables(conn, [table]):
                conn.execute(f"DELETE FROM {table} WHERE {column} IN ({marks})", cluster_ids)
        if "cluster_relations" in existing_tables(conn, ["cluster_relations"]):
            conn.execute(f"DELETE FROM cluster_relations WHERE to_cluster_id IN ({marks})", cluster_ids)
        conn.execute(f"DELETE FROM event_clusters WHERE cluster_id IN ({marks})", cluster_ids)
    if event_ids:
        marks = qmarks(event_ids)
        for table, column in [("topic_events", "event_id"), ("relations", "event_id"), ("claims", "event_id"), ("review_queue", "target_id"), ("reports", "object_id")]:
            if table in existing_tables(conn, [table]):
                if table == "review_queue":
                    conn.execute(f"DELETE FROM review_queue WHERE target_type = 'event' AND target_id IN ({marks})", event_ids)
                else:
                    conn.execute(f"DELETE FROM {table} WHERE {column} IN ({marks})", event_ids)
        conn.execute(f"DELETE FROM events WHERE event_id IN ({marks})", event_ids)
    if entity_ids:
        conn.execute(f"DELETE FROM entities WHERE entity_id IN ({qmarks(entity_ids)}) AND entity_id NOT IN (SELECT DISTINCT entity_id FROM item_entities)", entity_ids)
    if topic_ids:
        conn.execute(f"DELETE FROM topics WHERE topic_id IN ({qmarks(topic_ids)}) AND topic_id NOT IN (SELECT DISTINCT topic_id FROM topic_items)", topic_ids)


def clear_source_item_downstream(conn, item_ids: list[str], downstream: dict[str, list[str]]) -> dict[str, Any]:
    """Remove target-source item links while preserving mixed-source objects as stale."""
    if not item_ids:
        return {"stale_cluster_ids": [], "stale_event_ids": [], "deleted_cluster_ids": [], "deleted_event_ids": []}
    marks = qmarks(item_ids)
    for table in ["semantic_extractions", "item_entities", "topic_items", "dedupe_group_items", "cluster_items", "event_items", "item_cards", "source_signals"]:
        if table in existing_tables(conn, [table]):
            conn.execute(f"DELETE FROM {table} WHERE item_id IN ({marks})", item_ids)
    if "event_candidate_pairs" in existing_tables(conn, ["event_candidate_pairs"]):
        conn.execute(f"DELETE FROM event_candidate_pairs WHERE item_a_id IN ({marks}) OR item_b_id IN ({marks})", [*item_ids, *item_ids])
    if "item_relations" in existing_tables(conn, ["item_relations"]):
        conn.execute(f"DELETE FROM item_relations WHERE item_a_id IN ({marks}) OR item_b_id IN ({marks})", [*item_ids, *item_ids])
    if "llm_call_logs" in existing_tables(conn, ["llm_call_logs"]):
        conn.execute(f"DELETE FROM llm_call_logs WHERE item_id IN ({marks})", item_ids)

    stale_cluster_ids: list[str] = []
    deleted_cluster_ids: list[str] = []
    for cluster_id in downstream.get("cluster_ids", []):
        remaining = conn.execute("SELECT COUNT(*) AS n FROM cluster_items WHERE cluster_id = ?", (cluster_id,)).fetchone()["n"]
        if int(remaining or 0) == 0:
            conn.execute("DELETE FROM event_clusters WHERE cluster_id = ?", (cluster_id,))
            conn.execute("DELETE FROM cluster_cards WHERE cluster_id = ?", (cluster_id,))
            deleted_cluster_ids.append(cluster_id)
        else:
            conn.execute("UPDATE event_clusters SET status = 'stale', updated_at = ? WHERE cluster_id = ?", (utc_now(), cluster_id))
            stale_cluster_ids.append(cluster_id)

    stale_event_ids: list[str] = []
    deleted_event_ids: list[str] = []
    for event_id in downstream.get("event_ids", []):
        remaining = conn.execute("SELECT COUNT(*) AS n FROM event_items WHERE event_id = ?", (event_id,)).fetchone()["n"]
        if int(remaining or 0) == 0:
            conn.execute("DELETE FROM topic_events WHERE event_id = ?", (event_id,))
            conn.execute("DELETE FROM relations WHERE event_id = ?", (event_id,))
            conn.execute("DELETE FROM claims WHERE event_id = ?", (event_id,))
            conn.execute("DELETE FROM review_queue WHERE target_type = 'event' AND target_id = ?", (event_id,))
            conn.execute("DELETE FROM reports WHERE object_type = 'event' AND object_id = ?", (event_id,))
            conn.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
            deleted_event_ids.append(event_id)
        else:
            conn.execute("UPDATE events SET status = 'stale', updated_at = ? WHERE event_id = ?", (utc_now(), event_id))
            stale_event_ids.append(event_id)

    dedupe_group_ids = downstream.get("dedupe_group_ids", [])
    if dedupe_group_ids:
        conn.execute(f"DELETE FROM dedupe_groups WHERE dedupe_group_id IN ({qmarks(dedupe_group_ids)}) AND dedupe_group_id NOT IN (SELECT DISTINCT dedupe_group_id FROM dedupe_group_items)", dedupe_group_ids)
    entity_ids = downstream.get("entity_ids", [])
    if entity_ids:
        conn.execute(f"DELETE FROM entities WHERE entity_id IN ({qmarks(entity_ids)}) AND entity_id NOT IN (SELECT DISTINCT entity_id FROM item_entities)", entity_ids)
    topic_ids = downstream.get("topic_ids", [])
    if topic_ids:
        conn.execute(f"DELETE FROM topics WHERE topic_id IN ({qmarks(topic_ids)}) AND topic_id NOT IN (SELECT DISTINCT topic_id FROM topic_items)", topic_ids)
    return {
        "stale_cluster_ids": stale_cluster_ids,
        "stale_event_ids": stale_event_ids,
        "deleted_cluster_ids": deleted_cluster_ids,
        "deleted_event_ids": deleted_event_ids,
    }


def is_fresh_store(store: InboxStore) -> bool:
    try:
        return bool(environment_snapshot(store).get("is_fresh_database"))
    except Exception:
        return False


def reset_preview_data(store: InboxStore, level: str) -> dict[str, Any]:
    tables = reset_tables_for_level(level)
    counts = table_counts(store, tables)
    env = environment_snapshot(store)
    detail = RESET_SCOPE_DETAILS.get(level, {})
    return {
        "database_id": env.get("database_id"),
        "database_path": env.get("database_path"),
        "database_label": env.get("database_label"),
        "is_fresh_database": env.get("is_fresh_database"),
        "level": level,
        "label": detail.get("label", level),
        "description": detail.get("description", ""),
        "clears": detail.get("clears", []),
        "keeps": detail.get("keeps", []),
        "risk_level": detail.get("risk_level", "medium"),
        "tables_affected": tables,
        "counts_before": counts,
        "counts_after_expected": {table: 0 for table in counts},
        "legacy_db_affected": False,
        "recoverability": "soft audit only; cleared rows are not restored automatically",
        "requires_confirmation": detail.get("confirmation", "RESET"),
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


@router.get("/api/environment/databases")
def api_databases(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    current = str(store.database_path.resolve())
    return ok({"databases": discover_databases(current_path=current)})


@router.post("/api/environment/switch")
def api_switch_database(request: Request, payload: dict[str, Any] | None = None) -> Any:
    raw = (payload or {}).get("database_path", "")
    if not raw:
        return fail("MISSING_DATABASE_PATH", "database_path is required")
    target = Path(raw)
    if not target.is_absolute():
        target = BASE_DIR / target
    target = target.resolve()
    if not target.exists() or not target.is_file():
        return fail("DATABASE_NOT_FOUND", f"Database file not found: {target}")
    try:
        import sqlite3
        probe = sqlite3.connect(f"file:{target}?mode=ro", uri=True)
        probe.execute("SELECT 1")
        probe.close()
    except Exception as exc:
        return fail("INVALID_DATABASE", f"Cannot open as SQLite database: {exc}")

    new_store = InboxStore(target)
    is_legacy = target.resolve() == legacy_db_path().resolve()
    label = "content_inbox" if is_legacy else target.parent.name
    ensure_environment_metadata(new_store, label=label, is_fresh=True)
    request.app.state.store = new_store
    settings.database_path = target
    audit(new_store, "database_switched", message=f"Switched to {target}")
    return ok({"environment": environment_snapshot(new_store), "legacy_database": file_proof(legacy_db_path())})


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
        {"name": "not_legacy_default", "ok": True, "message": "content_inbox.sqlite3 is the default primary database."},
        {"name": "real_runs_enabled", "ok": env["real_runs_enabled"], "message": "Set CONTENT_INBOX_ENABLE_REAL_RUNS=1 for real-write runs."},
    ]
    return ok({"environment": env, "checks": checks})


@router.get("/api/environment/report")
def api_environment_report(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    return ok({"environment": environment_snapshot(store), "legacy_database": file_proof(legacy_db_path()), "generated_at": utc_now()})


@router.get("/api/environment/reset-options")
def api_reset_options(request: Request) -> dict[str, Any]:
    store = get_ops_store(request)
    env = environment_snapshot(store)
    return ok(
        {
            "environment": env,
            "enabled": bool(env.get("is_fresh_database")),
            "levels": [{"level": level, **details, "legacy_db_affected": False} for level, details in RESET_SCOPE_DETAILS.items()],
        }
    )


@router.post("/api/environment/reset/preview")
def api_reset_preview(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    level = payload.get("level") or "clear_runs_items_keep_sources"
    if level == "create_new_fresh_db":
        return api_fresh_db_preview(request, payload)
    if level not in RESET_SCOPE_DETAILS:
        return fail("INVALID_RESET_LEVEL", "Unknown reset level.")
    if level == "clear_by_run_id":
        run_id = str(payload.get("run_id") or "").strip()
        if not run_id:
            return fail("RUN_ID_REQUIRED", "请选择一个 run 后再 preview。")
        preview = {**reset_preview_data(store, level), "target": run_reset_analysis(store, run_id)}
        preview["counts_after_expected"] = dict(preview["counts_before"])
        preview["affected_summary"] = {
            "runs": 1 if preview["target"]["run"] else 0,
            "items_deleted": len(preview["target"]["exclusive_item_ids"]),
            "items_unlinked_only": len(preview["target"]["shared_item_ids"]),
            "events_or_clusters_touched": len(preview["target"]["event_ids"]) + len(preview["target"]["cluster_ids"]),
        }
    elif level == "clear_by_source_id":
        raw_ids = payload.get("source_ids") or payload.get("source_id") or []
        source_ids = [raw_ids] if isinstance(raw_ids, str) else list(raw_ids)
        source_ids = [str(sid).strip() for sid in source_ids if str(sid).strip()]
        if not source_ids:
            return fail("SOURCE_ID_REQUIRED", "请选择一个或多个 source 后再 preview。")
        preview = {**reset_preview_data(store, level), "target": {**source_reset_analysis(store, source_ids), "archive_sources": bool(payload.get("archive_sources"))}}
        preview["counts_after_expected"] = dict(preview["counts_before"])
        preview["affected_summary"] = {
            "sources": len(preview["target"]["sources"]),
            "items_deleted": len(preview["target"]["item_ids"]),
            "runs_touched": len(preview["target"]["run_ids"]),
            "events_or_clusters_touched": len(preview["target"]["event_ids"]) + len(preview["target"]["cluster_ids"]),
        }
        preview["safe_strategy"] = "目标 source 的 item 关系会被移除；混合 cluster/event 若仍有其他 item，会标记为 stale 而不是删除。"
    else:
        preview = reset_preview_data(store, level)
    if not preview["is_fresh_database"]:
        return fail("FRESH_DB_REQUIRED", "当前数据库不是 Fresh DB。为避免误删历史数据，已禁用清空操作。", status_code=409, details=preview)
    operation_id = f"reset_{uuid.uuid4().hex}"
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO operation_previews(operation_id, operation_type, payload_json, preview_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (operation_id, "environment_reset", json.dumps(payload, ensure_ascii=False), json.dumps(preview, ensure_ascii=False), utc_now()),
        )
    preview["operation_id"] = operation_id
    return ok(preview)


@router.post("/api/environment/reset/commit")
def api_reset_commit(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    if not is_fresh_store(store):
        return fail("FRESH_DB_REQUIRED", "当前数据库不是 Fresh DB。为避免误删历史数据，已禁用清空操作。", status_code=409)
    level = payload.get("level") or "clear_runs_items_keep_sources"
    if level == "create_new_fresh_db":
        if payload.get("confirmation") != "RESET":
            return fail("UNSAFE_OPERATION_REQUIRES_CONFIRMATION", "请输入 RESET 以确认只切换当前 Fresh DB。")
        return api_fresh_db_create(request, payload)
    if level not in RESET_SCOPE_DETAILS:
        return fail("INVALID_RESET_LEVEL", "Unknown reset level.")
    expected_confirmation = RESET_SCOPE_DETAILS[level].get("confirmation", "RESET")
    target: dict[str, Any] = {}
    if level == "clear_by_run_id":
        run_id = str(payload.get("run_id") or "").strip()
        if not run_id:
            return fail("RUN_ID_REQUIRED", "请选择一个 run 后再 commit。")
        expected_confirmation = f"RESET {run_id}"
        target = run_reset_analysis(store, run_id)
    elif level == "clear_by_source_id":
        raw_ids = payload.get("source_ids") or payload.get("source_id") or []
        source_ids = [raw_ids] if isinstance(raw_ids, str) else list(raw_ids)
        source_ids = [str(sid).strip() for sid in source_ids if str(sid).strip()]
        if not source_ids:
            return fail("SOURCE_ID_REQUIRED", "请选择一个或多个 source 后再 commit。")
        expected_confirmation = f"RESET {source_ids[0]}" if len(source_ids) == 1 else "RESET SOURCES"
        target = source_reset_analysis(store, source_ids)
        target["archive_sources"] = bool(payload.get("archive_sources"))
    if payload.get("confirmation") != expected_confirmation:
        return fail("UNSAFE_OPERATION_REQUIRES_CONFIRMATION", f"请输入 {expected_confirmation} 以确认只清空当前 Fresh DB。")
    tables = reset_tables_for_level(level)
    counts_before = table_counts(store, tables) if tables else {}
    with store.connect() as conn:
        if level in {"clear_runs_items_keep_sources", "clear_all_sources_and_content", "clear_pipeline_outputs_keep_items", "clear_outputs_keep_events"}:
            delete_all_from_tables(conn, tables)
            if level == "clear_pipeline_outputs_keep_items":
                conn.execute("UPDATE inbox_items SET semantic_status = 'pending', primary_cluster_id = NULL, semantic_error = NULL, last_semantic_at = NULL")
        elif level == "clear_by_run_id":
            run_id = target["run_id"]
            exclusive_item_ids = target["exclusive_item_ids"]
            shared_item_ids = target["shared_item_ids"]
            delete_item_downstream(conn, exclusive_item_ids, target)
            if exclusive_item_ids:
                conn.execute(f"DELETE FROM inbox_items WHERE item_id IN ({qmarks(exclusive_item_ids)})", exclusive_item_ids)
            if shared_item_ids:
                conn.execute(f"DELETE FROM item_run_links WHERE run_id = ? AND item_id IN ({qmarks(shared_item_ids)})", [run_id, *shared_item_ids])
            conn.execute("DELETE FROM item_run_links WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM ingest_run_events WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM rss_ingest_run_sources WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM rss_ingest_runs WHERE run_id = ?", (run_id,))
        elif level == "clear_by_source_id":
            source_ids = target["source_ids"]
            item_ids = target["item_ids"]
            target["downstream_cleanup"] = clear_source_item_downstream(conn, item_ids, target)
            if item_ids:
                conn.execute(f"DELETE FROM item_run_links WHERE item_id IN ({qmarks(item_ids)})", item_ids)
                conn.execute(f"DELETE FROM inbox_items WHERE item_id IN ({qmarks(item_ids)})", item_ids)
            if source_ids:
                marks = qmarks(source_ids)
                conn.execute(f"DELETE FROM rss_ingest_run_sources WHERE source_id IN ({marks})", source_ids)
                conn.execute(f"DELETE FROM ingest_run_events WHERE source_id IN ({marks})", source_ids)
                if target.get("archive_sources"):
                    conn.execute(f"UPDATE rss_sources SET status = 'archived', deleted_at = COALESCE(deleted_at, ?), updated_at = ? WHERE source_id IN ({marks})", [utc_now(), utc_now(), *source_ids])
        metadata_set(conn, "last_reset_at", utc_now())
        metadata_set(conn, "last_reset_level", level)
    counts_after = table_counts(store, tables) if tables else {}
    operation_id = payload.get("operation_id") or f"reset_{uuid.uuid4().hex}"
    audit(
        store,
        "environment_reset_committed",
        operation_id=operation_id,
        before={"counts": counts_before},
        after={"counts": counts_after, "level": level, "tables": tables, "target": target, "legacy_db_affected": False},
        message=f"Reset level {level} committed for current Fresh DB.",
    )
    return ok(
        {
            "operation_id": operation_id,
            "database_id": environment_snapshot(store).get("database_id"),
            "database_path": str(store.database_path),
            "level": level,
            "counts_before": counts_before,
            "counts_after": counts_after,
            "tables_affected": tables,
            "target": target,
            "legacy_db_affected": False,
        }
    )


@router.post("/api/environment/fresh-db/preview")
def api_fresh_db_preview(request: Request, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    label = (payload or {}).get("database_label") or f"fresh_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    db_path = BASE_DIR / "data" / "environments" / label / "content_inbox.db"
    return ok({"database_label": label, "database_path": str(db_path), "will_create": not db_path.exists(), "legacy_db_affected": False})


@router.post("/api/environment/fresh-db/create")
def api_fresh_db_create(request: Request, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    label = (payload or {}).get("database_label") or f"fresh_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    db_path = BASE_DIR / "data" / "environments" / label / "content_inbox.db"
    new_store = InboxStore(db_path)
    ensure_environment_metadata(new_store, label=label, is_fresh=True)
    request.app.state.store = new_store
    settings.database_path = db_path
    audit(new_store, "fresh_db_created", message=f"Fresh DB created and selected: {db_path}")
    return ok({"environment": environment_snapshot(new_store), "legacy_db_affected": False})


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


@router.post("/api/sources/check")
def api_source_check(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    feed_url = str(payload.get("feed_url") or "").strip()
    if not feed_url:
        return ok({"valid": False, "error_code": "SOURCE_INVALID_FEED_URL", "message": "feed_url is required."})
    normalized = normalize_url(feed_url) or feed_url
    with store.connect() as conn:
        exists = conn.execute("SELECT source_id FROM rss_sources WHERE normalized_feed_url = ?", (normalized,)).fetchone()
    result: dict[str, Any] = {"feed_url": feed_url, "normalized_feed_url": normalized, "duplicate": bool(exists), "existing_source_id": exists["source_id"] if exists else None}
    try:
        meta, entries = parse_feed(feed_url, source_name=payload.get("source_name"), source_category=payload.get("source_category"), limit=5)
        result.update({"valid": True, "parse_ok": True, "source_name": meta.get("source_name"), "sample_item_count": len(entries), "latest_published_at": entries[0].published_at if entries else None, "sample_titles": [entry.title for entry in entries[:3]]})
    except Exception as exc:
        code, message = classify_exception(exc)
        result.update({"valid": False, "parse_ok": False, "error_code": code, "message": message})
    return ok(result)


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


@router.post("/api/sources/{source_id}/archive")
def api_source_archive(request: Request, source_id: str) -> Any:
    return api_source_delete(request, source_id)


@router.post("/api/sources/{source_id}/restore")
def api_source_restore(request: Request, source_id: str) -> Any:
    store = get_ops_store(request)
    before = store.get_rss_source(source_id)
    if not before:
        return fail("SOURCE_NOT_FOUND", "Source not found.", status_code=404)
    source = store.update_rss_source(source_id, {"status": "active"})
    audit(store, "source_restored", source_id=source_id, before=before, after=source)
    return ok({"source": source})


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


@router.post("/api/sources/bulk/preview")
def api_source_bulk_preview(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    action = payload.get("action") or "archive"
    ids = payload.get("source_ids") or []
    sources = [source for sid in ids if (source := store.get_rss_source(sid))]
    preview = {
        "action": action,
        "source_count": len(sources),
        "sources": [{"source_id": s["source_id"], "source_name": s["source_name"], "status": s["status"]} for s in sources],
        "risk_level": "medium" if action in {"archive", "delete", "disable"} else "low",
        "default_delete_semantics": "soft_archive",
        "legacy_db_affected": False,
        "requires_confirmation": action in {"archive", "delete", "disable", "run"},
    }
    operation_id = f"bulk_{uuid.uuid4().hex}"
    with store.connect() as conn:
        conn.execute(
            "INSERT INTO operation_previews(operation_id, operation_type, payload_json, preview_json, created_at) VALUES (?, ?, ?, ?, ?)",
            (operation_id, "source_bulk", json.dumps(payload, ensure_ascii=False), json.dumps(preview, ensure_ascii=False), utc_now()),
        )
    preview["operation_id"] = operation_id
    return ok(preview)


@router.post("/api/sources/bulk/commit")
def api_source_bulk_commit(request: Request, payload: dict[str, Any]) -> Any:
    store = get_ops_store(request)
    operation_id = payload.get("operation_id")
    if operation_id:
        with store.connect() as conn:
            row = conn.execute("SELECT * FROM operation_previews WHERE operation_id = ?", (operation_id,)).fetchone()
        if not row:
            return fail("OPERATION_NOT_FOUND", "Bulk preview operation was not found.", status_code=404)
        preview = json.loads(row["preview_json"])
        source_ids = [source["source_id"] for source in preview.get("sources", [])]
        action = preview.get("action", "archive")
    else:
        source_ids = payload.get("source_ids") or []
        action = payload.get("action", "archive")
        operation_id = f"bulk_{uuid.uuid4().hex}"
    if action == "enable":
        return bulk_update_sources(request, {"source_ids": source_ids, "operation_id": operation_id}, "active", "source_enabled")
    if action == "disable":
        return bulk_update_sources(request, {"source_ids": source_ids, "operation_id": operation_id}, "disabled", "source_disabled")
    if action in {"archive", "delete"}:
        return bulk_update_sources(request, {"source_ids": source_ids, "operation_id": operation_id}, "archived", "source_archived")
    if action == "export":
        return api_source_export(request, {"format": payload.get("format", "json")})
    return fail("INVALID_BULK_ACTION", "Unsupported bulk action.")


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
        add_event(store, run_id, "semantic_started", message="Generating event-aware semantic objects.")
        semantic_result = generate_information_objects(store, run_id, linked_item_ids)
        add_event(store, run_id, "semantic_completed", message="Semantic objects generated.", payload=semantic_result)
        add_event(store, run_id, "cluster_completed", message="Event clusters generated.", payload={"clusters_created_or_updated": semantic_result.get("clusters_created_or_updated", 0)})
        add_event(store, run_id, "event_completed", message="Events generated.", payload={"events_created_or_updated": semantic_result.get("events_created_or_updated", 0)})
        add_event(store, run_id, "review_queue_generated", message="Review queue generated.", payload={"review_required": semantic_result.get("review_required", 0)})
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


EVENTNESS_NON_EVENT_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("ad", ("sponsored", "advertisement", "promo code", "limited offer", "成人", "广告", "优惠券")),
    ("digest", ("digest", "newsletter", "roundup", "weekly recap", "daily briefing", "market wrap", "日报", "周报", "简报", "综述", "汇总")),
    ("content", ("how to", "tutorial", "guide", "case study", "opinion", "analysis:", "教程", "指南", "如何", "观点", "案例")),
)


def _json_loads(value: Any, fallback: Any) -> Any:
    if value in (None, ""):
        return fallback
    try:
        return json.loads(str(value))
    except Exception:
        return fallback


def classify_item_eventness(row: dict[str, Any], signature: EventSignature | None = None) -> dict[str, Any]:
    title = row.get("title") or ""
    summary = row.get("summary") or ""
    text = f"{title}\n{summary}".strip()
    lowered = text.lower()
    reasons: list[str] = []
    negative_features: list[str] = []

    if not re.sub(r"https?://\S+", "", lowered).strip():
        return {"decision": "low_signal", "confidence": 0.95, "reasons": ["pure_link_or_empty"], "negative_features": ["pure_link_or_empty"]}
    if len(re.findall(r"[A-Za-z0-9\u4e00-\u9fff]", title)) < 8:
        return {"decision": "low_signal", "confidence": 0.9, "reasons": ["short_or_symbolic_title"], "negative_features": ["short_or_symbolic_title"]}

    for decision, needles in EVENTNESS_NON_EVENT_PATTERNS:
        hits = [needle for needle in needles if needle in lowered]
        if hits:
            negative_features.extend(hits)
            return {"decision": decision, "confidence": 0.88 if decision == "content" else 0.93, "reasons": [f"{decision}_keyword"], "negative_features": negative_features}

    signature = signature or extract_event_signature(row)
    if signature.semantic_level == "event_signature" and signature.is_concrete:
        reasons.append("concrete_event_signature")
        return {"decision": "event", "confidence": max(0.9, signature.confidence), "reasons": reasons, "negative_features": negative_features}
    if signature.semantic_level == "thread_signature":
        return {"decision": "thread", "confidence": max(0.62, signature.confidence), "reasons": ["thread_signature"], "negative_features": signature.invalid_reasons}
    if signature.semantic_level == "content_signature":
        return {"decision": "content", "confidence": max(0.7, signature.confidence), "reasons": ["content_signature"], "negative_features": signature.invalid_reasons}
    return {"decision": "unknown", "confidence": 0.55, "reasons": ["no_concrete_event_signature"], "negative_features": signature.invalid_reasons}


def _source_variants_from_raw(*values: Any) -> dict[str, list[str]]:
    urls: list[str] = []
    canonical_urls: list[str] = []
    guids: list[str] = []
    source_ids: list[str] = []
    for value in values:
        raw = _json_loads(value, {})
        if not isinstance(raw, dict):
            continue
        for key in ("url", "link"):
            if raw.get(key):
                urls.append(str(raw[key]))
                normalized = normalize_url(str(raw[key]))
                if normalized:
                    canonical_urls.append(normalized)
        if raw.get("guid"):
            guids.append(str(raw["guid"]))
        if raw.get("source_id"):
            source_ids.append(str(raw["source_id"]))
    return {
        "url_variants": sorted(set(urls))[:10],
        "canonical_url_variants": sorted(set(canonical_urls))[:10],
        "guid_variants": sorted(set(guids))[:10],
        "source_ids": sorted(set(source_ids))[:10],
    }


def _dedupe_method(row: dict[str, Any]) -> str:
    key = row.get("dedupe_key") or ""
    if key.startswith("url:"):
        return "url"
    if key.startswith("guid:"):
        return "guid"
    if "title_date" in key:
        return "title_date"
    if "content" in key:
        return "title_content"
    return "dedupe_key"


def _insert_semantic_extraction(conn: Any, row: dict[str, Any], now: str, eventness: dict[str, Any], signature: EventSignature) -> None:
    item_id = row["item_id"]
    title = row["title"]
    body = f"{title}\n{row['summary'] or ''}"
    terms = extract_terms(body)
    extraction_id = f"se_{stable_hash(item_id)[:16]}"
    normalized = {
        "entities": terms,
        "topics": [row["source_category"] or "General"],
        "claims": [title] if title else [],
        "eventness": eventness,
        "signature": signature.model_dump(),
    }
    conn.execute(
        "INSERT OR REPLACE INTO semantic_extractions(extraction_id, item_id, processor, confidence, needs_review, raw_output_json, normalized_output_json, evidence_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            extraction_id,
            item_id,
            "operational_event_pipeline_v2",
            "high" if eventness["decision"] == "event" else "medium",
            0 if eventness["decision"] == "event" and signature.is_concrete else 1,
            json.dumps({"title": title}, ensure_ascii=False),
            json.dumps(normalized, ensure_ascii=False),
            json.dumps({"eventness": eventness, "signature_invalid_reasons": signature.invalid_reasons}, ensure_ascii=False),
            now,
        ),
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


def _event_title(signature: EventSignature, representative: dict[str, Any]) -> str:
    if signature.actor and signature.product_or_model and signature.action != "other":
        return f"{signature.actor} {signature.action.replace('_', ' ')} {signature.product_or_model}"
    return representative["title"]


def _event_summary(signature: EventSignature, members: list[dict[str, Any]]) -> str:
    representative = members[0]
    if signature.actor and signature.product_or_model and signature.action != "other":
        return f"{signature.actor} {signature.action.replace('_', ' ')} {signature.product_or_model}; supported by {len(members)} item(s)."
    return representative.get("summary") or representative["title"]


def _relation_from_candidate(left: dict[str, Any], right: dict[str, Any], assessment: Any) -> tuple[str, int, int, int, str]:
    hard = deterministic_duplicate(left, right)
    if hard:
        relation = "item_duplicate" if hard[0] == "duplicate" else "near_duplicate"
        return relation, 1, 1, 0, "deterministic_duplicate"
    if assessment.candidate_priority in {"must_run", "high"} and not set(assessment.disqualifiers) & {"generic_entity_overlap", "generic_only_overlap", "same_account_boilerplate", "wide_time_window", "semantic_level_reject"}:
        return "same_event_repeat", 1, 1, 0, "high_confidence_same_event"
    if assessment.candidate_priority == "medium":
        return "uncertain", 0, 1, 1, "medium_candidate_requires_review"
    if assessment.candidate_priority == "suppress":
        return "non_event" if "semantic_level_reject" in assessment.disqualifiers else "different", 0, 0, 0, assessment.candidate_suppression_reason or "suppressed_candidate"
    return "same_topic_different_event", 0, 1, 1, "low_confidence_same_topic"


def generate_information_objects(store: InboxStore, run_id: str, item_ids: list[str]) -> dict[str, Any]:
    if not item_ids:
        return {"item_count": 0}
    now = utc_now()
    stats = {
        "item_count": 0,
        "eventness": {},
        "signature": {"event_signature": 0, "thread_signature": 0, "content_signature": 0, "reject": 0, "invalid": 0},
        "candidates_by_priority": {},
        "candidates_by_lane": {},
        "disqualifiers_by_reason": {},
        "alias_hit_count": 0,
        "auto_merged": 0,
        "review_required": 0,
        "rejected_non_event": 0,
        "clusters_created_or_updated": 0,
        "events_created_or_updated": 0,
    }
    with store.connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM inbox_items WHERE item_id IN ({','.join('?' for _ in item_ids)})",
            item_ids,
        ).fetchall()
        items = [dict(row) for row in rows]
        stats["item_count"] = len(items)
        enriched: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            signature = extract_event_signature(item)
            eventness = classify_item_eventness(item, signature)
            stats["eventness"][eventness["decision"]] = stats["eventness"].get(eventness["decision"], 0) + 1
            stats["signature"][signature.semantic_level] = stats["signature"].get(signature.semantic_level, 0) + 1
            if signature.invalid_reasons:
                stats["signature"]["invalid"] += 1
            stats["alias_hit_count"] += len(signature.alias_hits)
            _insert_semantic_extraction(conn, item, now, eventness, signature)
            enriched.append({"item": item, "signature": signature, "eventness": eventness})
            if eventness["decision"] != "event":
                stats["rejected_non_event"] += 1
                conn.execute(
                    "INSERT INTO review_queue(review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        "eventness_review",
                        "item",
                        item["item_id"],
                        "pending",
                        json.dumps({"eventness": eventness, "signature": signature.model_dump(), "action": "review_item_eventness"}, ensure_ascii=False),
                        "Item did not pass eventness gate; it will not be materialized as an event automatically.",
                        now,
                        now,
                    ),
                )

        event_like = [entry for entry in enriched if entry["eventness"]["decision"] == "event" and entry["signature"].is_concrete]
        parent = {entry["item"]["item_id"]: entry["item"]["item_id"] for entry in event_like}

        def find(item_id: str) -> str:
            while parent[item_id] != item_id:
                parent[item_id] = parent[parent[item_id]]
                item_id = parent[item_id]
            return item_id

        def union(left: str, right: str) -> None:
            root_left = find(left)
            root_right = find(right)
            if root_left != root_right:
                parent[root_right] = root_left

        item_by_id = {entry["item"]["item_id"]: entry for entry in event_like}
        relation_rows: list[dict[str, Any]] = []
        for idx, left_entry in enumerate(event_like):
            for right_entry in event_like[idx + 1 :]:
                left = left_entry["item"]
                right = right_entry["item"]
                assessment = assess_candidate(left, right)
                stats["candidates_by_priority"][assessment.candidate_priority] = stats["candidates_by_priority"].get(assessment.candidate_priority, 0) + 1
                stats["candidates_by_lane"][assessment.lane] = stats["candidates_by_lane"].get(assessment.lane, 0) + 1
                for disqualifier in assessment.disqualifiers:
                    stats["disqualifiers_by_reason"][disqualifier] = stats["disqualifiers_by_reason"].get(disqualifier, 0) + 1
                relation_type, same_event, same_topic, review_required, reason = _relation_from_candidate(left, right, assessment)
                status = "auto_merge" if same_event and relation_type in {"same_event_repeat", "same_event_new_info", "near_duplicate", "item_duplicate"} else ("review" if review_required else "rejected")
                conn.execute(
                    """
                    INSERT INTO event_candidate_pairs(run_id, item_a_id, item_b_id, candidate_score, candidate_priority, lane, features_json, disqualifiers_json, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        left["item_id"],
                        right["item_id"],
                        assessment.candidate_score,
                        assessment.candidate_priority,
                        assessment.lane,
                        json.dumps(assessment.model_dump(), ensure_ascii=False),
                        json.dumps(assessment.disqualifiers, ensure_ascii=False),
                        status,
                        now,
                    ),
                )
                relation_rows.append({"left": left, "right": right, "assessment": assessment, "relation_type": relation_type, "same_event": same_event, "same_topic": same_topic, "review_required": review_required, "reason": reason})
                if same_event:
                    union(left["item_id"], right["item_id"])
                    stats["auto_merged"] += 1
                elif review_required:
                    stats["review_required"] += 1
                    conn.execute(
                        "INSERT INTO review_queue(review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            "event_relation_review",
                            "item_pair",
                            f"{left['item_id']}:{right['item_id']}",
                            "pending",
                            json.dumps({"relation_type": relation_type, "candidate": assessment.model_dump(), "action": "review_relation"}, ensure_ascii=False),
                            reason,
                            now,
                            now,
                        ),
                    )

        groups: dict[str, list[dict[str, Any]]] = {}
        for entry in event_like:
            groups.setdefault(find(entry["item"]["item_id"]), []).append(entry)

        for root, members in groups.items():
            representative_entry = max(members, key=lambda entry: (entry["signature"].confidence, len(entry["item"].get("summary") or ""), entry["item"]["title"]))
            signature = representative_entry["signature"]
            member_items = [entry["item"] for entry in members]
            cluster_key = signature.signature_key or root
            cluster_id = "cluster_" + stable_hash(f"operational_v2:{cluster_key}")[:16]
            evidence = {
                "schema_version": "operational_v2",
                "run_id": run_id,
                "signature": signature.model_dump(),
                "eventness": [entry["eventness"] for entry in members],
                "member_item_ids": [entry["item"]["item_id"] for entry in members],
                "decision_source": "rule",
            }
            conn.execute(
                """
                INSERT OR REPLACE INTO event_clusters(cluster_id, cluster_title, cluster_summary, entities_json, representative_item_id, first_seen_at, last_seen_at, item_count, status, created_by, confidence, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cluster_id,
                    _event_title(signature, representative_entry["item"]),
                    _event_summary(signature, member_items),
                    json.dumps({"actor": signature.actor, "product": signature.product_or_model, "action": signature.action, "signature_key": signature.signature_key}, ensure_ascii=False),
                    representative_entry["item"]["item_id"],
                    min((entry["item"].get("published_at") or now) for entry in members),
                    max((entry["item"].get("published_at") or now) for entry in members),
                    len(members),
                    "active" if len(members) > 1 else "needs_review",
                    "operational_v2_rule",
                    min(0.98, max(0.72, signature.confidence if len(members) == 1 else signature.confidence + 0.05)),
                    now,
                    now,
                ),
            )
            for member in members:
                item = member["item"]
                item_relation = "source_material" if item["item_id"] == representative_entry["item"]["item_id"] else "same_event_repeat"
                relation = next((row for row in relation_rows if item["item_id"] in {row["left"]["item_id"], row["right"]["item_id"]} and row["same_event"]), None)
                if relation:
                    item_relation = relation["relation_type"]
                item_evidence = {
                    "schema_version": "operational_v2",
                    "run_id": run_id,
                    "signature": member["signature"].model_dump(),
                    "eventness": member["eventness"],
                    "cluster_evidence": evidence,
                }
                conn.execute(
                    """
                    INSERT OR REPLACE INTO cluster_items(cluster_id, item_id, primary_relation, same_event, same_topic, confidence, reason, evidence_json, decision_source, schema_version, input_fingerprint, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cluster_id,
                        item["item_id"],
                        item_relation,
                        1,
                        1,
                        member["signature"].confidence,
                        "High-confidence event signature/relation materialization.",
                        json.dumps(item_evidence, ensure_ascii=False),
                        "rule",
                        "operational_v2",
                        stable_hash(cluster_id + item["item_id"] + json.dumps(member["signature"].model_dump(), sort_keys=True)),
                        now,
                        now,
                    ),
                )
                conn.execute("UPDATE inbox_items SET primary_cluster_id = ? WHERE item_id = ?", (cluster_id, item["item_id"]))
            event_id = "event_" + stable_hash(cluster_id)[:16]
            relation_summary: dict[str, int] = {}
            for member in members:
                relation = "source_material" if member["item"]["item_id"] == representative_entry["item"]["item_id"] else "same_event_repeat"
                relation_summary[relation] = relation_summary.get(relation, 0) + 1
            event_evidence = {
                **evidence,
                "primary_cluster_id": cluster_id,
                "source_item_count": len(members),
                "source_count": len({entry["item"].get("source_id") or entry["item"].get("source_name") for entry in members}),
                "relation_summary": relation_summary,
            }
            conn.execute(
                "INSERT OR REPLACE INTO events(event_id, event_title, event_summary, event_type, event_time, status, importance, confidence, primary_cluster_id, evidence_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id,
                    _event_title(signature, representative_entry["item"]),
                    _event_summary(signature, member_items),
                    signature.action if signature.action != "other" else "event",
                    signature.date_bucket,
                    "ready" if len(members) > 1 else "needs_review",
                    min(5, max(1, len(members) + (1 if len(members) > 1 else 0))),
                    min(0.98, max(0.72, signature.confidence if len(members) == 1 else signature.confidence + 0.05)),
                    cluster_id,
                    json.dumps(event_evidence, ensure_ascii=False),
                    now,
                    now,
                ),
            )
            for member in members:
                role = "source_material" if member["item"]["item_id"] == representative_entry["item"]["item_id"] else "supporting"
                conn.execute("INSERT OR IGNORE INTO event_items(event_id, item_id, role, created_at) VALUES (?, ?, ?, ?)", (event_id, member["item"]["item_id"], role, now))
            if len(members) == 1:
                stats["review_required"] += 1
                conn.execute(
                    "INSERT INTO review_queue(review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    ("event_candidate", "event", event_id, "pending", json.dumps({"action": "review_event", "evidence": event_evidence}, ensure_ascii=False), "Single-item event cluster needs review before high-confidence use.", now, now),
                )
            stats["clusters_created_or_updated"] += 1
            stats["events_created_or_updated"] += 1
    return stats


def run_dedupe_stage(store: InboxStore, run_id: str, item_ids: list[str]) -> dict[str, Any]:
    now = utc_now()
    created = 0
    explained_duplicates = 0
    seen_multiple = 0
    with store.connect() as conn:
        rows = conn.execute(
            f"SELECT item_id, dedupe_key, url, guid, title, source_id, source_name, source_category, published_at, created_at, last_seen_at, seen_count, raw_json, latest_raw_json, latest_seen_summary FROM inbox_items WHERE item_id IN ({','.join('?' for _ in item_ids)})",
            item_ids,
        ).fetchall() if item_ids else []
        groups: dict[str, list[Any]] = {}
        for row in rows:
            key = row["dedupe_key"] or normalize_url(row["url"] or "") or normalized_title(row["title"])
            groups.setdefault(key, []).append(row)
        for key, members in groups.items():
            group_id = "dg_" + stable_hash(key)[:16]
            primary = members[0]["item_id"]
            total_seen = sum(int(member["seen_count"] or 1) for member in members)
            if total_seen > len(members):
                explained_duplicates += 1
            seen_multiple += sum(1 for member in members if int(member["seen_count"] or 1) > 1)
            variants = {}
            for member in members:
                merged = _source_variants_from_raw(member["raw_json"], member["latest_raw_json"])
                for variant_key, values in merged.items():
                    variants.setdefault(variant_key, set()).update(values)
            evidence = {
                "schema_version": "operational_v2",
                "run_id": run_id,
                "dedupe_key": key,
                "dedupe_method": _dedupe_method(dict(members[0])),
                "canonical_item_id": primary,
                "member_count": len(members),
                "seen_count": total_seen,
                "source_count": len({member["source_id"] or member["source_name"] for member in members}),
                "first_seen_at": min(member["created_at"] or now for member in members),
                "last_seen_at": max(member["last_seen_at"] or now for member in members),
                "latest_seen_summaries": [member["latest_seen_summary"] for member in members if member["latest_seen_summary"]][:5],
                "url_variants": sorted(variants.get("url_variants", set()))[:10],
                "canonical_url_variants": sorted(variants.get("canonical_url_variants", set()))[:10],
                "guid_variants": sorted(variants.get("guid_variants", set()))[:10],
                "source_ids": sorted(variants.get("source_ids", set()))[:10],
            }
            conn.execute(
                "INSERT OR REPLACE INTO dedupe_groups(dedupe_group_id, primary_item_id, dedupe_method, confidence, evidence_json, review_status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (group_id, primary, evidence["dedupe_method"], 0.9 if total_seen > 1 else 0.55, json.dumps(evidence, ensure_ascii=False), "reviewed" if total_seen == 1 else "explained", now, now),
            )
            for member in members:
                role = "canonical" if member["item_id"] == primary else _dedupe_method(dict(member))
                conn.execute("INSERT OR IGNORE INTO dedupe_group_items(dedupe_group_id, item_id, role, created_at) VALUES (?, ?, ?, ?)", (group_id, member["item_id"], role, now))
            created += 1
    coverage = explained_duplicates / seen_multiple if seen_multiple else 1.0
    return {"dedupe_groups_created_or_updated": created, "seen_count_gt_1_items": seen_multiple, "dedupe_explanation_count": explained_duplicates, "dedupe_explanation_coverage": round(coverage, 4)}


from app.semantic.operational_pipeline import generate_information_objects as generate_information_objects  # noqa: E402,F811
from app.semantic.operational_pipeline import run_dedupe_stage as run_dedupe_stage  # noqa: E402,F811


def item_ids_for_run(store: InboxStore, run_id: str) -> list[str]:
    with store.connect() as conn:
        return [row["item_id"] for row in conn.execute("SELECT DISTINCT item_id FROM item_run_links WHERE run_id = ?", (run_id,)).fetchall()]


def pipeline_status(store: InboxStore, run_id: str) -> dict[str, str]:
    with store.connect() as conn:
        event_types = {row["event_type"] for row in conn.execute("SELECT event_type FROM ingest_run_events WHERE run_id = ?", (run_id,)).fetchall()}
    return {
        "dedupe": "completed" if "dedupe_completed" in event_types else "pending",
        "semantic": "completed" if "semantic_completed" in event_types else "pending",
        "cluster": "completed" if "cluster_completed" in event_types else ("completed" if "semantic_completed" in event_types else "pending"),
        "event": "completed" if "event_completed" in event_types else ("completed" if "semantic_completed" in event_types else "pending"),
        "review_queue": "completed" if "review_queue_generated" in event_types else ("completed" if "semantic_completed" in event_types else "pending"),
        "briefing": "completed" if "briefing_generated" in event_types else "pending",
        "report": "completed" if "report_generated" in event_types else "pending",
    }


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
    return ok({"run": run, "sources": sources, "recent_events": events, "pipeline": pipeline_status(store, run_id), "environment": environment_snapshot(store)})


@router.get("/api/runs/{run_id}/report")
def api_run_report(request: Request, run_id: str) -> Any:
    store = get_ops_store(request)
    run = store.get_ingest_run(run_id)
    if not run:
        return fail("RUN_NOT_FOUND", "Run not found.", status_code=404)
    sources = store.list_ingest_run_sources(run_id)
    with store.connect() as conn:
        trusted_events = [
            dict(r)
            for r in conn.execute(
                """
                SELECT event_id, event_title, event_type, status, confidence, importance, primary_cluster_id
                FROM events
                WHERE status = 'ready' OR confidence >= 0.9
                ORDER BY importance DESC, COALESCE(event_time, created_at) DESC
                LIMIT 10
                """
            ).fetchall()
        ]
        pending_reviews = int(conn.execute("SELECT COUNT(*) AS n FROM review_queue WHERE status = 'pending'").fetchone()["n"] or 0)
    event_lines = "\n".join(
        f"- {event['event_title']}：{event['event_type']}，置信度 {float(event['confidence'] or 0):.2f}"
        for event in trusted_events
    ) or "- 暂无可信事件"
    body = (
        f"# 运行报告 {run_id}\n\n"
        f"状态: {run['status']}\n\n"
        f"新增条目: {run['new_items_count']}\n\n"
        f"信息源数量: {len(sources)}\n\n"
        "## 可信事件\n"
        f"{event_lines}\n\n"
        "## 质量概览\n"
        f"- 可信事件数: {len(trusted_events)}\n"
        f"- 待审核项: {pending_reviews}\n"
        "- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。\n"
    )
    return ok({"format": "markdown", "content": body, "run": run, "sources": sources})


@router.post("/api/runs/{run_id}/pipeline/{stage}")
def api_run_pipeline_stage(request: Request, run_id: str, stage: str) -> Any:
    store = get_ops_store(request)
    if not store.get_ingest_run(run_id):
        return fail("RUN_NOT_FOUND", "Run not found.", status_code=404)
    item_ids = item_ids_for_run(store, run_id)
    if stage == "dedupe":
        add_event(store, run_id, "dedupe_started", message="去重阶段开始。")
        result = run_dedupe_stage(store, run_id, item_ids)
        add_event(store, run_id, "dedupe_completed", message="去重阶段完成。", payload=result)
    elif stage in {"semantic", "clusters", "events", "review"}:
        add_event(store, run_id, "semantic_started", message="语义/聚合/事件阶段开始。")
        result = generate_information_objects(store, run_id, item_ids)
        add_event(store, run_id, "semantic_completed", message="语义提取完成。", payload=result)
        add_event(store, run_id, "cluster_completed", message="聚合线索生成完成。", payload={"clusters_created_or_updated": result.get("clusters_created_or_updated", 0)})
        add_event(store, run_id, "event_completed", message="事件生成完成。", payload={"events_created_or_updated": result.get("events_created_or_updated", 0)})
        add_event(store, run_id, "review_queue_generated", message="审核队列生成完成。", payload={"review_required": result.get("review_required", 0)})
    elif stage == "briefing":
        briefing = generate_briefing(store, "daily")
        add_event(store, run_id, "briefing_generated", message="每日简报已生成。", payload={"briefing_id": briefing["briefing_id"]})
        result = {"briefing": briefing}
    elif stage == "report":
        report = api_report_generate(request, {"report_type": "run", "object_type": "run", "object_id": run_id})["data"]
        add_event(store, run_id, "report_generated", message="运行报告已生成。", payload=report)
        result = report
    else:
        return fail("INVALID_PIPELINE_STAGE", "Unsupported pipeline stage.")
    audit(store, "pipeline_stage_completed", run_id=run_id, object_type="pipeline_stage", object_id=stage, after=result)
    return ok({"run_id": run_id, "stage": stage, "result": result, "pipeline": pipeline_status(store, run_id)})


@router.post("/api/runs/{run_id}/briefing")
def api_run_briefing(request: Request, run_id: str) -> Any:
    return api_run_pipeline_stage(request, run_id, "briefing")


@router.post("/api/runs/{run_id}/report")
def api_run_report_generate(request: Request, run_id: str) -> Any:
    return api_run_pipeline_stage(request, run_id, "report")


@router.post("/api/runs/{run_id}/cancel")
def api_run_cancel(request: Request, run_id: str) -> dict[str, Any]:
    store = get_ops_store(request)
    _CANCELLED_RUNS.add(run_id)
    add_event(store, run_id, "run_cancelled", level="warning", message="已请求取消任务。")
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
        events = [
            dict(r)
            for r in conn.execute(
                """
                SELECT *
                FROM events
                WHERE status = 'ready' OR confidence >= 0.9
                ORDER BY importance DESC, COALESCE(event_time, created_at) DESC
                LIMIT 10
                """
            ).fetchall()
        ]
        reviews = [dict(r) for r in conn.execute("SELECT * FROM review_queue WHERE status = 'pending' ORDER BY created_at DESC LIMIT 10").fetchall()]
        type_cn = "每日" if briefing_type == "daily" else "每周"
        title = f"{type_cn}简报 {now[:10]}"
        event_lines = "\n".join(f"- {e['event_title']}（可信事件，置信度 {float(e['confidence'] or 0):.2f}）" for e in events) or "- 暂无可信事件"
        review_lines = "\n".join(f"- {r['review_type']} {r['target_type']}:{r['target_id']}" for r in reviews) or "- 暂无待审核项"
        body = "# " + title + "\n\n## 可信事件\n" + event_lines + "\n\n## 待审核\n" + review_lines
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
    return ok({"query": payload.get("query"), "format": payload.get("format", "compact"), "context_pack": compact, "markdown": markdown, "json": compact, "human": markdown or "没有匹配的条目。"})


@router.get("/api/reports")
def api_reports(request: Request) -> dict[str, Any]:
    return list_table(request, "reports", "reports", 50, 0)


@router.post("/api/reports/generate")
def api_report_generate(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    store = get_ops_store(request)
    now = utc_now()
    report_id = f"report_{stable_hash(now + json.dumps(payload, sort_keys=True))[:12]}"
    report_type = payload.get("report_type", "summary")
    type_cn = {"summary": "总体摘要", "source_health": "信息源健康度", "event": "事件报告", "run": "运行报告"}.get(report_type, report_type)
    title = f"{type_cn}"
    with store.connect() as conn:
        trusted_events = [
            dict(r)
            for r in conn.execute(
                """
                SELECT event_id, event_title, event_type, status, confidence, importance, event_time, primary_cluster_id
                FROM events
                WHERE status = 'ready' OR confidence >= 0.9
                ORDER BY importance DESC, COALESCE(event_time, created_at) DESC
                LIMIT 10
                """
            ).fetchall()
        ]
        pending_reviews = int(conn.execute("SELECT COUNT(*) AS n FROM review_queue WHERE status = 'pending'").fetchone()["n"] or 0)
        event_total = int(conn.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"] or 0)
    event_lines = "\n".join(
        f"- {event['event_title']}：{event['event_type']}，置信度 {float(event['confidence'] or 0):.2f}，cluster {event['primary_cluster_id'] or 'none'}"
        for event in trusted_events
    ) or "- 暂无可信事件"
    body = (
        f"# {title}\n\n"
        f"生成时间: {now}\n\n"
        f"关联对象: {payload.get('object_type', 'environment')} {payload.get('object_id', '')}\n\n"
        "## 可信事件\n"
        f"{event_lines}\n\n"
        "## 质量概览\n"
        f"- 可信事件数: {len(trusted_events)}\n"
        f"- 全部事件数: {event_total}\n"
        f"- 待审核项: {pending_reviews}\n"
        "- 输入策略: 仅消费已物化事件，不直接消费 raw item 或 weak candidate。\n"
    )
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
