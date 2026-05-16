from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.storage import InboxStore
from app.utils import normalize_url


def backfill_items(store: InboxStore, *, apply: bool = False) -> dict[str, Any]:
    with store.connect() as conn:
        item_rows = conn.execute(
            "SELECT item_id, source_id, feed_url, source_name, source_category, raw_json FROM inbox_items"
        ).fetchall()
        source_rows = conn.execute("SELECT * FROM rss_sources WHERE deleted_at IS NULL").fetchall()

    by_feed: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_name_cat: dict[tuple[str, str | None], list[dict[str, Any]]] = defaultdict(list)
    for source in source_rows:
        source_dict = {
            "source_id": source["source_id"],
            "normalized_feed_url": source["normalized_feed_url"],
            "source_name": source["source_name"],
            "source_category": source["source_category"],
            "feed_url": source["feed_url"],
        }
        by_feed[source["normalized_feed_url"]].append(source_dict)
        by_name_cat[(source["source_name"], source["source_category"])].append(source_dict)

    stats = {"scanned": 0, "matched": 0, "updated": 0, "ambiguous": 0, "unmatched": 0}
    updates: list[tuple[str, str, str]] = []
    for item in item_rows:
        stats["scanned"] += 1
        if item["source_id"]:
            continue
        candidates: list[dict[str, Any]] = []
        if item["feed_url"]:
            candidates = by_feed.get(normalize_url(item["feed_url"]) or item["feed_url"], [])
        if not candidates:
            candidates = by_name_cat.get((item["source_name"], item["source_category"]), [])
        if len(candidates) == 1:
            stats["matched"] += 1
            updates.append((candidates[0]["source_id"], candidates[0]["normalized_feed_url"], item["item_id"]))
        elif len(candidates) > 1:
            stats["ambiguous"] += 1
        else:
            stats["unmatched"] += 1

    if apply and updates:
        with store.connect() as conn:
            conn.executemany(
                "UPDATE inbox_items SET source_id = ?, feed_url = ? WHERE item_id = ?",
                updates,
            )
        stats["updated"] = len(updates)
    return {"ok": True, "stats": stats, "apply": apply}
