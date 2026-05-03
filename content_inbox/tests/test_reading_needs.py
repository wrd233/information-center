from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.app_config import load_prompts, load_reading_needs, load_watch_topics
from app.config import settings
from app.models import ClusteringResult, NormalizedContent, ScreeningResult
from app.screener import ai_screen
from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    store = InboxStore(tmp_path / "reading_needs.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app), store


def make_screening(
    *,
    summary: str,
    category: str,
    value_score: int,
    personal_relevance: int,
    need_matches: list[dict] | None = None,
    topic_matches: list[dict] | None = None,
) -> ScreeningResult:
    return ScreeningResult(
        summary=summary,
        category=category,
        title_cn="",
        value_score=value_score,
        personal_relevance=personal_relevance,
        novelty_score=3,
        source_quality=3,
        actionability=3,
        hidden_signals=[],
        entities=[],
        event_hint=summary,
        suggested_action="skim",
        followup_type="none",
        reason="测试数据",
        tags=[],
        confidence=0.85,
        evidence_level="summary",
        needs_more_context=False,
        suggested_next_step="none",
        need_matches=need_matches or [],
        topic_matches=topic_matches or [],
        screening_method="ai",
        screening_status="ok",
    )


def test_prompt_and_matching_configs_load() -> None:
    base_dir = Path(__file__).resolve().parents[1]

    prompts = load_prompts(base_dir)
    assert prompts["version"] == "reading_needs_v1"
    assert prompts["basic_screening"]["purpose"]
    assert prompts["need_matching"]["output_contract"]["need_matches"]
    assert prompts["incremental"]["system"]

    reading_needs = load_reading_needs(base_dir)
    assert any(need["id"] == "entertainment" for need in reading_needs["needs"])
    assert any(need["enabled"] for need in reading_needs["needs"])

    watch_topics = load_watch_topics(base_dir)
    assert any(topic["id"] == "ai_agent" for topic in watch_topics["topics"])
    assert any(topic["keywords"] for topic in watch_topics["topics"])


def test_entertainment_need_can_match_even_with_lower_general_value(monkeypatch) -> None:
    content = NormalizedContent(
        title="深夜整活合集",
        source_name="娱乐号",
        source_category="最娱乐",
        content_type="article",
        summary="轻松搞笑的短内容合集。",
    )

    def fake_call_prompt_json(
        prompt_name: str,
        basic_input: dict,
        output_contract: dict,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        if prompt_name == "basic_screening":
            return {
                "summary": "轻松搞笑的娱乐内容。",
                "title_cn": "",
                "category": "娱乐内容",
                "value_score": 2,
                "personal_relevance": 2,
                "novelty_score": 2,
                "source_quality": 3,
                "actionability": 1,
                "hidden_signals": [],
                "entities": [],
                "event_hint": "轻松娱乐内容",
                "suggested_action": "skim",
                "followup_type": "none",
                "suggested_next_step": "none",
                "reason": "适合放松，但不是高项目价值内容。",
                "tags": ["娱乐"],
                "confidence": 0.74,
                "evidence_level": "summary",
                "needs_more_context": False,
                "_raw_response": {"id": "basic"},
            }
        return {
            "need_matches": [
                {
                    "need_id": "entertainment",
                    "need_name": "今天看什么娱乐",
                    "score": 5,
                    "decision": "include",
                    "priority": "P1",
                    "reason": "轻松有趣，适合今天放松看一下。",
                    "evidence": ["轻松", "搞笑"],
                    "confidence": 0.9,
                    "needs_more_context": False,
                }
            ],
            "topic_matches": [],
            "_raw_response": {"id": "matching"},
        }

    monkeypatch.setattr("app.screener.call_prompt_json", fake_call_prompt_json)

    result = ai_screen(content)

    assert result.value_score == 2
    assert result.need_matches[0].need_id == "entertainment"
    assert result.need_matches[0].score == 5
    assert result.need_matches[0].decision == "include"


def test_ai_screen_supports_title_cn_frontier_topic_and_new_need(monkeypatch) -> None:
    content = NormalizedContent(
        title="OpenAI Agent SDK ships",
        source_name="Tech Blog",
        source_category="英文博客",
        content_type="article",
        summary="A short post about an Agent SDK release.",
    )
    old_needs = settings.reading_needs
    old_topics = settings.watch_topics
    settings.reading_needs = [
        {
            "id": "frontier",
            "name": "我关注的前沿咋样了",
            "enabled": True,
        },
        {
            "id": "custom_signal",
            "name": "我新加的需求",
            "enabled": True,
        },
    ]
    settings.watch_topics = [
        {
            "id": "ai_agent",
            "name": "AI Agent",
            "keywords": ["Agent", "MCP"],
        }
    ]

    def fake_call_prompt_json(
        prompt_name: str,
        basic_input: dict,
        output_contract: dict,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        if prompt_name == "basic_screening":
            return {
                "summary": "OpenAI 发布了一个新的 Agent SDK。",
                "title_cn": "OpenAI 发布 Agent SDK",
                "category": "AI工具",
                "value_score": 4,
                "personal_relevance": 4,
                "novelty_score": 4,
                "source_quality": 4,
                "actionability": 4,
                "hidden_signals": ["Agent 工具链继续 API 化"],
                "entities": ["OpenAI", "Agent SDK"],
                "event_hint": "OpenAI 发布 Agent SDK",
                "suggested_action": "read",
                "followup_type": "none",
                "suggested_next_step": "fetch_fulltext",
                "reason": "属于值得关注的工具链变化。",
                "tags": ["OpenAI", "Agent"],
                "confidence": 0.68,
                "evidence_level": "summary",
                "needs_more_context": True,
                "_raw_response": {"id": "basic"},
            }
        return {
            "need_matches": [
                {
                    "need_id": "frontier",
                    "need_name": "我关注的前沿咋样了",
                    "score": 5,
                    "decision": "include",
                    "priority": "P0",
                    "reason": "有明确的 Agent SDK 新动态。",
                    "evidence": ["OpenAI", "Agent SDK"],
                    "confidence": 0.91,
                    "needs_more_context": False,
                },
                {
                    "need_id": "custom_signal",
                    "need_name": "我新加的需求",
                    "score": 4,
                    "decision": "include",
                    "priority": "P1",
                    "reason": "证明新增需求不需要改固定 schema。",
                    "evidence": ["custom_signal"],
                    "confidence": 0.8,
                    "needs_more_context": False,
                },
            ],
            "topic_matches": [
                {
                    "topic_id": "ai_agent",
                    "topic_name": "AI Agent",
                    "score": 4,
                    "update_type": "new_event",
                    "reason": "直接讨论 Agent SDK。",
                    "confidence": 0.86,
                }
            ],
            "_raw_response": {"id": "matching"},
        }

    monkeypatch.setattr("app.screener.call_prompt_json", fake_call_prompt_json)
    try:
        result = ai_screen(content)
    finally:
        settings.reading_needs = old_needs
        settings.watch_topics = old_topics

    assert result.title_cn == "OpenAI 发布 Agent SDK"
    assert result.evidence_level == "summary"
    assert result.needs_more_context is True
    assert any(match.need_id == "frontier" for match in result.need_matches)
    assert any(match.need_id == "custom_signal" for match in result.need_matches)
    assert any(match.topic_id == "ai_agent" for match in result.topic_matches)


def test_inbox_filters_by_need_and_topic_and_old_items_do_not_crash(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)

    entertainment_item = store.insert(
        "dedupe:entertainment",
        NormalizedContent(
            title="今天刷点轻松的",
            source_name="娱乐号",
            source_category="最娱乐",
            content_type="article",
            summary="今天看点轻松娱乐内容。",
        ),
        make_screening(
            summary="今天看点轻松娱乐内容。",
            category="娱乐内容",
            value_score=2,
            personal_relevance=2,
            need_matches=[
                {
                    "need_id": "entertainment",
                    "need_name": "今天看什么娱乐",
                    "score": 5,
                    "decision": "include",
                    "priority": "P1",
                    "reason": "适合放松。",
                    "evidence": ["轻松", "娱乐"],
                    "confidence": 0.9,
                    "needs_more_context": False,
                }
            ],
        ),
        ClusteringResult(notification_decision="silent", clustering_status="skipped"),
    )
    assert entertainment_item["item_id"]

    frontier_item = store.insert(
        "dedupe:frontier",
        NormalizedContent(
            title="OpenAI Agent SDK ships",
            source_name="Tech Blog",
            source_category="英文博客",
            content_type="article",
            summary="Agent SDK release.",
        ),
        make_screening(
            summary="OpenAI 发布 Agent SDK。",
            category="AI工具",
            value_score=4,
            personal_relevance=4,
            need_matches=[
                {
                    "need_id": "frontier",
                    "need_name": "我关注的前沿咋样了",
                    "score": 5,
                    "decision": "include",
                    "priority": "P0",
                    "reason": "前沿产品动态。",
                    "evidence": ["OpenAI", "Agent SDK"],
                    "confidence": 0.92,
                    "needs_more_context": False,
                }
            ],
            topic_matches=[
                {
                    "topic_id": "ai_agent",
                    "topic_name": "AI Agent",
                    "score": 4,
                    "update_type": "new_event",
                    "reason": "与 AI Agent 主题直接相关。",
                    "confidence": 0.88,
                }
            ],
        ),
        ClusteringResult(notification_decision="full_push", clustering_status="ok"),
    )
    assert frontier_item["item_id"]

    legacy_item = store.insert(
        "dedupe:legacy",
        NormalizedContent(
            title="旧数据",
            source_name="Legacy",
            source_category="Articles",
            content_type="article",
            summary="这是一个旧 item。",
        ),
        make_screening(
            summary="这是一个旧 item。",
            category="其他",
            value_score=3,
            personal_relevance=3,
        ),
        ClusteringResult(notification_decision="manual_review", clustering_status="ok"),
    )
    with store.connect() as conn:
        legacy_screening = json.loads(
            conn.execute(
                "SELECT screening_json FROM inbox_items WHERE item_id = ?",
                (legacy_item["item_id"],),
            ).fetchone()["screening_json"]
        )
        legacy_screening.pop("need_matches", None)
        legacy_screening.pop("topic_matches", None)
        conn.execute(
            "UPDATE inbox_items SET screening_json = ? WHERE item_id = ?",
            (json.dumps(legacy_screening, ensure_ascii=False), legacy_item["item_id"]),
        )

    entertainment_response = client.get(
        "/api/inbox?need_id=entertainment&min_need_score=4"
    )
    assert entertainment_response.status_code == 200
    entertainment_body = entertainment_response.json()
    assert entertainment_body["ok"] is True
    assert [item["title"] for item in entertainment_body["items"]] == ["今天刷点轻松的"]
    assert entertainment_body["filters"]["include_silent"] is True
    assert entertainment_body["filters"]["include_ignored"] is True

    frontier_response = client.get("/api/inbox?need_id=frontier&priority=P0&include_silent=true")
    assert frontier_response.status_code == 200
    frontier_body = frontier_response.json()
    assert frontier_body["ok"] is True
    assert [item["title"] for item in frontier_body["items"]] == ["OpenAI Agent SDK ships"]

    topic_response = client.get("/api/inbox?topic_id=ai_agent")
    assert topic_response.status_code == 200
    topic_body = topic_response.json()
    assert topic_body["ok"] is True
    assert [item["title"] for item in topic_body["items"]] == ["OpenAI Agent SDK ships"]
    assert topic_body["filters"]["include_silent"] is True
    assert topic_body["filters"]["include_ignored"] is True

    legacy_response = client.get("/api/inbox?need_id=entertainment&include_silent=true&limit=10")
    assert legacy_response.status_code == 200
    assert legacy_response.json()["ok"] is True
