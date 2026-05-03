"""Unit tests for process_content_thread_safe lock restructuring.

No real LLM/embedding/API calls. Uses monkeypatch on store and screen_content.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.models import ClusteringResult, ContentAnalyzeRequest, ProcessResult, ScreeningResult
from app.processor import process_content_thread_safe


SAMPLE_PAYLOAD = ContentAnalyzeRequest(
    title="DeepSeek开源DeepSeek-V4新一代MoE模型",
    summary="DeepSeek正式开源DeepSeek-V4模型",
    content_text="DeepSeek今天开源了新一代MoE模型DeepSeek-V4。",
    source_name="AI前沿日报",
    content_type="article",
    screen=True,
)

UNSCREENED_PAYLOAD = ContentAnalyzeRequest(
    title="Another Article",
    summary="Some content",
    content_text="Some more content.",
    source_name="Test Source",
    content_type="article",
    screen=False,
)

_SHARED_SCREENING_DICT = {
    "summary": "test screening summary",
    "category": "AI前沿",
    "value_score": 4,
    "personal_relevance": 4,
    "novelty_score": 4,
    "source_quality": 4,
    "actionability": 4,
    "hidden_signals": [],
    "entities": [],
    "event_hint": "",
    "suggested_action": "read",
    "followup_type": "none",
    "reason": "test",
    "tags": [],
    "confidence": 0.9,
    "evidence_level": "partial_text",
    "needs_more_context": False,
    "suggested_next_step": "none",
    "need_matches": [],
    "topic_matches": [],
    "screening_method": "ai",
    "screening_status": "ok",
    "prompt_version": "v1",
    "model": "test-model",
}

_SHARED_CLUSTERING_DICT = {
    "cluster_id": None,
    "cluster_title": None,
    "cluster_relation": "disabled",
    "max_similarity": None,
    "entity_overlap_ratio": None,
    "notification_decision": "manual_review",
    "incremental_summary": "",
    "embedding_text": None,
    "embedding_model": None,
    "clustering_status": "disabled",
    "error": None,
}


def _make_mock_item(item_id="item-1", **overrides):
    item = {
        "item_id": item_id,
        "dedupe_key": "hash:abc",
        "title": "DeepSeek开源DeepSeek-V4新一代MoE模型",
        "url": "http://example.com/1",
        "guid": None,
        "source_name": "AI前沿日报",
        "source_category": "AI",
        "content_type": "article",
        "published_at": "2024-01-01T00:00:00",
        "author": None,
        "summary": "Test summary",
        "content_text": "Test content text",
        "screening": _SHARED_SCREENING_DICT,
        "clustering": _SHARED_CLUSTERING_DICT,
        "embedding_text": None,
        "embedding_model": None,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "last_seen_at": "2024-01-01T00:00:00",
        "seen_count": 1,
    }
    item.update(overrides)
    return item


def _mock_store(get_by_dedupe_key_returns=None):
    """Create a MagicMock InboxStore with minimal required methods."""
    store = MagicMock()
    item = _make_mock_item()
    store.get_by_dedupe_key.return_value = get_by_dedupe_key_returns
    store.mark_seen.return_value = item
    store.insert.return_value = item
    store.update_item_clustering.return_value = item
    return store


def _mock_screening_result(screening_status="ok", screening_method="ai"):
    return ScreeningResult(
        summary="Test screening",
        category="AI前沿",
        value_score=4,
        personal_relevance=4,
        novelty_score=4,
        source_quality=4,
        actionability=4,
        hidden_signals=[],
        entities=["DeepSeek"],
        event_hint="DeepSeek发布新模型",
        suggested_action="read",
        followup_type="none",
        reason="高价值AI新闻",
        tags=["AI"],
        confidence=0.9,
        evidence_level="partial_text",
        needs_more_context=False,
        suggested_next_step="none",
        need_matches=[],
        topic_matches=[],
        screening_method=screening_method,
        screening_status=screening_status,
        prompt_version="v1",
        model="test-model",
    )


def _mock_clustering_result():
    return ClusteringResult(
        cluster_relation="new_event",
        notification_decision="full_push",
        clustering_status="ok",
        cluster_id="cluster-1",
        cluster_title="DeepSeek发布新模型",
    )


class TestPreDedupeHit:
    def test_skips_screen_content_when_dedupe_hit(self, monkeypatch):
        """Phase 1 dedupe hit must not call screen_content."""
        store = _mock_store(get_by_dedupe_key_returns=_make_mock_item())
        screen_called = False

        def fake_screen(content, use_ai):
            nonlocal screen_called
            screen_called = True
            return _mock_screening_result()

        monkeypatch.setattr("app.processor.screen_content", fake_screen)
        result = process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert result.is_duplicate is True
        assert result.item_id == "item-1"
        assert not screen_called

    def test_marks_seen_on_duplicate(self, monkeypatch):
        """Pre-dedupe hit should call mark_seen on the existing item."""
        store = _mock_store(get_by_dedupe_key_returns=_make_mock_item())
        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        process_content_thread_safe(store, SAMPLE_PAYLOAD)
        store.mark_seen.assert_called_once_with("item-1")

    def test_returns_existing_item_data(self, monkeypatch):
        """Duplicate result should reflect the existing item's data."""
        existing = _make_mock_item(item_id="existing-abc", title="Existing Title")
        store = _mock_store(get_by_dedupe_key_returns=existing)
        store.mark_seen.return_value = existing
        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        result = process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert result.is_duplicate is True
        assert result.item_id == "existing-abc"
        assert result.normalized.title == "Existing Title"


class TestNewContentFlow:
    def test_screen_content_is_called_for_new_item(self, monkeypatch):
        """New (non-duplicate) content must go through screen_content."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        screen_calls = []

        def fake_screen(content, use_ai):
            screen_calls.append((content.title, use_ai))
            return _mock_screening_result()

        monkeypatch.setattr("app.processor.screen_content", fake_screen)
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        result = process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert result.is_duplicate is False
        assert len(screen_calls) == 1
        assert screen_calls[0][1] is True  # use_ai=True

    def test_new_item_is_inserted(self, monkeypatch):
        """New content should result in store.insert being called."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        process_content_thread_safe(store, SAMPLE_PAYLOAD)
        store.insert.assert_called_once()

    def test_cluster_content_is_called_for_new_item(self, monkeypatch):
        """cluster_content must be called for new non-duplicate items."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        cluster_calls = []

        def fake_cluster(store, item_id, normalized, screening):
            cluster_calls.append(item_id)
            return _mock_clustering_result()

        monkeypatch.setattr("app.processor.screen_content", lambda c, use_ai: _mock_screening_result())
        monkeypatch.setattr("app.processor.cluster_content", fake_cluster)
        process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert len(cluster_calls) == 1
        assert cluster_calls[0] == "item-1"

    def test_unscreened_mode_still_inserts(self, monkeypatch):
        """screen=false should produce unscreened result and still insert."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        result = process_content_thread_safe(store, UNSCREENED_PAYLOAD)

        assert result.is_duplicate is False
        assert result.screening.screening_method == "none"
        store.insert.assert_called_once()


class TestSecondaryDedupe:
    def test_secondary_dedupe_prevents_insert(self, monkeypatch):
        """When another thread inserts between phase 1 and phase 3, commit must not insert again."""
        existing = _make_mock_item(item_id="other-thread-item")
        store = _mock_store(get_by_dedupe_key_returns=existing)
        # get_by_dedupe_key first returns None (phase 1), then existing (phase 3)
        store.get_by_dedupe_key.side_effect = [None, existing]
        store.mark_seen.return_value = existing

        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        result = process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert result.is_duplicate is True
        assert result.item_id == "other-thread-item"
        store.insert.assert_not_called()

    def test_secondary_dedupe_marks_seen(self, monkeypatch):
        """Secondary dedupe hit should mark_seen on the existing item."""
        existing = _make_mock_item(item_id="late-dup-item")
        store = _mock_store()
        store.get_by_dedupe_key.side_effect = [None, existing]
        store.mark_seen.return_value = existing

        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert store.mark_seen.call_count == 1
        store.mark_seen.assert_called_with("late-dup-item")

    def test_secondary_dedupe_returns_duplicate(self, monkeypatch):
        """Secondary dedupe should return is_duplicate=True."""
        existing = _make_mock_item(item_id="late-dup-2")
        store = _mock_store()
        store.get_by_dedupe_key.side_effect = [None, existing]
        store.mark_seen.return_value = existing

        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        result = process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert result.is_duplicate is True
        assert result.item_id == "late-dup-2"


class TestScreeningModePreservation:
    def test_two_stage_path_preserved(self, monkeypatch):
        """screen_content is called with use_ai=True for screen=True payloads."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        captured_use_ai = []

        def fake_screen(content, use_ai):
            captured_use_ai.append(use_ai)
            return _mock_screening_result(screening_method="ai")

        monkeypatch.setattr("app.processor.screen_content", fake_screen)
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert captured_use_ai == [True]

    def test_screen_false_produces_unscreened(self, monkeypatch):
        """screen=False should result in unscreened screening status."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        result = process_content_thread_safe(store, UNSCREENED_PAYLOAD)

        assert result.screening.screening_method == "none"
        assert result.screening.screening_status == "skipped"


class TestPreLLMGate:
    def test_gate_applies_to_screening(self, monkeypatch):
        """pre_llm_gate hints are attached to screening result."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        monkeypatch.setattr(
            "app.processor.screen_content", lambda c, use_ai: _mock_screening_result()
        )
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        result = process_content_thread_safe(store, SAMPLE_PAYLOAD)

        assert result.is_duplicate is False
        # pre_llm_gate should add gate_hints for this title
        assert hasattr(result.screening, "gate_hints")


class TestEmptyContentFallback:
    def test_very_short_content_flows_through_gate(self, monkeypatch):
        """Very short content should pass through pre_llm_gate without crashing."""
        store = _mock_store(get_by_dedupe_key_returns=None)
        monkeypatch.setattr(
            "app.processor.cluster_content",
            lambda store, item_id, normalized, screening: _mock_clustering_result(),
        )
        payload = ContentAnalyzeRequest(
            title="Ab", source_name="Test", content_type="article"
        )
        result = process_content_thread_safe(store, payload)

        assert result.is_duplicate is False
        store.insert.assert_called_once()
