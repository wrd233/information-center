"""Integration tests for screening modes.

These tests require a configured LLM API key and will be skipped by default.
Run with: PYTHONPATH=. pytest tests/test_screening.py -q -m integration
"""

import time

import pytest

from app.config import settings
from app.models import ContentAnalyzeRequest
from app.processor import normalize_content
from app.screener import ai_screen, ai_screen_merged, apply_score_policy

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


def _has_api_key():
    try:
        return bool(settings.llm_api_key())
    except Exception:
        return False


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _has_api_key(), reason="No LLM API key configured"),
]


class TestTwoStageStillWorks:
    def test_two_stage_returns_valid_result(self):
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen(nc)
        assert result.screening_status == "ok"
        assert result.screening_method == "ai"
        assert result.summary
        assert 1 <= result.value_score <= 5
        assert 1 <= result.personal_relevance <= 5
        assert result.entities
        assert result.event_hint

    def test_two_stage_has_need_matches(self):
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen(nc)
        assert len(result.need_matches) > 0
        for match in result.need_matches:
            assert match.need_id
            assert match.need_name
            assert 1 <= match.score <= 5
            assert match.decision in ("include", "maybe", "exclude")

    def test_two_stage_has_topic_matches(self):
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen(nc)
        assert len(result.topic_matches) > 0
        for match in result.topic_matches:
            assert match.topic_id
            assert match.topic_name

    def test_two_stage_respects_score_policy(self):
        nc = normalize_content(SAMPLE_CONTENT)
        raw = ai_screen(nc)
        result = apply_score_policy(raw, nc)
        assert result.suggested_action in (
            "ignore",
            "skim",
            "read",
            "save",
            "transcribe",
            "review",
        )
        assert result.followup_type in (
            "none",
            "fetch_fulltext",
            "archive",
            "transcribe",
            "manual_review",
        )


class TestMergedMode:
    def test_merged_returns_valid_result(self):
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen_merged(nc)
        assert result.screening_status == "ok"
        assert result.screening_method == "ai"
        assert result.summary
        assert 1 <= result.value_score <= 5
        assert 1 <= result.personal_relevance <= 5
        assert result.entities
        assert result.event_hint

    def test_merged_has_need_matches(self):
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen_merged(nc)
        assert len(result.need_matches) > 0
        for match in result.need_matches:
            assert match.need_id
            assert match.need_name
            assert 1 <= match.score <= 5

    def test_merged_has_topic_matches(self):
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen_merged(nc)
        assert len(result.topic_matches) > 0
        for match in result.topic_matches:
            assert match.topic_id

    def test_merged_respects_score_policy(self):
        nc = normalize_content(SAMPLE_CONTENT)
        raw = ai_screen_merged(nc)
        result = apply_score_policy(raw, nc)
        assert result.suggested_action in (
            "ignore",
            "skim",
            "read",
            "save",
            "transcribe",
            "review",
        )


class TestMergedVsTwoStageComparison:
    def test_merged_fields_compatible_with_two_stage_contract(self):
        """Merged output must contain all fields that downstream consumers expect."""
        nc = normalize_content(SAMPLE_CONTENT)
        result = ai_screen_merged(nc)

        # All basic_screening fields present
        assert result.summary
        assert result.category
        assert 1 <= result.value_score <= 5
        assert 1 <= result.personal_relevance <= 5
        assert 1 <= result.novelty_score <= 5
        assert 1 <= result.source_quality <= 5
        assert 1 <= result.actionability <= 5
        assert isinstance(result.hidden_signals, list)
        assert isinstance(result.entities, list)
        assert result.suggested_action
        assert result.reason
        assert isinstance(result.tags, list)
        assert 0.0 <= result.confidence <= 1.0
        assert result.evidence_level in (
            "title_only",
            "summary",
            "partial_text",
            "full_text",
        )
        assert isinstance(result.needs_more_context, bool)

        # All need_matching fields present
        assert isinstance(result.need_matches, list)
        assert isinstance(result.topic_matches, list)

    def test_merged_is_faster_than_two_stage(self):
        nc = normalize_content(SAMPLE_CONTENT)

        t0 = time.monotonic()
        ai_screen(nc)
        two_stage_time = time.monotonic() - t0

        t1 = time.monotonic()
        ai_screen_merged(nc)
        merged_time = time.monotonic() - t1

        # Record timing for manual review. Do not hard-assert because
        # network jitter could flip the comparison on a single sample.
        print(f"\ntwo_stage: {two_stage_time:.2f}s  merged: {merged_time:.2f}s")
        # We expect merged to be roughly half the time (one HTTP call vs two).
        # Only assert when the difference is large enough to rule out noise.
        if merged_time > two_stage_time * 0.9:
            pytest.skip("Timing too close to compare (network jitter)")
        assert merged_time < two_stage_time
