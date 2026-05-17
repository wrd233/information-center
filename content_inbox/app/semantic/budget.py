from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.semantic.config import STAGE_BUDGET_PROFILES
from app.storage import InboxStore


@dataclass(frozen=True)
class BudgetPolicy:
    total_budget: int = 0
    stage_profile: str = "phase1_3_advisory"
    enforce_hard_cap: bool = False

    @property
    def stage_budgets(self) -> dict[str, int]:
        if self.total_budget <= 0:
            return {}
        ratios = STAGE_BUDGET_PROFILES.get(self.stage_profile, STAGE_BUDGET_PROFILES["phase1_3_advisory"])
        return {stage: int(self.total_budget * ratio) for stage, ratio in ratios.items()}


def tokens_used(store: InboxStore) -> int:
    with store.connect() as conn:
        row = conn.execute("SELECT COALESCE(SUM(total_tokens), 0) AS n FROM llm_call_logs WHERE status = 'ok'").fetchone()
    return int(row["n"] or 0)


def stage_token_cap(store: InboxStore, policy: BudgetPolicy, stage: str) -> int | None:
    if not policy.enforce_hard_cap:
        return None
    budget = policy.stage_budgets.get(stage)
    if not budget:
        return None
    return tokens_used(store) + budget


def quality_skip_tier(priority: str | None, stage: str) -> str:
    if priority == "must_run":
        return "skipped_must_run_candidates"
    if priority == "high":
        return "skipped_high_priority_candidates"
    if priority == "medium":
        return "skipped_medium_priority_candidates"
    if stage == "item_card":
        return "skipped_item_card"
    return "skipped_low_score_candidates"


def summarize_budget_skips(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_stage: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    must_run = 0
    for row in rows:
        stage = str(row.get("stage") or "unknown")
        priority = str(row.get("candidate_priority") or "unknown")
        by_stage[stage] = by_stage.get(stage, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
        if "must_run" in priority:
            must_run += 1
    return {"by_stage": by_stage, "by_priority": by_priority, "must_run_skip_count": must_run, "total": len(rows)}

