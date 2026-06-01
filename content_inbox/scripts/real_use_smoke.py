from __future__ import annotations

import argparse
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from app.config import BASE_DIR, settings
from app.ops_api import api_report_generate, api_run_report, ensure_environment_metadata, generate_briefing
from app.semantic.cards import generate_item_cards
from app.semantic.evaluate import copy_sample_to_eval_store
from app.semantic.operational_pipeline import generate_information_objects, run_dedupe_stage
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
            "- No live LLM calls are made by this script.",
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
            "warnings": warnings,
        },
        "source_scope": source_scope_summary(source_store),
        "pipeline": {"dedupe": dedupe, "item_cards": item_cards, "information_objects": information_objects},
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
    args = parser.parse_args()
    result = run_smoke(
        db_path=args.db_path,
        output=args.output,
        limit=args.limit,
        sample_mode=args.sample_mode,
        source_filter=args.source_filter,
        source_url_prefix=args.source_url_prefix,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
