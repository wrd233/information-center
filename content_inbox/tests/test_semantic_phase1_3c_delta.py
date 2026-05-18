from __future__ import annotations

import json
from pathlib import Path

from app.semantic.signatures import extract_event_signature, is_invalid_product


FIXTURE = Path(__file__).parent / "fixtures" / "semantic_phase1_3c_delta_benchmark.jsonl"


def item(title: str, source_name: str = "api.xgo.ing test") -> dict:
    return {
        "title": title,
        "source_name": source_name,
        "published_at": "2026-05-18T00:00:00+00:00",
    }


def load_delta() -> list[dict]:
    return [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_phase1_3c_garbage_products_are_blocked() -> None:
    garbage = [
        "sow0e7ym",
        "iobqd8a9",
        "CERX3N35",
        "May 4th",
        "June 4th",
        "around 1897",
        "of 12M",
        "a 48-hour",
        "com 1Dl",
        "Git semantics for every file your agent",
        "just built issue was the initial characters",
    ]
    for product in garbage:
        assert is_invalid_product(product), product


def test_phase1_3c_valid_products_survive_validator() -> None:
    valid = [
        "OpenShell v0.0.40",
        "OpenShell v0.0.41",
        "Notion CLI",
        "LangSmith Fleet",
        "GitHub Copilot Desktop",
        "DeepSeek V4",
        "DeepSeek-V4 Preview",
        "Claude Code",
        "QVeris CLI",
        "Stelline Developer Kit",
        "Token calling plan",
        "Googlebook",
    ]
    for product in valid:
        assert not is_invalid_product(product), product


def test_phase1_3c_chinese_event_triggers_are_not_rejected() -> None:
    examples = [
        ("五月惊喜，ColaOS 新模型上线，限时免费尝鲜。记得更新到最新版本。", "ColaOS", "pricing"),
        ("企业里的人+Agent 协作产品 Syncless 发布了", "Syncless", "release"),
        ("开源一个月的时间，飞书 CLI 在 Github 破万星了。", "Feishu CLI", "adoption_metric"),
        ("GitHub 发布了 GitHub Copilot 桌面端的技术预览版。现在需要申请 waitlist", "GitHub Copilot Desktop", "availability"),
    ]
    for title, product, action in examples:
        sig = extract_event_signature(item(title))
        assert sig.semantic_level == "event_signature", title
        assert sig.product_or_model == product
        assert sig.action == action
        assert sig.is_concrete


def test_phase1_3c_chinese_thread_like_items_do_not_become_events() -> None:
    examples = [
        "有位朋友创业做的好好的，又赚钱又开心又不用上班...结果天天被投资人 PUA 说要融资。",
        "李想 × 老罗播客笔记 AI 与一人公司，很多一人公司都在更新内容来验证这个概念成立。",
        "实践是获得真理和获悉真相的唯一途径。",
    ]
    for title in examples:
        sig = extract_event_signature(item(title))
        assert sig.semantic_level in {"thread_signature", "content_signature", "reject"}
        assert not sig.is_concrete


def test_phase1_3c_delta_fixture_is_available() -> None:
    rows = load_delta()
    assert len(rows) == 30
    assert any(row["kind"] == "single_item_chinese_fn" for row in rows)
    assert any(row["kind"] == "single_item_garbage_product" for row in rows)
