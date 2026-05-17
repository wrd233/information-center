from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import BASE_DIR, settings
from app.models import NormalizedContent, ScreeningResult
from app.semantic.cards import generate_item_cards
from app.semantic.candidates import assess_candidate, hotspot_key_candidates, infer_event_relation_type, relation_cluster_eligible, relation_pair_key
from app.semantic.clusters import patch_cluster_card, process_item_clusters
from app.semantic.evidence import build_review_bundle, export_evidence, write_json
from app.semantic.live_smoke import live_enabled
from app.semantic.relations import process_item_relations, semantic_tokens
from app.semantic.source_profiles import recompute_source_profiles
from app.storage import InboxStore, row_to_item
from app.utils import utc_now


def run_evaluation(
    *,
    db_path: str | None,
    output: str | None,
    limit: int,
    max_calls: int,
    max_candidates: int,
    batch_size: int,
    live: bool,
    dry_run: bool,
    write_real_db: bool,
    model: str | None,
    strong_model: str | None,
    token_budget: int,
    include_archived: bool,
    concurrency: int,
    source_filter: str | None = None,
    source_url_prefix: str | None = None,
    sample_mode: str = "recent",
    stage_budget_profile: str = "balanced",
    persist_evidence: bool = False,
    evidence_dir: str | None = None,
    phase_label: str = "semantic_eval",
    backup_path: str | None = None,
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    t0 = time.monotonic()
    run_id = f"semantic_eval_{started.strftime('%Y%m%d_%H%M%S_%f')}"
    output_root = Path(output) if output else BASE_DIR / "outputs" / "semantic_eval"
    run_dir = output_root if output else output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    source_db_path = Path(db_path) if db_path else settings.database_path
    source_store = InboxStore(source_db_path)
    write_real = bool(db_path and write_real_db and not dry_run)
    warnings: list[str] = []
    if live:
        live_ok, live_reason = live_enabled()
        if not live_ok:
            warnings.append(f"live skipped: {live_reason}")
            live = False
    if write_real:
        target_store = source_store
        target_db_path = source_db_path
        sampled_items = sample_existing_items(
            source_store,
            limit,
            source_filter=source_filter,
            source_url_prefix=source_url_prefix,
            sample_mode=sample_mode,
        )
    else:
        target_store, target_db_path = make_temp_eval_store()
        sampled_items = copy_sample_to_eval_store(
            source_store,
            target_store,
            limit,
            warnings,
            source_filter=source_filter,
            source_url_prefix=source_url_prefix,
            sample_mode=sample_mode,
        )

    max_items = len(sampled_items)
    stage_budgets = stage_budget_split(token_budget, stage_budget_profile)
    metadata: dict[str, Any] = {
        "run_id": run_id,
        "started_at": started.isoformat(),
        "db_path": str(source_db_path),
        "evaluation_db_path": str(target_db_path),
        "write_real_db": write_real,
        "live": live,
        "dry_run": dry_run,
        "model": model or settings.llm.get("model"),
        "strong_model": strong_model,
        "max_items": limit,
        "items_sampled": max_items,
        "max_calls": max_calls,
        "max_candidates": max_candidates,
        "batch_size": batch_size,
        "token_budget": token_budget,
        "stage_budget_profile": stage_budget_profile,
        "stage_budgets": stage_budgets,
        "include_archived": include_archived,
        "concurrency": concurrency,
        "source_filter": source_filter,
        "source_url_prefix": source_url_prefix,
        "sample_mode": sample_mode,
        "recall_strategy": "lexical/entity/time/source hybrid",
        "vector_index": False,
        "git_commit": git_commit_hash(),
        "warnings": warnings,
    }

    steps: dict[str, Any] = {}
    if max_items == 0:
        warnings.append("no inbox_items available for evaluation")
    else:
        remaining = remaining_calls(target_store, max_calls)
        steps["item_cards"] = generate_item_cards(
            target_store,
            limit=max_items,
            batch_size=batch_size,
            live=live,
            model=model,
            max_calls=max_calls,
            token_budget=stage_cap(target_store, stage_budgets, "item_card"),
            global_call_limit=True,
            concurrency=concurrency,
        )
        remaining = remaining_calls(target_store, max_calls)
        steps["item_relations"] = process_item_relations(
            target_store,
            limit=max_items,
            live=live and remaining > 0,
            max_candidates=max_candidates,
            max_calls=max_calls,
            model=model,
            token_budget=stage_cap(target_store, stage_budgets, "item_relation"),
            global_call_limit=True,
            concurrency=concurrency,
        )
        remaining = remaining_calls(target_store, max_calls)
        steps["item_clusters"] = process_item_clusters(
            target_store,
            limit=max_items,
            live=live and remaining > 0,
            max_candidates=max_candidates,
            max_calls=max_calls,
            model=model,
            include_archived=include_archived,
            token_budget=stage_cap(target_store, stage_budgets, "item_cluster_relation"),
            global_call_limit=True,
            patch_cards=False,
        )
        remaining = remaining_calls(target_store, max_calls)
        for cluster_id in sample_cluster_ids(target_store, limit=3):
            if remaining <= 0:
                break
            steps.setdefault("cluster_card_patch", []).append(
                patch_cluster_card(
                    target_store,
                    cluster_id,
                    live=live,
                    model=strong_model or model,
                    max_calls=max_calls,
                    token_budget=stage_cap(target_store, stage_budgets, "cluster_card_patch"),
                    global_call_limit=True,
                )
            )
            remaining = remaining_calls(target_store, max_calls)
        steps["source_profiles"] = recompute_source_profiles(target_store)

    finished = datetime.now(timezone.utc)
    metadata["finished_at"] = finished.isoformat()
    metadata["duration_seconds"] = round(time.monotonic() - t0, 3)
    source_scope = source_scope_summary(source_store, sampled_items, source_filter, source_url_prefix)
    summary = build_summary(target_store, metadata, steps, sampled_items, source_scope)
    evidence_result: dict[str, Any] | None = None
    if persist_evidence:
        evidence_result = export_evidence(
            run_dir=Path(evidence_dir) if evidence_dir else run_dir,
            source_store=source_store,
            target_store=target_store,
            metadata=metadata,
            summary=summary,
            sampled_items=sampled_items,
            phase_label=phase_label,
            backup_path=backup_path,
        )
        summary["evidence"] = {
            "persisted": True,
            "manifest_path": str((Path(evidence_dir) if evidence_dir else run_dir) / "semantic_run_manifest.json"),
            "counts": evidence_result.get("counts", {}),
            "files": evidence_result.get("evidence_files", []),
        }
    report = build_markdown_report(summary)
    report_path = run_dir / "semantic_quality_report.md"
    summary_path = run_dir / "semantic_quality_summary.json"
    report_path.write_text(report, encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "ok": True,
        "run_id": run_id,
        "report_path": str(report_path),
        "summary_path": str(summary_path),
        "metadata": metadata,
        "summary": compact_console_summary(summary),
        "evidence": evidence_result,
    }


def stage_budget_split(total_budget: int, profile: str) -> dict[str, int]:
    if total_budget <= 0:
        return {}
    profiles = {
        "balanced": {
            "item_card": 0.40,
            "item_relation": 0.25,
            "item_cluster_relation": 0.25,
            "cluster_card_patch": 0.07,
            "source_profile": 0.03,
        },
        "relation_heavy": {
            "item_card": 0.32,
            "item_relation": 0.34,
            "item_cluster_relation": 0.24,
            "cluster_card_patch": 0.07,
            "source_profile": 0.03,
        },
        "cluster_heavy": {
            "item_card": 0.32,
            "item_relation": 0.22,
            "item_cluster_relation": 0.36,
            "cluster_card_patch": 0.07,
            "source_profile": 0.03,
        },
        "card_heavy": {
            "item_card": 0.55,
            "item_relation": 0.18,
            "item_cluster_relation": 0.17,
            "cluster_card_patch": 0.07,
            "source_profile": 0.03,
        },
        "phase1_2e_profile": {
            "item_card": 0.30,
            "item_relation": 0.30,
            "item_cluster_relation": 0.27,
            "cluster_card_patch": 0.08,
            "source_profile": 0.05,
        },
    }
    ratios = profiles.get(profile, profiles["balanced"])
    return {stage: int(total_budget * ratio) for stage, ratio in ratios.items()}


def tokens_used(store: InboxStore) -> int:
    with store.connect() as conn:
        row = conn.execute("SELECT COALESCE(SUM(total_tokens), 0) AS n FROM llm_call_logs WHERE status = 'ok'").fetchone()
    return int(row["n"] or 0)


def stage_cap(store: InboxStore, budgets: dict[str, int], stage: str) -> int | None:
    budget = budgets.get(stage)
    if not budget:
        return None
    return tokens_used(store) + budget


def make_temp_eval_store() -> tuple[InboxStore, Path]:
    tmp = tempfile.NamedTemporaryFile(prefix="content_inbox_semantic_eval_", suffix=".sqlite3", delete=False)
    tmp.close()
    path = Path(tmp.name)
    return InboxStore(path), path


def sample_existing_items(
    store: InboxStore,
    limit: int,
    *,
    source_filter: str | None = None,
    source_url_prefix: str | None = None,
    sample_mode: str = "recent",
) -> list[dict[str, Any]]:
    with store.connect() as conn:
        where, params = source_scope_where(source_filter, source_url_prefix, conn=conn)
        order_sql = sample_order_sql(sample_mode)
        if sample_mode == "event_hotspots":
            rows = sample_event_hotspots(conn, where, params, limit)
        else:
            rows = conn.execute(
                f"SELECT * FROM inbox_items {where} {order_sql} LIMIT ?",
                (*params, limit),
            ).fetchall()
    return [row_to_item(row) for row in rows]


def sample_event_hotspots(conn: sqlite3.Connection, where: str, params: list[str], limit: int) -> list[Any]:
    rows = conn.execute(
        f"""
        SELECT *
        FROM inbox_items
        {where}
        ORDER BY COALESCE(published_at, created_at) DESC
        LIMIT ?
        """,
        (*params, max(limit * 8, 400)),
    ).fetchall()
    items = list(rows)
    token_sources: dict[str, set[str]] = {}
    token_items: dict[str, list[Any]] = {}
    for row in items:
        keys = hotspot_key_candidates(dict(row))
        signature = keys.get("event_signature") or {}
        seed_values: list[str] = []
        if signature.get("signature_key"):
            seed_values.append(signature["signature_key"])
        for token in seed_values:
            if len(token) < 3:
                continue
            token_sources.setdefault(token, set()).add(row["source_id"] or row["source_name"] or "")
            token_items.setdefault(token, []).append(row)
    hotspot_tokens = sorted(
        token_items,
        key=lambda token: (len(token_sources.get(token, set())), len(token_items[token]), len(token)),
        reverse=True,
    )
    selected: list[Any] = []
    seen: set[str] = set()
    for token in hotspot_tokens:
        if len(token_sources.get(token, set())) < 2 and len(token_items[token]) < 3:
            continue
        group = sorted(
            token_items[token],
            key=lambda row: (row["source_id"] or "", row["published_at"] or row["created_at"] or ""),
            reverse=True,
        )
        for row in group[:6]:
            if row["item_id"] in seen:
                continue
            selected.append(row)
            seen.add(row["item_id"])
            if len(selected) >= limit:
                return selected
    for row in items:
        if row["item_id"] not in seen:
            selected.append(row)
            seen.add(row["item_id"])
            if len(selected) >= limit:
                break
    return selected


def _resolve_source_url_prefix(
    conn: sqlite3.Connection, prefix: str
) -> tuple[list[str], list[tuple[str, str | None]]]:
    """Resolve a URL prefix against rss_sources, returning matching source_ids
    and (source_name, source_category) pairs for items with NULL linkage."""
    search = f"%{prefix}%"
    # Normalize: also match without scheme
    clean = prefix.removeprefix("https://").removeprefix("http://")
    clean_search = f"%{clean}%"
    rows = conn.execute(
        """
        SELECT source_id, source_name, source_category
        FROM rss_sources
        WHERE feed_url LIKE ?
           OR normalized_feed_url LIKE ?
           OR feed_url LIKE ?
           OR normalized_feed_url LIKE ?
        """,
        (search, search, clean_search, clean_search),
    ).fetchall()
    source_ids = [row[0] for row in rows]
    pairs = [(row[1], row[2]) for row in rows]
    return source_ids, pairs


def source_scope_where(
    source_filter: str | None,
    source_url_prefix: str | None,
    conn: sqlite3.Connection | None = None,
) -> tuple[str, list[str]]:
    clauses: list[str] = []
    params: list[str] = []
    if source_filter:
        like = f"%{source_filter}%"
        clauses.append("(COALESCE(source_id, '') LIKE ? OR COALESCE(feed_url, '') LIKE ? OR COALESCE(url, '') LIKE ? OR COALESCE(source_name, '') LIKE ? OR COALESCE(source_category, '') LIKE ?)")
        params.extend([like, like, like, like, like])
    if source_url_prefix:
        if conn is not None:
            source_ids, name_pairs = _resolve_source_url_prefix(conn, source_url_prefix)
        else:
            source_ids, name_pairs = [], []
        if source_ids:
            id_placeholders = ",".join("?" for _ in source_ids)
            name_conditions: list[str] = []
            name_params: list[str] = []
            for sname, scat in name_pairs:
                if scat is not None:
                    name_conditions.append("(COALESCE(source_name, '') = ? AND COALESCE(source_category, '') = ?)")
                    name_params.extend([sname, scat])
                else:
                    name_conditions.append("(COALESCE(source_name, '') = ? AND (source_category IS NULL OR source_category = ''))")
                    name_params.append(sname)
            parts = [f"source_id IN ({id_placeholders})"]
            params.extend(source_ids)
            if name_conditions:
                parts.append(f"({' OR '.join(name_conditions)})")
                params.extend(name_params)
            clauses.append(f"({' OR '.join(parts)})")
        else:
            like = f"%{source_url_prefix}%"
            clauses.append("(COALESCE(feed_url, '') LIKE ? OR COALESCE(url, '') LIKE ? OR COALESCE(source_id, '') LIKE ? OR COALESCE(source_name, '') LIKE ?)")
            params.extend([like, like, like, like])
    return (f"WHERE {' AND '.join(clauses)}" if clauses else "", params)


def sample_order_sql(sample_mode: str) -> str:
    if sample_mode == "duplicate_candidates":
        return "ORDER BY LOWER(title), published_at DESC, created_at DESC"
    if sample_mode == "cluster_candidates":
        return "ORDER BY COALESCE(published_at, created_at) DESC, LOWER(source_name), LOWER(title)"
    if sample_mode == "source_scope_full":
        return "ORDER BY COALESCE(published_at, created_at) ASC, source_name, title"
    if sample_mode == "mixed":
        return "ORDER BY source_name, COALESCE(published_at, created_at) DESC, title"
    if sample_mode == "event_hotspots":
        return "ORDER BY COALESCE(published_at, created_at) DESC, source_name, title"
    return "ORDER BY created_at DESC"


def copy_sample_to_eval_store(
    source_store: InboxStore,
    target_store: InboxStore,
    limit: int,
    warnings: list[str],
    *,
    source_filter: str | None = None,
    source_url_prefix: str | None = None,
    sample_mode: str = "recent",
) -> list[dict[str, Any]]:
    sampled = sample_existing_items(
        source_store,
        limit,
        source_filter=source_filter,
        source_url_prefix=source_url_prefix,
        sample_mode=sample_mode,
    )
    copied: list[dict[str, Any]] = []
    for idx, item in enumerate(reversed(sampled)):
        try:
            screening = ScreeningResult.model_validate(item["screening"])
        except Exception:
            screening = ScreeningResult(
                summary=item.get("summary") or item.get("title") or "semantic eval item",
                category="其他",
                value_score=3,
                personal_relevance=3,
                suggested_action="review",
                reason="fallback screening for semantic evaluation",
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
        try:
            inserted = target_store.insert(f"eval-{idx}-{item['item_id']}", normalized, screening, raw={"source_item_id": item["item_id"]})
            copied.append(inserted)
        except Exception as exc:
            warnings.append(f"failed to copy sample item {item.get('item_id')}: {exc}")
    return copied


def remaining_calls(store: InboxStore, max_calls: int) -> int:
    with store.connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM llm_call_logs WHERE status IN ('ok', 'failed')"
        ).fetchone()
    return max(0, max_calls - int(row["n"] or 0))


def sample_cluster_ids(store: InboxStore, limit: int) -> list[str]:
    with store.connect() as conn:
        rows = conn.execute(
            "SELECT cluster_id FROM event_clusters ORDER BY updated_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [row["cluster_id"] for row in rows]


def source_scope_summary(
    store: InboxStore,
    sampled_items: list[dict[str, Any]],
    source_filter: str | None,
    source_url_prefix: str | None,
) -> dict[str, Any]:
    sampled_counts = Counter(item.get("source_id") or item.get("feed_url") or item.get("source_name") for item in sampled_items)
    with store.connect() as conn:
        where, params = source_scope_where(source_filter, source_url_prefix, conn=conn)
        rows = conn.execute(
            f"""
            SELECT COALESCE(source_id, feed_url, source_name) AS source_id,
                   source_name,
                   feed_url,
                   COUNT(*) AS item_count,
                   MAX(COALESCE(published_at, created_at)) AS latest_item_time
            FROM inbox_items
            {where}
            GROUP BY COALESCE(source_id, feed_url, source_name), source_name, feed_url
            ORDER BY item_count DESC
            """,
            params,
        ).fetchall()
    sources = []
    for row in rows:
        source_id = row["source_id"]
        sources.append(
            {
                "source_id": source_id,
                "source_name": row["source_name"],
                "feed_url": row["feed_url"],
                "item_count": row["item_count"],
                "sampled_item_count": sampled_counts.get(source_id, 0),
                "latest_item_time": row["latest_item_time"],
            }
        )
    return {
        "source_filter": source_filter,
        "source_url_prefix": source_url_prefix,
        "matched_source_count": len(sources),
        "sources": sources,
    }


def build_summary(
    store: InboxStore,
    metadata: dict[str, Any],
    steps: dict[str, Any],
    sampled_items: list[dict[str, Any]],
    source_scope: dict[str, Any],
) -> dict[str, Any]:
    with store.connect() as conn:
        item_cards = conn.execute("SELECT * FROM item_cards WHERE is_current = 1").fetchall()
        item_relations = conn.execute("SELECT * FROM item_relations").fetchall()
        cluster_items = conn.execute("SELECT * FROM cluster_items").fetchall()
        clusters = conn.execute("SELECT * FROM event_clusters").fetchall()
        cluster_cards = conn.execute("SELECT * FROM cluster_cards WHERE is_current = 1").fetchall()
        source_profiles = conn.execute("SELECT * FROM source_profiles").fetchall()
        reviews = conn.execute("SELECT * FROM review_queue").fetchall()
        llm_logs = conn.execute("SELECT * FROM llm_call_logs").fetchall()

    enriched_metadata = {**metadata, **llm_totals(llm_logs)}
    return {
        "metadata": enriched_metadata,
        "source_scope": source_scope,
        "input_sample": input_sample_summary(sampled_items),
        "item_cards": item_card_summary(item_cards, llm_logs),
        "item_relations": item_relation_summary(item_relations, llm_logs, store),
        "item_clusters": cluster_relation_summary(cluster_items, clusters, cluster_cards),
        "source_profiles": source_profile_summary(source_profiles, reviews),
        "token_cost": token_summary(llm_logs),
        "stage_budgets": stage_budget_summary(llm_logs, metadata),
        "concurrency": concurrency_summary(llm_logs, enriched_metadata),
        "errors_fallbacks": error_summary(llm_logs, reviews, steps, metadata),
        "prompt_iteration_notes": prompt_iteration_notes(metadata),
        "readiness_assessment": readiness_assessment(item_relations, cluster_items, llm_logs, metadata),
        "steps": steps,
        "recommendations": recommendations(item_relations, cluster_items, enriched_metadata),
    }


def llm_totals(rows: list[Any]) -> dict[str, Any]:
    return {
        "actual_calls": sum(1 for row in rows if row["status"] in {"ok", "failed"}),
        "actual_tokens": sum(int(row["total_tokens"] or 0) for row in rows),
        "cache_hit_tokens": sum(int(row["cache_hit_tokens"] or 0) for row in rows),
        "cache_miss_tokens": sum(int(row["cache_miss_tokens"] or 0) for row in rows),
    }


def input_sample_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    sources = Counter(item.get("source_id") or item.get("feed_url") or item.get("source_name") for item in items)
    languages = Counter("zh" if has_cjk((item.get("title") or "") + (item.get("summary") or "")) else "en_or_unknown" for item in items)
    created = [item.get("created_at") for item in items if item.get("created_at")]
    return {
        "items_sampled": len(items),
        "time_range": {"min_created_at": min(created) if created else None, "max_created_at": max(created) if created else None},
        "source_count": len(sources),
        "top_sources": sources.most_common(10),
        "items_with_raw_content": sum(1 for item in items if item.get("content_text")),
        "items_with_summary_only": sum(1 for item in items if item.get("summary") and not item.get("content_text")),
        "items_too_short": sum(1 for item in items if len((item.get("summary") or item.get("content_text") or item.get("title") or "")) < 40),
        "languages": dict(languages),
    }


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def item_card_summary(rows: list[Any], llm_logs: list[Any]) -> dict[str, Any]:
    roles = Counter(row["content_role"] for row in rows)
    warnings = Counter()
    tiers = Counter()
    tier_confidence: dict[str, list[float]] = {}
    entity_counts = []
    confidence = []
    samples = []
    heuristic_count = 0
    for row in rows:
        try:
            warnings.update(json.loads(row["warnings_json"] or "[]"))
            entity_counts.append(len(json.loads(row["entities_json"] or "[]")))
        except Exception:
            pass
        confidence.append(float(row["confidence"] or 0.0))
        tier = "unknown"
        try:
            tier = (json.loads(row["quality_hints_json"] or "{}") or {}).get("card_tier") or tier
        except Exception:
            pass
        tiers[tier] += 1
        tier_confidence.setdefault(tier, []).append(float(row["confidence"] or 0.0))
        if (row["model"] or "") == "heuristic":
            heuristic_count += 1
        if len(samples) < 10:
            samples.append({"item_id": row["item_id"], "title": row["canonical_title"], "role": row["content_role"], "summary": row["short_summary"]})
    return {
        "item_cards_generated_or_reused": len(rows),
        "item_cards_generated": len(rows),
        "item_cards_reused": 0,
        "item_cards_failed": sum(1 for row in llm_logs if row["task_type"] == "item_card" and row["status"] == "failed"),
        "heuristic_card_fallback_count": heuristic_count,
        "avg_confidence": round(sum(confidence) / max(len(confidence), 1), 3),
        "content_role_distribution": dict(roles),
        "card_tier_distribution": dict(tiers),
        "avg_confidence_by_tier": {
            tier: round(sum(values) / max(len(values), 1), 3)
            for tier, values in sorted(tier_confidence.items())
        },
        "llm_failures_by_tier": llm_failures_by_tier(llm_logs),
        "avg_tokens_by_tier": avg_tokens_by_tier(llm_logs),
        "entity_count_distribution": dict(Counter(entity_counts)),
        "warnings_distribution": dict(warnings),
        "samples": samples,
    }


def llm_failures_by_tier(llm_logs: list[Any]) -> dict[str, int]:
    out = Counter()
    for row in llm_logs:
        if row["task_type"] != "item_card" or row["status"] != "failed":
            continue
        tier = "unknown"
        try:
            request = json.loads(row["request_json"] or "{}")
            tier = request.get("card_tier") or tier
        except Exception:
            pass
        out[tier] += 1
    return dict(out)


def avg_tokens_by_tier(llm_logs: list[Any]) -> dict[str, float]:
    tokens: dict[str, list[int]] = {}
    for row in llm_logs:
        if row["task_type"] != "item_card" or row["status"] not in {"ok", "failed"}:
            continue
        tier = "mixed_llm"
        try:
            request = json.loads(row["request_json"] or "{}")
            tier = request.get("card_tier") or tier
        except Exception:
            pass
        tokens.setdefault(tier, []).append(int(row["total_tokens"] or 0))
    return {tier: round(sum(values) / max(len(values), 1), 1) for tier, values in tokens.items()}


def item_relation_summary(rows: list[Any], llm_logs: list[Any], store: InboxStore) -> dict[str, Any]:
    rels = Counter(row["primary_relation"] for row in rows)
    unique_pairs: set[str] = set()
    duplicate_direction_count = 0
    event_types = Counter()
    cluster_eligible_count = 0
    for row in rows:
        left_item = get_item_dict(store, row["item_a_id"])
        right_item = get_item_dict(store, row["item_b_id"])
        key = relation_pair_key(left_item, right_item) if left_item and right_item else f"{row['item_a_id']}|{row['item_b_id']}"
        if key in unique_pairs:
            duplicate_direction_count += 1
        unique_pairs.add(key)
        assessment = assess_candidate(left_item or {}, right_item or {})
        event_type = infer_event_relation_type(
            row["primary_relation"],
            assessment,
            reason=row["reason"] or "",
            evidence=json.loads(row["evidence_json"] or "[]"),
            new_information=json.loads(row["new_information_json"] or "[]"),
        )
        event_types[event_type] += 1
        if relation_cluster_eligible(row["primary_relation"], event_type):
            cluster_eligible_count += 1
    candidate_stats = candidate_event_summary(store)
    confidences = [float(row["confidence"] or 0.0) for row in rows]
    examples = []
    low_conf = []
    for row in rows:
        example = relation_example(store, row)
        if len(examples) < 10:
            examples.append(example)
        if float(row["confidence"] or 0.0) < 0.6 and len(low_conf) < 10:
            low_conf.append(example)
    return {
        "candidate_pairs_considered": len(rows),
        "raw_relation_count": len(rows),
        "unique_relation_pair_count": len(unique_pairs),
        "duplicate_direction_suppressed_count": duplicate_direction_count + candidate_stats.get("duplicate_direction_suppressed_count", 0),
        "event_relation_type_distribution": dict(event_types),
        "cluster_eligible_count": cluster_eligible_count,
        "candidate_priority_distribution": candidate_stats.get("candidate_priority_distribution", {}),
        "candidates_suppressed_without_llm": candidate_stats.get("candidates_suppressed_without_llm", 0),
        "high_priority_skips": candidate_stats.get("high_priority_skips", 0),
        "llm_item_relation_calls": sum(1 for row in llm_logs if row["task_type"] == "item_relation" and row["status"] in {"ok", "failed"}),
        "duplicate": rels.get("duplicate", 0),
        "near_duplicate": rels.get("near_duplicate", 0),
        "related_with_new_info": rels.get("related_with_new_info", 0),
        "different": rels.get("different", 0),
        "relations_by_primary_relation": dict(rels),
        "fold_candidates": sum(1 for row in rows if row["should_fold"]),
        "related_with_new_info_count": rels.get("related_with_new_info", 0),
        "uncertain_count": rels.get("uncertain", 0),
        "avg_confidence": round(sum(confidences) / max(len(confidences), 1), 3),
        "examples": examples,
        "low_confidence_examples": low_conf,
    }


def relation_example(store: InboxStore, row: Any) -> dict[str, Any]:
    left = get_title(store, row["item_a_id"])
    right = get_title(store, row["item_b_id"])
    return {
        "new_item_title": left.get("title"),
        "candidate_item_title": right.get("title"),
        "primary_relation": row["primary_relation"],
        "secondary_roles": json.loads(row["secondary_roles_json"] or "[]"),
        "confidence": row["confidence"],
        "should_fold": bool(row["should_fold"]),
        "reason": row["reason"],
        "source": left.get("source_id") or left.get("source_name"),
        "published_at": left.get("published_at"),
    }


def get_title(store: InboxStore, item_id: str) -> dict[str, Any]:
    with store.connect() as conn:
        row = conn.execute(
            "SELECT title, source_id, source_name, published_at FROM inbox_items WHERE item_id = ?", (item_id,)
        ).fetchone()
    return dict(row) if row else {"title": item_id}


def get_item_dict(store: InboxStore, item_id: str) -> dict[str, Any]:
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
    return dict(row) if row else {}


def candidate_event_summary(store: InboxStore) -> dict[str, Any]:
    with store.connect() as conn:
        try:
            rows = conn.execute("SELECT * FROM semantic_candidate_events").fetchall()
        except Exception:
            return {}
    priority = Counter(row["candidate_priority"] or "unknown" for row in rows)
    return {
        "candidate_priority_distribution": dict(priority),
        "candidates_suppressed_without_llm": sum(1 for row in rows if row["status"] == "suppressed" or row["candidate_priority"] == "suppress"),
        "duplicate_direction_suppressed_count": sum(1 for row in rows if row["status"] == "duplicate_direction_suppressed"),
        "high_priority_skips": sum(
            1
            for row in rows
            if row["status"] == "suppressed"
            and row["candidate_priority"] in {"must_run", "high"}
        ),
    }


def cluster_relation_summary(cluster_items: list[Any], clusters: list[Any], cluster_cards: list[Any]) -> dict[str, Any]:
    rels = Counter(row["primary_relation"] for row in cluster_items)
    actions = Counter()
    for row in cluster_items:
        if row["primary_relation"] in {"source_material", "repeat", "new_info", "analysis", "experience", "context"}:
            actions["attach_to_cluster"] += 1
        elif row["primary_relation"] == "follow_up":
            actions["create_new_cluster"] += 1
        elif row["primary_relation"] == "uncertain":
            actions["uncertain"] += 1
    created_clusters = sum(1 for cluster in clusters if cluster["created_by"] in {"rule", "llm"})
    attached_existing = max(0, len(cluster_items) - created_clusters)
    confidences = [float(row["confidence"] or 0.0) for row in cluster_items]
    multi_item_clusters = [cluster for cluster in clusters if int(cluster["item_count"] or 0) > 1]
    samples = []
    cards_by_cluster = {row["cluster_id"]: row for row in cluster_cards}
    for cluster in clusters[:20]:
        card = cards_by_cluster.get(cluster["cluster_id"])
        samples.append({
            "cluster_title": cluster["cluster_title"],
            "cluster_status": cluster["status"],
            "item_count": cluster["item_count"],
            "core_facts": json.loads(card["core_facts_json"] or "[]") if card else [],
            "known_angles": json.loads(card["known_angles_json"] or "[]") if card else [],
            "representative_items": json.loads(card["representative_items_json"] or "[]") if card else [cluster["representative_item_id"]],
        })
    return {
        "candidate_clusters_considered": len(clusters),
        "actions": dict(actions),
        "created_clusters": created_clusters,
        "attached_existing_clusters": attached_existing,
        "uncertain_clusters": rels.get("uncertain", 0),
        "relations": dict(rels),
        "same_event": dict(Counter(bool(row["same_event"]) for row in cluster_items)),
        "same_topic": dict(Counter(bool(row["same_topic"]) for row in cluster_items)),
        "follow_up_event": dict(Counter(bool(row["follow_up_event"]) for row in cluster_items)),
        "should_update_cluster_card_count": sum(1 for row in cluster_items if row["should_update_cluster_card"]),
        "should_notify_count": sum(1 for row in cluster_items if row["should_notify"]),
        "multi_item_cluster_count": len(multi_item_clusters),
        "avg_items_per_cluster": round(
            sum(int(cluster["item_count"] or 0) for cluster in clusters) / max(len(clusters), 1),
            3,
        ),
        "top_clusters": [
            {"cluster_id": cluster["cluster_id"], "cluster_title": cluster["cluster_title"], "item_count": cluster["item_count"]}
            for cluster in sorted(clusters, key=lambda row: int(row["item_count"] or 0), reverse=True)[:10]
        ],
        "avg_confidence": round(sum(confidences) / max(len(confidences), 1), 3),
        "cluster_samples": samples,
        "manual_review_suggestions": manual_review_suggestions(cluster_items, clusters),
    }


def manual_review_suggestions(cluster_items: list[Any], clusters: list[Any]) -> dict[str, Any]:
    uncertain = [dict(row) for row in cluster_items if row["primary_relation"] == "uncertain"][:20]
    same_topic = [dict(row) for row in cluster_items if row["primary_relation"] == "same_topic"][:20]
    follow_up = [dict(row) for row in cluster_items if row["follow_up_event"]][:20]
    return {
        "possible_miscluster": same_topic,
        "possible_missplit": follow_up,
        "high_uncertain": uncertain,
        "top_review_items_or_clusters": uncertain + same_topic + follow_up,
    }


def source_profile_summary(rows: list[Any], reviews: list[Any]) -> dict[str, Any]:
    profiles = [dict(row) for row in rows]
    pending = [dict(row) for row in reviews if row["status"] == "pending"]
    source_priority_pending = [
        row for row in pending
        if row.get("review_type") == "source_priority_suggestion"
        and row.get("target_type") == "source"
    ]
    insufficient = [
        p for p in profiles
        if (p.get("total_items") or 0) < 10 or (p.get("llm_processed_items") or 0) < 5
    ]
    return {
        "sources_recomputed": len(rows),
        "high_candidates": [p for p in profiles if p.get("priority_suggestion") == "high"][:20],
        "low_candidates": [p for p in profiles if p.get("priority_suggestion") == "low"][:20],
        "disabled_for_llm_candidates": [p for p in profiles if p.get("priority_suggestion") == "disabled_for_llm"][:20],
        "pending_reviews_created": len(source_priority_pending),
        "pending_reviews_created_all_types": len(pending),
        "reviews_suppressed_due_to_insufficient_data": len(insufficient),
        "top_sources_by_llm_yield": sorted(profiles, key=lambda p: p.get("llm_yield_score") or 0, reverse=True)[:10],
        "top_sources_by_duplicate_rate": sorted(profiles, key=lambda p: p.get("duplicate_rate") or 0, reverse=True)[:10],
        "top_sources_by_incremental_value_avg": sorted(profiles, key=lambda p: p.get("incremental_value_avg") or 0, reverse=True)[:10],
        "top_sources_by_report_value_avg": sorted(profiles, key=lambda p: p.get("report_value_avg") or 0, reverse=True)[:10],
        "llm_total_tokens_by_source": {
            p["source_id"]: p.get("llm_total_tokens", 0) for p in sorted(profiles, key=lambda p: p.get("llm_total_tokens") or 0, reverse=True)[:30]
        },
        "sources_with_insufficient_data": insufficient[:20],
    }


def token_summary(rows: list[Any]) -> list[dict[str, Any]]:
    tasks = ["item_card", "item_relation", "item_cluster_relation", "cluster_card_patch", "cluster_card_rebuild", "source_review", "json_repair"]
    out = []
    for task in tasks:
        subset = [row for row in rows if row["task_type"] == task]
        latencies = sorted(int(row["latency_ms"] or 0) for row in subset if row["status"] in {"ok", "failed"})
        llm_subset = [row for row in subset if row["status"] in {"ok", "failed"}]
        out.append({
            "task_type": task,
            "operation_count": len(subset),
            "llm_call_count": len(llm_subset),
            "calls": len(llm_subset),
            "success": sum(1 for row in llm_subset if row["status"] == "ok"),
            "failed": sum(1 for row in llm_subset if row["status"] == "failed"),
            "skipped": sum(1 for row in subset if row["status"] == "skipped"),
            "input_tokens": sum(int(row["prompt_tokens"] or 0) for row in subset),
            "output_tokens": sum(int(row["completion_tokens"] or 0) for row in subset),
            "total_tokens": sum(int(row["total_tokens"] or 0) for row in subset),
            "cache_hit_tokens": sum(int(row["cache_hit_tokens"] or 0) for row in subset),
            "cache_miss_tokens": sum(int(row["cache_miss_tokens"] or 0) for row in subset),
            "avg_latency_ms": round(sum(latencies) / max(len(latencies), 1), 1),
            "p50_latency_ms": percentile(latencies, 0.5),
            "p95_latency_ms": percentile(latencies, 0.95),
            "rate_limit_errors": sum(1 for row in subset if "429" in (row["error"] or "")),
            "parse_failures": sum(1 for row in subset if "JSON" in (row["error"] or "")),
            "retry_count": sum(1 for row in subset if row["status"] == "failed"),
            "avg_candidates_per_call": None,
        })
    return out


def stage_budget_summary(rows: list[Any], metadata: dict[str, Any]) -> dict[str, Any]:
    budgets = metadata.get("stage_budgets") or {}
    by_task = {item["task_type"]: item for item in token_summary(rows)}
    out: dict[str, Any] = {
        "total_token_budget": metadata.get("token_budget", 0),
        "stage_budget_profile": metadata.get("stage_budget_profile"),
        "stages": {},
        "downstream_starved": False,
    }
    mapping = {
        "item_card": "item_card",
        "item_relation": "item_relation",
        "item_cluster_relation": "item_cluster_relation",
        "cluster_card_patch": "cluster_card_patch",
        "source_profile": "source_review",
    }
    for stage, task in mapping.items():
        consumed = int((by_task.get(task) or {}).get("total_tokens", 0) or 0)
        budget = int(budgets.get(stage, 0) or 0)
        skipped = int((by_task.get(task) or {}).get("skipped", 0) or 0)
        out["stages"][stage] = {
            "budget": budget,
            "consumed_tokens": consumed,
            "remaining_budget": max(0, budget - consumed) if budget else None,
            "calls": int((by_task.get(task) or {}).get("llm_call_count", 0) or 0),
            "skipped": skipped,
            "skipped_due_to_budget": skipped if budget and consumed >= budget else 0,
        }
    out["downstream_starved"] = (
        bool(budgets)
        and out["stages"]["item_card"]["consumed_tokens"] >= out["stages"]["item_card"]["budget"]
        and (
            out["stages"]["item_relation"]["calls"] == 0
            or out["stages"]["item_cluster_relation"]["calls"] == 0
        )
    )
    return out


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    idx = min(len(values) - 1, max(0, int(round((len(values) - 1) * pct))))
    return values[idx]


def error_summary(rows: list[Any], reviews: list[Any], steps: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    tokens = metadata.get("actual_tokens", 0)
    card_stats = ((steps.get("item_cards") or {}).get("stats") or {}) if isinstance(steps.get("item_cards"), dict) else {}
    item_card_count = int(card_stats.get("written") or 0)
    heuristic_fallback_count = sum(1 for row in rows if row["task_type"] == "item_card" and row["model"] == "heuristic")
    return {
        "llm_parse_failures": sum(1 for row in rows if row["status"] == "failed" and "JSON" in (row["error"] or "")),
        "repair_retry_count": sum(1 for row in rows if row["status"] == "failed"),
        "final_failures": sum(1 for row in rows if row["status"] == "failed"),
        "item_card_count": item_card_count,
        "llm_card_count": sum(1 for row in rows if row["task_type"] == "item_card" and row["status"] == "ok"),
        "heuristic_fallback_count": heuristic_fallback_count,
        "fallback_rate": round(heuristic_fallback_count / max(item_card_count, 1), 4),
        "failed_batch_count": int(card_stats.get("failed_batch_count") or 0),
        "split_retry_success_count": int(card_stats.get("split_retry_success_count") or 0),
        "single_retry_success_count": int(card_stats.get("single_retry_success_count") or 0),
        "review_queue_entries_due_to_failure": sum(1 for row in reviews if "failed" in (row["reason"] or "").lower()),
        "skipped_due_to_max_calls": any("max calls" in (row["error"] or "") for row in rows),
        "skipped_due_to_token_budget": bool(metadata.get("token_budget") and tokens >= metadata.get("token_budget")),
        "skipped_due_to_missing_card": 0,
        "skipped_due_to_no_candidate": 0,
        "db_lock_errors": sum(1 for row in rows if "locked" in (row["error"] or "").lower()),
    }


def concurrency_summary(rows: list[Any], metadata: dict[str, Any]) -> dict[str, Any]:
    all_latencies = sorted(int(row["latency_ms"] or 0) for row in rows if row["status"] in {"ok", "failed"})
    duration = float(metadata.get("duration_seconds") or 0)
    total_calls = sum(1 for row in rows if row["status"] in {"ok", "failed"})
    total_tokens = sum(int(row["total_tokens"] or 0) for row in rows)
    cache_hit_tokens = sum(int(row["cache_hit_tokens"] or 0) for row in rows)
    by_task = {}
    for item in token_summary(rows):
        by_task[item["task_type"]] = {
            "concurrency": metadata.get("concurrency"),
            "task_type": item["task_type"],
            "calls": item["llm_call_count"],
            "success": item["success"],
            "failed": item["failed"],
            "avg_latency_ms": item["avg_latency_ms"],
            "p50_latency_ms": item["p50_latency_ms"],
            "p95_latency_ms": item["p95_latency_ms"],
            "total_tokens": item["total_tokens"],
            "cache_hit_tokens": item["cache_hit_tokens"],
            "parse_failures": item["parse_failures"],
            "rate_limit_errors": item["rate_limit_errors"],
            "db_lock_errors": 0,
            "retry_count": item["retry_count"],
        }
    return {
        "max_concurrency": metadata.get("concurrency"),
        "duration_seconds": duration,
        "actual_calls": total_calls,
        "actual_tokens": total_tokens,
        "cache_hit_tokens": cache_hit_tokens,
        "cache_hit_rate": round(cache_hit_tokens / max(total_tokens, 1), 4),
        "calls_per_sec": round(total_calls / duration, 4) if duration else 0,
        "tokens_per_sec": round(total_tokens / duration, 2) if duration else 0,
        "avg_latency_ms": round(sum(all_latencies) / max(len(all_latencies), 1), 1),
        "p50_latency_ms": percentile(all_latencies, 0.5),
        "p95_latency_ms": percentile(all_latencies, 0.95),
        "rate_limit_errors": sum(1 for row in rows if "429" in (row["error"] or "") or "rate" in (row["error"] or "").lower()),
        "parse_failures": sum(1 for row in rows if "JSON" in (row["error"] or "") or "validation" in (row["error"] or "").lower()),
        "repair_retry_count": sum(1 for row in rows if row["status"] == "failed"),
        "final_failures": sum(1 for row in rows if row["status"] == "failed"),
        "db_lock_errors": sum(1 for row in rows if "locked" in (row["error"] or "").lower()),
        "by_task": by_task,
    }


def recommendations(item_relations: list[Any], cluster_items: list[Any], metadata: dict[str, Any]) -> list[str]:
    recs = []
    uncertain_rel = sum(1 for row in item_relations if row["primary_relation"] == "uncertain")
    uncertain_cluster = sum(1 for row in cluster_items if row["primary_relation"] == "uncertain")
    if uncertain_rel + uncertain_cluster:
        recs.append("Review uncertain relations and tune prompts with real examples.")
    recs.append("Add vector indexes for item_cards and cluster_cards before larger runs.")
    recs.append("Keep primary relation enum unchanged for now; it covered Phase 1.1 control flow.")
    recs.append("Collect more source_signals before trusting source_profile priority suggestions.")
    recs.append("Run a larger dry-run before any write-real-db semantic pass.")
    if metadata.get("token_budget") and metadata.get("actual_tokens", 0) >= metadata["token_budget"]:
        recs.append("Increase token_budget or lower max_items for more complete evaluation.")
    return recs


def prompt_iteration_notes(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "iteration": "phase1_2f",
            "changes": [
                "event-signature hotspot keys",
                "generic AI/template token suppression",
                "scarcer must_run/high candidate priorities",
                "same_product_different_event and same_thread secondary roles",
                "cluster seed precision diagnostics",
                "budget skip quality tiers",
                "item-card split retry metrics",
            ],
            "sample_mode": metadata.get("sample_mode"),
            "max_items": metadata.get("max_items"),
            "max_calls": metadata.get("max_calls"),
            "concurrency": metadata.get("concurrency"),
            "notes": "Primary relation enums remain stable; prompt versions bumped to v3 with stricter same-event rules.",
        }
    ]


def readiness_assessment(item_relations: list[Any], cluster_items: list[Any], llm_logs: list[Any], metadata: dict[str, Any]) -> dict[str, Any]:
    failures = sum(1 for row in llm_logs if row["status"] == "failed")
    real_write_recommended = False
    reasons = [
        "Use dry-run reports for manual review before write-real-db.",
        "Candidate recall is still lexical/entity/time/source hybrid, not vector-indexed.",
    ]
    if failures:
        reasons.append(f"{failures} LLM failures observed in this run.")
    if not item_relations:
        reasons.append("No item-item relation rows were produced; duplicate-focused sampling may be needed.")
    if cluster_items:
        avg_cluster_signal = len(cluster_items)
    else:
        avg_cluster_signal = 0
        reasons.append("No cluster_items produced.")
    return {
        "write_real_db_recommended_now": real_write_recommended,
        "cluster_signal_count": avg_cluster_signal,
        "reasons": reasons,
    }


def build_markdown_report(summary: dict[str, Any]) -> str:
    m = summary["metadata"]
    lines = [
        "# Semantic Quality Report",
        "",
        "## 1. Run Metadata",
        "",
        json_block(m),
        "",
        "## 2. Source Scope",
        "",
        json_block(summary["source_scope"]),
        "",
        "## 3. Input Sample Summary",
        "",
        json_block(summary["input_sample"]),
        "",
        "## 4. Item Card Quality",
        "",
        json_block(summary["item_cards"]),
        "",
        "## 5. Item-Item Relation Quality",
        "",
        json_block(summary["item_relations"]),
        "",
        "## 6. Event Signature Hotspots",
        "",
        json_block({
            "sample_mode": m.get("sample_mode"),
            "evidence_files": ["event_hotspots.jsonl", "event_hotspot_items.csv"],
            "generic_token_policy": "generic AI/template tokens are supporting evidence only and cannot independently create high-priority hotspots",
        }),
        "",
        "## 7. Candidate Priority Distribution",
        "",
        json_block({
            "candidate_priority_distribution": summary["item_relations"].get("candidate_priority_distribution", {}),
            "candidates_suppressed_without_llm": summary["item_relations"].get("candidates_suppressed_without_llm", 0),
            "warning": "must_run/high should remain scarce; inspect candidate_generation.jsonl if inflated",
        }),
        "",
        "## 8. Relation Precision Review",
        "",
        json_block({
            "near_duplicate": summary["item_relations"].get("near_duplicate", 0),
            "related_with_new_info": summary["item_relations"].get("related_with_new_info", 0),
            "event_relation_type_distribution": summary["item_relations"].get("event_relation_type_distribution", {}),
            "examples": summary["item_relations"].get("examples", []),
        }),
        "",
        "## 9. Item-Cluster Relation Quality",
        "",
        json_block(summary["item_clusters"]),
        "",
        "## 10. Cluster Seed Review",
        "",
        json_block({
            "multi_item_cluster_count": summary["item_clusters"].get("multi_item_cluster_count", 0),
            "evidence_files": ["cluster_seed_candidates.jsonl", "cluster_seed_rejections.jsonl", "clusters_final.jsonl"],
            "cluster_samples": summary["item_clusters"].get("cluster_samples", []),
        }),
        "",
        "## 11. Budget Skip Quality",
        "",
        json_block(summary["stage_budgets"]),
        "",
        "## 12. Cost / Yield",
        "",
        json_block(summary["token_cost"]),
        "",
        "## 13. Cluster Quality Samples",
        "",
        json_block(summary["item_clusters"].get("cluster_samples", [])),
        "",
        "## 14. Source Profile Results",
        "",
        json_block(summary["source_profiles"]),
        "",
        "## 15. Token / Latency / Cache Summary",
        "",
        json_block(summary["token_cost"]),
        "",
        "## 16. Concurrency Summary",
        "",
        json_block(summary["concurrency"]),
        "",
        "## 17. Stage Budget Summary",
        "",
        json_block(summary["stage_budgets"]),
        "",
        "## 18. Errors / Fallbacks / Retries",
        "",
        json_block(summary["errors_fallbacks"]),
        "",
        "## 19. Prompt Iteration Notes",
        "",
        json_block(summary["prompt_iteration_notes"]),
        "",
        "## 20. Manual Review Suggestions",
        "",
        json_block(summary["item_clusters"]["manual_review_suggestions"]),
        "",
        "## 21. Readiness Assessment",
        "",
        json_block(summary["readiness_assessment"]),
        "",
        "## 22. Recommendations",
        "",
    ]
    lines.extend([f"- {rec}" for rec in summary["recommendations"]])
    lines.extend([
        "",
        "## 10. Concurrency Summary",
        "",
        json_block(summary["concurrency"]),
        "",
        "## 14. Readiness Assessment",
        "",
        json_block(summary["readiness_assessment"]),
    ])
    lines.append("")
    return "\n".join(lines)


def json_block(value: Any) -> str:
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n```"


def compact_console_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "items_sampled": summary["input_sample"]["items_sampled"],
        "item_cards": summary["item_cards"]["item_cards_generated_or_reused"],
        "item_relations": summary["item_relations"]["relations_by_primary_relation"],
        "cluster_relations": summary["item_clusters"]["relations"],
        "source_profiles": summary["source_profiles"]["sources_recomputed"],
        "actual_calls": summary["metadata"]["actual_calls"],
        "actual_tokens": summary["metadata"]["actual_tokens"],
        "source_scope": summary["source_scope"]["matched_source_count"],
        "readiness": summary["readiness_assessment"]["write_real_db_recommended_now"],
        "warnings": summary["metadata"]["warnings"],
    }


def git_commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE_DIR.parent, text=True).strip()
    except Exception:
        return "unknown"
