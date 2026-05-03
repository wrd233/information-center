"""Unit tests for screening modes (no API key required — monkeypatch call_llm)."""

import json
from unittest import mock

import pytest

from app.config import settings
from app.models import ContentAnalyzeRequest
from app.processor import normalize_content
from app.screener import (
    ai_screen,
    ai_screen_merged,
    apply_score_policy,
    call_prompt_json,
    prompt_output_contract,
    screen_content,
    _normalize_action_fields,
)


def _fake_llm_response(content_text, finish_reason="stop", completion_tokens=None):
    return {
        "choices": [
            {
                "message": {"content": content_text},
                "finish_reason": finish_reason,
            }
        ],
        "usage": {"completion_tokens": completion_tokens or max(len(content_text) // 4, 1)},
    }


VALID_MERGED_JSON = json.dumps({
    "summary": "DeepSeek 开源了新一代 MoE 模型 DeepSeek-V4。",
    "title_cn": "",
    "category": "AI前沿",
    "value_score": 5,
    "personal_relevance": 4,
    "novelty_score": 5,
    "source_quality": 4,
    "actionability": 3,
    "hidden_signals": ["开源模型竞争加剧"],
    "entities": ["DeepSeek", "DeepSeek-V4"],
    "event_hint": "DeepSeek 发布 DeepSeek-V4 模型",
    "suggested_action": "read",
    "followup_type": "none",
    "suggested_next_step": "none",
    "reason": "重要 AI 模型发布。",
    "tags": ["AI", "开源"],
    "confidence": 0.9,
    "evidence_level": "summary",
    "needs_more_context": False,
    "need_matches": [
        {
            "need_id": "frontier",
            "need_name": "我关注的前沿咋样了",
            "score": 5,
            "decision": "include",
            "priority": "P0",
            "reason": "重要 AI 产品动态。",
            "evidence": ["DeepSeek"],
            "confidence": 0.9,
            "needs_more_context": False,
        }
    ],
    "topic_matches": [
        {
            "topic_id": "ai_model",
            "topic_name": "AI 模型",
            "score": 4,
            "update_type": "new_event",
            "reason": "新模型发布。",
            "confidence": 0.85,
        }
    ],
})

SAMPLE_CONTENT = ContentAnalyzeRequest(
    title="DeepSeek 开源 DeepSeek-V4: 新一代 MoE 模型",
    summary=(
        "DeepSeek 今天正式开源了 DeepSeek-V4 模型，采用新一代 MoE 架构，"
        "在多项基准测试中超越 GPT-4。模型支持 128K 上下文窗口，"
        "API 价格大幅下降。"
    ),
    source_name="AI 前沿日报",
    content_type="article",
    screen=True,
)


class TestMergedUnit:
    """Unit tests for merged screening mode with mocked call_llm."""

    def test_merged_uses_screen_and_match_prompt(self, monkeypatch):
        """screen_content with mode=merged calls screen_and_match prompt."""
        monkeypatch.setattr("app.screener.call_llm", lambda body: _fake_llm_response(VALID_MERGED_JSON))
        monkeypatch.setattr(settings, "screening", {**settings.screening, "mode": "merged"})
        nc = normalize_content(SAMPLE_CONTENT)
        result = screen_content(nc, use_ai=True)
        assert result.screening_status == "ok"
        assert result.need_matches
        assert result.topic_matches

    def test_merged_uses_dedicated_max_tokens(self, monkeypatch):
        """ai_screen_merged uses merged_max_tokens, not llm.max_tokens."""
        captured_max_tokens = {}

        def fake_call_prompt_json(prompt_name, basic_input, output_contract, temperature, max_tokens):
            captured_max_tokens["max_tokens"] = max_tokens
            return json.loads(VALID_MERGED_JSON)

        monkeypatch.setattr("app.screener.call_prompt_json", fake_call_prompt_json)
        monkeypatch.setattr(settings, "screening", {**settings.screening, "merged_max_tokens": 4000})
        monkeypatch.setattr(settings, "llm", {**settings.llm, "max_tokens": 1200})
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen_merged(nc)
        assert result.screening_status == "ok"
        assert captured_max_tokens["max_tokens"] == 4000

    def test_call_prompt_json_detects_truncation(self, monkeypatch):
        """JSONDecodeError + finish_reason=length produces 'truncated' error message."""
        truncated_json = VALID_MERGED_JSON[:300]

        monkeypatch.setattr(
            "app.screener.call_llm",
            lambda body: _fake_llm_response(truncated_json, finish_reason="length", completion_tokens=1200),
        )
        contract = prompt_output_contract("screen_and_match")
        with pytest.raises(RuntimeError) as exc_info:
            call_prompt_json(
                "screen_and_match",
                basic_input={"content": {}, "categories": [], "reading_needs": [], "watch_topics": []},
                output_contract=contract,
                temperature=0.2,
                max_tokens=1200,
            )
        msg = str(exc_info.value)
        assert "truncated" in msg.lower() or "finish_reason=length" in msg
        assert "max_tokens=1200" in msg
        assert "content_chars=" in msg
        assert "tail_preview=" in msg

    def test_call_prompt_json_invalid_json_not_truncated(self, monkeypatch):
        """JSONDecodeError + finish_reason=stop produces 'invalid' error message."""
        invalid_json = "not valid json {{{"

        monkeypatch.setattr(
            "app.screener.call_llm",
            lambda body: _fake_llm_response(invalid_json, finish_reason="stop", completion_tokens=10),
        )
        contract = prompt_output_contract("screen_and_match")
        with pytest.raises(RuntimeError) as exc_info:
            call_prompt_json(
                "screen_and_match",
                basic_input={"content": {}, "categories": [], "reading_needs": [], "watch_topics": []},
                output_contract=contract,
                temperature=0.2,
                max_tokens=3000,
            )
        msg = str(exc_info.value)
        assert "invalid" in msg.lower()
        assert "truncated" not in msg.lower()
        assert "finish_reason=stop" in msg

    def test_call_prompt_json_truncation_message_no_full_content(self, monkeypatch):
        """Truncation error message must not include the full content_text."""
        long_truncated = "x" * 2000

        monkeypatch.setattr(
            "app.screener.call_llm",
            lambda body: _fake_llm_response(long_truncated, finish_reason="length", completion_tokens=1200),
        )
        contract = prompt_output_contract("screen_and_match")
        with pytest.raises(RuntimeError) as exc_info:
            call_prompt_json(
                "screen_and_match",
                basic_input={"content": {}, "categories": [], "reading_needs": [], "watch_topics": []},
                output_contract=contract,
                temperature=0.2,
                max_tokens=1200,
            )
        msg = str(exc_info.value)
        # tail_preview should only have last 300 chars, not the full 2000
        assert "x" * 400 not in msg
        assert len(msg) < 2000

    def test_two_stage_still_uses_llm_max_tokens(self, monkeypatch):
        """ai_screen (two_stage) uses llm.max_tokens, not merged_max_tokens."""
        captured = []

        def fake_call_prompt_json(prompt_name, basic_input, output_contract, temperature, max_tokens):
            captured.append((prompt_name, max_tokens))
            if prompt_name == "basic_screening":
                return json.loads(VALID_MERGED_JSON)
            if prompt_name == "need_matching":
                return json.loads('{"need_matches": [], "topic_matches": []}')
            raise RuntimeError(f"unexpected prompt: {prompt_name}")

        monkeypatch.setattr("app.screener.call_prompt_json", fake_call_prompt_json)
        monkeypatch.setattr(settings, "screening", {**settings.screening, "merged_max_tokens": 9999})
        monkeypatch.setattr(settings, "llm", {**settings.llm, "max_tokens": 1200})
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen(nc)
        assert result.screening_status == "ok"
        for _, mt in captured:
            assert mt == 1200

    def test_default_mode_is_two_stage(self):
        """Default screening mode is two_stage."""
        mode = settings.screening.get("mode", "two_stage")
        assert mode == "two_stage"


class TestNormalizeActionFields:
    """Unit tests for _normalize_action_fields."""

    def test_normalize_fetch_fulltext_to_review(self):
        """suggested_action='fetch_fulltext' is normalized to review + fetch_fulltext followup."""
        result = _normalize_action_fields({"suggested_action": "fetch_fulltext"})
        assert result["suggested_action"] == "review"
        assert result["followup_type"] == "fetch_fulltext"
        assert result["suggested_next_step"] == "fetch_fulltext"

    def test_normalize_preserves_existing_followup(self):
        """When followup_type is already set (not none), don't overwrite it."""
        result = _normalize_action_fields({
            "suggested_action": "fetch_fulltext",
            "followup_type": "archive",
        })
        assert result["suggested_action"] == "review"
        assert result["followup_type"] == "archive"

    def test_normalize_preserves_legal_action(self):
        """Legal suggested_action is left unchanged."""
        input_data = {"suggested_action": "read", "followup_type": "archive"}
        result = _normalize_action_fields(dict(input_data))
        assert result == input_data

    def test_normalize_other_illegal_action_unchanged(self):
        """Other illegal suggested_action values are NOT silently fixed."""
        result = _normalize_action_fields({"suggested_action": "random_garbage"})
        assert result["suggested_action"] == "random_garbage"


class TestPromptContractMentionsFetchFulltextRule:
    """Ensure prompt output_contracts explicitly warn about fetch_fulltext placement."""

    def test_basic_screening_contract_warns_fetch_fulltext(self):
        contract = prompt_output_contract("basic_screening")
        sa = contract.get("suggested_action", "")
        assert "review" in sa
        assert "fetch_fulltext" in sa

    def test_screen_and_match_contract_warns_fetch_fulltext(self):
        contract = prompt_output_contract("screen_and_match")
        sa = contract.get("suggested_action", "")
        assert "review" in sa
        assert "fetch_fulltext" in sa
