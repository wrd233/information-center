from __future__ import annotations

import copy
import json
import math
import os
import re
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import settings
from app.models import NormalizedContent, ScreeningResult
from app.profiler import profiler
from app.utils import truncate


# ---------------------------------------------------------------------------
# LLM concurrency control
# ---------------------------------------------------------------------------

_LLM_SEMAPHORE: threading.Semaphore | None = None


def _get_llm_semaphore() -> threading.Semaphore:
    global _LLM_SEMAPHORE
    if _LLM_SEMAPHORE is None:
        max_concurrency = int(settings.llm.get("max_concurrency", 2))
        _LLM_SEMAPHORE = threading.Semaphore(max_concurrency)
    return _LLM_SEMAPHORE


# ---------------------------------------------------------------------------
# Thread-local state for full LLM request body dumping
# ---------------------------------------------------------------------------

_dump = threading.local()

_SENSITIVE_RE = re.compile(
    r"(?:sk-[A-Za-z0-9]{32,})"
    r"|(?:Bearer\s+[A-Za-z0-9_\-\.]+=*)"
    r"|(?:api_key[=:]\s*[\"']?[A-Za-z0-9_\-]{16,})"
    r"|(?:secret[=:]\s*[\"']?[A-Za-z0-9_\-]{16,})",
)


def _init_dump():
    if not hasattr(_dump, "initialized"):
        _dump.enabled = False
        _dump.output_dir = ""
        _dump.counter = 0
        _dump.item_context: dict[str, str] = {}
        _dump.prompt_context: dict[str, str] = {}
        _dump.initialized = True


def configure_llm_dump(enabled: bool, output_dir: str = ""):
    """Enable/disable full LLM request body dumping. Called from server.py."""
    _init_dump()
    _dump.enabled = enabled
    _dump.output_dir = output_dir
    _dump.counter = 0


def set_dump_item_context(
    source_name: str = "",
    source_url: str = "",
    item_title: str = "",
    item_url: str = "",
):
    """Set per-item metadata for dump filenames. Called from ai_screen/ai_screen_merged."""
    _init_dump()
    _dump.item_context = {
        "source_name": source_name or "",
        "source_url": source_url or "",
        "item_title": item_title or "",
        "item_url": item_url or "",
    }


def _set_dump_prompt_context(prompt_name: str, stage: str):
    """Set per-call prompt context. Called before each call_prompt_json."""
    _init_dump()
    _dump.prompt_context = {"prompt_name": prompt_name, "stage": stage}


# Whitelist of basic_screening fields allowed into need_matching prompt.
# Excludes _raw_response, _ prefixed internals, and raw API fields (choices, usage, etc.)
_SCREENING_WHITELIST = frozenset({
    "summary", "title_cn", "category",
    "value_score", "personal_relevance", "novelty_score",
    "source_quality", "actionability",
    "hidden_signals", "entities", "event_hint",
    "suggested_action", "followup_type", "suggested_next_step",
    "reason", "tags", "confidence", "evidence_level",
    "needs_more_context",
})


def _sanitize_screening_for_matching(data: dict[str, Any]) -> dict[str, Any]:
    """Keep only whitelisted business fields for need_matching input."""
    return {k: v for k, v in data.items() if k in _SCREENING_WHITELIST}


def screen_content(content: NormalizedContent, use_ai: bool) -> ScreeningResult:
    if not use_ai:
        return unscreened_result(content)
    if not settings.ai_enabled or not settings.screening.get("enabled", True):
        return failed_screening(content, "AI screening is disabled")
    if not settings.llm_api_key():
        return failed_screening(
            content,
            "screen=true requires CONTENT_INBOX_DEEPSEEK_API_KEY or configured llm.api_key_env",
        )
    try:
        mode = settings.screening.get("mode", "two_stage")
        if mode == "merged":
            return apply_score_policy(ai_screen_merged(content), content)
        return apply_score_policy(ai_screen(content), content)
    except Exception as exc:
        return failed_screening(content, str(exc))


def _normalize_action_fields(data: dict[str, Any]) -> dict[str, Any]:
    """Fix known model mistake: fetch_fulltext misplaced into suggested_action."""
    if data.get("suggested_action") == "fetch_fulltext":
        data = dict(data)
        data["suggested_action"] = "review"
        if not data.get("followup_type") or data.get("followup_type") == "none":
            data["followup_type"] = "fetch_fulltext"
        if not data.get("suggested_next_step") or data.get("suggested_next_step") == "none":
            data["suggested_next_step"] = "fetch_fulltext"
    return data


def ai_screen(content: NormalizedContent) -> ScreeningResult:
    set_dump_item_context(
        source_name=content.source_name or "",
        source_url=content.url or "",
        item_title=content.title or "",
        item_url=content.url or "",
    )
    content_payload = content.model_dump()
    content_payload["content_text"] = truncate(
        content_payload.get("content_text"),
        int(settings.screening.get("max_input_chars", 4000)),
    )

    t0 = time.monotonic()
    basic_contract = prompt_output_contract("basic_screening")
    basic_input = {
        "content": content_payload,
        "categories": settings.screening.get("categories", []),
    }
    _set_dump_prompt_context("basic_screening", "two_stage_stage1")
    basic_data = call_prompt_json(
        "basic_screening",
        basic_input=basic_input,
        output_contract=basic_contract,
        temperature=settings.llm.get("temperature", 0.2),
        max_tokens=settings.llm.get("max_tokens", 1200),
    )
    profiler.record("llm_basic_screening_seconds", time.monotonic() - t0)

    basic_raw = basic_data.pop("_raw_response", None)
    t1 = time.monotonic()
    matching_input = {
        "content": content_payload,
        "basic_screening": _sanitize_screening_for_matching(basic_data),
        "reading_needs": settings.reading_needs,
        "watch_topics": settings.watch_topics,
    }
    _set_dump_prompt_context("need_matching", "two_stage_stage2")
    matching_data = call_prompt_json(
        "need_matching",
        basic_input=matching_input,
        output_contract=prompt_output_contract("need_matching"),
        temperature=settings.llm.get("temperature", 0.2),
        max_tokens=settings.llm.get("max_tokens", 1200),
    )
    profiler.record("llm_need_matching_seconds", time.monotonic() - t1)

    matching_raw = matching_data.pop("_raw_response", None)
    merged = dict(basic_data)
    merged["need_matches"] = matching_data.get("need_matches", [])
    merged["topic_matches"] = matching_data.get("topic_matches", [])
    merged["screening_method"] = "ai"
    merged["screening_status"] = "ok"
    merged["prompt_version"] = settings.prompt_version
    merged["model"] = settings.llm.get("model")
    merged["raw_model_response"] = {
        "basic_screening": basic_raw,
        "need_matching": matching_raw,
    }
    merged = _normalize_action_fields(merged)
    return ScreeningResult.model_validate(merged)


def ai_screen_merged(content: NormalizedContent) -> ScreeningResult:
    set_dump_item_context(
        source_name=content.source_name or "",
        source_url=content.url or "",
        item_title=content.title or "",
        item_url=content.url or "",
    )
    content_payload = content.model_dump()
    content_payload["content_text"] = truncate(
        content_payload.get("content_text"),
        int(settings.screening.get("max_input_chars", 4000)),
    )

    t0 = time.monotonic()
    merged_input = {
        "content": content_payload,
        "categories": settings.screening.get("categories", []),
        "reading_needs": settings.reading_needs,
        "watch_topics": settings.watch_topics,
    }
    _set_dump_prompt_context("screen_and_match", "merged")
    merged_data = call_prompt_json(
        "screen_and_match",
        basic_input=merged_input,
        output_contract=prompt_output_contract("screen_and_match"),
        temperature=settings.llm.get("temperature", 0.2),
        max_tokens=int(settings.screening.get("merged_max_tokens", 3000)),
    )
    profiler.record("llm_basic_screening_seconds", time.monotonic() - t0)
    profiler.record("llm_need_matching_seconds", 0.0)

    raw_response = merged_data.pop("_raw_response", None)
    merged_data["screening_method"] = "ai"
    merged_data["screening_status"] = "ok"
    merged_data["prompt_version"] = settings.prompt_version
    merged_data["model"] = settings.llm.get("model")
    merged_data["raw_model_response"] = {"screen_and_match": raw_response}
    merged_data = _normalize_action_fields(merged_data)
    return ScreeningResult.model_validate(merged_data)


def build_prompt_messages(
    prompt_name: str,
    input_data: dict[str, Any],
    output_contract: dict[str, Any],
) -> list[dict[str, str]]:
    prompt = settings.prompts[prompt_name]
    user_template = prompt.get("user_template", "")
    user_content = user_template.format(
        input_json=json.dumps(input_data, ensure_ascii=False),
        output_contract_json=json.dumps(output_contract, ensure_ascii=False),
    )
    return [
        {"role": "system", "content": prompt.get("system", "")},
        {"role": "user", "content": user_content},
    ]


def call_prompt_json(
    prompt_name: str,
    basic_input: dict[str, Any],
    output_contract: dict[str, Any],
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    messages = build_prompt_messages(prompt_name, basic_input, output_contract)
    body = {
        "model": settings.llm["model"],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": messages,
        "response_format": {"type": "json_object"},
    }
    with _get_llm_semaphore():
        payload = call_llm(body)
    content_text = payload["choices"][0]["message"]["content"]
    try:
        data = json.loads(content_text)
    except json.JSONDecodeError:
        try:
            data = json.loads(content_text, strict=False)
        except json.JSONDecodeError as exc:
            finish_reason = payload["choices"][0].get("finish_reason")
            usage = payload.get("usage", {})
            completion_tokens = usage.get("completion_tokens")
            content_chars = len(content_text)
            tail_preview = content_text[-300:]
            if finish_reason == "length":
                raise RuntimeError(
                    f"{prompt_name} JSON truncated: finish_reason=length, "
                    f"max_tokens={max_tokens}, "
                    f"completion_tokens={completion_tokens}, "
                    f"content_chars={content_chars}, "
                    f"tail_preview={tail_preview}"
                ) from exc
            raise RuntimeError(
                f"invalid {prompt_name} JSON (finish_reason={finish_reason}): "
                f"content_chars={content_chars}, "
                f"tail_preview={tail_preview}"
            ) from exc
    data["_raw_response"] = payload
    return data


def _sanitize_body(body: dict[str, Any]) -> dict[str, Any]:
    """Deep-copy and redact any API-key-like strings in the body."""
    sanitized = copy.deepcopy(body)

    def _redact(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: _redact(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_redact(v) for v in obj]
        if isinstance(obj, str) and _SENSITIVE_RE.search(obj):
            return "[REDACTED]"
        return obj

    return _redact(sanitized)


def _dump_llm_body(body: dict[str, Any]) -> None:
    """Write the full LLM request body to a dump file if dumping is enabled."""
    if not (hasattr(_dump, "enabled") and _dump.enabled and _dump.output_dir):
        return

    _dump.counter += 1
    seq = _dump.counter
    prompt_name = _dump.prompt_context.get("prompt_name", "unknown")
    stage = _dump.prompt_context.get("stage", "unknown")

    # Compute stats from messages
    messages = body.get("messages", [])
    system_msg = messages[0]["content"] if len(messages) > 0 else ""
    user_msg = messages[1]["content"] if len(messages) > 1 else ""
    system_chars = len(system_msg)
    user_chars = len(user_msg)
    total_chars = system_chars + user_chars
    full_text = system_msg + user_msg

    stats = {
        "system_chars": system_chars,
        "user_chars": user_chars,
        "total_chars": total_chars,
        "estimated_tokens_chars_div4": math.ceil(total_chars / 4),
        "estimated_tokens_cjk_aware": _estimate_tokens_cjk(full_text),
        "url_count": len(re.findall(r"https?://", full_text)),
        "html_tag_count": len(
            re.findall(r"<\s*(?:a|p|div|span|img|br|li|ul|ol|table|tr|td|th|h[1-6])\b[^>]*>", full_text, re.IGNORECASE)
        ),
        "markdown_link_count": len(re.findall(r"\[([^\]]*)\]\(https?://[^\)]+\)", full_text)),
        "image_url_count": len(
            re.findall(r"https?://[^\s\"'<>]+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^\s\"'<>]*)?", full_text, re.IGNORECASE)
        ),
    }

    dump_record = {
        "dump_type": "llm_request_body",
        "exact_api_payload": True,
        "prompt_name": prompt_name,
        "stage": stage,
        "source_name": _dump.item_context.get("source_name", ""),
        "source_url": _dump.item_context.get("source_url", ""),
        "item_title": _dump.item_context.get("item_title", ""),
        "item_url": _dump.item_context.get("item_url", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_body": _sanitize_body(body),
        "stats": stats,
    }

    out_dir = Path(_dump.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{seq:04d}_{prompt_name}_request.json"
    filepath = out_dir / filename
    filepath.write_text(json.dumps(dump_record, ensure_ascii=False, indent=2), encoding="utf-8")

    # Short stdout notice only
    print(f"[PROMPT_DUMP] wrote {filepath}", flush=True)


def _estimate_tokens_cjk(text: str) -> int:
    """Rough CJK-aware token estimate: each CJK char ≈ 1 token, others ≈ chars/4."""
    cjk = 0
    other = 0
    for ch in text:
        if "一" <= ch <= "鿿" or "　" <= ch <= "〿" or "＀" <= ch <= "￯":
            cjk += 1
        else:
            other += 1
    return cjk + math.ceil(other / 4)


def call_llm(body: dict[str, Any]) -> dict[str, Any]:
    # Dump full request body if enabled (before HTTP call)
    _dump_llm_body(body)

    req = urllib.request.Request(
        f"{settings.llm['base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {settings.llm_api_key()}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=float(settings.llm.get("timeout_seconds", 60))) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI-compatible API returned {exc.code}: {detail}") from exc


def audit_prompt_messages(
    prompt_name: str,
    messages: list[dict[str, str]],
    input_data: dict[str, Any],
) -> dict[str, Any]:
    """Compute audit stats for assembled prompt messages without calling LLM."""
    system_msg = messages[0]["content"]
    user_msg = messages[1]["content"]

    system_chars = len(system_msg)
    user_chars = len(user_msg)
    total_chars = system_chars + user_chars
    estimated_tokens = math.ceil(total_chars / 4)

    input_json_str = json.dumps(input_data, ensure_ascii=False)
    input_json_chars = len(input_json_str)

    content = input_data.get("content", {}) or {}
    content_text = content.get("content_text", "") or ""
    summary = content.get("summary", "") or ""
    title = content.get("title", "") or ""

    content_text_chars = len(content_text)
    summary_chars = len(summary)
    title_chars = len(title)

    categories = input_data.get("categories", []) or []
    categories_chars = len(json.dumps(categories, ensure_ascii=False))

    reading_needs = input_data.get("reading_needs", []) or []
    reading_needs_chars = len(json.dumps(reading_needs, ensure_ascii=False))

    watch_topics = input_data.get("watch_topics", []) or []
    watch_topics_chars = len(json.dumps(watch_topics, ensure_ascii=False))

    basic_screening_context = input_data.get("basic_screening", {}) or {}
    basic_screening_context_chars = len(json.dumps(basic_screening_context, ensure_ascii=False))

    output_contract_chars = len(json.dumps(prompt_output_contract(prompt_name), ensure_ascii=False))

    # Noise detection
    full_text = system_msg + user_msg
    url_count = len(re.findall(r"https?://", full_text))
    html_tag_count = len(
        re.findall(r"<\s*(?:a|p|div|span|img|br|li|ul|ol|table|tr|td|th|h[1-6])\b[^>]*>", full_text, re.IGNORECASE)
    )
    markdown_link_count = len(
        re.findall(r"\[([^\]]*)\]\(https?://[^\)]+\)", full_text)
    )
    image_url_count = len(
        re.findall(
            r"https?://[^\s\"'<>]+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^\s\"'<>]*)?",
            full_text,
            re.IGNORECASE,
        )
    )

    # Longest sub-fields (top 5 by char length)
    field_lengths: list[tuple[str, int]] = []
    if content_text:
        field_lengths.append(("content_text", len(content_text)))
    if summary:
        field_lengths.append(("summary", len(summary)))
    if title:
        field_lengths.append(("title", len(title)))
    for key, value in (content or {}).items():
        if isinstance(value, str) and key not in ("content_text", "summary", "title"):
            field_lengths.append((f"content.{key}", len(value)))
    field_lengths.sort(key=lambda x: -x[1])
    longest_fields = [{"field": k, "chars": v} for k, v in field_lengths[:5]]

    # Truncated previews
    content_preview = (truncate(content_text, 300) or "")[:300]
    summary_preview = (truncate(summary, 200) or "")[:200]
    title_preview = (truncate(title, 200) or "")[:200]

    return {
        "audit_type": "prompt_audit",
        "prompt_name": prompt_name,
        "system_chars": system_chars,
        "user_chars": user_chars,
        "total_chars": total_chars,
        "estimated_tokens": estimated_tokens,
        "input_json_chars": input_json_chars,
        "content_text_chars": content_text_chars,
        "summary_chars": summary_chars,
        "title_chars": title_chars,
        "categories_chars": categories_chars,
        "reading_needs_chars": reading_needs_chars,
        "watch_topics_chars": watch_topics_chars,
        "basic_screening_context_chars": basic_screening_context_chars,
        "output_contract_chars": output_contract_chars,
        "url_count": url_count,
        "html_tag_count": html_tag_count,
        "markdown_link_count": markdown_link_count,
        "image_url_count": image_url_count,
        "longest_fields": longest_fields,
        "preview": {
            "title": title_preview,
            "summary_preview": summary_preview,
            "content_preview": content_preview,
        },
    }


def audit_screen_content(content: NormalizedContent) -> list[dict[str, Any]]:
    """Assemble prompts for all screening stages and return audit records.

    Never calls the LLM. Returns one record per prompt call that would have been made.
    """
    content_payload = content.model_dump()
    content_payload["content_text"] = truncate(
        content_payload.get("content_text"),
        int(settings.screening.get("max_input_chars", 4000)),
    )

    source_name = content.source_name or ""
    source_url = content.url or ""
    item_title = content.title or ""
    item_url = content.url or ""
    mode = settings.screening.get("mode", "two_stage")
    records: list[dict[str, Any]] = []

    base_meta = {
        "source_name": source_name,
        "source_url": source_url,
        "item_title": item_title,
        "item_url": item_url,
    }

    if mode == "merged":
        merged_input: dict[str, Any] = {
            "content": content_payload,
            "categories": settings.screening.get("categories", []),
            "reading_needs": settings.reading_needs,
            "watch_topics": settings.watch_topics,
        }
        messages = build_prompt_messages(
            "screen_and_match",
            merged_input,
            prompt_output_contract("screen_and_match"),
        )
        record = audit_prompt_messages("screen_and_match", messages, merged_input)
        record.update(**base_meta, mode=mode)
        records.append(record)
    else:
        # Stage 1: basic_screening
        basic_input: dict[str, Any] = {
            "content": content_payload,
            "categories": settings.screening.get("categories", []),
        }
        messages_1 = build_prompt_messages(
            "basic_screening",
            basic_input,
            prompt_output_contract("basic_screening"),
        )
        record_1 = audit_prompt_messages("basic_screening", messages_1, basic_input)
        record_1.update(**base_meta, mode=f"{mode}_stage1")
        records.append(record_1)

        # Stage 2: need_matching (basic_screening context is empty since no LLM call)
        matching_input: dict[str, Any] = {
            "content": content_payload,
            "basic_screening": {},
            "reading_needs": settings.reading_needs,
            "watch_topics": settings.watch_topics,
        }
        messages_2 = build_prompt_messages(
            "need_matching",
            matching_input,
            prompt_output_contract("need_matching"),
        )
        record_2 = audit_prompt_messages("need_matching", messages_2, matching_input)
        record_2.update(**base_meta, mode=f"{mode}_stage2")
        records.append(record_2)

    return records


def prompt_output_contract(prompt_name: str) -> dict[str, Any]:
    contract = settings.prompts.get(prompt_name, {}).get("output_contract")
    if not isinstance(contract, dict):
        raise RuntimeError(f"prompt '{prompt_name}' missing valid output_contract")
    return contract


def apply_score_policy(screening: ScreeningResult, content: NormalizedContent) -> ScreeningResult:
    policy = settings.score_policy
    action = screening.suggested_action
    followup = screening.followup_type

    if screening.needs_more_context and screening.suggested_next_step in {"fetch_fulltext", "manual_review"}:
        followup = screening.suggested_next_step
        if screening.confidence < float(policy.get("manual_review_confidence_below", 0.6)):
            action = "review"
            followup = "manual_review"
    elif screening.confidence < float(policy.get("manual_review_confidence_below", 0.6)):
        action = "review"
        followup = "manual_review"
    elif screening.value_score <= int(policy.get("ignore_below_value_score", 2)):
        action = "ignore"
        followup = "none"
    elif content.content_type in {"video", "audio"} and (
        screening.value_score >= int(policy.get("transcribe_min_value_score", 4))
        and screening.personal_relevance
        >= int(policy.get("transcribe_min_personal_relevance", 3))
    ):
        action = "transcribe"
        followup = "transcribe"
    elif (
        screening.value_score >= int(policy.get("save_min_value_score", 4))
        and screening.personal_relevance >= int(policy.get("save_min_personal_relevance", 4))
    ):
        action = "save"
        followup = "archive"
    elif (
        screening.value_score >= int(policy.get("read_min_value_score", 4))
        and screening.personal_relevance >= int(policy.get("read_min_personal_relevance", 3))
        and action not in {"save", "transcribe"}
    ):
        action = "read"
        if followup == "manual_review":
            followup = "none"
    elif action not in {"ignore", "skim", "review"}:
        action = "skim"
        if followup == "archive":
            followup = "none"

    screening.suggested_action = action
    screening.followup_type = followup
    return screening


def infer_evidence_level(content: NormalizedContent) -> str:
    text = (content.content_text or "").strip()
    summary = (content.summary or "").strip()
    title = (content.title or "").strip()
    if text:
        return "full_text" if len(text) >= 4000 else "partial_text"
    if summary:
        return "summary"
    if title:
        return "title_only"
    return "title_only"


def unscreened_result(content: NormalizedContent) -> ScreeningResult:
    return ScreeningResult(
        summary=truncate(content.summary or content.content_text or content.title, 120)
        or "本次请求关闭了粗筛。",
        title_cn="",
        category="未筛选",
        value_score=3,
        personal_relevance=3,
        novelty_score=3,
        source_quality=3,
        actionability=3,
        hidden_signals=[],
        entities=[],
        event_hint="",
        suggested_action="review",
        reason="请求参数 screen=false，已保存内容但未调用 AI 粗筛。",
        tags=[],
        confidence=0.0,
        evidence_level=infer_evidence_level(content),
        needs_more_context=True,
        suggested_next_step="manual_review",
        need_matches=[],
        topic_matches=[],
        followup_type="manual_review",
        screening_method="none",
        screening_status="skipped",
        prompt_version=settings.prompt_version,
        model=None,
    )


def failed_screening(content: NormalizedContent, error: str) -> ScreeningResult:
    return ScreeningResult(
        summary=truncate(content.summary or content.content_text or content.title, 160)
        or "打分过滤失败，需要人工复核。",
        title_cn="",
        category="其他",
        value_score=1,
        personal_relevance=1,
        novelty_score=1,
        source_quality=1,
        actionability=1,
        hidden_signals=[],
        entities=[],
        event_hint="",
        suggested_action="review",
        followup_type="manual_review",
        reason="打分过滤失败，未伪造模型判断，已转入人工复核。",
        tags=[],
        confidence=0.0,
        evidence_level=infer_evidence_level(content),
        needs_more_context=True,
        suggested_next_step="manual_review",
        need_matches=[],
        topic_matches=[],
        screening_method="ai",
        screening_status="failed",
        prompt_version=settings.prompt_version,
        model=settings.llm.get("model"),
        error=error,
    )


def gated_screening(content: NormalizedContent, reason: str, hints: list[str]) -> ScreeningResult:
    return ScreeningResult(
        summary=truncate(content.summary or content.content_text or content.title, 120) or "无内容",
        title_cn="",
        category="其他",
        value_score=1,
        personal_relevance=1,
        novelty_score=1,
        source_quality=1,
        actionability=1,
        hidden_signals=[],
        entities=[],
        event_hint="",
        suggested_action="ignore",
        followup_type="none",
        suggested_next_step="none",
        reason=f"pre-LLM gate skipped: {reason}",
        tags=[],
        confidence=0.0,
        evidence_level=infer_evidence_level(content),
        needs_more_context=False,
        need_matches=[],
        topic_matches=[],
        screening_method="ai" if reason != "empty_content" else "none",
        screening_status="ok",
        prompt_version=settings.prompt_version,
        model=None,
        gate_hints=hints,
    )


def summarize_increment(
    cluster_title: str,
    cluster_summary: str,
    new_item_title: str,
    new_item_summary: str,
    hidden_signals: list[str],
    entities: list[str],
) -> dict[str, Any]:
    if not settings.llm_api_key():
        raise RuntimeError("missing llm api key for incremental summary")
    prompt = settings.prompts["incremental"]
    user_content = prompt.get("user_template", "").format(
        input_json=json.dumps(
            {
                "cluster_title": cluster_title,
                "cluster_summary": cluster_summary,
                "new_item_title": new_item_title,
                "new_item_summary": new_item_summary,
                "new_item_hidden_signals": hidden_signals,
                "new_item_entities": entities,
            },
            ensure_ascii=False,
        ),
        output_contract_json=json.dumps(prompt_output_contract("incremental"), ensure_ascii=False),
    )
    body = {
        "model": settings.llm["model"],
        "temperature": 0.1,
        "max_tokens": 800,
        "messages": [
            {"role": "system", "content": prompt.get("system", "")},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_object"},
    }
    payload = call_llm(body)
    content_text = payload["choices"][0]["message"]["content"]
    return json.loads(content_text)
