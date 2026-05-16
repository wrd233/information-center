#!/usr/bin/env python3
"""Analyze a run's source_results.csv and print a performance profile report."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze RSS run performance profile from source_results.csv")
    parser.add_argument("--run-dir", required=True, help="Path to run directory containing source_results.csv")
    parser.add_argument("--top-n", type=int, default=20, help="Show top N slowest sources (default: 20)")
    return parser.parse_args()


def read_results(run_dir: Path) -> list[dict[str, Any]]:
    path = run_dir / "source_results.csv"
    if not path.exists():
        print(f"ERROR: source_results.csv not found at {path}")
        sys.exit(2)
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def safe_float(value: str, default: float = 0.0) -> float:
    if not value or str(value).strip() == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def format_seconds(s: float) -> str:
    if s < 1:
        return f"{s*1000:.0f}ms"
    if s < 60:
        return f"{s:.1f}s"
    minutes = s / 60
    return f"{minutes:.1f}m"


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * pct / 100.0)
    idx = max(0, min(idx, len(sorted_vals) - 1))
    return sorted_vals[idx]


def classify_error(error_type: str) -> str:
    mapping = {
        "feed_parse_error": "feed_parse_error",
        "timeout": "timeout",
        "network_error": "network_error",
        "content_inbox_error": "api_error",
        "embedding_error": "embedding_error",
        "model_error": "model_error",
        "rsshub_503": "rsshub_503",
        "skipped_known_failed": "skipped_known_failed",
        "worker_error": "worker_error",
    }
    return mapping.get(error_type, error_type or "unknown")


def main() -> None:
    args = parse_args()
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.is_dir():
        print(f"ERROR: run directory not found: {run_dir}")
        sys.exit(2)

    rows = read_results(run_dir)
    if not rows:
        print("ERROR: no rows in source_results.csv")
        sys.exit(2)

    # Count stats
    total = len(rows)
    success_rows = [r for r in rows if r.get("status") == "success"]
    failed_rows = [r for r in rows if r.get("status") == "failed"]
    skipped_rows = [r for r in rows if r.get("status") == "skipped_known_failed"]
    audited_rows = [r for r in rows if r.get("status") == "audited"]

    total_new = sum(int(r.get("new_items", 0)) for r in rows)
    total_items = sum(int(r.get("total_items", 0)) for r in rows)

    # Profile analysis (success rows only)
    source_times = [safe_float(r.get("source_total_seconds", 0)) for r in success_rows]
    source_times = [t for t in source_times if t > 0]
    fetch_total = sum(safe_float(r.get("fetch_feed_seconds", 0)) for r in success_rows)
    llm_screening_total = sum(safe_float(r.get("llm_basic_screening_seconds", 0)) for r in success_rows)
    llm_need_matching_total = sum(safe_float(r.get("llm_need_matching_seconds", 0)) for r in success_rows)
    embedding_total = sum(safe_float(r.get("embedding_seconds", 0)) for r in success_rows)
    lock_wait_total = sum(safe_float(r.get("lock_wait_seconds", 0)) for r in success_rows)
    lock_held_total = sum(safe_float(r.get("lock_held_seconds", 0)) for r in success_rows)
    pre_dedupe_wait = sum(safe_float(r.get("pre_dedupe_lock_wait_seconds", 0)) for r in success_rows)
    pre_dedupe_held = sum(safe_float(r.get("pre_dedupe_lock_held_seconds", 0)) for r in success_rows)
    commit_wait = sum(safe_float(r.get("commit_lock_wait_seconds", 0)) for r in success_rows)
    commit_held = sum(safe_float(r.get("commit_lock_held_seconds", 0)) for r in success_rows)
    source_total_sum = sum(source_times)

    total_wall_clock = source_total_sum  # Aggregate sum of per-source wall clock

    # ============================================================
    # Report
    # ============================================================
    print("=" * 70)
    print("RSS Run Performance Profile")
    print(f"Run directory: {run_dir}")
    print("=" * 70)

    # 1. Overview
    print("\n--- 1. Overview ---")
    print(f"  Total sources:            {total:>6}")
    print(f"  Successful:               {len(success_rows):>6}")
    print(f"  Failed:                   {len(failed_rows):>6}")
    print(f"  Skipped (known failed):   {len(skipped_rows):>6}")
    print(f"  Audited:                  {len(audited_rows):>6}")
    print(f"  Total items:              {total_items:>6}")
    print(f"  New items:                {total_new:>6}")
    print(f"  Success rate:             {len(success_rows)/total*100:>5.1f}%" if total > 0 else "  N/A")
    print(f"  Total wall-clock (agg):   {format_seconds(total_wall_clock):>6}")

    # 2. Slowest sources
    print(f"\n--- 2. Slowest {min(args.top_n, len(success_rows))} Sources ---")
    ranked = sorted(success_rows, key=lambda r: safe_float(r.get("source_total_seconds", 0)), reverse=True)
    print(f"  {'#':<4} {'Source':<40} {'Total':>8} {'Fetch':>8} {'LLM':>8} {'Need':>8} {'Embed':>8} {'LockW':>8} {'LockH':>8}")
    for i, r in enumerate(ranked[: args.top_n], 1):
        name = (r.get("source_name") or "")[:38]
        t = safe_float(r.get("source_total_seconds", 0))
        f = safe_float(r.get("fetch_feed_seconds", 0))
        l = safe_float(r.get("llm_basic_screening_seconds", 0))
        n = safe_float(r.get("llm_need_matching_seconds", 0))
        e = safe_float(r.get("embedding_seconds", 0))
        lw = safe_float(r.get("lock_wait_seconds", 0))
        lh = safe_float(r.get("lock_held_seconds", 0))
        print(f"  {i:<4} {name:<40} {format_seconds(t):>8} {format_seconds(f):>8} {format_seconds(l):>8} {format_seconds(n):>8} {format_seconds(e):>8} {format_seconds(lw):>8} {format_seconds(lh):>8}")

    # 3-8. Time breakdown
    print(f"\n--- 3-8. Time Breakdown (success rows: {len(success_rows)}) ---")
    def pct_of_total(val: float) -> str:
        if total_wall_clock == 0:
            return "N/A"
        return f"{val/total_wall_clock*100:.1f}%"

    print(f"  {'Category':<35} {'Total':>10} {'% of Total':>12} {'Per Source':>10}")
    print(f"  {'fetch_feed_seconds':<35} {format_seconds(fetch_total):>10} {pct_of_total(fetch_total):>12} {format_seconds(fetch_total/len(success_rows)):>10}" if success_rows else "")
    print(f"  {'llm_basic_screening_seconds':<35} {format_seconds(llm_screening_total):>10} {pct_of_total(llm_screening_total):>12} {format_seconds(llm_screening_total/len(success_rows)):>10}" if success_rows else "")
    print(f"  {'llm_need_matching_seconds':<35} {format_seconds(llm_need_matching_total):>10} {pct_of_total(llm_need_matching_total):>12} {format_seconds(llm_need_matching_total/len(success_rows)):>10}" if success_rows else "")
    print(f"  {'embedding_seconds':<35} {format_seconds(embedding_total):>10} {pct_of_total(embedding_total):>12} {format_seconds(embedding_total/len(success_rows)):>10}" if success_rows else "")
    print(f"  {'lock_wait_seconds':<35} {format_seconds(lock_wait_total):>10} {pct_of_total(lock_wait_total):>12} {format_seconds(lock_wait_total/len(success_rows)):>10}" if success_rows else "")
    print(f"  {'lock_held_seconds':<35} {format_seconds(lock_held_total):>10} {pct_of_total(lock_held_total):>12} {format_seconds(lock_held_total/len(success_rows)):>10}" if success_rows else "")

    # Lock detail (post-split)
    if pre_dedupe_wait > 0 or pre_dedupe_held > 0 or commit_wait > 0 or commit_held > 0:
        print(f"\n  Lock detail (split phases):")
        print(f"  {'pre_dedupe_lock_wait_seconds':<35} {format_seconds(pre_dedupe_wait):>10}")
        print(f"  {'pre_dedupe_lock_held_seconds':<35} {format_seconds(pre_dedupe_held):>10}")
        print(f"  {'commit_lock_wait_seconds':<35} {format_seconds(commit_wait):>10}")
        print(f"  {'commit_lock_held_seconds':<35} {format_seconds(commit_held):>10}")

    # Profile completeness check
    rows_with_profile = [r for r in success_rows if safe_float(r.get("source_total_seconds", 0)) > 0]
    rows_without_profile = len(success_rows) - len(rows_with_profile)
    if rows_without_profile > 0:
        print(f"\n  WARNING: {rows_without_profile}/{len(success_rows)} success rows have no profile data (source_total_seconds=0 or empty)")

    # 9. Percentiles
    print(f"\n--- 9. source_total_seconds Percentiles ---")
    if source_times:
        print(f"  P50:  {format_seconds(percentile(source_times, 50))}")
        print(f"  P90:  {format_seconds(percentile(source_times, 90))}")
        print(f"  P95:  {format_seconds(percentile(source_times, 95))}")
        print(f"  P99:  {format_seconds(percentile(source_times, 99))}")
        print(f"  Max:  {format_seconds(max(source_times))}")
    else:
        print("  No profile data available")

    # 10. Category breakdown
    print(f"\n--- 10. Time by source_category ---")
    cat_times: dict[str, list[float]] = defaultdict(list)
    cat_counts: dict[str, int] = defaultdict(int)
    for r in success_rows:
        cat = r.get("source_category") or "Uncategorized"
        t = safe_float(r.get("source_total_seconds", 0))
        if t > 0:
            cat_times[cat].append(t)
        cat_counts[cat] += 1

    for cat in sorted(cat_times.keys(), key=lambda c: sum(cat_times[c]), reverse=True):
        cat_total = sum(cat_times[cat])
        cat_avg = cat_total / len(cat_times[cat]) if cat_times[cat] else 0
        print(f"  {cat:<40} count={cat_counts[cat]:>3}  total={format_seconds(cat_total):>8}  avg={format_seconds(cat_avg)}")

    # 11. Failed source classification
    if failed_rows:
        print(f"\n--- 11. Failed Source Classification ---")
        error_types: dict[str, int] = defaultdict(int)
        for r in failed_rows:
            et = classify_error(r.get("error_type", "unknown"))
            error_types[et] += 1
        for et, count in sorted(error_types.items(), key=lambda x: -x[1]):
            print(f"  {et:<25} {count:>3}")

    # Overall assessment
    print(f"\n--- Overall ---")
    has_profile = len(rows_with_profile) > 0
    if has_profile:
        slowest_pct = "LLM screening" if llm_screening_total > fetch_total else "Feed fetching"
        print(f"  Dominant cost: {slowest_pct}")
        print(f"  LLM screening accounts for {pct_of_total(llm_screening_total)} of total time")
        avg_per_item = total_wall_clock / total_new if total_new > 0 else 0
        print(f"  Average time per new item: {format_seconds(avg_per_item)}")
    else:
        print("  No profile data available. Check that --profile flag was used and Docker image is up-to-date.")
    print("=" * 70)


if __name__ == "__main__":
    main()
