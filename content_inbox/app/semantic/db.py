from __future__ import annotations

import json
import sqlite3
from typing import Any

from app.storage import InboxStore, row_to_item
from app.utils import stable_hash, utc_now


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def input_fingerprint(value: Any) -> str:
    return stable_hash(dumps(value))


def rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def select_items_without_cards(store: InboxStore, limit: int, *, force: bool = False) -> list[dict[str, Any]]:
    with store.connect() as conn:
        if force:
            rows = conn.execute(
                "SELECT * FROM inbox_items ORDER BY created_at ASC LIMIT ?", (limit,)
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT i.*
                FROM inbox_items i
                LEFT JOIN item_cards c ON c.item_id = i.item_id AND c.is_current = 1
                WHERE c.id IS NULL
                ORDER BY i.created_at ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return [row_to_item(row) for row in rows]


def get_item(store: InboxStore, item_id: str) -> dict[str, Any] | None:
    with store.connect() as conn:
        row = conn.execute("SELECT * FROM inbox_items WHERE item_id = ?", (item_id,)).fetchone()
    return row_to_item(row) if row else None


def get_current_item_card(store: InboxStore, item_id: str) -> dict[str, Any] | None:
    with store.connect() as conn:
        row = conn.execute(
            "SELECT * FROM item_cards WHERE item_id = ? AND is_current = 1", (item_id,)
        ).fetchone()
    return dict(row) if row else None


def list_current_item_cards(store: InboxStore, *, exclude_item_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    params: list[Any] = []
    where = "WHERE is_current = 1"
    if exclude_item_id:
        where += " AND item_id != ?"
        params.append(exclude_item_id)
    params.append(limit)
    with store.connect() as conn:
        rows = conn.execute(
            f"SELECT * FROM item_cards {where} ORDER BY created_at DESC LIMIT ?", params
        ).fetchall()
    return rows_to_dicts(rows)


def upsert_item_card(
    store: InboxStore,
    card: dict[str, Any],
    *,
    schema_version: str,
    prompt_version: str | None,
    model: str | None,
    fingerprint: str,
    llm_call_id: int | None,
) -> dict[str, Any]:
    now = utc_now()
    with store.connect() as conn:
        conn.execute("UPDATE item_cards SET is_current = 0, updated_at = ? WHERE item_id = ?", (now, card["item_id"]))
        version_row = conn.execute(
            "SELECT COALESCE(MAX(card_version), 0) + 1 AS next_version FROM item_cards WHERE item_id = ?",
            (card["item_id"],),
        ).fetchone()
        version = int(version_row["next_version"])
        cur = conn.execute(
            """
            INSERT INTO item_cards (
                item_id, card_version, schema_version, prompt_version, model, input_fingerprint,
                canonical_title, language, short_summary, embedding_text, entities_json,
                event_hint, content_role, confidence, warnings_json, key_facts_json,
                key_opinions_json, cited_sources_json, source_material_candidates_json,
                quality_hints_json, llm_call_id, is_current, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (
                card["item_id"],
                version,
                schema_version,
                prompt_version,
                model,
                fingerprint,
                card["canonical_title"],
                card.get("language", "unknown"),
                card["short_summary"],
                card["embedding_text"],
                dumps(card.get("entities", [])),
                card.get("event_hint"),
                card.get("content_role", "unknown"),
                float(card.get("confidence", 0.0)),
                dumps(card.get("warnings", [])),
                dumps(card.get("key_facts", [])),
                dumps(card.get("key_opinions", [])),
                dumps(card.get("cited_sources", [])),
                dumps(card.get("source_material_candidates", [])),
                dumps(card.get("quality_hints", {})),
                llm_call_id,
                now,
                now,
            ),
        )
        conn.execute(
            """
            UPDATE inbox_items
            SET semantic_status = 'carded', semantic_error = NULL, last_semantic_at = ?, updated_at = ?
            WHERE item_id = ?
            """,
            (now, now, card["item_id"]),
        )
        row = conn.execute("SELECT * FROM item_cards WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


def insert_llm_call_log(
    store: InboxStore,
    *,
    task_type: str,
    model: str,
    prompt_version: str | None,
    schema_version: str | None,
    fingerprint: str,
    latency_ms: int | None,
    status: str,
    request: dict[str, Any] | None = None,
    raw_output: str | None = None,
    parsed_output: dict[str, Any] | None = None,
    usage: dict[str, Any] | None = None,
    error: str | None = None,
) -> int:
    usage = usage or {}
    prompt_tokens = usage.get("prompt_tokens")
    completion_tokens = usage.get("completion_tokens")
    total_tokens = usage.get("total_tokens")
    details = usage.get("prompt_tokens_details") or usage.get("completion_tokens_details") or {}
    cache_hit = usage.get("cache_hit_tokens") or details.get("cached_tokens")
    cache_miss = usage.get("cache_miss_tokens")
    now = utc_now()
    with store.connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO llm_call_logs (
                task_type, model, prompt_version, schema_version, input_fingerprint,
                latency_ms, status, prompt_tokens, completion_tokens, total_tokens,
                cache_hit_tokens, cache_miss_tokens, request_json, raw_output,
                parsed_output_json, error, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_type,
                model,
                prompt_version,
                schema_version,
                fingerprint,
                latency_ms,
                status,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                cache_hit,
                cache_miss,
                dumps(request or {}),
                raw_output,
                dumps(parsed_output) if parsed_output is not None else None,
                error,
                now,
                now,
            ),
        )
    return int(cur.lastrowid)


def list_llm_logs(store: InboxStore, limit: int = 20) -> list[dict[str, Any]]:
    with store.connect() as conn:
        rows = conn.execute(
            "SELECT * FROM llm_call_logs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return rows_to_dicts(rows)
