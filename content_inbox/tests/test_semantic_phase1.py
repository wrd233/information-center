from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from app.models import NormalizedContent, ScreeningResult
from app.semantic.cards import generate_item_cards
from app.semantic.clusters import process_item_clusters, show_cluster, update_cluster_statuses
from app.semantic.clusters import candidate_clusters
from app.semantic.evaluate import run_evaluation
from app.semantic.live_smoke import run_live_smoke
from app.semantic.relations import process_item_relations
from app.semantic.review import decide_review, list_reviews
from app.semantic.schemas import cluster_relation_action, item_relation_should_fold
from app.semantic.source_profiles import get_profile, recompute_source_profiles
from app.storage import InboxStore


def make_store(tmp_path: Path) -> InboxStore:
    return InboxStore(tmp_path / "semantic.sqlite3")


def seed_item(store: InboxStore, title: str, *, source_id: str = "source-a", url: str | None = None) -> str:
    screening = ScreeningResult(
        summary=f"Summary for {title}",
        category="AI前沿",
        value_score=4,
        personal_relevance=4,
        suggested_action="read",
        reason="test",
        screening_method="none",
    )
    normalized = NormalizedContent(
        title=title,
        url=url,
        source_id=source_id,
        source_name=source_id,
        content_type="article",
        summary=f"{title} summary",
    )
    row = store.insert(f"dedupe-{title}-{url}", normalized, screening, raw={"title": title})
    return row["item_id"]


def test_semantic_migration_idempotent(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    store.init_schema()
    with store.connect() as conn:
        tables = {row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(inbox_items)")}
    assert {"item_cards", "item_relations", "cluster_items", "cluster_cards", "source_profiles", "llm_call_logs", "review_queue"} <= tables
    assert {"semantic_status", "primary_cluster_id", "semantic_attempts", "last_semantic_at"} <= columns


def test_relation_action_mapping() -> None:
    assert item_relation_should_fold("duplicate") is True
    assert item_relation_should_fold("related_with_new_info") is False
    assert cluster_relation_action("source_material") == "attach_update_card"
    assert cluster_relation_action("new_info") == "attach_update_card"
    assert cluster_relation_action("same_topic") == "do_not_attach"


def test_item_card_generation_heuristic_and_llm_log_skip(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    item_id = seed_item(store, "OpenAI releases GPT-5.5", url="https://example.com/a")
    result = generate_item_cards(store, limit=10, live=False)
    assert result["ok"] is True
    with store.connect() as conn:
        card = conn.execute("SELECT * FROM item_cards WHERE item_id = ?", (item_id,)).fetchone()
        log = conn.execute("SELECT * FROM llm_call_logs WHERE task_type = 'item_card'").fetchone()
    assert card is not None
    assert card["is_current"] == 1
    assert log["status"] == "skipped"


def test_item_relation_rule_duplicate(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    seed_item(store, "Same title", url="https://example.com/a")
    second = seed_item(store, "Same title", url="https://example.com/b")
    generate_item_cards(store, limit=10)
    result = process_item_relations(store, limit=10, live=False)
    assert result["ok"] is True
    with store.connect() as conn:
        rows = conn.execute("SELECT * FROM item_relations").fetchall()
        folded = conn.execute("SELECT semantic_status FROM inbox_items WHERE item_id = ?", (second,)).fetchone()
    assert rows
    assert any(row["primary_relation"] in {"duplicate", "near_duplicate"} for row in rows)
    assert folded["semantic_status"] in {"folded", "carded"}


def test_cluster_create_and_card_patch(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    seed_item(store, "OpenAI releases GPT-5.5", url="https://example.com/a")
    generate_item_cards(store, limit=10)
    result = process_item_clusters(store, limit=10, live=False)
    assert result["ok"] is True
    with store.connect() as conn:
        cluster = conn.execute("SELECT * FROM event_clusters").fetchone()
        cluster_item = conn.execute("SELECT * FROM cluster_items").fetchone()
        cluster_card = conn.execute("SELECT * FROM cluster_cards").fetchone()
    assert cluster is not None
    assert cluster_item is not None
    assert cluster_card is not None
    shown = show_cluster(store, cluster["cluster_id"])
    assert shown and shown["cluster_card"]


def test_source_profile_review_approve(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    seed_item(store, "OpenAI releases GPT-5.5", source_id="valuable", url="https://example.com/a")
    generate_item_cards(store, limit=10)
    process_item_clusters(store, limit=10, live=False)
    result = recompute_source_profiles(store)
    assert result["ok"] is True
    profile = get_profile(store, "valuable")
    assert profile is not None
    reviews = list_reviews(store)
    if reviews:
        decided = decide_review(store, reviews[0]["id"], "approved")
        assert decided["ok"] is True


def test_cluster_lifecycle_update(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    seed_item(store, "Old event", url="https://example.com/old")
    generate_item_cards(store, limit=10)
    process_item_clusters(store, limit=10, live=False)
    with store.connect() as conn:
        conn.execute("UPDATE event_clusters SET last_seen_at = '2000-01-01T00:00:00+00:00', last_major_update_at = '2000-01-01T00:00:00+00:00'")
    result = update_cluster_statuses(store)
    assert result["ok"] is True


def test_semantic_cli_smoke(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    seed_item(store, "CLI semantic item", url="https://example.com/cli")
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "content_inbox.semantic",
            "--db-path",
            str(store.database_path),
            "cards",
            "--limit",
            "5",
        ],
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "PYTHONPATH": "."},
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True


def test_live_smoke_disabled_skips(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CONTENT_INBOX_LLM_ENABLE_LIVE", raising=False)
    result = run_live_smoke("item-card", limit=1, db_path=str(tmp_path / "x.sqlite3"))
    assert result["skipped"] is True


def test_source_profile_token_attribution_not_global(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    first = seed_item(store, "First source item", source_id="source-one", url="https://example.com/1")
    second = seed_item(store, "Second source item", source_id="source-two", url="https://example.com/2")
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO llm_call_logs (
                task_type, model, input_fingerprint, status, total_tokens,
                source_id, created_at, updated_at
            )
            VALUES ('item_relation', 'test', 'fp1', 'ok', 123, 'source-one', 'now', 'now')
            """
        )
        conn.execute(
            """
            INSERT INTO llm_call_logs (
                task_type, model, input_fingerprint, status, total_tokens,
                item_id, created_at, updated_at
            )
            VALUES ('item_cluster_relation', 'test', 'fp2', 'ok', 50, ?, 'now', 'now')
            """,
            (first,),
        )
        conn.execute(
            """
            INSERT INTO llm_call_logs (
                task_type, model, input_fingerprint, status, total_tokens,
                created_at, updated_at
            )
            VALUES ('item_card', 'test', 'global', 'ok', 999, 'now', 'now')
            """
        )
    recompute_source_profiles(store)
    one = get_profile(store, "source-one")
    two = get_profile(store, "source-two")
    assert one["llm_total_tokens"] == 173
    assert two["llm_total_tokens"] == 0


def test_source_material_rate_and_new_event_rate_are_separate(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    item_id = seed_item(store, "Source material item", source_id="source-metrics", url="https://example.com/source")
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO source_signals (
                source_id, item_id, cluster_id, source_role, new_event_signal,
                incremental_value, report_value, created_at, updated_at
            )
            VALUES ('source-metrics', ?, 'cluster_x', 'source_material', 0, 4, 3, 'now', 'now')
            """,
            (item_id,),
        )
    result = recompute_source_profiles(store)
    profile = get_profile(store, "source-metrics")
    assert result["stats"]["total_sources_processed"] == 1
    assert profile["source_material_rate"] == 1.0
    assert profile["new_event_rate"] == 0.0


def test_evaluate_dry_run_writes_report_not_source_db(tmp_path: Path) -> None:
    source_store = make_store(tmp_path / "source")
    seed_item(source_store, "Evaluation sample", source_id="eval-source", url="https://example.com/eval")
    output = tmp_path / "eval-output"
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(output),
        limit=10,
        max_calls=5,
        max_candidates=3,
        batch_size=2,
        live=False,
        dry_run=True,
        write_real_db=False,
        model=None,
        strong_model=None,
        token_budget=0,
        include_archived=False,
        concurrency=2,
    )
    assert result["ok"] is True
    assert Path(result["report_path"]).exists()
    assert Path(result["summary_path"]).exists()
    with source_store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) AS n FROM item_cards").fetchone()["n"] == 0


def test_evaluate_missing_live_env_skips_live_calls(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CONTENT_INBOX_LLM_ENABLE_LIVE", raising=False)
    source_store = make_store(tmp_path / "source-live")
    seed_item(source_store, "No live env item", source_id="eval-source", url="https://example.com/live")
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(tmp_path / "eval-live"),
        limit=10,
        max_calls=5,
        max_candidates=3,
        batch_size=2,
        live=True,
        dry_run=True,
        write_real_db=False,
        model=None,
        strong_model=None,
        token_budget=0,
        include_archived=False,
        concurrency=2,
    )
    assert any("live skipped" in warning for warning in result["metadata"]["warnings"])


def test_evaluate_max_calls_and_token_budget_marked(tmp_path: Path) -> None:
    source_store = make_store(tmp_path / "source-budget")
    seed_item(source_store, "Budget item", source_id="budget-source", url="https://example.com/budget")
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(tmp_path / "eval-budget"),
        limit=10,
        max_calls=0,
        max_candidates=3,
        batch_size=2,
        live=True,
        dry_run=True,
        write_real_db=False,
        model=None,
        strong_model=None,
        token_budget=1,
        include_archived=False,
        concurrency=2,
    )
    summary = json.loads(Path(result["summary_path"]).read_text(encoding="utf-8"))
    assert summary["metadata"]["actual_calls"] == 0


def test_archived_cluster_excluded_unless_requested(tmp_path: Path) -> None:
    store = make_store(tmp_path)
    seed_item(store, "Archived OpenAI event", url="https://example.com/archived")
    generate_item_cards(store, limit=10)
    process_item_clusters(store, limit=10, live=False)
    with store.connect() as conn:
        cluster_id = conn.execute("SELECT cluster_id FROM event_clusters").fetchone()["cluster_id"]
        conn.execute("UPDATE event_clusters SET status = 'archived' WHERE cluster_id = ?", (cluster_id,))
        card = conn.execute("SELECT * FROM item_cards LIMIT 1").fetchone()
    assert candidate_clusters(store, dict(card), 5) == []
    assert candidate_clusters(store, dict(card), 5, include_archived=True)


@pytest.mark.live_deepseek
def test_live_deepseek_smoke_item_card() -> None:
    result = run_live_smoke("item-card", limit=1, max_calls=2)
    assert result["ok"] is True
