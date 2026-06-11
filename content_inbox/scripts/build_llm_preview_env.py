#!/usr/bin/env python3
"""Build an LLM Preview environment from a real, read-only database.

This script is the entry point for the LLM Preview workflow:

    1. Copy sampled items from the real DB (read-only) to a preview DB.
    2. Run the operational v3 pipeline (dedupe → item cards → information objects).
    3. Optionally run live LLM proposal-only passes (candidate_discovery,
       signature_repair, relation_judge, cluster_proposal).
    4. Write audit logs, review queue entries, and a structured manifest.
    5. The resulting preview DB can be served by the backend and inspected via
       the frontend console.

Safety properties
-----------------
- The source (real) database is **never** written to.
- All LLM calls are **proposal-only** — no auto-merge, no real-write.
- The preview DB is a completely separate file.

Usage
-----

    # Build preview DB with defaults (event_hotspots, 40 items)
    PYTHONPATH=. python3 scripts/build_llm_preview_env.py

    # Build with live LLM
    CONTENT_INBOX_LLM_ENABLE_LIVE=1 \\
    PYTHONPATH=. python3 scripts/build_llm_preview_env.py \\
      --source-db data/content_inbox.sqlite3 \\
      --preview-db data/environments/llm_preview/content_inbox.db \\
      --reset-preview \\
      --limit 40 \\
      --sample-mode event_hotspots \\
      --enable-live-llm \\
      --max-llm-calls 20

    # Build larger sample without LLM
    PYTHONPATH=. python3 scripts/build_llm_preview_env.py \\
      --limit 100 \\
      --sample-mode recent \\
      --preview-db data/environments/llm_preview/content_inbox.db
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from app.config import BASE_DIR, settings
from app.ops_api import api_report_generate, api_run_report, ensure_environment_metadata, generate_briefing
from app.semantic import db as semantic_db
from app.semantic.cards import generate_item_cards
from app.semantic.clusters import process_item_clusters
from app.semantic.evaluate import (
    build_markdown_report,
    build_summary,
    copy_sample_to_eval_store,
    sample_existing_items,
    source_scope_summary,
)
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.operational_pipeline import generate_information_objects, run_dedupe_stage
from app.semantic.relations import insert_review
from app.semantic.signatures import extract_event_signature
from app.semantic.schemas import (
    CANDIDATE_DISCOVERY_PROMPT_VERSION,
    SCHEMA_VERSION,
    SIGNATURE_REPAIR_PROMPT_VERSION,
    SEMANTIC_RELATION_JUDGE_PROMPT_VERSION,
    CandidateDiscoveryOutput,
    SignatureRepairOutput,
    SemanticRelationJudgeProposal,
)
from app.storage import InboxStore
from app.utils import stable_hash, utc_now


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _request_for(store: InboxStore) -> Any:
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=store)))


def _fetch_all(store: InboxStore, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with store.connect() as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def _fetch_one(store: InboxStore, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
    with store.connect() as conn:
        row = conn.execute(sql, params).fetchone()
    return dict(row) if row else {}


def _parse_json(value: Any, fallback: Any = None) -> Any:
    if value in (None, ""):
        return fallback
    try:
        return json.loads(str(value))
    except Exception:
        return fallback


# ---------------------------------------------------------------------------
# LLM proposal passes (adapted from real_use_smoke.py)
# ---------------------------------------------------------------------------

def run_live_llm_passes(
    store: InboxStore,
    *,
    max_calls: int,
    enabled_modes: list[str],
    model: str = "deepseek-v4-flash",
) -> dict[str, Any]:
    live_enabled = os.getenv("CONTENT_INBOX_LLM_ENABLE_LIVE") == "1"
    if not live_enabled:
        return {
            "enabled": False,
            "reason": "CONTENT_INBOX_LLM_ENABLE_LIVE is not 1",
            "calls_attempted": 0,
            "calls_succeeded": 0,
            "calls_failed": 0,
            "calls_skipped": 1,
            "schema_valid": 0,
            "schema_invalid": 0,
            "timeout_count": 0,
            "modes_run": [],
            "proposals": {},
        }

    client = SemanticLLMClient(store, live=True, max_calls=max_calls, model=model)
    stats = {
        "enabled": True,
        "provider": model,
        "max_calls": max_calls,
        "calls_attempted": 0,
        "calls_succeeded": 0,
        "calls_failed": 0,
        "calls_skipped": 0,
        "schema_valid": 0,
        "schema_invalid": 0,
        "timeout_count": 0,
        "modes_run": [],
        "proposals": {},
        "examples": [],
    }

    mode_funcs = {
        "candidate_discovery": _run_candidate_discovery_pass,
        "signature_repair": _run_signature_repair_pass,
        "relation_judge": _run_relation_judge_pass,
        "cluster_proposal": _run_cluster_proposal_pass,
    }

    enabled_count = sum(1 for m in enabled_modes if m in mode_funcs)
    per_mode_calls = max(1, max_calls // max(enabled_count, 1)) if enabled_count else max_calls

    for mode in enabled_modes:
        if mode not in mode_funcs:
            continue
        if client.calls >= max_calls:
            stats["calls_skipped"] += 1
            continue
        remaining = min(per_mode_calls, max_calls - client.calls)
        try:
            result = mode_funcs[mode](store, client, max_calls=remaining)
            stats["modes_run"].append(mode)
            stats["proposals"][mode] = result.get("proposal_count", 0)
            stats["calls_succeeded"] += result.get("succeeded", 0)
            stats["calls_failed"] += result.get("failed", 0)
            stats["calls_skipped"] += result.get("skipped", 0)
            stats["schema_valid"] += result.get("schema_valid", 0)
            stats["schema_invalid"] += result.get("schema_invalid", 0)
            stats["timeout_count"] += result.get("timeout_count", 0)
            for example in result.get("examples", []):
                if len(stats["examples"]) < 10:
                    stats["examples"].append({"mode": mode, **example})
        except Exception as exc:
            stats["modes_run"].append(mode)
            stats["proposals"][mode] = 0
            stats["calls_failed"] += 1
            stats["examples"].append({"mode": mode, "error": str(exc)[:200]})

    stats["calls_attempted"] = stats["calls_succeeded"] + stats["calls_failed"]
    return stats


def _run_candidate_discovery_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    items = _fetch_all(
        store,
        """
        SELECT ic.*, ii.title, ii.summary, ii.source_name, ii.published_at
        FROM item_cards ic
        JOIN inbox_items ii ON ii.item_id = ic.item_id
        WHERE ic.is_current = 1
        ORDER BY ii.published_at DESC
        LIMIT 30
        """,
    )
    if len(items) < 2:
        return result

    pairs = []
    for i in range(len(items)):
        sig_i = extract_event_signature(items[i])
        if sig_i.semantic_level != "event_signature":
            continue
        for j in range(i + 1, min(i + 6, len(items))):
            sig_j = extract_event_signature(items[j])
            if sig_j.semantic_level != "event_signature":
                continue
            if sig_i.signature_key and sig_i.signature_key == sig_j.signature_key:
                continue
            pairs.append((items[i], items[j]))
            if len(pairs) >= max_calls * 2:
                break
        if len(pairs) >= max_calls * 2:
            break

    for left, right in pairs[:max_calls]:
        if client.calls >= client.max_calls:
            result["skipped"] += 1
            continue
        input_data = {
            "item_a": {
                "item_id": left["item_id"],
                "title": left.get("title") or left.get("canonical_title"),
                "summary": left.get("summary") or left.get("short_summary"),
                "source": left.get("source_name"),
                "published_at": left.get("published_at"),
            },
            "item_b": {
                "item_id": right["item_id"],
                "title": right.get("title") or right.get("canonical_title"),
                "summary": right.get("summary") or right.get("short_summary"),
                "source": right.get("source_name"),
                "published_at": right.get("published_at"),
            },
        }
        output, call_id, reason = client.call_json(
            task_type="candidate_discovery",
            prompt_version=CANDIDATE_DISCOVERY_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=CandidateDiscoveryOutput,
            max_tokens=1200,
            item_id=left["item_id"],
            source_id=left.get("source_name"),
        )
        if output and output.candidates:
            result["succeeded"] += 1
            result["schema_valid"] += 1
            for candidate in output.candidates:
                if candidate.should_create_candidate and candidate.confidence >= 0.6:
                    insert_review(
                        store,
                        "llm_candidate_discovery",
                        "item",
                        left["item_id"],
                        {
                            "reason": f"LLM candidate discovery: {candidate.reason_code}",
                            "candidate_item_id": right["item_id"],
                            "candidate_lane": candidate.candidate_lane,
                            "candidate_relation_hint": candidate.candidate_relation_hint,
                            "confidence": candidate.confidence,
                            "evidence": candidate.evidence,
                            "risk_flags": candidate.risk_flags,
                            "llm_call_id": call_id,
                        },
                    )
                    result["proposal_count"] += 1
                if len(result["examples"]) < 3:
                    result["examples"].append({
                        "type": "candidate_discovery",
                        "left_title": (left.get("title") or left.get("canonical_title"))[:80],
                        "right_title": (right.get("title") or right.get("canonical_title"))[:80],
                        "should_create": candidate.should_create_candidate,
                        "confidence": candidate.confidence,
                        "reason_code": candidate.reason_code,
                    })
        elif output:
            result["succeeded"] += 1
            result["schema_valid"] += 1
        else:
            result["failed"] += 1
            if "timeout" in (reason or "").lower():
                result["timeout_count"] += 1
            else:
                result["schema_invalid"] += 1
    return result


def _run_signature_repair_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    items = _fetch_all(
        store,
        """
        SELECT ic.*, ii.title, ii.summary, ii.source_name, ii.published_at
        FROM item_cards ic
        JOIN inbox_items ii ON ii.item_id = ic.item_id
        WHERE ic.is_current = 1
        ORDER BY ii.published_at DESC
        LIMIT 20
        """,
    )
    repair_candidates = []
    for item in items:
        sig = extract_event_signature(item)
        if sig.semantic_level != "event_signature":
            entities_raw = item.get("entities_json") or "[]"
            try:
                entities = json.loads(entities_raw) if isinstance(entities_raw, str) else entities_raw
            except Exception:
                entities = []
            if entities and len(entities) >= 2:
                repair_candidates.append(item)

    for item in repair_candidates[:max_calls]:
        if client.calls >= client.max_calls:
            result["skipped"] += 1
            continue
        input_data = {
            "item_id": item["item_id"],
            "title": item.get("title") or item.get("canonical_title"),
            "summary": item.get("summary") or item.get("short_summary"),
            "entities": (
                json.loads(item.get("entities_json") or "[]")
                if isinstance(item.get("entities_json"), str)
                else item.get("entities_json") or []
            ),
            "source": item.get("source_name"),
            "published_at": item.get("published_at"),
        }
        output, call_id, reason = client.call_json(
            task_type="signature_repair",
            prompt_version=SIGNATURE_REPAIR_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=SignatureRepairOutput,
            max_tokens=1200,
            item_id=item["item_id"],
            source_id=item.get("source_name"),
        )
        if output and output.repairs:
            result["succeeded"] += 1
            result["schema_valid"] += 1
            for repair in output.repairs:
                if repair.confidence >= 0.5:
                    insert_review(
                        store,
                        "llm_signature_repair",
                        "item",
                        repair.item_id or item["item_id"],
                        {
                            "reason": f"LLM signature repair: {repair.proposed_event_signature}",
                            "proposed_actor": repair.proposed_actor,
                            "proposed_product": repair.proposed_product,
                            "proposed_action": repair.proposed_action,
                            "proposed_event_signature": repair.proposed_event_signature,
                            "confidence": repair.confidence,
                            "evidence": repair.evidence,
                            "risk_flags": repair.risk_flags,
                            "llm_call_id": call_id,
                        },
                    )
                    result["proposal_count"] += 1
                if len(result["examples"]) < 3:
                    result["examples"].append({
                        "type": "signature_repair",
                        "title": (item.get("title") or item.get("canonical_title"))[:80],
                        "proposed_actor": repair.proposed_actor,
                        "proposed_product": repair.proposed_product,
                        "proposed_action": repair.proposed_action,
                        "confidence": repair.confidence,
                    })
        elif output:
            result["succeeded"] += 1
            result["schema_valid"] += 1
        else:
            result["failed"] += 1
            if "timeout" in (reason or "").lower():
                result["timeout_count"] += 1
            else:
                result["schema_invalid"] += 1
    return result


def _run_relation_judge_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    candidates = _fetch_all(
        store,
        """
        SELECT ecp.*,
               a.title AS left_title, a.summary AS left_summary,
               a.source_name AS left_source, a.published_at AS left_published,
               b.title AS right_title, b.summary AS right_summary,
               b.source_name AS right_source, b.published_at AS right_published
        FROM event_candidate_pairs ecp
        LEFT JOIN inbox_items a ON a.item_id = ecp.item_a_id
        LEFT JOIN inbox_items b ON b.item_id = ecp.item_b_id
        WHERE ecp.status IN ('review', 'pending')
        ORDER BY
            CASE ecp.candidate_priority
                WHEN 'must_run' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                ELSE 4
            END
        LIMIT ?
        """,
        (max_calls,),
    )
    for candidate in candidates[:max_calls]:
        if client.calls >= client.max_calls:
            result["skipped"] += 1
            continue
        input_data = {
            "item_a": {
                "item_id": candidate["item_a_id"],
                "title": candidate["left_title"],
                "summary": candidate["left_summary"],
                "source": candidate["left_source"],
                "published_at": candidate["left_published"],
            },
            "item_b": {
                "item_id": candidate["item_b_id"],
                "title": candidate["right_title"],
                "summary": candidate["right_summary"],
                "source": candidate["right_source"],
                "published_at": candidate["right_published"],
            },
        }
        output, call_id, reason = client.call_json(
            task_type="relation_judge",
            prompt_version=SEMANTIC_RELATION_JUDGE_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=SemanticRelationJudgeProposal,
            max_tokens=1200,
            item_id=candidate["item_a_id"],
            source_id=candidate.get("left_source"),
        )
        if output:
            result["succeeded"] += 1
            result["schema_valid"] += 1
            insert_review(
                store,
                "llm_relation_judge",
                "candidate_pair",
                candidate["item_a_id"],
                {
                    "reason": f"LLM relation judge: {output.relation}",
                    "candidate_item_id": candidate["item_b_id"],
                    "relation": output.relation,
                    "confidence": output.confidence,
                    "should_merge_event_cluster": output.should_merge_event_cluster,
                    "should_link_as_thread": output.should_link_as_thread,
                    "reason_code": output.reason_code,
                    "evidence": output.evidence,
                    "risk_flags": output.risk_flags,
                    "llm_call_id": call_id,
                },
            )
            result["proposal_count"] += 1
            if len(result["examples"]) < 3:
                result["examples"].append({
                    "type": "relation_judge",
                    "left_title": (candidate.get("left_title") or "")[:80],
                    "right_title": (candidate.get("right_title") or "")[:80],
                    "relation": output.relation,
                    "confidence": output.confidence,
                    "reason_code": output.reason_code,
                })
        else:
            result["failed"] += 1
            if "timeout" in (reason or "").lower():
                result["timeout_count"] += 1
            else:
                result["schema_invalid"] += 1
    return result


def _run_cluster_proposal_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    try:
        cluster_result = process_item_clusters(
            store,
            limit=20,
            live=True,
            max_candidates=3,
            max_calls=max_calls,
            model=client.model,
            llm_proposal_only=True,
            allow_controlled_auto_merge=False,
            patch_cards=False,
        )
        stats = cluster_result.get("stats", {})
        result["proposal_count"] = stats.get("review", 0)
        result["succeeded"] = stats.get("llm_calls", 0)
        result["schema_valid"] = stats.get("llm_calls", 0)
        result["failed"] = stats.get("llm_items", 0) - stats.get("llm_calls", 0)
    except Exception as exc:
        result["failed"] = 1
        result["examples"].append({"type": "cluster_proposal", "error": str(exc)[:200]})
    return result


# ---------------------------------------------------------------------------
# Preview DB build
# ---------------------------------------------------------------------------

def build_preview_env(
    *,
    source_db: Path,
    preview_db: Path,
    reset_preview: bool = False,
    limit: int = 40,
    sample_mode: str = "event_hotspots",
    source_filter: str | None = None,
    source_url_prefix: str | None = None,
    enable_live_llm: bool = False,
    llm_provider: str = "deepseek-v4-flash",
    max_llm_calls: int = 20,
    llm_mode: str = "candidate_discovery,signature_repair,relation_judge,cluster_proposal",
) -> dict[str, Any]:
    """Build the LLM preview environment."""
    started = datetime.now(timezone.utc)
    warnings: list[str] = []

    # 1. Validate source DB
    if not source_db.is_file():
        return {"ok": False, "error": f"Source DB does not exist: {source_db}"}

    # 2. Prepare preview DB
    preview_db.parent.mkdir(parents=True, exist_ok=True)
    if reset_preview and preview_db.exists():
        preview_db.unlink()
    if preview_db.exists():
        return {"ok": False, "error": f"Preview DB already exists: {preview_db}. Use --reset-preview to overwrite."}

    # Copy source DB to preview DB
    import sqlite3
    import shutil

    # For a clean preview, we create a fresh DB from the source schema + sampled data
    shutil.copy2(str(source_db), str(preview_db))

    # 3. Open stores
    source_store = InboxStore(source_db)
    preview_store = InboxStore(preview_db)

    # 4. Sample items from source (read-only)
    source_scope = {}
    with source_store.connect() as conn:
        item_count = int(conn.execute("SELECT COUNT(*) AS n FROM inbox_items WHERE deleted_at IS NULL").fetchone()["n"] or 0)
        distinct_sources = conn.execute("SELECT COUNT(DISTINCT COALESCE(source_id, source_name, feed_url, 'unknown')) AS n FROM inbox_items WHERE deleted_at IS NULL").fetchone()["n"] or 0
        source_scope = {
            "item_count": item_count,
            "source_count": int(distinct_sources),
        }

    sampled_items = sample_existing_items(
        source_store,
        limit,
        source_filter=source_filter,
        source_url_prefix=source_url_prefix,
        sample_mode=sample_mode,
    )

    if not sampled_items:
        return {"ok": False, "error": "No items sampled from source DB"}

    # 5. Clear preview DB data and re-insert sampled items
    _reset_preview_data(preview_store, sampled_items)

    # 6. Run pipeline on preview DB
    run_id = "llm_preview_" + stable_hash(utc_now())[:12]
    now = utc_now()
    ensure_environment_metadata(preview_store, label="llm_preview", is_fresh=True)
    preview_store.create_ingest_run({
        "run_id": run_id,
        "trigger_type": "llm_preview_build",
        "source_mode": sample_mode,
        "status": "success",
        "started_at": now,
        "finished_at": now,
        "selected_source_count": len({item.get("source_id") or item.get("source_name") for item in sampled_items}),
        "success_source_count": len({item.get("source_id") or item.get("source_name") for item in sampled_items}),
        "new_items_count": len(sampled_items),
        "processed_items_count": len(sampled_items),
        "created_by": "build_llm_preview_env",
        "request": {"limit": limit, "sample_mode": sample_mode, "source_filter": source_filter, "source_url_prefix": source_url_prefix},
        "summary": {"warnings": warnings},
    })

    item_ids = [item["item_id"] for item in sampled_items]
    dedupe = run_dedupe_stage(preview_store, run_id, item_ids)
    item_cards = generate_item_cards(preview_store, limit=len(item_ids), batch_size=5, live=False)
    information_objects = generate_information_objects(preview_store, run_id, item_ids)

    # 7. Run live LLM passes if enabled
    live_llm_stats: dict[str, Any] | None = None
    if enable_live_llm:
        enabled_modes = [mode.strip() for mode in llm_mode.split(",") if mode.strip()]
        live_llm_stats = run_live_llm_passes(
            preview_store,
            max_calls=max_llm_calls,
            enabled_modes=enabled_modes,
            model=llm_provider,
        )

    # 8. Generate briefings and reports
    daily_briefing = generate_briefing(preview_store, "daily")
    req = _request_for(preview_store)
    run_report = api_report_generate(req, {"report_type": "run", "object_type": "run", "object_id": run_id})["data"]
    run_endpoint_report = api_run_report(req, run_id)["data"]

    # 9. Collect statistics
    review_count = int(_fetch_one(preview_store, "SELECT COUNT(*) AS n FROM review_queue WHERE status = 'pending'").get("n") or 0)
    event_count = int(_fetch_one(preview_store, "SELECT COUNT(*) AS n FROM events").get("n") or 0)
    cluster_count = int(_fetch_one(preview_store, "SELECT COUNT(*) AS n FROM event_clusters").get("n") or 0)
    llm_call_count = int(_fetch_one(preview_store, "SELECT COUNT(*) AS n FROM llm_call_logs WHERE status = 'ok'").get("n") or 0)
    llm_fail_count = int(_fetch_one(preview_store, "SELECT COUNT(*) AS n FROM llm_call_logs WHERE status = 'failed'").get("n") or 0)

    # 10. Build manifest
    manifest = {
        "source_db": str(source_db.resolve()),
        "preview_db": str(preview_db.resolve()),
        "created_at": started.isoformat(),
        "sample_mode": sample_mode,
        "limit": limit,
        "sampled_items": len(sampled_items),
        "real_db_item_count": source_scope["item_count"],
        "real_db_source_count": source_scope["source_count"],
        "llm_enabled": enable_live_llm,
        "llm_provider": llm_provider if enable_live_llm else None,
        "max_llm_calls": max_llm_calls if enable_live_llm else 0,
        "llm_calls_succeeded": live_llm_stats.get("calls_succeeded", 0) if live_llm_stats else 0,
        "llm_calls_failed": live_llm_stats.get("calls_failed", 0) if live_llm_stats else 0,
        "llm_calls_schema_invalid": live_llm_stats.get("schema_invalid", 0) if live_llm_stats else 0,
        "llm_modes_run": live_llm_stats.get("modes_run", []) if live_llm_stats else [],
        "llm_proposals": live_llm_stats.get("proposals", {}) if live_llm_stats else {},
        "review_queue_pending": review_count,
        "event_count": event_count,
        "cluster_count": cluster_count,
        "total_llm_calls": llm_call_count + llm_fail_count,
        "write_mode": "preview_db_only",
        "auto_merge_enabled": False,
        "sample_item_ids": [item["item_id"] for item in sampled_items[:20]],
        "warnings": warnings,
    }

    # 11. Write manifest
    manifest_path = preview_db.parent / "preview_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    # 12. Write report
    finished = datetime.now(timezone.utc)
    report_path = preview_db.parent / "llm_preview_report.md"
    report_md = _render_preview_report(
        manifest=manifest,
        source_scope=source_scope,
        dedupe=dedupe,
        item_cards=item_cards,
        information_objects=information_objects,
        live_llm=live_llm_stats,
        daily_briefing=daily_briefing,
        run_report=run_report,
        run_endpoint_report=run_endpoint_report,
        warnings=warnings,
        started=started,
        finished=finished,
    )
    report_path.write_text(report_md, encoding="utf-8")

    return {
        "ok": True,
        "manifest": manifest,
        "manifest_path": str(manifest_path),
        "report_path": str(report_path),
        "preview_db": str(preview_db.resolve()),
    }


def _reset_preview_data(store: InboxStore, sampled_items: list[dict[str, Any]]) -> None:
    """Clear operational/semantic tables in preview DB and re-insert sampled items.

    The DB file was copied from source, so it has the full schema and data.
    We clear items not in our sample, and also clear all derived pipeline tables.
    """
    from app.dedupe import build_dedupe_key
    from app.models import NormalizedContent, ScreeningResult

    # Phase 1: Clear derived/pipeline tables (must commit before inserts use separate connections)
    with store.connect() as conn:
        tables_to_clear = [
            "item_cards", "item_relations", "cluster_items", "cluster_cards",
            "cluster_relations", "event_clusters", "events", "event_items",
            "entities", "item_entities", "relations", "claims",
            "semantic_extractions", "event_candidate_pairs",
            "source_signals", "source_profiles",
            "review_queue", "llm_call_logs",
            "dedupe_groups", "dedupe_group_items",
            "briefings", "reports",
            "topics", "topic_items", "topic_events",
            "saved_views",
            "ingest_run_events", "item_run_links", "source_operation_audit",
            "audit_log", "operation_previews",
            "rss_ingest_runs", "rss_ingest_run_sources",
        ]
        for table in tables_to_clear:
            try:
                conn.execute(f"DELETE FROM {table}")
            except Exception:
                pass  # table may not exist yet
        conn.execute("DELETE FROM inbox_items")

    # Phase 2: Re-insert sampled items (separate connection, no lock conflict)
    for item in sampled_items:
        try:
            screening = ScreeningResult.model_validate(item["screening"])
        except Exception:
            screening = ScreeningResult(
                summary=item.get("summary") or item.get("title"),
                category="其他",
                value_score=3,
                personal_relevance=3,
                suggested_action="review",
                reason="fallback screening for preview",
                screening_status="skipped",
            )
        normalized = NormalizedContent(
            title=item["title"],
            url=item.get("url"),
            source_id=item.get("source_id"),
            feed_url=item.get("feed_url"),
            source_name=item.get("source_name") or "unknown",
            source_category=item.get("source_category"),
            content_type=item.get("content_type") or "article",
            published_at=item.get("published_at"),
            author=item.get("author"),
            summary=item.get("summary"),
            content_text=item.get("content_text"),
            guid=item.get("guid"),
        )
        store.insert(build_dedupe_key(normalized), normalized, screening, raw={"source_item_id": item["item_id"]})


def _render_preview_report(
    *,
    manifest: dict[str, Any],
    source_scope: dict[str, Any],
    dedupe: dict[str, Any],
    item_cards: dict[str, Any],
    information_objects: dict[str, Any],
    live_llm: dict[str, Any] | None,
    daily_briefing: dict[str, Any],
    run_report: dict[str, Any],
    run_endpoint_report: dict[str, Any],
    warnings: list[str],
    started: datetime,
    finished: datetime,
) -> str:
    lines = [
        "# LLM Preview Environment Report",
        "",
        f"Generated: {started.isoformat()}",
        f"Duration: {(finished - started).total_seconds():.1f}s",
        "",
        "## Scope",
        "",
        f"- **Source DB:** `{manifest['source_db']}`",
        f"- **Preview DB:** `{manifest['preview_db']}`",
        f"- **Write mode:** preview_db_only (real DB untouched)",
        f"- **Auto-merge:** disabled",
        f"- **Sample mode:** {manifest['sample_mode']}",
        f"- **Limit:** {manifest['limit']}",
        f"- **Sampled items:** {manifest['sampled_items']}",
        f"- **Real DB item count:** {manifest['real_db_item_count']}",
        f"- **Real DB source count:** {manifest['real_db_source_count']}",
        "",
        "## Live LLM Status",
        "",
    ]
    if live_llm:
        lines.extend([
            f"- **Provider:** {live_llm.get('provider', 'unknown')}",
            f"- **Calls attempted:** {live_llm.get('calls_attempted', 0)}",
            f"- **Calls succeeded:** {live_llm.get('calls_succeeded', 0)}",
            f"- **Calls failed:** {live_llm.get('calls_failed', 0)}",
            f"- **Schema valid:** {live_llm.get('schema_valid', 0)}",
            f"- **Schema invalid:** {live_llm.get('schema_invalid', 0)}",
            f"- **Modes run:** {', '.join(live_llm.get('modes_run', []))}",
            f"- **Proposals:** {json.dumps(live_llm.get('proposals', {}))}",
            "",
            "### LLM Examples",
            "",
        ])
        for example in live_llm.get("examples", []):
            lines.append(f"- `{json.dumps(example, ensure_ascii=False)}`")
        lines.append("")
    else:
        lines.extend([
            "- **Status:** disabled (set CONTENT_INBOX_LLM_ENABLE_LIVE=1 to enable)",
            "",
        ])

    lines.extend([
        "## Pipeline Results",
        "",
        f"- Dedupe: `{json.dumps(dedupe, ensure_ascii=False)}`",
        f"- Item cards: `{json.dumps(item_cards.get('stats', {}), ensure_ascii=False)}`",
        f"- Information objects: `{json.dumps(information_objects, ensure_ascii=False)}`",
        "",
        "## Review Queue",
        "",
        f"- Pending reviews: {manifest['review_queue_pending']}",
        f"- Events: {manifest['event_count']}",
        f"- Clusters: {manifest['cluster_count']}",
        f"- Total LLM calls: {manifest['total_llm_calls']}",
        "",
        "## Daily Briefing Preview",
        "",
        "```markdown",
        daily_briefing.get("body_markdown", "")[:2000],
        "```",
        "",
        "## Warnings",
        "",
    ])
    for w in warnings:
        lines.append(f"- {w}")
    if not warnings:
        lines.append("- None")

    lines.extend([
        "",
        "## Frontend Startup",
        "",
        "```bash",
        "# Terminal 1: Start backend pointing to preview DB",
        "cd content_inbox",
        f"CONTENT_INBOX_DB_PATH={manifest['preview_db']} \\",
        "CONTENT_INBOX_ENABLE_REAL_RUNS=0 \\",
        "PYTHONPATH=. python3 -m app.server",
        "",
        "# Terminal 2: Start frontend console",
        "cd content_inbox_console",
        "CONTENT_INBOX_FRONTEND_API_BASE=http://127.0.0.1:8787 \\",
        "uvicorn app.main:app --host 127.0.0.1 --port 8788 --reload",
        "",
        "# Open in browser:",
        "# http://127.0.0.1:8788/dashboard",
        "# http://127.0.0.1:8788/review-queue",
        "# http://127.0.0.1:8788/events",
        "# http://127.0.0.1:8788/clusters",
        "# http://127.0.0.1:8788/briefings",
        "# http://127.0.0.1:8788/reports",
        "# http://127.0.0.1:8788/environment",
        "```",
        "",
        "## Verification Checklist",
        "",
        "- [ ] Backend health check shows preview DB path",
        "- [ ] Environment page shows `llm_preview` label",
        "- [ ] Dashboard shows preview data",
        "- [ ] Review queue shows LLM proposals (if enabled)",
        "- [ ] Events page shows generated events",
        "- [ ] Clusters page shows event clusters",
        "- [ ] Briefings page shows generated briefing",
        "- [ ] Reports page shows run report",
        "- [ ] Real DB file modification time unchanged",
        "",
        "## Known Issues",
        "",
        "- None reported",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build LLM Preview environment from a real, read-only database.",
    )
    parser.add_argument(
        "--source-db",
        default=str(settings.database_path),
        help="Path to the real (source) SQLite database. Default: current settings DB.",
    )
    parser.add_argument(
        "--preview-db",
        default=str(BASE_DIR / "data" / "environments" / "llm_preview" / "content_inbox.db"),
        help="Path for the preview database. Default: data/environments/llm_preview/content_inbox.db",
    )
    parser.add_argument(
        "--reset-preview",
        action="store_true",
        default=False,
        help="Delete existing preview DB before building.",
    )
    parser.add_argument(
        "--limit", type=int, default=40,
        help="Maximum number of items to sample. Default: 40.",
    )
    parser.add_argument(
        "--sample-mode",
        choices=["recent", "duplicate_candidates", "cluster_candidates", "source_scope_full", "mixed", "event_hotspots"],
        default="event_hotspots",
        help="Sampling strategy. Default: event_hotspots.",
    )
    parser.add_argument("--source-filter")
    parser.add_argument("--source-url-prefix")
    parser.add_argument(
        "--enable-live-llm",
        action="store_true",
        default=False,
        help="Enable live DeepSeek LLM calls.",
    )
    parser.add_argument(
        "--llm-provider",
        default="deepseek-v4-flash",
        help="LLM model name. Default: deepseek-v4-flash.",
    )
    parser.add_argument(
        "--max-llm-calls", type=int, default=20,
        help="Maximum live LLM calls. Default: 20.",
    )
    parser.add_argument(
        "--llm-mode",
        default="candidate_discovery,signature_repair,relation_judge,cluster_proposal",
        help="Comma-separated LLM capability modes.",
    )
    parser.add_argument(
        "--write-mode",
        default="preview_db_only",
        choices=["preview_db_only"],
        help="Write mode. Only preview_db_only is supported (real DB is never written).",
    )

    args = parser.parse_args()

    source_db = Path(args.source_db)
    preview_db = Path(args.preview_db)

    print(f"Source DB: {source_db}")
    print(f"Preview DB: {preview_db}")
    print(f"Reset preview: {args.reset_preview}")
    print(f"Limit: {args.limit}, Sample mode: {args.sample_mode}")
    print(f"Live LLM: {args.enable_live_llm}")
    if args.enable_live_llm:
        print(f"  Provider: {args.llm_provider}, Max calls: {args.max_llm_calls}")
        print(f"  Modes: {args.llm_mode}")
    print()

    result = build_preview_env(
        source_db=source_db,
        preview_db=preview_db,
        reset_preview=args.reset_preview,
        limit=args.limit,
        sample_mode=args.sample_mode,
        source_filter=args.source_filter,
        source_url_prefix=args.source_url_prefix,
        enable_live_llm=args.enable_live_llm,
        llm_provider=args.llm_provider,
        max_llm_calls=args.max_llm_calls,
        llm_mode=args.llm_mode,
    )

    if result.get("ok"):
        print("✓ Preview environment built successfully")
        print(f"  Preview DB: {result['preview_db']}")
        print(f"  Manifest:   {result['manifest_path']}")
        print(f"  Report:     {result['report_path']}")
        m = result["manifest"]
        print(f"  Items:      {m['sampled_items']}")
        print(f"  Reviews:    {m['review_queue_pending']}")
        print(f"  Events:     {m['event_count']}")
        print(f"  Clusters:   {m['cluster_count']}")
        if m.get("llm_enabled"):
            print(f"  LLM calls:  {m['llm_calls_succeeded']} succeeded, {m['llm_calls_failed']} failed")
        print()
        print("To start the preview backend:")
        print(f"  CONTENT_INBOX_DB_PATH={result['preview_db']} PYTHONPATH=. python3 -m app.server")
        print()
        print("Real DB has NOT been modified.")
        return 0
    else:
        print(f"✗ Failed: {result.get('error')}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
