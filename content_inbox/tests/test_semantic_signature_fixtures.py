from __future__ import annotations

import json
from pathlib import Path

from app.semantic.signatures import extract_event_signature


FIXTURE = Path(__file__).parent / "fixtures" / "semantic_signature_benchmark_phase1_3b.jsonl"


def load_rows() -> list[dict]:
    return [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines() if line.strip()]


def item_from_fixture(row: dict) -> dict:
    return {
        "item_id": row["item_id"],
        "title": row["title"],
        "summary": "",
        "content_text": "",
        "source_name": row.get("source_name") or "",
        "published_at": "2026-05-17T00:00:00+00:00",
    }


def by_product(rows: list[dict], product: str) -> dict:
    return next(row for row in rows if row.get("expected_product_or_model") == product)


def by_title(rows: list[dict], needle: str) -> dict:
    return next(row for row in rows if needle in row["title"])


def test_phase1_3b_signature_fixture_core_examples() -> None:
    rows = load_rows()
    checks = [
        (by_product(rows, "Googlebook"), "event_signature", "release"),
        (by_product(rows, "Token calling plan"), "event_signature", "pricing"),
        (by_product(rows, "LangSmith Fleet"), "event_signature", "pricing"),
        (by_product(rows, "GitHub Copilot Desktop"), "event_signature", "availability"),
        (by_product(rows, "OpenShell v0.0.40"), "event_signature", "release"),
        (by_product(rows, "OpenShell v0.0.41"), "event_signature", "release"),
    ]
    for row, expected_level, expected_action in checks:
        sig = extract_event_signature(item_from_fixture(row))
        assert sig.semantic_level == expected_level, row["fixture_id"]
        assert sig.action == expected_action, row["fixture_id"]
        assert sig.is_concrete, row["fixture_id"]


def test_phase1_3b_actor_disambiguation() -> None:
    rows = load_rows()
    recursive = extract_event_signature(item_from_fixture(by_product(rows, "Recursive Superintelligence")))
    qveris = extract_event_signature(item_from_fixture(by_product(rows, "QVeris CLI")))
    assert recursive.actor != "Meta"
    assert recursive.actor == "Recursive"
    assert qveris.actor != "Claude"
    assert qveris.actor == "QVeris"


def test_phase1_3b_low_signal_rejects() -> None:
    rows = load_rows()
    for needle in ["Great advice", "Banger", "Concerning."]:
        sig = extract_event_signature(item_from_fixture(by_title(rows, needle)))
        assert sig.semantic_level == "reject"
        assert not sig.is_concrete


def test_configured_alias_registry_normalizes_actor_product_action() -> None:
    sig = extract_event_signature(
        {
            "item_id": "alias-gpt-55",
            "title": "OpenAI makes GPT 5.5 now available to coding teams",
            "summary": "",
            "content_text": "",
            "source_name": "Fixture",
            "published_at": "2026-05-17T00:00:00+00:00",
        }
    )

    assert sig.semantic_level == "event_signature"
    assert sig.actor == "OpenAI"
    assert sig.product_or_model == "GPT-5.5"
    assert sig.action == "availability"
    assert sig.signature_key == "openai|gpt55|availability|2026-05-17"
    assert {"type": "product", "alias": "GPT 5.5", "canonical": "GPT-5.5"} in sig.alias_hits


def test_operational_v3_recall_repair_signature_phrasing() -> None:
    cases = [
        (
            "OpenAI rolls out GPT-5.5 model aimed at coding agents",
            "OpenAI rolled out GPT-5.5 for coding agents with enterprise controls.",
            ("OpenAI", "GPT-5.5", "release", "openai|gpt55|release|2026-05-30"),
        ),
        (
            "DeepSeek 发布 V4.1 模型，推理延迟下降",
            "DeepSeek 发布 V4.1 模型，降低推理延迟。",
            ("DeepSeek", "DeepSeek V4", "release", "deepseek|deepseekv4|release|2026-05-30"),
        ),
        (
            "Anthropic raises $2B at $60B valuation",
            "Anthropic raised $2B at a $60B valuation from strategic investors.",
            ("Anthropic", "Funding round $2B", "funding", "anthropic|fundinground2b|funding|2026-05-30"),
        ),
        (
            "European Commission issues AI Act guidance for model providers",
            "The European Commission issued AI Act guidance for model providers.",
            ("European Commission", "AI Act", "policy", "europeancommission|aiact|policy|2026-05-30"),
        ),
    ]
    for title, summary, expected in cases:
        sig = extract_event_signature(
            {
                "item_id": title,
                "title": title,
                "summary": summary,
                "content_text": "",
                "source_name": "Fixture",
                "published_at": "2026-05-30T10:00:00+00:00",
            }
        )
        assert (sig.actor, sig.product_or_model, sig.action, sig.signature_key) == expected
        assert sig.semantic_level == "event_signature"
        assert sig.is_concrete


def test_phase1_3b_invalid_products_are_not_accepted() -> None:
    rows = load_rows()
    for row in rows:
        sig = extract_event_signature(item_from_fixture(row))
        forbidden = {str(value).lower() for value in row.get("must_not_extract_as_product") or []}
        assert sig.product_or_model.lower() not in forbidden, row["fixture_id"]
        assert not any(reason.startswith("invalid_product") for reason in sig.invalid_reasons), row["fixture_id"]


def test_phase1_3b_semantic_levels_match_benchmark_without_overfitting() -> None:
    rows = load_rows()
    matches = 0
    for row in rows:
        sig = extract_event_signature(item_from_fixture(row))
        if sig.semantic_level == row["expected_semantic_level"]:
            matches += 1
    assert matches / len(rows) >= 0.85
