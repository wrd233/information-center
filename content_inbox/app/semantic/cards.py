from __future__ import annotations

import json
import re
from typing import Any

from app.semantic import db
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.schemas import ITEM_CARD_PROMPT_VERSION, SCHEMA_VERSION, ItemCardBatchOutput, ItemCardData
from app.storage import InboxStore
from app.utils import truncate, utc_now


def build_heuristic_card(item: dict[str, Any]) -> ItemCardData:
    title = item.get("title") or "Untitled"
    body = item.get("summary") or item.get("content_text") or title
    entities = []
    for token in re.findall(r"[A-Z][A-Za-z0-9_.-]{2,}|[\u4e00-\u9fff]{2,8}", f"{title} {body}")[:8]:
        if token not in entities:
            entities.append(token)
    role = "report"
    lowered = f"{title} {body}".lower()
    if any(word in lowered for word in ["release", "changelog", "paper", "公告", "发布"]):
        role = "source_material"
    elif any(word in lowered for word in ["review", "analysis", "分析", "解读"]):
        role = "analysis"
    elif any(word in lowered for word in ["hands-on", "体验", "实测"]):
        role = "firsthand"
    summary = truncate(" ".join(str(body).split()), 360) or title
    event_hint = truncate(title, 160)
    embedding_text = "\n".join([f"title: {title}", f"summary: {summary}", f"entities: {', '.join(entities)}"])
    return ItemCardData(
        item_id=item["item_id"],
        canonical_title=truncate(title, 180) or title,
        language=detect_language(title + " " + summary),
        short_summary=summary,
        embedding_text=embedding_text,
        entities=entities,
        event_hint=event_hint,
        content_role=role,  # type: ignore[arg-type]
        confidence=0.55,
        warnings=["heuristic_card"],
    )


def detect_language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    ascii_letters = len(re.findall(r"[A-Za-z]", text))
    if cjk > ascii_letters / 2:
        return "zh"
    if ascii_letters:
        return "en"
    return "unknown"


def item_payload(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "item_id": item["item_id"],
        "title": item.get("title"),
        "url": item.get("url"),
        "guid": item.get("guid"),
        "source_id": item.get("source_id"),
        "source_name": item.get("source_name"),
        "source_category": item.get("source_category"),
        "published_at": item.get("published_at"),
        "summary": truncate(item.get("summary"), 1000),
        "content_text": truncate(item.get("content_text"), 2000),
    }


def generate_item_cards(
    store: InboxStore,
    *,
    limit: int = 100,
    batch_size: int = 5,
    live: bool = False,
    dry_run: bool = False,
    force: bool = False,
    model: str | None = None,
    max_calls: int | None = None,
) -> dict[str, Any]:
    items = db.select_items_without_cards(store, limit, force=force)
    client = SemanticLLMClient(store, live=live, model=model, max_calls=max_calls, dry_run=dry_run)
    stats = {"selected": len(items), "written": 0, "llm_calls": 0, "skipped": 0, "errors": 0, "dry_run": dry_run}
    results: list[dict[str, Any]] = []
    for start in range(0, len(items), max(1, batch_size)):
        batch = items[start : start + max(1, batch_size)]
        input_data = {
            "task": "item_card_batch",
            "items": [item_payload(item) for item in batch],
        }
        output, call_id, reason = client.call_json(
            task_type="item_card",
            prompt_version=ITEM_CARD_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=ItemCardBatchOutput,
            max_tokens=1800,
        )
        stats["llm_calls"] = client.calls
        cards_by_id: dict[str, ItemCardData] = {}
        if output:
            cards_by_id = {card.item_id: card for card in output.item_cards}
        for item in batch:
            card = cards_by_id.get(item["item_id"]) or build_heuristic_card(item)
            fingerprint = db.input_fingerprint({"item": item_payload(item), "prompt": ITEM_CARD_PROMPT_VERSION})
            if dry_run:
                stats["skipped"] += 1
                results.append(card.model_dump())
                continue
            try:
                row = db.upsert_item_card(
                    store,
                    card.model_dump(),
                    schema_version=SCHEMA_VERSION,
                    prompt_version=ITEM_CARD_PROMPT_VERSION if output else None,
                    model=client.model if output else "heuristic",
                    fingerprint=fingerprint,
                    llm_call_id=call_id if output else None,
                )
                stats["written"] += 1
                results.append({"id": row["id"], "item_id": item["item_id"], "source": "llm" if output else "heuristic", "reason": reason})
            except Exception as exc:
                mark_item_semantic_error(store, item["item_id"], str(exc))
                stats["errors"] += 1
    return {"ok": stats["errors"] == 0, "stats": stats, "items": results}


def mark_item_semantic_error(store: InboxStore, item_id: str, error: str) -> None:
    now = utc_now()
    with store.connect() as conn:
        conn.execute(
            """
            UPDATE inbox_items
            SET semantic_status = 'failed', semantic_error = ?, semantic_attempts = semantic_attempts + 1,
                last_semantic_at = ?, updated_at = ?
            WHERE item_id = ?
            """,
            (error[:1000], now, now, item_id),
        )
