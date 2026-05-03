from __future__ import annotations

import threading
import time
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.clusterer import cluster_content
from app.models import ContentAnalyzeRequest, NormalizedContent, ProcessResult, ScreeningResult
from app.screener import apply_score_policy
from app.rss_runner import sort_entries_for_processing
from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> TestClient:
    store = InboxStore(tmp_path / "inbox.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app)


def test_content_analyze_deduplicates_without_rescreening(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    payload = {
        "url": "https://example.com/article#fragment",
        "title": "AI Agent 自动化实践",
        "source_name": "Manual",
        "source_category": "Articles/AI",
        "summary": "介绍 AI Agent 如何帮助个人信息管理。",
        "screen": False,
    }

    first = client.post("/api/content/analyze", json=payload)
    second = client.post("/api/content/analyze", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    first_body = first.json()
    second_body = second.json()
    assert first_body["is_duplicate"] is False
    assert second_body["is_duplicate"] is True
    assert first_body["item_id"] == second_body["item_id"]
    assert first_body["screening"]["screening_method"] == "none"


def test_rss_analyze_and_query_inbox(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    feed_path = Path(__file__).parent / "sample_feed.xml"

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": feed_path.as_uri(),
            "source_category": "Articles/AI",
            "limit": 2,
            "screen": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["total_items"] == 2
    assert body["new_items"] == 2

    inbox = client.get("/api/inbox?min_score=3&include_silent=true&limit=10")
    assert inbox.status_code == 200
    inbox_body = inbox.json()
    assert inbox_body["ok"] is True
    assert len(inbox_body["items"]) == 2
    assert inbox_body["items"][0]["screening"]["suggested_action"] == "review"


def test_rss_analyze_batch_processes_multiple_sources(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        entries = [
            ContentAnalyzeRequest(
                url=f"{feed_url}/1",
                title=f"{feed_url}-1",
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-01T00:00:00+00:00",
                screen=False,
            ),
            ContentAnalyzeRequest(
                url=f"{feed_url}/2",
                title=f"{feed_url}-2",
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-02T00:00:00+00:00",
                screen=False,
            ),
        ]
        return {"source_name": source_name or feed_url}, entries

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {"source_id": "s1", "feed_url": "feed-a", "source_name": "A"},
                {"source_id": "s2", "feed_url": "feed-b", "source_name": "B"},
            ],
            "limit_per_source": 2,
            "screen": False,
            "max_concurrent_sources": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["total_sources"] == 2
    assert body["successful_sources"] == 2
    assert body["failed_sources"] == 0
    assert body["partial_failed_sources"] == 0
    assert body["total_items"] == 4
    assert body["new_items"] == 4
    assert [item["source_id"] for item in body["source_results"]] == ["s1", "s2"]
    assert [item["feed_url"] for item in body["source_results"]] == ["feed-a", "feed-b"]


def test_rss_batch_honors_max_concurrent_sources_serial(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        return {"source_name": source_name or feed_url}, [
            ContentAnalyzeRequest(
                url=f"{feed_url}/1",
                title=feed_url,
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-01T00:00:00+00:00",
                screen=False,
            )
        ]

    def fake_process(store: InboxStore, payload: ContentAnalyzeRequest, raw: dict | None = None):
        nonlocal active, max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        return make_process_result(payload)

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)
    monkeypatch.setattr("app.rss_runner.process_content_thread_safe", fake_process)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {"source_id": "s1", "feed_url": "feed-a"},
                {"source_id": "s2", "feed_url": "feed-b"},
                {"source_id": "s3", "feed_url": "feed-c"},
            ],
            "screen": False,
            "max_concurrent_sources": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["successful_sources"] == 3
    assert max_active == 1


def test_rss_batch_runs_sources_concurrently(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)
    active = 0
    max_active = 0
    lock = threading.Lock()

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        return {"source_name": source_name or feed_url}, [
            ContentAnalyzeRequest(
                url=f"{feed_url}/1",
                title=feed_url,
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-01T00:00:00+00:00",
                screen=False,
            )
        ]

    def fake_process(store: InboxStore, payload: ContentAnalyzeRequest, raw: dict | None = None):
        nonlocal active, max_active
        with lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        return make_process_result(payload)

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)
    monkeypatch.setattr("app.rss_runner.process_content_thread_safe", fake_process)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {"source_id": "s1", "feed_url": "feed-a"},
                {"source_id": "s2", "feed_url": "feed-b"},
                {"source_id": "s3", "feed_url": "feed-c"},
            ],
            "screen": False,
            "max_concurrent_sources": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["successful_sources"] == 3
    assert max_active >= 2


def test_sort_entries_for_processing_orders_dated_entries_and_keeps_undated_stable() -> None:
    entries = [
        ContentAnalyzeRequest(title="new", summary="1", published_at="2024-01-03T00:00:00+00:00"),
        ContentAnalyzeRequest(title="undated-a", summary="2"),
        ContentAnalyzeRequest(title="old", summary="3", published_at="2024-01-01T00:00:00+00:00"),
        ContentAnalyzeRequest(title="undated-b", summary="4"),
    ]

    ordered = sort_entries_for_processing(entries)

    assert [entry.title for entry in ordered] == ["old", "new", "undated-a", "undated-b"]


def test_rss_batch_source_failure_does_not_block_other_sources(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        if feed_url == "bad-feed":
            raise ValueError("boom")
        return {"source_name": source_name or feed_url}, [
            ContentAnalyzeRequest(
                url=f"{feed_url}/1",
                title=feed_url,
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-01T00:00:00+00:00",
                screen=False,
            )
        ]

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {"source_id": "bad", "feed_url": "bad-feed"},
                {"source_id": "good", "feed_url": "good-feed"},
            ],
            "screen": False,
            "max_concurrent_sources": 2,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["failed_sources"] == 1
    assert body["successful_sources"] == 1
    assert body["source_results"][0]["source_id"] == "bad"
    assert body["source_results"][0]["error"] == "boom"
    assert body["source_results"][1]["source_id"] == "good"
    assert body["source_results"][1]["new_items"] == 1


def test_rss_analyze_entry_failure_does_not_stop_later_entries(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)
    seen_titles: list[str] = []

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        return {"source_name": source_name or feed_url}, [
            ContentAnalyzeRequest(title="first", summary="1", source_name="src", screen=False),
            ContentAnalyzeRequest(title="second", summary="2", source_name="src", screen=False),
        ]

    def fake_process(store: InboxStore, payload: ContentAnalyzeRequest, raw: dict | None = None):
        seen_titles.append(payload.title or "")
        if payload.title == "first":
            raise RuntimeError("first failed")
        return make_process_result(payload)

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)
    monkeypatch.setattr("app.rss_runner.process_content_thread_safe", fake_process)

    response = client.post(
        "/api/rss/analyze",
        json={"feed_url": "feed-a", "screen": False},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["ok"] is False
    assert body["failed_items"] == 1
    assert body["new_items"] == 1
    assert seen_titles == ["first", "second"]


def test_rss_batch_preserves_input_source_order(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        if feed_url == "feed-a":
            time.sleep(0.05)
        return {"source_name": source_name or feed_url}, [
            ContentAnalyzeRequest(
                url=f"{feed_url}/1",
                title=feed_url,
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-01T00:00:00+00:00",
                screen=False,
            )
        ]

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {"source_id": "first", "feed_url": "feed-a"},
                {"source_id": "second", "feed_url": "feed-b"},
            ],
            "screen": False,
            "max_concurrent_sources": 2,
        },
    )

    assert response.status_code == 200
    assert [result["source_id"] for result in response.json()["source_results"]] == [
        "first",
        "second",
    ]


def test_rss_batch_duplicate_urls_do_not_raise_unique_constraint(tmp_path: Path, monkeypatch) -> None:
    client = make_client(tmp_path)

    def fake_parse_feed(feed_url: str, source_name: str | None = None, **_: object):
        return {"source_name": source_name or feed_url}, [
            ContentAnalyzeRequest(
                url="https://example.com/shared",
                title=f"{feed_url}-title",
                source_name=source_name or feed_url,
                summary="summary",
                published_at="2024-01-01T00:00:00+00:00",
                screen=False,
            )
        ]

    monkeypatch.setattr("app.rss_runner.parse_feed", fake_parse_feed)

    response = client.post(
        "/api/rss/analyze-batch",
        json={
            "sources": [
                {"source_id": "s1", "feed_url": "feed-a"},
                {"source_id": "s2", "feed_url": "feed-b"},
            ],
            "screen": False,
            "max_concurrent_sources": 2,
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["failed_sources"] == 0
    assert body["partial_failed_sources"] == 0
    assert body["new_items"] == 1
    assert body["duplicate_items"] == 1
    assert all("UNIQUE constraint failed" not in str(item) for item in body["source_results"])


def test_screen_true_without_key_is_saved_for_manual_review(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    old_key = settings.openai_api_key
    old_env = settings.llm["api_key_env"]
    settings.llm["api_key_env"] = "__MISSING_CONTENT_INBOX_TEST_KEY__"
    settings.openai_api_key = ""
    try:
        response = client.post(
            "/api/content/analyze",
            json={
                "title": "需要模型粗筛的内容",
                "summary": "没有 API key 时不应该走本地粗筛。",
                "screen": True,
            },
        )
    finally:
        settings.openai_api_key = old_key
        settings.llm["api_key_env"] = old_env
    assert response.status_code == 200
    body = response.json()
    assert body["screening"]["screening_status"] == "failed"
    assert body["screening"]["suggested_action"] == "review"
    assert body["screening"]["followup_type"] == "manual_review"
    assert body["clustering"]["cluster_relation"] == "skipped_low_value"


def test_score_policy_corrects_model_action() -> None:
    screening = ScreeningResult(
        summary="重要工具发布",
        category="AI工具",
        value_score=5,
        personal_relevance=5,
        novelty_score=5,
        source_quality=4,
        actionability=4,
        hidden_signals=["工具链正在 API 化"],
        entities=["Cursor"],
        event_hint="Cursor 发布新的 Agent SDK",
        suggested_action="skim",
        followup_type="none",
        reason="模型先给了轻量建议",
        tags=["Cursor"],
        confidence=0.9,
        screening_method="ai",
        screening_status="ok",
    )
    corrected = apply_score_policy(
        screening,
        NormalizedContent(
            title="Cursor SDK",
            source_name="Test",
            source_category="AI",
            content_type="article",
        ),
    )
    assert corrected.suggested_action == "save"
    assert corrected.followup_type == "archive"


def test_cluster_content_creates_new_event(tmp_path: Path, monkeypatch) -> None:
    store = InboxStore(tmp_path / "cluster.sqlite3")
    normalized = NormalizedContent(
        title="OpenAI 发布 Agent SDK",
        source_name="Test",
        source_category="Articles/AI",
        content_type="article",
        summary="OpenAI 发布面向开发者的 Agent SDK。",
    )
    screening = ScreeningResult(
        summary="OpenAI 发布面向开发者的 Agent SDK。",
        category="AI工具",
        value_score=4,
        personal_relevance=4,
        novelty_score=4,
        source_quality=4,
        actionability=4,
        hidden_signals=["Agent 工具链继续 API 化"],
        entities=["OpenAI", "Agent SDK"],
        event_hint="OpenAI 发布 Agent SDK",
        suggested_action="save",
        followup_type="archive",
        reason="值得跟进",
        tags=["OpenAI", "Agent"],
        confidence=0.9,
        screening_method="ai",
        screening_status="ok",
    )
    inserted = store.insert("dedupe:test", normalized, screening)
    monkeypatch.setattr("app.clusterer.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr(store, "search_active_clusters", lambda vector, top_k: [])

    clustering = cluster_content(store, inserted["item_id"], normalized, screening)

    assert clustering.cluster_relation == "new_event"
    assert clustering.notification_decision == "full_push"
    assert clustering.cluster_id
    assert clustering.embedding_text


def test_cluster_content_new_event_score_three_defaults_to_silent(tmp_path: Path, monkeypatch) -> None:
    store = InboxStore(tmp_path / "cluster_score3.sqlite3")
    normalized = NormalizedContent(
        title="普通但相关的新事件",
        source_name="Test",
        source_category="Articles/AI",
        content_type="article",
        summary="这是一个分数为 3 的新事件。",
    )
    screening = ScreeningResult(
        summary="这是一个分数为 3 的新事件。",
        category="AI工具",
        value_score=3,
        personal_relevance=3,
        novelty_score=3,
        source_quality=3,
        actionability=3,
        hidden_signals=[],
        entities=["Example"],
        event_hint="一个分数为3的新事件",
        suggested_action="skim",
        followup_type="none",
        reason="中等价值",
        tags=["Example"],
        confidence=0.9,
        screening_method="ai",
        screening_status="ok",
    )
    inserted = store.insert("dedupe:test:score3", normalized, screening)
    monkeypatch.setattr("app.clusterer.embed_text", lambda text: [0.1, 0.2, 0.3])
    monkeypatch.setattr(store, "search_active_clusters", lambda vector, top_k: [])

    clustering = cluster_content(store, inserted["item_id"], normalized, screening)

    assert clustering.cluster_relation == "new_event"
    assert clustering.notification_decision == "silent"


def make_process_result(payload: ContentAnalyzeRequest) -> ProcessResult:
    normalized = NormalizedContent(
        title=payload.title or payload.url or "Untitled",
        url=payload.url,
        source_name=payload.source_name or "Unknown",
        source_category=payload.source_category,
        content_type=payload.content_type or "unknown",
        published_at=payload.published_at,
        author=payload.author,
        summary=payload.summary,
        content_text=payload.content_text,
        guid=payload.guid,
    )
    screening = ScreeningResult(
        summary=payload.summary or payload.title or "summary",
        category="其他",
        value_score=3,
        personal_relevance=3,
        novelty_score=3,
        source_quality=3,
        actionability=3,
        suggested_action="review",
        followup_type="manual_review",
        reason="test",
        screening_method="none",
        screening_status="ok",
    )
    return ProcessResult(
        item_id=f"item-{payload.title or payload.url or 'x'}",
        is_duplicate=False,
        normalized=normalized,
        screening=screening,
        notification_decision="silent",
        cluster_relation="disabled",
        incremental_summary="",
    )
