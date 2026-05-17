from __future__ import annotations

import json
import re
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.semantic import db
from app.semantic.card_policy import card_limits, choose_card_tier as policy_choose_card_tier, fallback_classification
from app.semantic.llm_client import SemanticLLMClient
from app.semantic.schemas import ITEM_CARD_PROMPT_VERSION, SCHEMA_VERSION, ItemCardBatchOutput, ItemCardData
from app.storage import InboxStore
from app.utils import truncate, utc_now


AI_ENTITY_RE = re.compile(
    r"\b(?:OpenAI|ChatGPT|Codex|GPT[-\w.]*|o[134](?:-mini)?|Anthropic|Claude|Google|Gemini|DeepMind|xAI|Grok|DeepSeek|Qwen|Alibaba|Cursor|Windsurf|Cognition|Devin|LangChain|LlamaIndex|Perplexity|Hugging Face|NVIDIA|v\d+(?:\.\d+)?|V\d+(?:\.\d+)?|R1)\b",
    re.IGNORECASE,
)


def build_heuristic_card(item: dict[str, Any], *, tier: str = "heuristic", fallback_reason: str | None = None) -> ItemCardData:
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
    if tier in {"minimal", "deterministic_minimal"}:
        fallback_type = "fallback_deterministic_minimal"
        warnings = ["deterministic_minimal_card"]
        tier = "minimal"
    else:
        fallback_type = fallback_classification(source="heuristic", reason=fallback_reason)
        warnings = ["heuristic_card", fallback_type]
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
        quality_hints={"card_tier": tier, "fallback_type": fallback_type, "fallback_reason": fallback_reason or ""},
    )


def choose_card_tier(item: dict[str, Any]) -> str:
    tier = policy_choose_card_tier(item)
    if tier == "minimal":
        return "minimal"
    title = item.get("title") or ""
    summary = item.get("summary") or ""
    content = item.get("content_text") or ""
    text = f"{title}\n{summary}\n{content}".strip()
    has_ai_entity = bool(AI_ENTITY_RE.search(text))
    official_hint = any(word in text.lower() for word in ["release", "launch", "announc", "paper", "benchmark", "open-source", "api", "model"])
    if has_ai_entity and official_hint:
        return "full"
    return tier


def detect_language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    ascii_letters = len(re.findall(r"[A-Za-z]", text))
    if cjk > ascii_letters / 2:
        return "zh"
    if ascii_letters:
        return "en"
    return "unknown"


def is_transient_or_parse_failure(reason: str | None) -> bool:
    text = (reason or "").lower()
    if not text:
        return True
    return any(token in text for token in ["json", "validation", "timeout", "timed out", "request failed", "temporarily", "rate", "429"])


def item_payload(item: dict[str, Any]) -> dict[str, Any]:
    tier = choose_card_tier(item)
    summary_limit, content_limit = card_limits(tier)
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
        "deterministic_minimal_cards": 0,
        "heuristic_fallback_count": 0,
        "parse_error_fallback_count": 0,
        "budget_skip_fallback_count": 0,
        "failed_batch_count": 0,
        "split_retry_success_count": 0,
        "single_retry_success_count": 0,
    }
    results: list[dict[str, Any]] = []
    local_items = [item for item in items if choose_card_tier(item) == "minimal"]
    llm_items = [item for item in items if choose_card_tier(item) != "minimal"]
    batches = [llm_items[start : start + max(1, batch_size)] for start in range(0, len(llm_items), max(1, batch_size))]

    def write_local_minimal(item: dict[str, Any]) -> dict[str, Any]:
        card = build_heuristic_card(item, tier="deterministic_minimal", fallback_reason="local deterministic minimal card")
        fingerprint = db.input_fingerprint({"item": item_payload(item), "prompt": "item_card_minimal_rule"})
        call_id = None
        if not live:
            call_id = db.insert_llm_call_log(
                store,
                task_type="item_card",
                model="deterministic_minimal",
                prompt_version="item_card_deterministic_minimal_rule",
                schema_version=SCHEMA_VERSION,
                fingerprint=fingerprint,
                latency_ms=0,
                status="skipped",
                request={"reason": "local deterministic minimal card", "fallback_type": "fallback_deterministic_minimal"},
                error="local deterministic minimal card",
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
                prompt_version="item_card_deterministic_minimal_rule",
                model="deterministic_minimal",
                fingerprint=fingerprint,
                llm_call_id=call_id,
            )
            return {"skipped": 0, "written": 1, "errors": 0, "item": {"id": row["id"], "item_id": item["item_id"], "source": "deterministic_minimal", "reason": "local deterministic minimal card"}}
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
        batch_id = f"card_batch_{uuid.uuid4().hex[:12]}"
        call_results: list[tuple[ItemCardBatchOutput | None, int | None, str, list[dict[str, Any]], str, int]] = []

        def call_cards(items_for_call: list[dict[str, Any]], retry_strategy: str, attempt: int) -> tuple[ItemCardBatchOutput | None, int | None, str]:
            input_data = {
                "task": "item_card_batch",
                "tier_policy": "minimal cards are generated locally; this batch contains standard/full cards only",
                "items": [item_payload(item) for item in items_for_call],
            }
            return client.call_json(
                task_type="item_card",
                prompt_version=ITEM_CARD_PROMPT_VERSION,
                schema_version=SCHEMA_VERSION,
                input_data=input_data,
                output_model=ItemCardBatchOutput,
                max_tokens=4000 if len(items_for_call) > 1 else 1800,
                item_id=",".join(item["item_id"] for item in items_for_call),
                source_id=",".join(str(item.get("source_id") or item.get("feed_url") or item.get("source_name") or "") for item in items_for_call),
                request_metadata={
                    "batch_id": batch_id,
                    "batch_size": len(items_for_call),
                    "attempt_number": attempt,
                    "retry_attempt": attempt - 1,
                    "retry_strategy": retry_strategy,
                    "affected_item_count": len(items_for_call),
                    "prompt_variant": "retry" if attempt > 1 or retry_strategy != "initial_batch" else "full",
                    "card_tier": "mixed_llm",
                },
            )

        output, call_id, reason = call_cards(batch, "initial_batch", 1)
        call_results.append((output, call_id, reason, batch, "initial_batch", 1))
        if not output and len(batch) > 1 and is_transient_or_parse_failure(reason):
            midpoint = max(1, len(batch) // 2)
            merged_cards: dict[str, ItemCardData] = {}
            merged_call_id = call_id
            merged_reason = reason
            split_success = False
            for half_index, half in enumerate([batch[:midpoint], batch[midpoint:]], start=1):
                if not half:
                    continue
                half_output, half_call_id, half_reason = call_cards(half, f"split_half_{half_index}", 3)
                call_results.append((half_output, half_call_id, half_reason, half, f"split_half_{half_index}", 3))
                merged_call_id = half_call_id
                merged_reason = half_reason
                if half_output:
                    split_success = True
                    merged_cards.update({card.item_id: card for card in half_output.item_cards})
            if split_success:
                output = ItemCardBatchOutput(item_cards=list(merged_cards.values()))
                call_id = merged_call_id
                reason = merged_reason
        cards_by_id: dict[str, ItemCardData] = {}
        final_call_id_by_item: dict[str, int | None] = {}
        final_reason_by_item: dict[str, str] = {}
        if output:
            cards_by_id = {card.item_id: card for card in output.item_cards}
            for item in batch:
                final_call_id_by_item[item["item_id"]] = call_id
                final_reason_by_item[item["item_id"]] = reason
            if any(result[4].startswith("split_half") and result[0] for result in call_results):
                local["split_retry_success_count"] = 1
        if not output:
            local["failed_batch_count"] = 1
        missing_items = [item for item in batch if item["item_id"] not in cards_by_id]
        if missing_items:
            for item in missing_items:
                single_output, single_call_id, single_reason = call_cards([item], "split_single", 4)
                call_results.append((single_output, single_call_id, single_reason, [item], "split_single", 4))
                if single_output:
                    cards_by_id.update({card.item_id: card for card in single_output.item_cards})
                    local["single_retry_success_count"] = int(local.get("single_retry_success_count", 0)) + 1
                final_call_id_by_item[item["item_id"]] = single_call_id
                final_reason_by_item[item["item_id"]] = single_reason
        local["llm_calls"] = client.calls
        for item in batch:
            fallback_reason = final_reason_by_item.get(item["item_id"])
            card = cards_by_id.get(item["item_id"]) or build_heuristic_card(item, fallback_reason=fallback_reason)
            fingerprint = db.input_fingerprint({"item": item_payload(item), "prompt": ITEM_CARD_PROMPT_VERSION})
            if dry_run:
                local["skipped"] += 1
                local["items"].append(card.model_dump())
                continue
            try:
                card_data = card.model_dump()
                card_data.setdefault("quality_hints", {})
                card_data["quality_hints"]["card_tier"] = choose_card_tier(item)
                if item["item_id"] not in cards_by_id:
                    fallback_type = fallback_classification(source="heuristic", reason=fallback_reason)
                    card_data["quality_hints"]["fallback_type"] = fallback_type
                    if fallback_type == "fallback_due_to_llm_parse_error":
                        local["parse_error_fallback_count"] = int(local.get("parse_error_fallback_count", 0)) + 1
                    elif fallback_type == "fallback_due_to_budget_skip":
                        local["budget_skip_fallback_count"] = int(local.get("budget_skip_fallback_count", 0)) + 1
                    else:
                        local["heuristic_fallback_count"] = int(local.get("heuristic_fallback_count", 0)) + 1
                row = db.upsert_item_card(
                    store,
                    card_data,
                    schema_version=SCHEMA_VERSION,
                    prompt_version=ITEM_CARD_PROMPT_VERSION if item["item_id"] in cards_by_id else None,
                    model=client.model if item["item_id"] in cards_by_id else "heuristic",
                    fingerprint=fingerprint,
                    llm_call_id=final_call_id_by_item.get(item["item_id"]) if item["item_id"] in cards_by_id else None,
                )
                local["written"] += 1
                local["items"].append({"id": row["id"], "item_id": item["item_id"], "source": "llm" if item["item_id"] in cards_by_id else "heuristic", "reason": final_reason_by_item.get(item["item_id"])})
            except Exception as exc:
                mark_item_semantic_error(store, item["item_id"], str(exc))
                local["errors"] += 1
        return local

    for item in local_items:
        local = write_local_minimal(item)
        stats["local_minimal_cards"] += 1
        stats["deterministic_minimal_cards"] += 1
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
                for key in ["failed_batch_count", "split_retry_success_count", "single_retry_success_count", "heuristic_fallback_count", "parse_error_fallback_count", "budget_skip_fallback_count"]:
                    stats[key] += int(local.get(key, 0))
                results.extend(local["items"])
    else:
        for batch in batches:
            local = process_batch(batch)
            for key in ["written", "llm_calls", "skipped", "errors"]:
                stats[key] += int(local[key])
            for key in ["failed_batch_count", "split_retry_success_count", "single_retry_success_count", "heuristic_fallback_count", "parse_error_fallback_count", "budget_skip_fallback_count"]:
                stats[key] += int(local.get(key, 0))
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
