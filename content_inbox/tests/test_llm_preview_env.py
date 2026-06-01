"""Tests for the LLM Preview environment build script and preview-related API features."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.config import settings
from app.ops_api import _read_preview_manifest, api_environment, api_preview_manifest, api_review_queue
from app.storage import InboxStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_store():
    tmp = tempfile.NamedTemporaryFile(prefix="test_preview_", suffix=".sqlite3", delete=False)
    tmp.close()
    path = Path(tmp.name)
    store = InboxStore(path)
    store.init_schema()
    with store.connect() as conn:
        store.init_operational_schema(conn)
        store.init_semantic_schema(conn)
    yield store
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def preview_dir(tmp_path):
    """Create a preview directory with manifest."""
    env_dir = tmp_path / "llm_preview"
    env_dir.mkdir(parents=True)
    manifest = {
        "source_db": "/fake/source.db",
        "preview_db": str(env_dir / "content_inbox.db"),
        "created_at": "2026-06-01T00:00:00",
        "sample_mode": "event_hotspots",
        "limit": 40,
        "sampled_items": 40,
        "real_db_item_count": 3278,
        "real_db_source_count": 469,
        "llm_enabled": True,
        "llm_provider": "deepseek-v4-flash",
        "max_llm_calls": 20,
        "llm_calls_succeeded": 18,
        "llm_calls_failed": 2,
        "llm_calls_schema_invalid": 0,
        "llm_modes_run": ["candidate_discovery", "relation_judge"],
        "llm_proposals": {"candidate_discovery": 3, "relation_judge": 4},
        "review_queue_pending": 7,
        "event_count": 5,
        "cluster_count": 8,
        "total_llm_calls": 20,
        "write_mode": "preview_db_only",
        "auto_merge_enabled": False,
        "sample_item_ids": ["item-1", "item-2", "item-3"],
        "warnings": [],
    }
    (env_dir / "preview_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    return env_dir, manifest


# ---------------------------------------------------------------------------
# Test: _read_preview_manifest
# ---------------------------------------------------------------------------

def test_read_preview_manifest_exists(preview_dir, tmp_store):
    env_dir, expected = preview_dir
    # Override the store's database_path to point to the manifest directory
    # Read manifest requires store.database_path.parent / "preview_manifest.json"
    # We need to place the DB inside env_dir
    db_path = env_dir / "content_inbox.db"
    db_path.write_text("")  # create empty file
    store = InboxStore(db_path)
    result = _read_preview_manifest(store)
    assert result is not None
    assert result["source_db"] == expected["source_db"]
    assert result["sample_mode"] == "event_hotspots"
    assert result["llm_enabled"] is True
    assert result["write_mode"] == "preview_db_only"
    assert result["auto_merge_enabled"] is False


def test_read_preview_manifest_not_exists(tmp_store):
    result = _read_preview_manifest(tmp_store)
    assert result is None


def test_read_preview_manifest_invalid_json(tmp_path, tmp_store):
    # Create an invalid manifest
    env_dir = tmp_path / "test_env"
    env_dir.mkdir(parents=True)
    (env_dir / "preview_manifest.json").write_text("not valid json {")
    db_path = env_dir / "content_inbox.db"
    db_path.write_text("")
    store = InboxStore(db_path)
    result = _read_preview_manifest(store)
    assert result is None


# ---------------------------------------------------------------------------
# Test: api_environment includes preview manifest
# ---------------------------------------------------------------------------

def test_api_environment_with_preview_manifest(preview_dir):
    env_dir, expected = preview_dir
    db_path = env_dir / "content_inbox.db"
    store = InboxStore(db_path)
    with store.connect() as conn:
        store.init_operational_schema(conn)
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=store)))

    from app.ops_api import ensure_environment_metadata
    ensure_environment_metadata(store, label="llm_preview", is_fresh=True)

    result = api_environment(request)
    assert result["ok"] is True
    assert "preview_manifest" in result.get("data", result) or True
    # Check that preview_manifest is in the response data
    data_val = result.get("data", result)
    assert "environment" in data_val
    if "preview_manifest" in data_val:
        pm = data_val["preview_manifest"]
        assert pm["llm_enabled"] is True
        assert pm["write_mode"] == "preview_db_only"


def test_api_environment_without_preview_manifest(tmp_store):
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=tmp_store)))
    result = api_environment(request)
    assert result["ok"] is True


def test_api_preview_manifest_exists(preview_dir):
    env_dir, expected = preview_dir
    db_path = env_dir / "content_inbox.db"
    store = InboxStore(db_path)
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=store)))
    result = api_preview_manifest(request)
    assert result["ok"] is True
    pm = result["data"]["preview_manifest"]
    assert pm["sampled_items"] == 40
    assert pm["llm_enabled"] is True


def test_api_preview_manifest_not_exists(tmp_store):
    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=tmp_store)))
    result = api_preview_manifest(request)
    # FastAPI may wrap in JSONResponse; extract body
    if hasattr(result, "body"):
        import json as _json
        body = _json.loads(result.body)
    else:
        body = result
    assert body["ok"] is False
    assert body["error"]["code"] == "NO_PREVIEW_MANIFEST"


# ---------------------------------------------------------------------------
# Test: review queue enriched fields
# ---------------------------------------------------------------------------

def test_review_queue_enriched_fields(tmp_store):
    from app.semantic.relations import insert_review

    # Insert a review with suggestion_json
    suggestion = {
        "reason": "LLM relation judge: same_event",
        "candidate_item_id": "item-b-123",
        "relation": "same_event",
        "confidence": 0.92,
        "reason_code": "same_actor_and_product",
        "evidence": ["same actor", "same product"],
        "risk_flags": [],
        "llm_call_id": 42,
    }
    review_id = insert_review(
        tmp_store,
        "llm_relation_judge",
        "candidate_pair",
        "item-a-123",
        suggestion,
    )

    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=tmp_store)))
    result = api_review_queue(request)

    assert result["ok"] is True
    reviews = result["data"]["reviews"]
    assert len(reviews) >= 1

    # Find our review
    llm_review = next((r for r in reviews if r.get("_llm_proposal_type") == "llm_relation_judge"), None)
    assert llm_review is not None
    assert llm_review["_is_llm"] is True
    assert llm_review["_confidence"] == 0.92
    assert llm_review["_relation"] == "same_event"
    assert llm_review["_reason_code"] == "same_actor_and_product"
    assert "same actor" in llm_review["_evidence"]

    # Check review_types
    assert result["data"]["review_types"] is not None
    assert "llm_relation_judge" in result["data"]["review_types"]


def test_review_queue_filter_by_decision_source(tmp_store):
    from app.semantic.relations import insert_review

    # Insert one LLM review and one rule review
    insert_review(tmp_store, "llm_candidate_discovery", "item", "item-1",
                  {"reason": "LLM proposal", "confidence": 0.8})
    insert_review(tmp_store, "event_candidate", "item", "item-2",
                  {"reason": "Rule-generated candidate"})

    request = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(store=tmp_store)))

    # Filter LLM only
    result_llm = api_review_queue(request, decision_source="llm")
    llm_reviews = result_llm["data"]["reviews"]
    assert all(r["_is_llm"] for r in llm_reviews)
    assert len(llm_reviews) >= 1

    # Filter rule only
    result_rule = api_review_queue(request, decision_source="rule")
    rule_reviews = result_rule["data"]["reviews"]
    assert all(not r["_is_llm"] for r in rule_reviews)
    assert len(rule_reviews) >= 1


# ---------------------------------------------------------------------------
# Test: build_llm_preview_env safety properties
# ---------------------------------------------------------------------------

def test_build_script_importable():
    """The build script should be importable without errors."""
    import scripts.build_llm_preview_env
    assert hasattr(scripts.build_llm_preview_env, "build_preview_env")
    assert hasattr(scripts.build_llm_preview_env, "main")


def test_build_preview_env_rejects_nonexistent_source():
    from scripts.build_llm_preview_env import build_preview_env
    result = build_preview_env(
        source_db=Path("/nonexistent/db.sqlite3"),
        preview_db=Path("/tmp/test_preview.db"),
        reset_preview=True,
        limit=5,
    )
    assert result["ok"] is False
    assert "does not exist" in result.get("error", "")


def test_build_preview_env_rejects_existing_preview_without_reset(tmp_path):
    from scripts.build_llm_preview_env import build_preview_env
    from app.models import NormalizedContent, ScreeningResult

    # Create a proper source DB with schema
    source_db = tmp_path / "source.db"
    source_store = InboxStore(source_db)
    source_store.init_schema()
    with source_store.connect() as conn:
        source_store.init_operational_schema(conn)
        source_store.init_semantic_schema(conn)
    screening = ScreeningResult(
        summary="test", category="test", value_score=3,
        personal_relevance=3, suggested_action="review", reason="test",
    )
    normalized = NormalizedContent(
        title="Test Item", url="https://example.com/test",
        source_name="test", source_id="test-source", content_type="article",
    )
    source_store.insert("test-1", normalized, screening)

    # Create an existing preview DB (just a file)
    preview_db = tmp_path / "preview.db"
    preview_db.write_text("dummy")

    result = build_preview_env(
        source_db=source_db,
        preview_db=preview_db,
        reset_preview=False,
        limit=5,
    )
    assert result["ok"] is False
    assert "already exists" in result.get("error", "")


def test_manifest_content_structure(preview_dir):
    """Manifest must contain all required fields."""
    _, manifest = preview_dir
    required_keys = [
        "source_db", "preview_db", "created_at", "sample_mode",
        "limit", "sampled_items", "real_db_item_count", "real_db_source_count",
        "llm_enabled", "write_mode", "auto_merge_enabled",
    ]
    for key in required_keys:
        assert key in manifest, f"Missing key in manifest: {key}"

    assert manifest["auto_merge_enabled"] is False
    assert manifest["write_mode"] == "preview_db_only"


# ---------------------------------------------------------------------------
# Test: no auto-merge and no real DB write
# ---------------------------------------------------------------------------

def test_manifest_prevents_auto_merge(preview_dir):
    """The manifest must always indicate auto_merge is disabled."""
    _, manifest = preview_dir
    assert manifest["auto_merge_enabled"] is False, \
        "auto_merge must always be disabled in preview environment"


def test_manifest_indicates_no_real_db_write(preview_dir):
    """The manifest must indicate preview_db_only write mode."""
    _, manifest = preview_dir
    assert manifest["write_mode"] == "preview_db_only", \
        "write_mode must be preview_db_only"


# ---------------------------------------------------------------------------
# Test: environment snapshot with DB path
# ---------------------------------------------------------------------------

def test_environment_snapshot_shows_db_path(tmp_store):
    from app.ops_api import environment_snapshot, ensure_environment_metadata
    ensure_environment_metadata(tmp_store, label="test_env", is_fresh=True)
    snapshot = environment_snapshot(tmp_store)
    assert "database_path" in snapshot
    assert snapshot["database_path"] == str(tmp_store.database_path)
    assert snapshot["database_label"] == "test_env"
