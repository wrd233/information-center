from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from app.models import NormalizedContent, ScreeningResult
from app.semantic.cards import generate_item_cards
from app.semantic.card_policy import fallback_classification
from app.semantic.candidates import assess_candidate, hotspot_key_candidates, normalize_relation_label, relation_pair_key
from app.semantic.cluster_policy import cluster_decision_attach_eligible
from app.semantic.clusters import process_item_clusters, show_cluster, update_cluster_statuses
from app.semantic.clusters import candidate_clusters
from app.semantic.evaluate import run_evaluation
from app.semantic.evidence import export_evidence
from app.semantic.live_smoke import run_live_smoke
from app.semantic.relations import process_item_relations
from app.semantic.review import decide_review, list_reviews
from app.semantic.schemas import cluster_relation_action, item_relation_should_fold
from app.semantic.signatures import extract_event_signature
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
    assert item_relation_should_fold("same_product_different_event") is False
    assert item_relation_should_fold("same_thread") is False
    assert cluster_relation_action("source_material") == "attach_update_card"
    assert cluster_relation_action("new_info") == "attach_update_card"
    assert cluster_relation_action("same_topic") == "do_not_attach"


def test_phase1_3_event_signature_validation() -> None:
    good = extract_event_signature(
        {
            "item_id": "a",
            "title": "Firecrawl launches PHP SDK for Laravel",
            "summary": "The Firecrawl PHP SDK is live for PHP and Laravel projects.",
            "published_at": "2026-05-05T16:00:00+00:00",
            "source_id": "socialmedia-firecrawl-firecrawl-dev",
        }
    )
    assert good.is_concrete is True
    assert good.actor.lower() == "firecrawl"
    assert "php" in good.product_or_model.lower() or "laravel" in good.product_or_model.lower()
    assert good.signature_key

    generic = extract_event_signature(
        {
            "item_id": "b",
            "title": "agent api research update",
            "summary": "AI agent API research model paper update powered by xgo.ing",
            "published_at": "2026-05-05T16:00:00+00:00",
        }
    )
    assert generic.is_concrete is False
    assert generic.invalid_reasons

    bad_actor = extract_event_signature(
        {
            "item_id": "c",
            "title": "v2.10 feature update is available",
            "summary": "v2.10 update at 50 powered by xgo.ing",
            "published_at": "2026-05-05T16:00:00+00:00",
        }
    )
    assert bad_actor.is_concrete is False

    url_fragment = extract_event_signature(
        {
            "item_id": "d",
            "title": "paper: https://t.co/fkR2wVD129",
            "summary": "May 14 security paper update powered by xgo.ing",
            "published_at": "2026-05-14T16:00:00+00:00",
        }
    )
    assert url_fragment.is_concrete is False


def test_phase1_3_fallback_classification() -> None:
    assert fallback_classification(source="deterministic_minimal") == "fallback_deterministic_minimal"
    assert fallback_classification(source="heuristic", reason="JSON validation failed") == "fallback_due_to_llm_parse_error"
    assert fallback_classification(source="heuristic", reason="live token budget reached") == "fallback_due_to_budget_skip"


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
        source_filter=None,
        source_url_prefix=None,
        sample_mode="recent",
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
        source_filter=None,
        source_url_prefix=None,
        sample_mode="recent",
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
        source_filter=None,
        source_url_prefix=None,
        sample_mode="recent",
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


def test_evaluate_source_scope_filter_and_report_sections(tmp_path: Path) -> None:
    source_store = make_store(tmp_path / "source-scope")
    seed_item(
        source_store,
        "XGO scoped AI item",
        source_id="xgo-ai",
        url="https://api.xgo.ing/rss/ai/1",
    )
    seed_item(
        source_store,
        "Other item",
        source_id="other",
        url="https://example.com/other",
    )
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(tmp_path / "eval-scope"),
        limit=10,
        max_calls=0,
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
        source_filter=None,
        source_url_prefix="api.xgo.ing",
        sample_mode="source_scope_full",
    )
    summary = json.loads(Path(result["summary_path"]).read_text(encoding="utf-8"))
    report = Path(result["report_path"]).read_text(encoding="utf-8")
    assert summary["input_sample"]["items_sampled"] == 1
    assert summary["source_scope"]["matched_source_count"] == 1
    assert "## 2. Source Scope" in report
    assert "## 10. Concurrency Summary" in report
    assert "## 14. Readiness Assessment" in report


def test_phase1_3_scoped_write_requires_confirmation(tmp_path: Path) -> None:
    source_store = make_store(tmp_path / "source-write-refusal")
    seed_item(source_store, "XGO scoped write item", source_id="xgo-ai", url="https://api.xgo.ing/rss/ai/2")
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(tmp_path / "eval-write-refusal"),
        limit=1,
        max_calls=0,
        max_candidates=1,
        batch_size=1,
        live=False,
        dry_run=False,
        write_real_db=True,
        model=None,
        strong_model=None,
        token_budget=0,
        include_archived=False,
        concurrency=1,
        source_filter=None,
        source_url_prefix="api.xgo.ing",
        sample_mode="source_scope_full",
    )
    assert result["ok"] is False
    assert "confirm-scoped-semantic-write" in result["error"]


def test_phase1_2d_evidence_persistence_exports_auditable_files(tmp_path: Path) -> None:
    source_store = make_store(tmp_path / "evidence-source")
    first = seed_item(source_store, "OpenAI launches Codex agent", source_id="xgo-openai", url="https://api.xgo.ing/a")
    second = seed_item(source_store, "OpenAI launches Codex coding agent", source_id="xgo-dev", url="https://api.xgo.ing/b")
    output = tmp_path / "phase1_2d_eval"
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(output),
        limit=10,
        max_calls=0,
        max_candidates=5,
        batch_size=2,
        live=False,
        dry_run=True,
        write_real_db=False,
        model=None,
        strong_model=None,
        token_budget=1,
        include_archived=False,
        concurrency=5,
        source_filter=None,
        source_url_prefix="api.xgo.ing",
        sample_mode="event_hotspots",
        stage_budget_profile="relation_heavy",
        persist_evidence=True,
        phase_label="phase1_2d",
    )
    assert result["ok"] is True
    manifest = output / "semantic_run_manifest.json"
    assert manifest.exists()
    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    assert manifest_data["phase"] == "phase1_2d"
    assert manifest_data["concurrency"] == 5
    items_path = output / "semantic_items.jsonl"
    relations_path = output / "relations_all.jsonl"
    interesting_path = output / "relations_interesting.jsonl"
    hotspots_path = output / "event_hotspots.jsonl"
    failures_path = output / "item_card_failures.jsonl"
    attachments_path = output / "cluster_attachments.jsonl"
    budget_skips_path = output / "budget_skips.jsonl"
    for path in [items_path, relations_path, interesting_path, hotspots_path, failures_path, attachments_path, budget_skips_path]:
        assert path.exists()
    items = [json.loads(line) for line in items_path.read_text(encoding="utf-8").splitlines()]
    assert {row["original_item_id"] for row in items} == {first, second}
    assert all(row["dedupe_key"] for row in items)
    with source_store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) AS n FROM item_cards").fetchone()["n"] == 0


def test_phase1_2e_relation_pair_key_is_canonical() -> None:
    a = {"item_id": "dry-a", "raw_json": json.dumps({"source_item_id": "prod-a"})}
    b = {"item_id": "dry-b", "raw_json": json.dumps({"source_item_id": "prod-b"})}
    assert relation_pair_key(a, b) == relation_pair_key(b, a)


def test_phase1_2e_relation_tightening_same_topic_and_same_event() -> None:
    pika = {"item_id": "a", "title": "Pika launches UGC ads for creators", "summary": "AI video advertising update"}
    skywork = {"item_id": "b", "title": "Skywork Hermes Agent adds browser skills", "summary": "Agent workflow demo"}
    weak = assess_candidate(pika, skywork)
    label, event_type, eligible, disqualifiers = normalize_relation_label(
        "related_with_new_info",
        weak,
        reason="Both discuss agent skills.",
        evidence=["agent skills"],
        new_information=[],
    )
    assert label == "different"
    assert event_type in {"same_topic_only", "entity_overlap_only", "same_product_different_event"}
    assert eligible is False
    assert disqualifiers

    redis_a = {"item_id": "a", "title": "Redis adds vector set array support", "summary": "Redis releases array support on Monday"}
    redis_b = {"item_id": "b", "title": "Redis array support rollout includes playground", "summary": "Adds playground link and pricing detail"}
    strong = assess_candidate(redis_a, redis_b)
    label, event_type, eligible, _disqualifiers = normalize_relation_label(
        "related_with_new_info",
        strong,
        reason="Both cover the same Redis array support rollout.",
        evidence=["Redis array support"],
        new_information=["Adds playground link"],
    )
    assert label == "related_with_new_info"
    assert event_type == "same_event"
    assert eligible is True


def test_phase1_2e_hotspot_filters_xgo_proxy_key() -> None:
    item = {
        "item_id": "x",
        "title": "Qwen3.6 FlashQLA benchmark released",
        "summary": "powered by xgo.ing view on twitter",
        "url": "https://api.xgo.ing/rss/abc",
    }
    keys = hotspot_key_candidates(item)
    assert keys["selected_hotspot_key"] != "xgo.ing"
    assert keys["selected_hotspot_key"] != "api.xgo.ing"
    assert keys["proxy_domain_filtered"] is True


def test_phase1_2f_hotspot_uses_event_signature_not_generic_agent() -> None:
    item = {
        "item_id": "x",
        "title": "Replit launches Parallel Agents for app builders",
        "summary": "Meet Replit Parallel Agents. Build faster by running agents in parallel. Powered by xgo.ing",
        "published_at": "2026-05-11T17:34:28+00:00",
        "url": "https://api.xgo.ing/rss/replit",
    }
    keys = hotspot_key_candidates(item)
    assert keys["key_source"] == "event_signature"
    assert "replit" in keys["selected_hotspot_key"]
    assert "parallelagents" in keys["selected_hotspot_key"] or "parallel agents" in keys["selected_hotspot_key"]
    assert keys["selected_hotspot_key"] != "agent"


def test_phase1_2e_candidate_suppression_and_priority() -> None:
    generic_a = {"item_id": "a", "title": "AI agent tips", "summary": "General agent ideas"}
    generic_b = {"item_id": "b", "title": "Agent workflow notes", "summary": "Generic AI agent ideas"}
    generic = assess_candidate(generic_a, generic_b)
    assert generic.candidate_priority == "suppress"
    assert generic.generic_only is True

    dup_a = {"item_id": "a", "title": "Qwen FlashQLA ships", "url": "https://example.com/qwen"}
    dup_b = {"item_id": "b", "title": "Qwen FlashQLA ships", "url": "https://example.com/qwen"}
    duplicate = assess_candidate(dup_a, dup_b)
    assert duplicate.candidate_priority == "must_run"
    assert duplicate.lane == "deterministic"


def test_phase1_2f_event_signature_pair_beats_generic_same_product() -> None:
    launch_a = {
        "item_id": "a",
        "title": "Replit launches Parallel Agents",
        "summary": "Parallel Agents are now available in Replit.",
        "published_at": "2026-05-11T17:34:28+00:00",
    }
    launch_b = {
        "item_id": "b",
        "title": "Try Replit Parallel Agents today",
        "summary": "Replit Parallel Agents launch lets users run up to 10 agents.",
        "published_at": "2026-05-11T18:34:28+00:00",
    }
    strong = assess_candidate(launch_a, launch_b)
    assert strong.candidate_priority in {"must_run", "high"}
    assert strong.lane in {"event_signature", "same_actor_product", "near_title"}
    assert strong.event_signature_match is True or "same_actor_product_action_72h" in strong.same_event_evidence

    product_a = {
        "item_id": "c",
        "title": "Perplexity Computer is available in Microsoft Marketplace",
        "summary": "Get Perplexity Computer from the marketplace.",
        "published_at": "2026-05-04T18:06:02+00:00",
    }
    product_b = {
        "item_id": "d",
        "title": "Perplexity adds premium health sources",
        "summary": "Available to Max subscribers in Perplexity and Computer.",
        "published_at": "2026-05-05T17:07:22+00:00",
    }
    weak = assess_candidate(product_a, product_b)
    assert weak.candidate_priority in {"medium", "low", "suppress"}
    assert weak.candidate_priority != "must_run"


def test_phase1_3_relation_policy_same_product_and_thread() -> None:
    assessment = assess_candidate(
        {"item_id": "a", "title": "Manus Recommended Connectors launches", "summary": "Manus ships recommended connectors."},
        {"item_id": "b", "title": "Manus Projects memory learns from tasks", "summary": "Manus projects can learn from completed tasks."},
    )
    label, event_type, eligible, _ = normalize_relation_label(
        "related_with_new_info",
        assessment,
        reason="Same product but different feature update.",
        evidence=["same product"],
        new_information=["different feature"],
    )
    assert label == "same_product_different_event"
    assert event_type == "same_product_different_event"
    assert eligible is False


def test_phase1_3_cluster_attach_policy_rejects_thread() -> None:
    class Decision:
        primary_relation = "new_info"
        cluster_relation_type = "same_thread"
        same_event = True
        confidence = 0.95
        attach_eligible = True

    assert cluster_decision_attach_eligible(Decision()) is False


def test_phase1_2e_evidence_exports_new_candidate_files(tmp_path: Path) -> None:
    source_store = make_store(tmp_path / "phase1_2e-source")
    seed_item(source_store, "Qwen FlashQLA ships", source_id="xgo-a", url="https://api.xgo.ing/qwen-a")
    seed_item(source_store, "Qwen FlashQLA benchmark ships", source_id="xgo-b", url="https://api.xgo.ing/qwen-b")
    output = tmp_path / "phase1_2e_eval"
    result = run_evaluation(
        db_path=str(source_store.database_path),
        output=str(output),
        limit=10,
        max_calls=0,
        max_candidates=5,
        batch_size=2,
        live=False,
        dry_run=True,
        write_real_db=False,
        model=None,
        strong_model=None,
        token_budget=1,
        include_archived=False,
        concurrency=5,
        source_filter=None,
        source_url_prefix="api.xgo.ing",
        sample_mode="event_hotspots",
        stage_budget_profile="phase1_2e_profile",
        persist_evidence=True,
        phase_label="phase1_2e",
    )
    assert result["ok"] is True
    for name in [
        "candidate_generation.jsonl",
        "candidate_suppression.jsonl",
        "cost_quality_metrics.json",
        "phase1_2d_vs_1_2e_comparison.json",
    ]:
        assert (output / name).exists()
    relation_rows = [json.loads(line) for line in (output / "relations_all.jsonl").read_text(encoding="utf-8").splitlines()]
    for row in relation_rows:
        assert "relation_pair_key" in row
        assert "event_relation_type" in row
        assert "cluster_eligible" in row
        assert "candidate_priority" in row
    manifest = json.loads((output / "semantic_run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["phase"] == "phase1_2e"


@pytest.mark.live_deepseek
def test_live_deepseek_smoke_item_card() -> None:
    result = run_live_smoke("item-card", limit=1, max_calls=2)
    assert result["ok"] is True
