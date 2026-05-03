#!/usr/bin/env python3
"""Focused test: merged mode on 3 sources from end of CSV.

- Picks 脑极体, InfoQ, 特工宇宙 (lines 493, 501, 495)
- Calls /api/rss/analyze with screen=true, profile=true
- Saves all outputs to a new rss_run directory
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import datetime as dt
from pathlib import Path

API_BASE = "http://127.0.0.1:8787"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "runs"

SOURCES = [
    {
        "feed_url": "http://192.168.1.6:8003/feed/MP_WXS_3515522183.atom",
        "source_name": "脑极体",
        "source_category": "Articles/AI",
        "limit": 3,
    },
    {
        "feed_url": "http://192.168.1.6:8003/feed/MP_WXS_3957475902.atom",
        "source_name": "阿伦AI学习笔记",
        "source_category": "Articles/AI",
        "limit": 3,
    },
    {
        "feed_url": "http://192.168.1.6:8003/feed/MP_WXS_3077513391.atom",
        "source_name": "Z Finance",
        "source_category": "Articles/AI",
        "limit": 3,
    },
]


def main():
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_DIR / f"rss_run_merged_test_{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    dump_dir = run_dir / "llm_prompt_dumps"
    dump_dir.mkdir(parents=True, exist_ok=True)

    print(f"[TEST] Run dir: {run_dir}")

    all_results = []

    for i, src in enumerate(SOURCES, start=1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(SOURCES)}] Testing: {src['source_name']}")
        print(f"[INFO] feed_url: {src['feed_url']}")
        print(f"[INFO] limit: {src['limit']}")

        payload = {
            "feed_url": src["feed_url"],
            "source_name": src["source_name"],
            "source_category": src["source_category"],
            "limit": src["limit"],
            "screen": True,
            "profile": True,
            "dump_llm_prompt": True,
            "dump_llm_prompt_dir": str(dump_dir),
        }

        t0 = time.monotonic()
        req = urllib.request.Request(
            f"{API_BASE}/api/rss/analyze",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                result = json.loads(raw)
        except urllib.error.HTTPError as e:
            result = {"ok": False, "error": e.read().decode("utf-8", errors="replace"), "_status": e.code}
        elapsed = time.monotonic() - t0

        result["_test_elapsed_seconds"] = round(elapsed, 2)
        result["_test_source_name"] = src["source_name"]

        profile = result.get("profile", {})
        print(f"[TIME] Total {elapsed:.2f}s | "
              f"fetch={profile.get('fetch_feed_seconds','?')} | "
              f"screen={profile.get('llm_basic_screening_seconds','?')} | "
              f"match={profile.get('llm_need_matching_seconds','?')}")

        print(f"[RESULT] ok={result.get('ok')} "
              f"total={result.get('total_items','?')} "
              f"new={result.get('new_items','?')} "
              f"screened={result.get('screened_items','?')} "
              f"recommended={result.get('recommended_items','?')} "
              f"failed_items={result.get('failed_items','?')}")

        items = result.get("items") or []
        for item in items:
            screening = item.get("screening") or {}
            title = item.get("title") or ""
            summary = screening.get("summary", "")
            score = screening.get("value_score", "")
            action = screening.get("suggested_action", "")
            need_matches = screening.get("need_matches", [])
            topic_matches = screening.get("topic_matches", [])
            error = screening.get("error", "")
            status = screening.get("screening_status", "")

            print(f"  [{status}] [{score}] [{action}] {title[:80]}")
            if summary:
                print(f"    summary: {summary[:120]}")
            if error:
                print(f"    ERROR: {error[:200]}")
            if need_matches:
                for nm in need_matches[:2]:
                    print(f"    need_match: {nm.get('need_name','')} score={nm.get('score','')} decision={nm.get('decision','')}")
            if topic_matches:
                for tm in topic_matches[:2]:
                    print(f"    topic_match: {tm.get('topic_name','')} score={tm.get('score','')}")

        all_results.append(result)

    # Save results summary
    summary_path = run_dir / "test_results.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n[DONE] Results saved to {summary_path}")

    # List dump files
    dump_files = sorted(dump_dir.glob("*.json"))
    print(f"[PROMPT_DUMP] {len(dump_files)} prompt dumps in {dump_dir}")
    for df in dump_files:
        print(f"  {df.name}")

    # Show first dump stats
    if dump_files:
        with dump_files[0].open(encoding="utf-8") as f:
            dump = json.load(f)
        stats = dump.get("stats", {})
        print(f"\n[PROMPT STATS] first dump ({dump_files[0].name}):")
        print(f"  prompt_name: {dump.get('prompt_name')}")
        print(f"  system_chars: {stats.get('system_chars')}")
        print(f"  user_chars: {stats.get('user_chars')}")
        print(f"  total_chars: {stats.get('total_chars')}")
        print(f"  estimated_tokens_cjk_aware: {stats.get('estimated_tokens_cjk_aware')}")


if __name__ == "__main__":
    main()
