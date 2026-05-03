from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from app.config import settings
from app.models import NormalizedContent, ScreeningResult
from app.utils import truncate


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
        return apply_score_policy(ai_screen(content), content)
    except Exception as exc:
        return failed_screening(content, str(exc))


def ai_screen(content: NormalizedContent) -> ScreeningResult:
    content_payload = content.model_dump()
    content_payload["content_text"] = truncate(
        content_payload.get("content_text"),
        int(settings.screening.get("max_input_chars", 4000)),
    )

    basic_contract = prompt_output_contract("basic_screening")
    basic_input = {
        "content": content_payload,
        "categories": settings.screening.get("categories", []),
    }
    basic_data = call_prompt_json(
        "basic_screening",
        basic_input=basic_input,
        output_contract=basic_contract,
        temperature=settings.llm.get("temperature", 0.2),
        max_tokens=settings.llm.get("max_tokens", 1200),
    )

    matching_input = {
        "content": content_payload,
        "basic_screening": basic_data,
        "reading_needs": settings.reading_needs,
        "watch_topics": settings.watch_topics,
    }
    matching_data = call_prompt_json(
        "need_matching",
        basic_input=matching_input,
        output_contract=prompt_output_contract("need_matching"),
        temperature=settings.llm.get("temperature", 0.2),
        max_tokens=settings.llm.get("max_tokens", 1200),
    )

    basic_raw = basic_data.pop("_raw_response", None)
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
    return ScreeningResult.model_validate(merged)


def call_prompt_json(
    prompt_name: str,
    basic_input: dict[str, Any],
    output_contract: dict[str, Any],
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    prompt = settings.prompts[prompt_name]
    user_template = prompt.get("user_template", "")
    user_content = user_template.format(
        input_json=json.dumps(basic_input, ensure_ascii=False),
        output_contract_json=json.dumps(output_contract, ensure_ascii=False),
    )
    body = {
        "model": settings.llm["model"],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": prompt.get("system", "")},
            {"role": "user", "content": user_content},
        ],
        "response_format": {"type": "json_object"},
    }
    payload = call_llm(body)
    content_text = payload["choices"][0]["message"]["content"]
    try:
        data = json.loads(content_text)
        data["_raw_response"] = payload
        return data
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid {prompt_name} JSON: {content_text}") from exc


def call_llm(body: dict[str, Any]) -> dict[str, Any]:
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
