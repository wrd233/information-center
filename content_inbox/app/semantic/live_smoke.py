from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from app.models import NormalizedContent, ScreeningResult
from app.semantic.cards import generate_item_cards
from app.semantic.clusters import patch_cluster_card, process_item_clusters
from app.semantic.relations import process_item_relations
from app.storage import InboxStore


def live_enabled() -> tuple[bool, str]:
    if os.getenv("CONTENT_INBOX_LLM_ENABLE_LIVE") != "1":
        return False, "CONTENT_INBOX_LLM_ENABLE_LIVE is not 1"
    if not (os.getenv("DEEPSEEK_API_KEY") or os.getenv("CONTENT_INBOX_DEEPSEEK_API_KEY")):
        return False, "DeepSeek API key is not configured"
    return True, "enabled"


def make_smoke_store(db_path: str | None, write_real_db: bool) -> tuple[InboxStore, str, bool]:
    if db_path and write_real_db:
        return InboxStore(Path(db_path)), db_path, False
    tmp = tempfile.NamedTemporaryFile(prefix="content_inbox_semantic_smoke_", suffix=".sqlite3", delete=False)
    tmp.close()
    return InboxStore(Path(tmp.name)), tmp.name, True


def seed_items(store: InboxStore, limit: int) -> list[str]:
    ids = []
    samples = [
        {
            "title": "OpenAI releases GPT-5.5 for developers",
            "summary": "OpenAI announced GPT-5.5 with stronger coding and agent capabilities.",
            "url": "https://example.com/openai-gpt-55",
            "source_name": "Example Tech",
            "source_id": "example-tech",
        },
        {
            "title": "Developers test GPT-5.5 coding improvements",
            "summary": "Hands-on reports compare GPT-5.5 with prior models on coding workflows.",
            "url": "https://example.com/gpt-55-hands-on",
            "source_name": "Example Lab",
            "source_id": "example-lab",
        },
        {
            "title": "OpenAI GPT-5.5 API outage reported by users",
            "summary": "Several developers report elevated errors when using the GPT-5.5 API.",
            "url": "https://example.com/gpt-55-outage",
            "source_name": "Example Ops",
            "source_id": "example-ops",
        },
    ][: max(1, limit)]
    screening = ScreeningResult(
        summary="seed semantic smoke item",
        category="AI前沿",
        value_score=4,
        personal_relevance=4,
        suggested_action="read",
        reason="smoke fixture",
        screening_method="none",
    )
    for idx, sample in enumerate(samples):
        normalized = NormalizedContent(
            title=sample["title"],
            url=sample["url"],
            source_id=sample["source_id"],
            source_name=sample["source_name"],
            content_type="article",
            summary=sample["summary"],
        )
        row = store.insert(f"semantic-smoke-{idx}", normalized, screening, raw=sample)
        ids.append(row["item_id"])
    return ids


def run_live_smoke(
    target: str,
    *,
    limit: int = 3,
    max_calls: int = 10,
    db_path: str | None = None,
    write_real_db: bool = False,
) -> dict[str, Any]:
    enabled, reason = live_enabled()
    if not enabled:
        return {"ok": True, "skipped": True, "reason": reason}
    store, actual_db_path, temporary_db = make_smoke_store(db_path, write_real_db)
    seed_items(store, limit)
    summary: dict[str, Any] = {
        "ok": True,
        "skipped": False,
        "db_path": actual_db_path,
        "temporary_db": temporary_db,
        "write_real_db": bool(db_path and write_real_db),
        "steps": {},
    }
    if target in {"item-card", "all"}:
        summary["steps"]["item-card"] = generate_item_cards(store, limit=limit, batch_size=limit, live=True, max_calls=max_calls)
    if target in {"item-relation", "all"}:
        generate_item_cards(store, limit=limit, batch_size=limit, live=True, max_calls=max_calls)
        summary["steps"]["item-relation"] = process_item_relations(store, limit=limit, live=True, max_calls=max_calls)
    if target in {"item-cluster", "all"}:
        generate_item_cards(store, limit=limit, batch_size=limit, live=True, max_calls=max_calls)
        summary["steps"]["item-cluster"] = process_item_clusters(store, limit=limit, live=True, max_calls=max_calls)
    if target in {"cluster-card", "all"}:
        generate_item_cards(store, limit=limit, batch_size=limit, live=True, max_calls=max_calls)
        process_item_clusters(store, limit=limit, live=True, max_calls=max_calls)
        clusters = summary_clusters(store)
        if clusters:
            summary["steps"]["cluster-card"] = patch_cluster_card(store, clusters[0]["cluster_id"], live=True, max_calls=max_calls)
        else:
            summary["steps"]["cluster-card"] = {"ok": False, "error": "no_cluster"}
    if target in {"source-review", "all"}:
        from app.semantic.source_profiles import recompute_source_profiles

        summary["steps"]["source-review"] = recompute_source_profiles(store)
    summary["llm_calls"] = sanitized_llm_summary(store)
    return summary


def summary_clusters(store: InboxStore) -> list[dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute("SELECT cluster_id FROM event_clusters ORDER BY created_at ASC LIMIT 5").fetchall()
    return [dict(row) for row in rows]


def sanitized_llm_summary(store: InboxStore) -> dict[str, Any]:
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT task_type, model, status, COUNT(*) AS calls,
                   COALESCE(SUM(total_tokens), 0) AS total_tokens,
                   COALESCE(SUM(cache_hit_tokens), 0) AS cache_hit_tokens,
                   COALESCE(SUM(cache_miss_tokens), 0) AS cache_miss_tokens
            FROM llm_call_logs
            GROUP BY task_type, model, status
            ORDER BY task_type, model, status
            """
        ).fetchall()
    return {"groups": [dict(row) for row in rows]}
