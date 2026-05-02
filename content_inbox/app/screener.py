from __future__ import annotations

import json
import urllib.error
import urllib.request

from pydantic import ValidationError

from app.config import settings
from app.models import NormalizedContent, ScreeningResult
from app.utils import truncate


SYSTEM_PROMPT = """你是一个本地 content-inbox 的内容打分过滤器。
你需要根据用户长期关注的信息管理、AI工具、工程实践、技术学习、社会观察等方向，对内容做结构化判断。
必须只输出 json object，不要输出 Markdown。"""

INCREMENTAL_SYSTEM_PROMPT = """你是 content-inbox 的事件增量判断器。
比较新内容和已有事件簇，判断新内容是否提供了新增信息。必须只输出 json object。"""


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
    input_payload = content.model_dump()
    input_payload["content_text"] = truncate(
        input_payload.get("content_text"), int(settings.screening.get("max_input_chars", 4000))
    )
    schema_hint = {
        "summary": "一句话说明这条内容在讲什么",
        "category": settings.screening.get("categories", []),
        "value_score": "1-5 的整数",
        "personal_relevance": "1-5 的整数",
        "novelty_score": "1-5 的整数",
        "source_quality": "1-5 的整数",
        "actionability": "1-5 的整数",
        "hidden_signals": ["标题和摘要表层之外的隐含趋势、风险、机会或工作流启发"],
        "entities": ["核心人物、公司、项目、产品、地点、政策、技术名词等"],
        "event_hint": "一句话事件描述，用于后续事件聚类",
        "suggested_action": "ignore|skim|read|save|transcribe|review",
        "followup_type": "none|fetch_fulltext|archive|transcribe|manual_review",
        "reason": "推荐、忽略或复核的理由",
        "tags": ["标签1", "标签2"],
        "confidence": "0-1 的数字",
    }
    body = {
        "model": settings.llm["model"],
        "temperature": settings.llm.get("temperature", 0.2),
        "max_tokens": settings.llm.get("max_tokens", 1200),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {"content": input_payload, "required_output": schema_hint},
                    ensure_ascii=False,
                ),
            },
        ],
        "response_format": {"type": "json_object"},
    }
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
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI-compatible API returned {exc.code}: {detail}") from exc

    content_text = payload["choices"][0]["message"]["content"]
    try:
        data = json.loads(content_text)
        data["screening_method"] = "ai"
        data["screening_status"] = "ok"
        data["prompt_version"] = settings.llm.get("prompt_version")
        data["model"] = settings.llm.get("model")
        data["raw_model_response"] = payload
        return ScreeningResult.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(f"invalid AI screening JSON: {content_text}") from exc


def apply_score_policy(screening: ScreeningResult, content: NormalizedContent) -> ScreeningResult:
    policy = settings.score_policy
    action = screening.suggested_action
    followup = screening.followup_type

    if screening.confidence < float(policy.get("manual_review_confidence_below", 0.6)):
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


def unscreened_result(content: NormalizedContent) -> ScreeningResult:
    return ScreeningResult(
        summary=truncate(content.summary or content.content_text or content.title, 120)
        or "本次请求关闭了粗筛。",
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
        followup_type="manual_review",
        screening_method="none",
        screening_status="skipped",
        prompt_version=settings.llm.get("prompt_version"),
        model=None,
    )


def failed_screening(content: NormalizedContent, error: str) -> ScreeningResult:
    return ScreeningResult(
        summary=truncate(content.summary or content.content_text or content.title, 160)
        or "打分过滤失败，需要人工复核。",
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
        screening_method="ai",
        screening_status="failed",
        prompt_version=settings.llm.get("prompt_version"),
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
) -> dict:
    if not settings.llm_api_key():
        raise RuntimeError("missing llm api key for incremental summary")
    body = {
        "model": settings.llm["model"],
        "temperature": 0.1,
        "max_tokens": 800,
        "messages": [
            {"role": "system", "content": INCREMENTAL_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "cluster_title": cluster_title,
                        "cluster_summary": cluster_summary,
                        "new_item_title": new_item_title,
                        "new_item_summary": new_item_summary,
                        "new_item_hidden_signals": hidden_signals,
                        "new_item_entities": entities,
                        "required_output": {
                            "has_incremental_value": True,
                            "incremental_summary": "相比已有内容新增了什么",
                            "new_entities": ["新实体"],
                            "should_update_cluster_summary": True,
                            "updated_cluster_summary": "更新后的事件簇摘要",
                        },
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        "response_format": {"type": "json_object"},
    }
    req = urllib.request.Request(
        f"{settings.llm['base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {settings.llm_api_key()}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=float(settings.llm.get("timeout_seconds", 60))) as response:
        payload = json.loads(response.read().decode("utf-8"))
    content_text = payload["choices"][0]["message"]["content"]
    return json.loads(content_text)
