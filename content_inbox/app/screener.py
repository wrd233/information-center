from __future__ import annotations

import json
import urllib.error
import urllib.request

from pydantic import ValidationError

from app.config import settings
from app.models import NormalizedContent, ScreeningResult
from app.utils import truncate


SYSTEM_PROMPT = """你是一个本地 content-inbox 的轻量内容粗筛器。
目标不是深度总结，而是判断这条内容是否值得后续阅读、保存、转录或人工复核。
必须只输出 json object，不要输出 Markdown。"""


def screen_content(content: NormalizedContent, use_ai: bool) -> ScreeningResult:
    if not use_ai:
        return unscreened_result(content)
    if not settings.ai_enabled:
        raise RuntimeError("AI screening is disabled by CONTENT_INBOX_AI_ENABLED=0")
    if not settings.openai_api_key:
        raise RuntimeError(
            "screen=true requires CONTENT_INBOX_DEEPSEEK_API_KEY or CONTENT_INBOX_OPENAI_API_KEY"
        )
    return ai_screen(content)


def ai_screen(content: NormalizedContent) -> ScreeningResult:
    input_payload = content.model_dump()
    input_payload["content_text"] = truncate(input_payload.get("content_text"), settings.max_content_chars)
    schema_hint = {
        "summary": "一句话说明这条内容在讲什么",
        "category": "粗分类",
        "value_score": "1-5 的整数",
        "personal_relevance": "1-5 的整数",
        "suggested_action": "ignore|skim|read|save|transcribe|review",
        "reason": "推荐或忽略原因",
        "tags": ["标签1", "标签2"],
        "followup_type": "none|fetch_fulltext|archive|transcribe|manual_review",
    }
    body = {
        "model": settings.openai_model,
        "temperature": 0.2,
        "max_tokens": 800,
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
        f"{settings.openai_base_url}/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {settings.openai_api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=settings.openai_timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI-compatible API returned {exc.code}: {detail}") from exc

    content_text = payload["choices"][0]["message"]["content"]
    try:
        data = json.loads(content_text)
        data["screening_method"] = "ai"
        return ScreeningResult.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(f"invalid AI screening JSON: {content_text}") from exc


def unscreened_result(content: NormalizedContent) -> ScreeningResult:
    return ScreeningResult(
        summary=truncate(content.summary or content.content_text or content.title, 120)
        or "本次请求关闭了粗筛。",
        category="未筛选",
        value_score=3,
        personal_relevance=3,
        suggested_action="review",
        reason="请求参数 screen=false，已保存内容但未调用 AI 粗筛。",
        tags=[],
        followup_type="manual_review",
        screening_method="none",
    )
