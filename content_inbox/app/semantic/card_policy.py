from __future__ import annotations

from typing import Any

from app.semantic.config import CARD_POLICY


def item_text_length(item: dict[str, Any]) -> int:
    return len(" ".join(str(item.get(key) or "") for key in ("title", "summary", "content_text")).strip())


def choose_card_tier(item: dict[str, Any]) -> str:
    text_len = item_text_length(item)
    if text_len <= CARD_POLICY.deterministic_minimal_chars:
        return "minimal"
    if text_len >= CARD_POLICY.long_item_chars:
        return "full"
    return "standard"


def card_limits(tier: str) -> tuple[int, int]:
    if tier == "minimal":
        return CARD_POLICY.minimal_summary_chars, CARD_POLICY.minimal_content_chars
    if tier == "full":
        return CARD_POLICY.full_summary_chars, CARD_POLICY.full_content_chars
    return CARD_POLICY.standard_summary_chars, CARD_POLICY.standard_content_chars


def fallback_classification(*, source: str, reason: str | None = None) -> str:
    reason_text = (reason or "").lower()
    if source == "deterministic_minimal":
        return "fallback_deterministic_minimal"
    if "budget" in reason_text:
        return "fallback_due_to_budget_skip"
    if "json" in reason_text or "validation" in reason_text or "unterminated" in reason_text:
        return "fallback_due_to_llm_parse_error"
    if "empty" in reason_text or "bad input" in reason_text:
        return "fallback_due_to_empty_or_bad_input"
    return "fallback_heuristic"

