from __future__ import annotations

import argparse
import json
import os
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from app.config import BASE_DIR, settings
from app.ops_api import api_report_generate, api_run_report, ensure_environment_metadata, generate_briefing
from app.semantic import db as semantic_db
from app.semantic.cards import generate_item_cards
from app.semantic.clusters import process_item_clusters
from app.semantic.evaluate import copy_sample_to_eval_store
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.operational_pipeline import generate_information_objects, run_dedupe_stage
from app.semantic.relations import insert_review
from app.semantic.signatures import extract_event_signature
from app.semantic.schemas import (
    CANDIDATE_DISCOVERY_PROMPT_VERSION,
    SIGNATURE_REPAIR_PROMPT_VERSION,
    SEMANTIC_RELATION_JUDGE_PROMPT_VERSION,
    SCHEMA_VERSION,
    CandidateDiscoveryOutput,
    SignatureRepairOutput,
    SemanticRelationJudgeProposal,
)
from app.storage import InboxStore
from app.utils import stable_hash, utc_now


def request_for(store: InboxStore) -> Any:
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=store)))


def make_temp_store() -> tuple[InboxStore, Path]:
    tmp = tempfile.NamedTemporaryFile(prefix="content_inbox_real_use_smoke_", suffix=".sqlite3", delete=False)
    tmp.close()
    path = Path(tmp.name)
    return InboxStore(path), path


def fetch_all(store: InboxStore, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with store.connect() as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def fetch_one(store: InboxStore, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
    with store.connect() as conn:
        row = conn.execute(sql, params).fetchone()
    return dict(row) if row else {}


def parse_json(value: Any, fallback: Any) -> Any:
    if value in (None, ""):
        return fallback
    try:
        return json.loads(str(value))
    except Exception:
        return fallback


def source_scope_summary(source_store: InboxStore) -> dict[str, Any]:
    with source_store.connect() as conn:
        item_count = int(conn.execute("SELECT COUNT(*) AS n FROM inbox_items WHERE deleted_at IS NULL").fetchone()["n"] or 0)
        source_count = int(conn.execute("SELECT COUNT(DISTINCT COALESCE(source_id, source_name, feed_url, 'unknown')) AS n FROM inbox_items WHERE deleted_at IS NULL").fetchone()["n"] or 0)
        latest = conn.execute("SELECT MAX(COALESCE(published_at, created_at)) AS latest_at FROM inbox_items WHERE deleted_at IS NULL").fetchone()["latest_at"]
    return {"item_count": item_count, "source_count": source_count, "latest_item_time": latest}


def cluster_audit(store: InboxStore) -> dict[str, Any]:
    clusters = fetch_all(
        store,
        """
        SELECT cluster_id, cluster_title, item_count, status, confidence, entities_json, representative_item_id
        FROM event_clusters
        ORDER BY item_count DESC, confidence DESC, cluster_title
        LIMIT 20
        """,
    )
    multi = [cluster for cluster in clusters if int(cluster.get("item_count") or 0) > 1]
    samples = []
    for cluster in clusters[:10]:
        members = fetch_all(
            store,
            """
            SELECT ci.primary_relation, ii.item_id, ii.title, ii.source_id, ii.source_name, ii.published_at
            FROM cluster_items ci
            JOIN inbox_items ii ON ii.item_id = ci.item_id
            WHERE ci.cluster_id = ?
            ORDER BY ci.created_at ASC
            LIMIT 6
            """,
            (cluster["cluster_id"],),
        )
        samples.append(
            {
                "cluster_id": cluster["cluster_id"],
                "title": cluster["cluster_title"],
                "item_count": cluster["item_count"],
                "status": cluster["status"],
                "confidence": cluster["confidence"],
                "signature": parse_json(cluster.get("entities_json"), {}),
                "members": members,
            }
        )
    relation_counts = Counter(row["primary_relation"] for row in fetch_all(store, "SELECT primary_relation FROM cluster_items"))
    return {
        "cluster_count": len(fetch_all(store, "SELECT cluster_id FROM event_clusters")),
        "multi_item_cluster_count": len(fetch_all(store, "SELECT cluster_id FROM event_clusters WHERE item_count > 1")),
        "ready_event_count": int(fetch_one(store, "SELECT COUNT(*) AS n FROM events WHERE status = 'ready' OR confidence >= 0.9").get("n") or 0),
        "cluster_item_relations": dict(relation_counts),
        "top_clusters": samples,
        "multi_item_clusters": multi[:10],
    }


def candidate_audit(store: InboxStore) -> dict[str, Any]:
    rows = fetch_all(store, "SELECT candidate_priority, lane, status, reason_code, features_json FROM event_candidate_pairs")
    by_priority = Counter(row.get("candidate_priority") or "unknown" for row in rows)
    by_lane = Counter(row.get("lane") or "unknown" for row in rows)
    by_status = Counter(row.get("status") or "unknown" for row in rows)
    review_rows = fetch_all(
        store,
        """
        SELECT review_type, target_type, target_id, reason, suggestion_json
        FROM review_queue
        WHERE status = 'pending'
        ORDER BY created_at DESC
        LIMIT 20
        """,
    )
    return {
        "candidate_pair_count": len(rows),
        "by_priority": dict(by_priority),
        "by_lane": dict(by_lane),
        "by_status": dict(by_status),
        "pending_review_count": int(fetch_one(store, "SELECT COUNT(*) AS n FROM review_queue WHERE status = 'pending'").get("n") or 0),
        "review_samples": review_rows[:10],
    }


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
        "candidate_discovery": run_candidate_discovery_pass,
        "signature_repair": run_signature_repair_pass,
        "relation_judge": run_relation_judge_pass,
        "cluster_proposal": run_cluster_proposal_pass,
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


def run_candidate_discovery_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    items = fetch_all(
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
                        "left_title": left.get("title") or left.get("canonical_title"),
                        "right_title": right.get("title") or right.get("canonical_title"),
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


def run_signature_repair_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    items = fetch_all(
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
                        "title": item.get("title") or item.get("canonical_title"),
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


def run_relation_judge_pass(
    store: InboxStore, client: SemanticLLMClient, max_calls: int
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "proposal_count": 0, "succeeded": 0, "failed": 0, "skipped": 0,
        "schema_valid": 0, "schema_invalid": 0, "timeout_count": 0, "examples": [],
    }
    candidates = fetch_all(
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


def run_cluster_proposal_pass(
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


def render_markdown(summary: dict[str, Any]) -> str:
    briefing = summary["outputs"]["daily_briefing_preview"]
    report = summary["outputs"]["run_report_preview"]
    clusters = summary["cluster_audit"]["top_clusters"]
    item_card_stats = (summary["pipeline"].get("item_cards") or {}).get("stats", {})
    information_objects = summary["pipeline"].get("information_objects") or {}
    cluster_lines = []
    for cluster in clusters[:8]:
        member_titles = "; ".join(member["title"] for member in cluster.get("members", [])[:3])
        cluster_lines.append(f"- {cluster['title']} | items={cluster['item_count']} | status={cluster['status']} | members={member_titles}")
    return "\n".join(
        [
            "# Operational v3 Real-Use Smoke Report",
            "",
            f"Generated at: {summary['metadata']['generated_at']}",
            "",
            "## Scope",
            "",
            f"- source_db_path: `{summary['metadata']['source_db_path']}`",
            f"- evaluation_db_path: `{summary['metadata']['evaluation_db_path']}`",
            f"- dry_run: `{summary['metadata']['dry_run']}`",
            f"- write_real_db: `{summary['metadata']['write_real_db']}`",
            f"- sample_mode: `{summary['metadata']['sample_mode']}`",
            f"- limit: `{summary['metadata']['limit']}`",
            f"- source_filter: `{summary['metadata']['source_filter']}`",
            f"- source_url_prefix: `{summary['metadata']['source_url_prefix']}`",
            f"- source item/source scope: `{summary['source_scope']}`",
            "",
            "## Pipeline",
            "",
            f"- sampled_items: {summary['metadata']['items_sampled']}",
            f"- dedupe: `{summary['pipeline']['dedupe']}`",
            f"- item_cards: `{item_card_stats}`",
            f"- information_objects: `{information_objects}`",
            "",
            "## Candidate And Review Trace",
            "",
            f"- candidate_pair_count: {summary['candidate_audit']['candidate_pair_count']}",
            f"- by_priority: `{summary['candidate_audit']['by_priority']}`",
            f"- by_lane: `{summary['candidate_audit']['by_lane']}`",
            f"- by_status: `{summary['candidate_audit']['by_status']}`",
            f"- pending_review_count: {summary['candidate_audit']['pending_review_count']}",
            "",
            "## Cluster Audit",
            "",
            f"- cluster_count: {summary['cluster_audit']['cluster_count']}",
            f"- multi_item_cluster_count: {summary['cluster_audit']['multi_item_cluster_count']}",
            f"- ready_event_count: {summary['cluster_audit']['ready_event_count']}",
            f"- cluster_item_relations: `{summary['cluster_audit']['cluster_item_relations']}`",
            "",
            "## Top Clusters",
            "",
            *(cluster_lines or ["- No clusters generated."]),
            "",
            "## Daily Briefing Preview",
            "",
            "```markdown",
            briefing,
            "```",
            "",
            "## Run Report Preview",
            "",
            "```markdown",
            report,
            "```",
            "",
            "## Readiness Notes",
            "",
            "- This smoke uses real inbox rows but writes only to a temporary evaluation database.",
            f"- Live LLM calls: {'enabled' if (summary.get('live_llm') or {}).get('enabled') else 'disabled'}. Attempted {(summary.get('live_llm') or {}).get('calls_attempted', 0)}, succeeded {(summary.get('live_llm') or {}).get('calls_succeeded', 0)}.",
            "- No gold labels are available for this real sample, so FN/FP proof remains qualitative: candidate/review/cluster traces are emitted for manual audit.",
            "- Briefing/report previews consume materialized `events` and `event_clusters`; they do not directly list raw inbox rows.",
            "",
        ]
    )


def run_smoke(
    *,
    db_path: str | None,
    output: str,
    limit: int,
    sample_mode: str,
    source_filter: str | None,
    source_url_prefix: str | None,
    enable_live_llm: bool = False,
    llm_provider: str = "deepseek-v4-flash",
    max_llm_calls: int = 5,
    llm_timeout_seconds: int = 30,
    llm_mode: str = "candidate_discovery,signature_repair,relation_judge,cluster_proposal",
) -> dict[str, Any]:
    source_db_path = Path(db_path) if db_path else settings.database_path
    source_store = InboxStore(source_db_path)
    target_store, target_db_path = make_temp_store()
    warnings: list[str] = []
    sampled = copy_sample_to_eval_store(
        source_store,
        target_store,
        limit,
        warnings,
        source_filter=source_filter,
        source_url_prefix=source_url_prefix,
        sample_mode=sample_mode,
    )
    run_id = "real_use_smoke_" + stable_hash(utc_now())[:12]
    now = utc_now()
    ensure_environment_metadata(target_store, label="real_use_smoke", is_fresh=True)
    target_store.create_ingest_run(
        {
            "run_id": run_id,
            "trigger_type": "real_use_smoke",
            "source_mode": sample_mode,
            "status": "success",
            "started_at": now,
            "finished_at": now,
            "selected_source_count": len({item.get("source_id") or item.get("source_name") for item in sampled}),
            "success_source_count": len({item.get("source_id") or item.get("source_name") for item in sampled}),
            "new_items_count": len(sampled),
            "processed_items_count": len(sampled),
            "created_by": "operational_v3_real_use_smoke",
            "request": {"limit": limit, "sample_mode": sample_mode, "source_filter": source_filter, "source_url_prefix": source_url_prefix},
            "summary": {"warnings": warnings},
        }
    )
    item_ids = [item["item_id"] for item in sampled]
    dedupe = run_dedupe_stage(target_store, run_id, item_ids)
    item_cards = generate_item_cards(target_store, limit=len(item_ids), batch_size=5, live=False)
    information_objects = generate_information_objects(target_store, run_id, item_ids)
    daily_briefing = generate_briefing(target_store, "daily")
    req = request_for(target_store)
    run_report = api_report_generate(req, {"report_type": "run", "object_type": "run", "object_id": run_id})["data"]
    run_endpoint_report = api_run_report(req, run_id)["data"]
    live_llm_stats: dict[str, Any] | None = None
    if enable_live_llm:
        enabled_modes = [mode.strip() for mode in llm_mode.split(",") if mode.strip()]
        live_llm_stats = run_live_llm_passes(
            target_store,
            max_calls=max_llm_calls,
            enabled_modes=enabled_modes,
            model=llm_provider,
        )
    summary = {
        "metadata": {
            "generated_at": utc_now(),
            "source_db_path": str(source_db_path),
            "evaluation_db_path": str(target_db_path),
            "dry_run": True,
            "write_real_db": False,
            "backup_path": None,
            "limit": limit,
            "items_sampled": len(sampled),
            "sample_mode": sample_mode,
            "source_filter": source_filter,
            "source_url_prefix": source_url_prefix,
            "live_llm_enabled": enable_live_llm,
            "live_llm_provider": llm_provider if enable_live_llm else None,
            "live_llm_max_calls": max_llm_calls if enable_live_llm else None,
            "warnings": warnings,
        },
        "source_scope": source_scope_summary(source_store),
        "pipeline": {"dedupe": dedupe, "item_cards": item_cards, "information_objects": information_objects},
        "live_llm": live_llm_stats,
        "candidate_audit": candidate_audit(target_store),
        "cluster_audit": cluster_audit(target_store),
        "outputs": {
            "daily_briefing_path": None,
            "run_report_path": None,
            "daily_briefing_preview": daily_briefing["body_markdown"][:2000],
            "run_report_preview": run_report["content"][:2000],
            "run_endpoint_report_preview": run_endpoint_report["content"][:2000],
        },
    }
    out_dir = Path(output)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "real_use_smoke_summary.json"
    report_path = out_dir / "real_use_smoke_report.md"
    summary["outputs"]["summary_path"] = str(summary_path)
    summary["outputs"]["report_path"] = str(report_path)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    report_path.write_text(render_markdown(summary), encoding="utf-8")
    return {"ok": True, "summary_path": str(summary_path), "report_path": str(report_path), "summary": {"items_sampled": len(sampled), "clusters": summary["cluster_audit"]["cluster_count"], "multi_item_clusters": summary["cluster_audit"]["multi_item_cluster_count"], "ready_events": summary["cluster_audit"]["ready_event_count"], "reviews": summary["candidate_audit"]["pending_review_count"]}}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a read-only operational v3 real-use smoke evaluation.")
    parser.add_argument("--db-path")
    parser.add_argument("--output", default=str(BASE_DIR / "docs" / "real_use_smoke_operational_v3_20260601"))
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--sample-mode", choices=["recent", "duplicate_candidates", "cluster_candidates", "source_scope_full", "mixed", "event_hotspots"], default="event_hotspots")
    parser.add_argument("--source-filter")
    parser.add_argument("--source-url-prefix")
    parser.add_argument("--enable-live-llm", action="store_true", default=False,
                        help="Enable live DeepSeek LLM calls for candidate discovery, signature repair, relation judge, and cluster proposal.")
    parser.add_argument("--llm-provider", default="deepseek-v4-flash",
                        help="LLM model name (default: deepseek-v4-flash)")
    parser.add_argument("--max-llm-calls", type=int, default=5,
                        help="Maximum live LLM calls (default: 5)")
    parser.add_argument("--llm-timeout-seconds", type=int, default=30,
                        help="LLM call timeout in seconds (default: 30)")
    parser.add_argument("--llm-mode", default="candidate_discovery,signature_repair,relation_judge,cluster_proposal",
                        help="Comma-separated LLM capability modes (default: candidate_discovery,signature_repair,relation_judge,cluster_proposal)")
    args = parser.parse_args()
    result = run_smoke(
        db_path=args.db_path,
        output=args.output,
        limit=args.limit,
        sample_mode=args.sample_mode,
        source_filter=args.source_filter,
        source_url_prefix=args.source_url_prefix,
        enable_live_llm=args.enable_live_llm,
        llm_provider=args.llm_provider,
        max_llm_calls=args.max_llm_calls,
        llm_timeout_seconds=args.llm_timeout_seconds,
        llm_mode=args.llm_mode,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
