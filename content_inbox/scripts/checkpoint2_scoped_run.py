"""Checkpoint 2: Scoped operational v3 run on real data."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Add content_inbox to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.storage import InboxStore
from app.semantic.operational_pipeline import generate_information_objects, run_dedupe_stage, SCHEMA_VERSION, CREATED_BY
from app.utils import stable_hash, utc_now


def main():
    db_path = Path(__file__).resolve().parent.parent / "data" / "content_inbox.sqlite3"
    print(f"Using DB: {db_path}")
    store = InboxStore(db_path)

    # Scoped AI sources
    scoped_sources = [
        "socialmedia-openai-openai",
        "socialmedia-anthropic-anthropicai",
        "socialmedia-deepseek-deepseek-ai",
        "socialmedia-ai-at-meta-aiatmeta",
        "socialmedia-ai-breakfast-aibreakfast",
        "socialmedia-mistral-ai-mistralai",
        "socialmedia-xai-xai",
        "socialmedia-openai-developers-openaidevs",
        "socialmedia-chatgpt-chatgptapp",
        "socialmedia-perplexity-perplexity-ai",
        # Additional relevant sources
        "socialmedia-hugging-face-huggingface",
        "socialmedia-stability-ai-stabilityai",
        "socialmedia-cohere-cohere",
        "socialmedia-runwayml-runwayml",
    ]

    # Get items from scoped sources
    with store.connect() as conn:
        placeholders = ",".join("?" for _ in scoped_sources)
        items = conn.execute(
            f"SELECT item_id, title, source_id, source_name, content_text, summary, url FROM inbox_items WHERE source_id IN ({placeholders})",
            scoped_sources,
        ).fetchall()
        item_ids = [r["item_id"] for r in items]
        print(f"\nScoped sources: {len(scoped_sources)}")
        print(f"Items found: {len(item_ids)}")

        if not item_ids:
            print("No items found for scoped sources. Aborting.")
            return

        # Source breakdown
        src_count = {}
        for r in items:
            src_count[r["source_id"]] = src_count.get(r["source_id"], 0) + 1
        print("\nItems per source:")
        for src, cnt in sorted(src_count.items(), key=lambda x: -x[1]):
            print(f"  {src}: {cnt}")

        # Show sample titles
        print("\nSample titles (first 10):")
        for r in items[:10]:
            title = (r["title"] or "")[:100]
            print(f"  [{r['source_id']}] {title}")

    # Create test run
    run_id = f"test_cp2_{stable_hash(utc_now())[:8]}"
    now = utc_now()
    with store.connect() as conn:
        # Insert run
        conn.execute(
            """INSERT INTO rss_ingest_runs(run_id, trigger_type, source_mode, status, started_at, created_by, selected_source_count, new_items_count, created_at, updated_at)
               VALUES (?, 'manual', 'scoped', 'running', ?, 'checkpoint_2_test', ?, ?, ?, ?)""",
            (run_id, now, len(scoped_sources), len(item_ids), now, now),
        )
        # Link items to run
        for item_id in item_ids:
            conn.execute(
                "INSERT OR IGNORE INTO item_run_links(item_id, run_id, source_id, created_at) VALUES (?, ?, ?, ?)",
                (item_id, run_id, "checkpoint_2", now),
            )
        # Insert run sources
        for src in scoped_sources:
            conn.execute(
                "INSERT OR IGNORE INTO rss_ingest_run_sources(run_id, source_id, created_at) VALUES (?, ?, ?)",
                (run_id, src, now),
            )
        conn.commit()
    print(f"\nCreated test run: {run_id}")

    # Run dedupe stage first
    print("\n=== STAGE 1: Dedupe ===")
    dedupe_result = run_dedupe_stage(store, run_id, item_ids)
    print(json.dumps(dedupe_result, indent=2, ensure_ascii=False))

    # Run operational pipeline
    print("\n=== STAGE 2: Operational Pipeline ===")
    result = generate_information_objects(store, run_id, item_ids)

    # Pretty-print summary
    print("\n=== PIPELINE RESULT SUMMARY ===")
    for key in [
        "item_count", "schema_version", "created_by",
        "eventness", "signature", "alias_hit_count",
        "candidates_by_priority", "candidates_by_lane",
        "disqualifiers_by_reason",
        "auto_merged", "review_required", "rejected_non_event",
        "clusters_created_or_updated", "events_created_or_updated",
        "llm_calls",
    ]:
        val = result.get(key, "N/A")
        print(f"  {key}: {val}")

    # Verify event_candidate_pairs
    with store.connect() as conn:
        pairs = conn.execute("SELECT COUNT(*) as n FROM event_candidate_pairs WHERE run_id = ?", (run_id,)).fetchone()[0]
        print(f"\n  event_candidate_pairs written: {pairs}")

        by_status = conn.execute(
            "SELECT status, COUNT(*) as n FROM event_candidate_pairs WHERE run_id = ? GROUP BY status",
            (run_id,),
        ).fetchall()
        print(f"  by status: {[(r['status'], r['n']) for r in by_status]}")

        by_lane = conn.execute(
            "SELECT lane, COUNT(*) as n FROM event_candidate_pairs WHERE run_id = ? GROUP BY lane",
            (run_id,),
        ).fetchall()
        print(f"  by lane: {[(r['lane'], r['n']) for r in by_lane]}")

        reviews = conn.execute("SELECT COUNT(*) as n FROM review_queue WHERE suggestion_json LIKE ?", (f"%{run_id}%",)).fetchone()[0]
        print(f"\n  review_queue entries: {reviews}")

        events_new = conn.execute("SELECT COUNT(*) as n FROM events WHERE created_at >= ?", (now,)).fetchone()[0]
        print(f"  new events created: {events_new}")

        clusters_new = conn.execute("SELECT COUNT(*) as n FROM event_clusters WHERE created_at >= ?", (now,)).fetchone()[0]
        print(f"  new clusters created: {clusters_new}")

        # Safety checks
        auto_merged = conn.execute(
            "SELECT COUNT(*) as n FROM event_candidate_pairs WHERE run_id = ? AND status = 'auto_merge'",
            (run_id,),
        ).fetchone()[0]
        print(f"\n  [SAFETY] auto_merge count: {auto_merged}")

        # Check for any medium/uncertain auto-merge
        medium_auto = conn.execute(
            "SELECT COUNT(*) as n FROM event_candidate_pairs WHERE run_id = ? AND status = 'auto_merge' AND candidate_priority IN ('medium', 'low')",
            (run_id,),
        ).fetchone()[0]
        if medium_auto > 0:
            print(f"  [BLOCKER] medium/low auto_merge count: {medium_auto} !!!")
        else:
            print(f"  [SAFETY] medium/low auto_merge count: {medium_auto} OK")

        # Check for hard-negative auto-merge
        hard_neg_auto = conn.execute(
            "SELECT COUNT(*) as n FROM event_candidate_pairs WHERE run_id = ? AND status = 'auto_merge' AND disqualifiers_json != '[]' AND disqualifiers_json != '' AND disqualifiers_json IS NOT NULL",
            (run_id,),
        ).fetchone()[0]
        if hard_neg_auto > 0:
            print(f"  [BLOCKER] auto_merge with disqualifiers: {hard_neg_auto} !!!")
        else:
            print(f"  [SAFETY] auto_merge with disqualifiers: {hard_neg_auto} OK")

        # Check for non-event items with events
        non_event_events = conn.execute(
            """SELECT COUNT(*) as n FROM events e
               JOIN event_items ei ON e.event_id = ei.event_id
               JOIN semantic_extractions se ON ei.item_id = se.item_id
               WHERE e.created_at >= ? AND se.eventness_decision != 'event'""",
            (now,),
        ).fetchone()[0]
        if non_event_events > 0:
            print(f"  [BLOCKER] non-event items in events: {non_event_events} !!!")
        else:
            print(f"  [SAFETY] non-event items in events: {non_event_events} OK")

        # Sample auto-merge candidates
        auto_samples = conn.execute(
            """SELECT ecp.*, a.title as title_a, b.title as title_b
               FROM event_candidate_pairs ecp
               JOIN inbox_items a ON ecp.item_a_id = a.item_id
               JOIN inbox_items b ON ecp.item_b_id = b.item_id
               WHERE ecp.run_id = ? AND ecp.status = 'auto_merge'
               LIMIT 5""",
            (run_id,),
        ).fetchall()
        if auto_samples:
            print(f"\n  Auto-merge samples:")
            for s in auto_samples:
                print(f"    lane={s['lane']} priority={s['candidate_priority']}")
                print(f"      A: {s['title_a'][:100]}")
                print(f"      B: {s['title_b'][:100]}")

        # Show new events
        evt_samples = conn.execute(
            "SELECT event_id, event_title, event_type, status, confidence, importance FROM events WHERE created_at >= ? LIMIT 5",
            (now,),
        ).fetchall()
        if evt_samples:
            print(f"\n  New events:")
            for e in evt_samples:
                title = (e['event_title'] or '')[:100]
                print(f"    {e['event_id']} | {e['event_type']} | {e['status']} | conf={e['confidence']} | {title}")

    # Mark run as completed
    with store.connect() as conn:
        conn.execute(
            "UPDATE rss_ingest_runs SET status = 'success', finished_at = ?, updated_at = ? WHERE run_id = ?",
            (utc_now(), utc_now(), run_id),
        )
        conn.commit()

    print(f"\n=== DONE ===")
    print(f"Run ID: {run_id}")
    print(f"Snapshot: data/backups/content_inbox_20260601_before_operational_v3_recall.sqlite3")
    print(f"Rollback: cp data/backups/content_inbox_20260601_before_operational_v3_recall.sqlite3 data/content_inbox.sqlite3")

    # Write results to JSON for later reference
    output = {
        "run_id": run_id,
        "scoped_sources": scoped_sources,
        "item_count": len(item_ids),
        "pipeline_result": result,
        "snapshot": "data/backups/content_inbox_20260601_before_operational_v3_recall.sqlite3",
    }
    output_path = Path(__file__).resolve().parent.parent / "outputs" / f"checkpoint2_result_{run_id}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
