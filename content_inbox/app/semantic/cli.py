from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from app.config import settings
from app.semantic.cards import generate_item_cards
from app.semantic.clusters import (
    list_clusters,
    patch_cluster_card,
    process_item_clusters,
    rebuild_cluster_card,
    show_cluster,
    update_cluster_statuses,
)
from app.semantic.evaluate import run_evaluation
from app.semantic.live_smoke import run_live_smoke
from app.semantic.relations import process_item_relations
from app.semantic.review import decide_review, list_reviews
from app.semantic.source_profiles import get_profile, list_suggestions, recompute_source_profiles, set_priority
from app.storage import InboxStore


def write_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, sort_keys=True))


def _print_probe_report(data: dict[str, Any]) -> None:
    """Print a human-readable probe report."""
    summary = data.get("summary", {})
    diags = data.get("diagnostics", [])
    sources = data.get("rss_sources_matched", [])

    print("=" * 60)
    print(f"Source Scope Probe: {data.get('source_url_prefix', '?')}")
    print("=" * 60)

    print(f"\nSummary:")
    print(f"  Total rss_sources: {summary.get('total_rss_sources', '?')}")
    print(f"  Sources matched:   {summary.get('total_sources_matched', '?')}")
    print(f"  Items via JOIN:    {summary.get('total_items_via_rss_join', '?')}")
    print(f"  Items via direct:  {summary.get('total_items_via_direct_search', '?')}")
    print(f"  NULL source_id:    {summary.get('total_items_with_null_source_id', '?')}")
    print(f"  NULL feed_url:     {summary.get('total_items_with_null_feed_url', '?')}")

    if diags:
        print(f"\nDiagnostics:")
        for d in diags:
            tag = d["severity"].upper()
            print(f"  [{tag}] [Case {d['case']}] {d['message']}")

    if sources:
        print(f"\nMatched Sources ({len(sources)}):")
        for s in sources:
            print(f"  {s['source_id']}")
            print(f"    name: {s['source_name']}")
            print(f"    feed_url: {s['feed_url']}")
            print(f"    status: {s['status']}  items: {s['item_count_total']}  "
                  f"(by source_id: {s['item_count_by_source_id']}, "
                  f"by name: {s['item_count_by_name_category']})")
            if s.get("last_error_message"):
                print(f"    last_error: {s['last_error_message']}")

    print()


def store_from_args(args: argparse.Namespace) -> InboxStore:
    return InboxStore(Path(args.db_path) if args.db_path else settings.database_path)


def add_db_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--db-path", default="")


def add_live_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--token-budget", type=int, default=0)
    parser.add_argument("--max-calls", type=int)
    parser.add_argument("--concurrency", type=int, default=1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="content_inbox semantic CLI")
    add_db_arg(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    cards = sub.add_parser("cards")
    add_live_args(cards)
    cards.add_argument("--limit", type=int, default=100)
    cards.add_argument("--batch-size", type=int, default=5)
    cards.add_argument("--dry-run", action="store_true")
    cards.add_argument("--force", action="store_true")

    dedupe = sub.add_parser("dedupe")
    add_live_args(dedupe)
    dedupe.add_argument("--limit", type=int, default=100)
    dedupe.add_argument("--max-candidates", type=int, default=5)

    cluster = sub.add_parser("cluster")
    add_live_args(cluster)
    cluster.add_argument("--limit", type=int, default=100)
    cluster.add_argument("--max-candidates", type=int, default=3)
    cluster.add_argument("--include-archived", action="store_true")

    patch = sub.add_parser("patch-cluster-card")
    add_live_args(patch)
    patch.add_argument("cluster_id")

    rebuild = sub.add_parser("rebuild-cluster-card")
    add_live_args(rebuild)
    rebuild.add_argument("cluster_id")

    clusters = sub.add_parser("clusters")
    clusters_sub = clusters.add_subparsers(dest="clusters_command", required=True)
    clusters_list = clusters_sub.add_parser("list")
    clusters_list.add_argument("--status")
    clusters_list.add_argument("--limit", type=int, default=50)
    clusters_show = clusters_sub.add_parser("show")
    clusters_show.add_argument("cluster_id")
    clusters_sub.add_parser("update-status")

    sp = sub.add_parser("source-profiles")
    sp_sub = sp.add_subparsers(dest="source_profiles_command", required=True)
    sp_recompute = sp_sub.add_parser("recompute")
    sp_recompute.add_argument("--json", action="store_true")
    sp_recompute.add_argument("--output")

    source = sub.add_parser("source")
    source_sub = source.add_subparsers(dest="source_command", required=True)
    source_sub.add_parser("suggestions")
    source_profile = source_sub.add_parser("profile")
    source_profile.add_argument("source_id")
    source_set = source_sub.add_parser("set-priority")
    source_set.add_argument("source_id")
    source_set.add_argument("priority", choices=["high", "normal", "low", "disabled_for_llm", "new_source_under_evaluation"])

    review = sub.add_parser("review")
    review_sub = review.add_subparsers(dest="review_command", required=True)
    review_list = review_sub.add_parser("list")
    review_list.add_argument("--status", default="pending")
    review_list.add_argument("--limit", type=int, default=50)
    review_approve = review_sub.add_parser("approve")
    review_approve.add_argument("review_id", type=int)
    review_reject = review_sub.add_parser("reject")
    review_reject.add_argument("review_id", type=int)

    smoke = sub.add_parser("live-smoke")
    smoke.add_argument("target", choices=["item-card", "item-relation", "item-cluster", "cluster-card", "source-review", "all"])
    smoke.add_argument("--limit", type=int, default=3)
    smoke.add_argument("--max-calls", type=int, default=50)
    smoke.add_argument("--write-real-db", action="store_true")

    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--db-path", default="")
    evaluate.add_argument("--limit", "--max-items", dest="limit", type=int, default=100)
    evaluate.add_argument("--max-calls", type=int, default=100)
    evaluate.add_argument("--max-candidates", type=int, default=5)
    evaluate.add_argument("--batch-size", type=int, default=5)
    evaluate.add_argument("--live", action="store_true")
    evaluate.add_argument("--dry-run", action="store_true")
    evaluate.add_argument("--write-real-db", action="store_true")
    evaluate.add_argument("--model")
    evaluate.add_argument("--strong-model")
    evaluate.add_argument("--token-budget", type=int, default=200000)
    evaluate.add_argument(
        "--stage-budget-profile",
        choices=["balanced", "relation_heavy", "cluster_heavy", "card_heavy", "phase1_2e_profile", "phase1_3_advisory"],
        default="phase1_3_advisory",
    )
    evaluate.add_argument("--concurrency", type=int, default=4)
    evaluate.add_argument("--include-archived", action="store_true")
    evaluate.add_argument("--output", "--output-dir", dest="output")
    evaluate.add_argument("--persist-evidence", action="store_true")
    evaluate.add_argument("--evidence-dir")
    evaluate.add_argument("--phase-label", default="semantic_eval")
    evaluate.add_argument("--backup-path")
    evaluate.add_argument("--confirm-scoped-semantic-write")
    evaluate.add_argument("--source-filter")
    evaluate.add_argument("--source-url-prefix")
    evaluate.add_argument(
        "--sample-mode",
        choices=["recent", "duplicate_candidates", "cluster_candidates", "source_scope_full", "mixed", "event_hotspots"],
        default="recent",
    )
    ingest = sub.add_parser("ingest-source-scope")
    ingest.add_argument("--dry-run", action="store_true", default=True)
    ingest.add_argument("--apply", action="store_true", help="Actually run ingestion (requires --apply)")
    ingest.add_argument("--limit-sources", type=int, default=0)
    ingest.add_argument("--concurrency", type=int, default=8)
    ingest.add_argument("--per-source-timeout", type=int, default=30)
    ingest.add_argument("--retry", type=int, default=1)
    ingest.add_argument("--output", "--output-dir", dest="output")
    ingest.add_argument("source_url_prefix", help="URL prefix of sources to ingest")

    probe = sub.add_parser("probe-source-scope")
    probe.add_argument("--json", "--json-output", dest="json_output", action="store_true")
    probe.add_argument("--output", "--output-dir", dest="output")
    probe.add_argument("source_url_prefix", help="URL prefix to probe (e.g., api.xgo.ing)")

    fix = sub.add_parser("fix-source-linkage")
    fix.add_argument("--dry-run", action="store_true", default=True)
    fix.add_argument("--apply", action="store_true", help="Apply fixes to real DB (requires --apply)")
    fix.add_argument("source_url_prefix")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "live-smoke":
            write_json(
                run_live_smoke(
                    args.target,
                    limit=args.limit,
                    max_calls=args.max_calls,
                    db_path=args.db_path or None,
                    write_real_db=args.write_real_db,
                )
            )
            return 0
        if args.command == "evaluate":
            data = run_evaluation(
                db_path=args.db_path or None,
                output=args.output,
                limit=args.limit,
                max_calls=args.max_calls,
                max_candidates=args.max_candidates,
                batch_size=args.batch_size,
                live=args.live,
                dry_run=args.dry_run,
                write_real_db=args.write_real_db,
                model=args.model,
                strong_model=args.strong_model,
                token_budget=args.token_budget,
                include_archived=args.include_archived,
                concurrency=args.concurrency,
                source_filter=args.source_filter,
                source_url_prefix=args.source_url_prefix,
                sample_mode=args.sample_mode,
                stage_budget_profile=args.stage_budget_profile,
                persist_evidence=args.persist_evidence,
                evidence_dir=args.evidence_dir,
                phase_label=args.phase_label,
                backup_path=args.backup_path,
                confirm_scoped_semantic_write=args.confirm_scoped_semantic_write,
            )
            write_json(data)
            return 0 if data.get("ok", True) else 1
        store = store_from_args(args)
        if args.command == "cards":
            data = generate_item_cards(
                store,
                limit=args.limit,
                batch_size=args.batch_size,
                live=args.live,
                dry_run=args.dry_run,
                force=args.force,
                model=args.model,
                max_calls=args.max_calls,
                token_budget=args.token_budget or None,
                concurrency=args.concurrency,
            )
        elif args.command == "dedupe":
            data = process_item_relations(
                store,
                limit=args.limit,
                live=args.live,
                max_candidates=args.max_candidates,
                max_calls=args.max_calls,
                model=args.model,
                token_budget=args.token_budget or None,
                concurrency=args.concurrency,
            )
        elif args.command == "cluster":
            data = process_item_clusters(
                store,
                limit=args.limit,
                live=args.live,
                max_candidates=args.max_candidates,
                max_calls=args.max_calls,
                model=args.model,
                include_archived=args.include_archived,
                token_budget=args.token_budget or None,
            )
        elif args.command == "patch-cluster-card":
            data = patch_cluster_card(store, args.cluster_id, live=args.live, model=args.model, max_calls=args.max_calls)
        elif args.command == "rebuild-cluster-card":
            data = rebuild_cluster_card(store, args.cluster_id, live=args.live, model=args.model, max_calls=args.max_calls)
        elif args.command == "clusters":
            if args.clusters_command == "list":
                data = {"ok": True, "clusters": list_clusters(store, status=args.status, limit=args.limit)}
            elif args.clusters_command == "show":
                data = {"ok": True, "cluster": show_cluster(store, args.cluster_id)}
            else:
                data = update_cluster_statuses(store)
        elif args.command == "source-profiles":
            data = recompute_source_profiles(store)
            if getattr(args, "output", None):
                Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        elif args.command == "source":
            if args.source_command == "suggestions":
                data = {"ok": True, "suggestions": list_suggestions(store)}
            elif args.source_command == "profile":
                data = {"ok": True, "profile": get_profile(store, args.source_id)}
            else:
                data = {"ok": True, "profile": set_priority(store, args.source_id, args.priority)}
        elif args.command == "review":
            if args.review_command == "list":
                data = {"ok": True, "reviews": list_reviews(store, status=args.status, limit=args.limit)}
            elif args.review_command == "approve":
                data = decide_review(store, args.review_id, "approved")
            else:
                data = decide_review(store, args.review_id, "rejected")
        elif args.command == "probe-source-scope":
            from app.semantic.probe import probe_markdown_report, probe_source_scope

            data = probe_source_scope(store, args.source_url_prefix)
            if getattr(args, "output", None):
                out = Path(args.output)
                if not out.suffix:
                    out.mkdir(parents=True, exist_ok=True)
                    (out / "probe_report.md").write_text(probe_markdown_report(data), encoding="utf-8")
                    (out / "probe_summary.json").write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
                elif out.suffix == ".md":
                    out.write_text(probe_markdown_report(data), encoding="utf-8")
                    out.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
                else:
                    out.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
            if getattr(args, "json_output", False):
                write_json(data)
            else:
                _print_probe_report(data)
        elif args.command == "fix-source-linkage":
            from app.semantic.probe import fix_source_linkage

            dry_run = not getattr(args, "apply", False)
            data = fix_source_linkage(store, args.source_url_prefix, apply=not dry_run, dry_run=dry_run)
            write_json(data)
        elif args.command == "ingest-source-scope":
            from app.semantic.probe import ingest_markdown_report, ingest_matching_sources

            dry_run = not getattr(args, "apply", False)
            data = ingest_matching_sources(
                store,
                args.source_url_prefix,
                dry_run=dry_run,
                limit=args.limit_sources or None,
                concurrency=args.concurrency,
                per_source_timeout_seconds=args.per_source_timeout,
                retry=args.retry,
            )
            if getattr(args, "output", None):
                out = Path(args.output)
                if not out.suffix:
                    out.mkdir(parents=True, exist_ok=True)
                    (out / "ingest_report.md").write_text(ingest_markdown_report(data), encoding="utf-8")
                    (out / "ingest_summary.json").write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
                elif out.suffix == ".md":
                    out.write_text(ingest_markdown_report(data), encoding="utf-8")
                    out.with_suffix(".json").write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
                else:
                    out.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
            write_json(data)
        else:
            raise ValueError(f"unknown command: {args.command}")
        write_json(data)
        return 0 if data.get("ok", True) else 1
    except Exception as exc:
        write_json({"ok": False, "error": {"error_code": "semantic_cli_error", "message": str(exc)}})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
