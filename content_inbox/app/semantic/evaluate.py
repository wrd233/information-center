from __future__ import annotations

import json
import os
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
from app.semantic.clusters import patch_cluster_card, process_item_clusters
from app.semantic.live_smoke import live_enabled
from app.semantic.relations import process_item_relations
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
) -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    t0 = time.monotonic()
    run_id = f"semantic_eval_{started.strftime('%Y%m%d_%H%M%S')}"
    output_root = Path(output) if output else BASE_DIR / "outputs" / "semantic_eval"
    run_dir = output_root / run_id
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
        sampled_items = sample_existing_items(source_store, limit)
    else:
        target_store, target_db_path = make_temp_eval_store()
        sampled_items = copy_sample_to_eval_store(source_store, target_store, limit, warnings)

    max_items = len(sampled_items)
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
        "include_archived": include_archived,
        "concurrency": concurrency,
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
            token_budget=token_budget or None,
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
            token_budget=token_budget or None,
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
            token_budget=token_budget or None,
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
                    token_budget=token_budget or None,
                    global_call_limit=True,
                )
            )
            remaining = remaining_calls(target_store, max_calls)
        steps["source_profiles"] = recompute_source_profiles(target_store)

    finished = datetime.now(timezone.utc)
    metadata["finished_at"] = finished.isoformat()
    metadata["duration_seconds"] = round(time.monotonic() - t0, 3)
    summary = build_summary(target_store, metadata, steps, sampled_items)
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
    }


def make_temp_eval_store() -> tuple[InboxStore, Path]:
    tmp = tempfile.NamedTemporaryFile(prefix="content_inbox_semantic_eval_", suffix=".sqlite3", delete=False)
    tmp.close()
    path = Path(tmp.name)
    return InboxStore(path), path


def sample_existing_items(store: InboxStore, limit: int) -> list[dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute(
            "SELECT * FROM inbox_items ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [row_to_item(row) for row in rows]


def copy_sample_to_eval_store(source_store: InboxStore, target_store: InboxStore, limit: int, warnings: list[str]) -> list[dict[str, Any]]:
    sampled = sample_existing_items(source_store, limit)
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


def build_summary(store: InboxStore, metadata: dict[str, Any], steps: dict[str, Any], sampled_items: list[dict[str, Any]]) -> dict[str, Any]:
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
        "input_sample": input_sample_summary(sampled_items),
        "item_cards": item_card_summary(item_cards),
        "item_relations": item_relation_summary(item_relations, store),
        "item_clusters": cluster_relation_summary(cluster_items, clusters, cluster_cards),
        "source_profiles": source_profile_summary(source_profiles, reviews),
        "token_cost": token_summary(llm_logs),
        "errors_fallbacks": error_summary(llm_logs, reviews, steps, metadata),
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


def item_card_summary(rows: list[Any]) -> dict[str, Any]:
    roles = Counter(row["content_role"] for row in rows)
    warnings = Counter()
    entity_counts = []
    confidence = []
    samples = []
    for row in rows:
        try:
            warnings.update(json.loads(row["warnings_json"] or "[]"))
            entity_counts.append(len(json.loads(row["entities_json"] or "[]")))
        except Exception:
            pass
        confidence.append(float(row["confidence"] or 0.0))
        if len(samples) < 10:
            samples.append({"item_id": row["item_id"], "title": row["canonical_title"], "role": row["content_role"], "summary": row["short_summary"]})
    return {
        "item_cards_generated_or_reused": len(rows),
        "avg_confidence": round(sum(confidence) / max(len(confidence), 1), 3),
        "content_role_distribution": dict(roles),
        "entity_count_distribution": dict(Counter(entity_counts)),
        "warnings_distribution": dict(warnings),
        "samples": samples,
    }


def item_relation_summary(rows: list[Any], store: InboxStore) -> dict[str, Any]:
    rels = Counter(row["primary_relation"] for row in rows)
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
    confidences = [float(row["confidence"] or 0.0) for row in cluster_items]
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
        "relations": dict(rels),
        "same_event": dict(Counter(bool(row["same_event"]) for row in cluster_items)),
        "same_topic": dict(Counter(bool(row["same_topic"]) for row in cluster_items)),
        "follow_up_event": dict(Counter(bool(row["follow_up_event"]) for row in cluster_items)),
        "should_update_cluster_card_count": sum(1 for row in cluster_items if row["should_update_cluster_card"]),
        "should_notify_count": sum(1 for row in cluster_items if row["should_notify"]),
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
    return {
        "sources_recomputed": len(rows),
        "high_candidates": [p for p in profiles if p.get("priority_suggestion") == "high"][:20],
        "low_candidates": [p for p in profiles if p.get("priority_suggestion") == "low"][:20],
        "disabled_for_llm_candidates": [p for p in profiles if p.get("priority_suggestion") == "disabled_for_llm"][:20],
        "pending_reviews_created": len(pending),
        "top_sources_by_llm_yield": sorted(profiles, key=lambda p: p.get("llm_yield_score") or 0, reverse=True)[:10],
        "top_sources_by_duplicate_rate": sorted(profiles, key=lambda p: p.get("duplicate_rate") or 0, reverse=True)[:10],
        "top_sources_by_incremental_value_avg": sorted(profiles, key=lambda p: p.get("incremental_value_avg") or 0, reverse=True)[:10],
        "top_sources_by_report_value_avg": sorted(profiles, key=lambda p: p.get("report_value_avg") or 0, reverse=True)[:10],
        "sources_with_insufficient_data": [p for p in profiles if (p.get("total_items") or 0) < 3][:20],
    }


def token_summary(rows: list[Any]) -> list[dict[str, Any]]:
    tasks = ["item_card", "item_relation", "item_cluster_relation", "cluster_card_patch", "cluster_card_rebuild", "source_review", "json_repair"]
    out = []
    for task in tasks:
        subset = [row for row in rows if row["task_type"] == task]
        out.append({
            "task_type": task,
            "calls": len(subset),
            "success": sum(1 for row in subset if row["status"] == "ok"),
            "failed": sum(1 for row in subset if row["status"] == "failed"),
            "input_tokens": sum(int(row["prompt_tokens"] or 0) for row in subset),
            "output_tokens": sum(int(row["completion_tokens"] or 0) for row in subset),
            "total_tokens": sum(int(row["total_tokens"] or 0) for row in subset),
            "cache_hit_tokens": sum(int(row["cache_hit_tokens"] or 0) for row in subset),
            "cache_miss_tokens": sum(int(row["cache_miss_tokens"] or 0) for row in subset),
            "avg_latency_ms": round(sum(int(row["latency_ms"] or 0) for row in subset) / max(len(subset), 1), 1),
        })
    return out


def error_summary(rows: list[Any], reviews: list[Any], steps: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    tokens = metadata.get("actual_tokens", 0)
    return {
        "llm_parse_failures": sum(1 for row in rows if row["status"] == "failed" and "JSON" in (row["error"] or "")),
        "repair_retry_count": sum(1 for row in rows if row["status"] == "failed"),
        "final_failures": sum(1 for row in rows if row["status"] == "failed"),
        "review_queue_entries_due_to_failure": sum(1 for row in reviews if "failed" in (row["reason"] or "").lower()),
        "skipped_due_to_max_calls": any("max calls" in (row["error"] or "") for row in rows),
        "skipped_due_to_token_budget": bool(metadata.get("token_budget") and tokens >= metadata.get("token_budget")),
        "skipped_due_to_missing_card": 0,
        "skipped_due_to_no_candidate": 0,
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


def build_markdown_report(summary: dict[str, Any]) -> str:
    m = summary["metadata"]
    lines = [
        "# Semantic Quality Report",
        "",
        "## Run Metadata",
        "",
        json_block(m),
        "",
        "## Input Sample Summary",
        "",
        json_block(summary["input_sample"]),
        "",
        "## Item Card Results",
        "",
        json_block(summary["item_cards"]),
        "",
        "## Item-Item Relation Results",
        "",
        json_block(summary["item_relations"]),
        "",
        "## Item-Cluster Relation Results",
        "",
        json_block(summary["item_clusters"]),
        "",
        "## Cluster Quality Manual Review Suggestions",
        "",
        json_block(summary["item_clusters"]["manual_review_suggestions"]),
        "",
        "## Source Profile Results",
        "",
        json_block(summary["source_profiles"]),
        "",
        "## Token And Cost Summary",
        "",
        json_block(summary["token_cost"]),
        "",
        "## Errors And Fallbacks",
        "",
        json_block(summary["errors_fallbacks"]),
        "",
        "## Recommendations",
        "",
    ]
    lines.extend([f"- {rec}" for rec in summary["recommendations"]])
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
        "warnings": summary["metadata"]["warnings"],
    }


def git_commit_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=BASE_DIR.parent, text=True).strip()
    except Exception:
        return "unknown"
