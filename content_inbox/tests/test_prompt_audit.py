"""Tests for prompt audit/debug feature.

Run with: PYTHONPATH=. pytest tests/test_prompt_audit.py -q
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import settings
from app.models import ContentAnalyzeRequest
from app.processor import normalize_content
from app.screener import (
    _set_dump_prompt_context,
    audit_prompt_messages,
    audit_screen_content,
    build_prompt_messages,
    configure_llm_dump,
    prompt_output_contract,
    set_dump_item_context,
)
from app.server import app, get_store
from app.storage import InboxStore


def make_client(tmp_path: Path) -> TestClient:
    store = InboxStore(tmp_path / "audit_test.sqlite3")
    app.dependency_overrides[get_store] = lambda: store
    return TestClient(app)


# ---------------------------------------------------------------------------
# Test 1: audit does not call real LLM
# ---------------------------------------------------------------------------


def test_audit_does_not_call_llm():
    nc = normalize_content(
        ContentAnalyzeRequest(
            title="Test Article",
            summary="A test summary.",
            source_name="Test Source",
            content_text="Some content text for testing.",
            url="https://example.com/test",
        )
    )
    records = audit_screen_content(nc)
    assert len(records) >= 1
    for record in records:
        assert record["audit_type"] == "prompt_audit"
        # No LLM response artifacts
        assert "_raw_response" not in record
        assert "model" not in record


# ---------------------------------------------------------------------------
# Test 2: audit outputs basic_screening length stats
# ---------------------------------------------------------------------------


def test_audit_basic_screening_length_stats():
    nc = normalize_content(
        ContentAnalyzeRequest(
            title="AI Agents in Production",
            summary="A comprehensive guide to deploying AI agents.",
            source_name="AI Weekly",
            source_category="Articles/AI",
            content_text="This is the full article text. " * 100,
            url="https://example.com/ai-agents",
        )
    )
    records = audit_screen_content(nc)

    basic_records = [r for r in records if r["prompt_name"] == "basic_screening"]
    assert len(basic_records) == 1
    r = basic_records[0]

    assert r["system_chars"] > 0
    assert r["user_chars"] > 0
    assert r["total_chars"] == r["system_chars"] + r["user_chars"]
    assert r["estimated_tokens"] == math.ceil(r["total_chars"] / 4)
    assert r["content_text_chars"] > 0
    assert r["categories_chars"] > 0
    assert r["output_contract_chars"] > 0
    assert isinstance(r["longest_fields"], list)
    assert len(r["longest_fields"]) > 0


# ---------------------------------------------------------------------------
# Test 3: audit output does not contain full content_text
# ---------------------------------------------------------------------------


def test_audit_does_not_contain_full_text():
    long_text = "Word " * 2000
    nc = normalize_content(
        ContentAnalyzeRequest(
            title="Long Article",
            summary="A long article about something.",
            source_name="Test",
            content_text=long_text,
        )
    )
    records = audit_screen_content(nc)

    for record in records:
        preview = record.get("preview", {})
        cp = preview.get("content_preview", "")
        sp = preview.get("summary_preview", "")
        tp = preview.get("title", "")
        assert len(cp) <= 300, f"content_preview too long: {len(cp)}"
        assert len(sp) <= 200, f"summary_preview too long: {len(sp)}"
        assert len(tp) <= 200, f"title preview too long: {len(tp)}"

        # Full content_text must not appear verbatim in the record
        record_str = json.dumps(record, ensure_ascii=False)
        # Preview truncates, so only first ~50 words appear; verify the 2000-word string is not present
        assert long_text.strip() not in record_str


# ---------------------------------------------------------------------------
# Test 4: audit counts URLs / HTML tags / Markdown links / image URLs
# ---------------------------------------------------------------------------


def test_audit_counts_urls_html_tags_markdown():
    rich_text = (
        "Check https://example.com and http://test.org for details. "
        '<a href="https://example.com">click</a> '
        "<p>Some paragraph</p> "
        "<div>Wrapper</div> "
        "[link](https://example.com/page) "
        "Image: https://cdn.example.com/photo.jpg?w=800 "
        "https://cdn.example.com/photo.png "
    )
    input_data = {
        "content": {
            "content_text": rich_text,
            "summary": "Summary with https://link.org",
            "title": "Title",
        },
        "categories": [],
    }
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Analyze: " + json.dumps(input_data, ensure_ascii=False)},
    ]
    record = audit_prompt_messages("basic_screening", messages, input_data)

    assert record["url_count"] >= 6
    assert record["html_tag_count"] >= 2
    assert record["markdown_link_count"] >= 1
    assert record["image_url_count"] >= 2


# ---------------------------------------------------------------------------
# Test 5: normal flow unchanged when audit_prompt absent
# ---------------------------------------------------------------------------


def test_normal_flow_without_audit_flag(tmp_path: Path):
    client = make_client(tmp_path)
    response = client.post(
        "/api/content/analyze",
        json={
            "title": "Normal Article",
            "summary": "This should not trigger audit.",
            "source_name": "Test",
            "screen": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body.get("audit_type") != "prompt_audit"
    assert "screening" in body
    assert body["screening"]["screening_method"] is not None


# ---------------------------------------------------------------------------
# Test 6: build_prompt_messages identical between paths
# ---------------------------------------------------------------------------


def test_build_prompt_messages_identical():
    nc = normalize_content(
        ContentAnalyzeRequest(
            title="Test Article",
            summary="Test summary.",
            source_name="Test",
            content_text="Test content.",
            url="https://example.com/test",
        )
    )
    content_payload = nc.model_dump()
    content_payload["content_text"] = nc.content_text or ""

    basic_input = {
        "content": content_payload,
        "categories": settings.screening.get("categories", []),
    }
    contract = prompt_output_contract("basic_screening")
    messages = build_prompt_messages("basic_screening", basic_input, contract)

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "{" in messages[1]["content"]  # JSON was injected


# ---------------------------------------------------------------------------
# Test 7: audit via /api/content/analyze endpoint
# ---------------------------------------------------------------------------


def test_audit_via_api_endpoint(tmp_path: Path):
    client = make_client(tmp_path)
    response = client.post(
        "/api/content/analyze",
        json={
            "title": "Audit Test Article",
            "summary": "Testing audit mode via API.",
            "source_name": "Test",
            "content_text": "Article body with https://example.com link.",
            "screen": True,
            "audit_prompt": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["audit_type"] == "prompt_audit"
    assert len(body["audit_records"]) >= 1
    for record in body["audit_records"]:
        assert record["audit_type"] == "prompt_audit"
        assert isinstance(record["total_chars"], int)
        assert record["total_chars"] > 0

    # Verify no items were stored
    inbox = client.get("/api/inbox?include_silent=true&limit=10")
    assert inbox.status_code == 200
    assert len(inbox.json()["items"]) == 0


# ---------------------------------------------------------------------------
# Test 8: audit via /api/rss/analyze endpoint
# ---------------------------------------------------------------------------


def test_audit_rss_via_api(tmp_path: Path):
    client = make_client(tmp_path)
    feed_path = Path(__file__).parent / "sample_feed.xml"

    response = client.post(
        "/api/rss/analyze",
        json={
            "feed_url": feed_path.as_uri(),
            "source_category": "Articles/AI",
            "limit": 2,
            "screen": True,
            "audit_prompt": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["audit_type"] == "prompt_audit"
    assert body["total_items"] >= 1
    assert len(body["audit_records"]) >= 1
    for record in body["audit_records"]:
        assert record["prompt_name"] in (
            "basic_screening",
            "need_matching",
            "screen_and_match",
        )

    # Verify no items were stored
    inbox = client.get("/api/inbox?include_silent=true&limit=10")
    assert inbox.status_code == 200
    assert len(inbox.json()["items"]) == 0


# ---------------------------------------------------------------------------
# Dump LLM prompt tests (--dump-llm-prompt)
# ---------------------------------------------------------------------------


def test_dump_disabled_by_default(tmp_path: Path):
    """When not enabled, no dump files are created."""
    dump_dir = tmp_path / "dumps"
    dump_dir.mkdir()
    configure_llm_dump(enabled=False, output_dir=str(dump_dir))

    set_dump_item_context(source_name="Test", item_title="Test Item")
    _set_dump_prompt_context("basic_screening", "two_stage_stage1")

    from app.screener import _dump_llm_body
    _dump_llm_body({"model": "test", "messages": [{"role": "system", "content": "hello"}]})

    files = list(dump_dir.glob("*.json"))
    assert len(files) == 0

    configure_llm_dump(enabled=False)


def test_dump_creates_files(tmp_path: Path):
    """When enabled, dump creates a JSON file with request_body."""
    dump_dir = tmp_path / "dumps"
    configure_llm_dump(enabled=True, output_dir=str(dump_dir))

    set_dump_item_context(
        source_name="Test Source",
        source_url="https://example.com",
        item_title="Test Item",
        item_url="https://example.com/item",
    )
    _set_dump_prompt_context("basic_screening", "two_stage_stage1")

    body = {
        "model": "test-model",
        "temperature": 0.2,
        "max_tokens": 1200,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": '{"content": {"title": "Hello"}}'},
        ],
        "response_format": {"type": "json_object"},
    }

    from app.screener import _dump_llm_body
    _dump_llm_body(body)

    files = sorted(dump_dir.glob("*.json"))
    assert len(files) == 1

    content = json.loads(files[0].read_text(encoding="utf-8"))
    assert content["dump_type"] == "llm_request_body"
    assert content["exact_api_payload"] is True
    assert content["prompt_name"] == "basic_screening"
    assert content["stage"] == "two_stage_stage1"
    assert content["source_name"] == "Test Source"
    assert content["request_body"]["model"] == "test-model"
    assert len(content["request_body"]["messages"]) == 2
    assert "stats" in content

    configure_llm_dump(enabled=False)


def test_dump_no_auth_in_file(tmp_path: Path):
    """Dump files must never contain Authorization headers or API key patterns."""
    dump_dir = tmp_path / "dumps"
    configure_llm_dump(enabled=True, output_dir=str(dump_dir))

    set_dump_item_context(source_name="Test", item_title="Test")
    _set_dump_prompt_context("basic_screening", "two_stage_stage1")

    body = {
        "model": "test-model",
        "messages": [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "User content with sk-abc123def456ghi789jkl012mno345pqr678stu901vwx"},
        ],
    }

    from app.screener import _dump_llm_body
    _dump_llm_body(body)

    files = sorted(dump_dir.glob("*.json"))
    raw_text = files[0].read_text(encoding="utf-8")

    assert "authorization" not in raw_text.lower()
    assert "Bearer" not in raw_text
    content = json.loads(raw_text)
    user_content = content["request_body"]["messages"][1]["content"]
    assert "sk-abc" not in user_content

    configure_llm_dump(enabled=False)


def test_dump_two_stage_creates_both_files(tmp_path: Path):
    """Two-stage mode produces basic_screening and need_matching dump files."""
    dump_dir = tmp_path / "dumps"
    configure_llm_dump(enabled=True, output_dir=str(dump_dir))

    set_dump_item_context(source_name="Test", item_title="Two Stage Test")

    from app.screener import _dump_llm_body

    _set_dump_prompt_context("basic_screening", "two_stage_stage1")
    _dump_llm_body({
        "model": "test",
        "messages": [
            {"role": "system", "content": "Basic screening system"},
            {"role": "user", "content": "Stage 1 input"},
        ],
    })

    _set_dump_prompt_context("need_matching", "two_stage_stage2")
    _dump_llm_body({
        "model": "test",
        "messages": [
            {"role": "system", "content": "Need matching system"},
            {"role": "user", "content": "Stage 2 input with real basic_screening data"},
        ],
    })

    files = sorted(dump_dir.glob("*.json"))
    assert len(files) == 2
    assert "basic_screening" in files[0].name
    assert "need_matching" in files[1].name

    stage2 = json.loads(files[1].read_text(encoding="utf-8"))
    assert stage2["stage"] == "two_stage_stage2"
    assert "real basic_screening" in stage2["request_body"]["messages"][1]["content"]

    configure_llm_dump(enabled=False)


def test_dump_via_api_endpoint(tmp_path: Path):
    """API endpoint with dump_llm_prompt=True handles the flag without errors."""
    client = make_client(tmp_path)
    dump_dir = tmp_path / "dumps"

    response = client.post(
        "/api/content/analyze",
        json={
            "title": "Dump Test Article",
            "summary": "Testing LLM dump mode.",
            "source_name": "Dump Test",
            "content_text": "Article content for dump test.",
            "screen": False,
            "dump_llm_prompt": True,
            "dump_llm_prompt_dir": str(dump_dir),
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert dump_dir.exists()
