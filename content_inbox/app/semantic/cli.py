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
from app.semantic.live_smoke import run_live_smoke
from app.semantic.relations import process_item_relations
from app.semantic.review import decide_review, list_reviews
from app.semantic.source_profiles import get_profile, list_suggestions, recompute_source_profiles, set_priority
from app.storage import InboxStore


def write_json(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, sort_keys=True))


def store_from_args(args: argparse.Namespace) -> InboxStore:
    return InboxStore(Path(args.db_path) if args.db_path else settings.database_path)


def add_db_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--db-path", default="")


def add_live_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--max-calls", type=int)


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
    sp_sub.add_parser("recompute")

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
    smoke.add_argument("--max-calls", type=int, default=10)
    smoke.add_argument("--write-real-db", action="store_true")
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
            )
        elif args.command == "dedupe":
            data = process_item_relations(
                store,
                limit=args.limit,
                live=args.live,
                max_candidates=args.max_candidates,
                max_calls=args.max_calls,
                model=args.model,
            )
        elif args.command == "cluster":
            data = process_item_clusters(
                store,
                limit=args.limit,
                live=args.live,
                max_candidates=args.max_candidates,
                max_calls=args.max_calls,
                model=args.model,
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
        else:
            raise ValueError(f"unknown command: {args.command}")
        write_json(data)
        return 0 if data.get("ok", True) else 1
    except Exception as exc:
        write_json({"ok": False, "error": {"error_code": "semantic_cli_error", "message": str(exc)}})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
