from __future__ import annotations

import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.semantic import db
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.schemas import ITEM_CARD_PROMPT_VERSION, SCHEMA_VERSION, ItemCardBatchOutput, ItemCardData
from app.storage import InboxStore
from app.utils import truncate, utc_now


AI_ENTITY_RE = re.compile(
    r"\b(?:OpenAI|ChatGPT|Codex|GPT[-\w.]*|o[134](?:-mini)?|Anthropic|Claude|Google|Gemini|DeepMind|xAI|Grok|DeepSeek|Qwen|Alibaba|Cursor|Windsurf|Cognition|Devin|LangChain|LlamaIndex|Perplexity|Hugging Face|NVIDIA|v\d+(?:\.\d+)?|V\d+(?:\.\d+)?|R1)\b",
    re.IGNORECASE,
)


def build_heuristic_card(item: dict[str, Any], *, tier: str = "heuristic") -> ItemCardData:
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
    warnings = ["heuristic_card"] if tier == "heuristic" else ["minimal_card"]
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
        warnings=warnings,
        quality_hints={"card_tier": tier},
    )


def choose_card_tier(item: dict[str, Any]) -> str:
    title = item.get("title") or ""
    summary = item.get("summary") or ""
    content = item.get("content_text") or ""
    text = f"{title}\n{summary}\n{content}".strip()
    length = len(text)
    source = f"{item.get('source_name') or ''} {item.get('source_id') or ''}".lower()
    is_social = "socialmedia" in source or "(@" in (item.get("source_name") or "")
    has_ai_entity = bool(AI_ENTITY_RE.search(text))
    official_hint = any(word in text.lower() for word in ["release", "launch", "announc", "paper", "benchmark", "open-source", "api", "model"])
    if length <= 260 and (is_social or not content):
        return "minimal"
    if length <= 700 and is_social and not (has_ai_entity and official_hint):
        return "minimal"
    if length >= 1800 or (has_ai_entity and official_hint):
        return "full"
    return "standard"


def detect_language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    ascii_letters = len(re.findall(r"[A-Za-z]", text))
    if cjk > ascii_letters / 2:
        return "zh"
    if ascii_letters:
        return "en"
    return "unknown"


def item_payload(item: dict[str, Any]) -> dict[str, Any]:
    tier = choose_card_tier(item)
    summary_limit = 420 if tier == "minimal" else 900 if tier == "standard" else 1400
    content_limit = 0 if tier == "minimal" else 900 if tier == "standard" else 2200
    return {
        "item_id": item["item_id"],
        "card_tier": tier,
        "title": item.get("title"),
        "url": item.get("url"),
        "guid": item.get("guid"),
        "source_id": item.get("source_id"),
        "source_name": item.get("source_name"),
        "source_category": item.get("source_category"),
        "published_at": item.get("published_at"),
        "summary": truncate(item.get("summary"), summary_limit),
        "content_text": truncate(item.get("content_text"), content_limit) if content_limit else None,
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
    token_budget: int | None = None,
    global_call_limit: bool = False,
    concurrency: int = 1,
) -> dict[str, Any]:
    items = db.select_items_without_cards(store, limit, force=force)
    tier_counts = Counter(choose_card_tier(item) for item in items)
    stats = {
        "selected": len(items),
        "written": 0,
        "llm_calls": 0,
        "skipped": 0,
        "errors": 0,
        "dry_run": dry_run,
        "card_tiers": dict(tier_counts),
        "local_minimal_cards": 0,
    }
    results: list[dict[str, Any]] = []
    local_items = [item for item in items if choose_card_tier(item) == "minimal"]
    llm_items = [item for item in items if choose_card_tier(item) != "minimal"]
    batches = [llm_items[start : start + max(1, batch_size)] for start in range(0, len(llm_items), max(1, batch_size))]

    def write_local_minimal(item: dict[str, Any]) -> dict[str, Any]:
        card = build_heuristic_card(item, tier="minimal")
        fingerprint = db.input_fingerprint({"item": item_payload(item), "prompt": "item_card_minimal_rule"})
        call_id = None
        if not live:
            call_id = db.insert_llm_call_log(
                store,
                task_type="item_card",
                model="minimal_rule",
                prompt_version="item_card_minimal_rule",
                schema_version=SCHEMA_VERSION,
                fingerprint=fingerprint,
                latency_ms=0,
                status="skipped",
                request={"reason": "local minimal card"},
                error="local minimal card",
                item_id=item["item_id"],
                source_id=item.get("source_id") or item.get("feed_url") or item.get("source_name"),
            )
        if dry_run:
            return {"skipped": 1, "written": 0, "errors": 0, "item": card.model_dump()}
        try:
            row = db.upsert_item_card(
                store,
                card.model_dump(),
                schema_version=SCHEMA_VERSION,
                prompt_version="item_card_minimal_rule",
                model="minimal_rule",
                fingerprint=fingerprint,
                llm_call_id=call_id,
            )
            return {"skipped": 0, "written": 1, "errors": 0, "item": {"id": row["id"], "item_id": item["item_id"], "source": "minimal_rule", "reason": "local minimal card"}}
        except Exception as exc:
            mark_item_semantic_error(store, item["item_id"], str(exc))
            return {"skipped": 0, "written": 0, "errors": 1, "item": {"item_id": item["item_id"], "error": str(exc)}}

    def process_batch(batch: list[dict[str, Any]]) -> dict[str, Any]:
        client = SemanticLLMClient(
            store,
            live=live,
            model=model,
            max_calls=max_calls,
            dry_run=dry_run,
            token_budget=token_budget,
            global_call_limit=global_call_limit,
        )
        local = {"written": 0, "llm_calls": 0, "skipped": 0, "errors": 0, "items": []}
        input_data = {
            "task": "item_card_batch",
            "tier_policy": "minimal cards are generated locally; this batch contains standard/full cards only",
            "items": [item_payload(item) for item in batch],
        }
        output, call_id, reason = client.call_json(
            task_type="item_card",
            prompt_version=ITEM_CARD_PROMPT_VERSION,
            schema_version=SCHEMA_VERSION,
            input_data=input_data,
            output_model=ItemCardBatchOutput,
            max_tokens=4000,
            item_id=",".join(item["item_id"] for item in batch),
            source_id=",".join(str(item.get("source_id") or item.get("feed_url") or item.get("source_name") or "") for item in batch),
        )
        local["llm_calls"] = client.calls
        cards_by_id: dict[str, ItemCardData] = {}
        if output:
            cards_by_id = {card.item_id: card for card in output.item_cards}
        for item in batch:
            card = cards_by_id.get(item["item_id"]) or build_heuristic_card(item)
            fingerprint = db.input_fingerprint({"item": item_payload(item), "prompt": ITEM_CARD_PROMPT_VERSION})
            if dry_run:
                local["skipped"] += 1
                local["items"].append(card.model_dump())
                continue
            try:
                card_data = card.model_dump()
                card_data.setdefault("quality_hints", {})
                card_data["quality_hints"]["card_tier"] = choose_card_tier(item)
                row = db.upsert_item_card(
                    store,
                    card_data,
                    schema_version=SCHEMA_VERSION,
                    prompt_version=ITEM_CARD_PROMPT_VERSION if output else None,
                    model=client.model if output else "heuristic",
                    fingerprint=fingerprint,
                    llm_call_id=call_id if output else None,
                )
                local["written"] += 1
                local["items"].append({"id": row["id"], "item_id": item["item_id"], "source": "llm" if output else "heuristic", "reason": reason})
            except Exception as exc:
                mark_item_semantic_error(store, item["item_id"], str(exc))
                local["errors"] += 1
        return local

    for item in local_items:
        local = write_local_minimal(item)
        stats["local_minimal_cards"] += 1
        stats["written"] += int(local["written"])
        stats["skipped"] += int(local["skipped"])
        stats["errors"] += int(local["errors"])
        results.append(local["item"])

    if concurrency > 1 and len(batches) > 1:
        with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
            futures = [executor.submit(process_batch, batch) for batch in batches]
            for future in as_completed(futures):
                local = future.result()
                for key in ["written", "llm_calls", "skipped", "errors"]:
                    stats[key] += int(local[key])
                results.extend(local["items"])
    else:
        for batch in batches:
            local = process_batch(batch)
            for key in ["written", "llm_calls", "skipped", "errors"]:
                stats[key] += int(local[key])
            results.extend(local["items"])
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
