from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from app.config import settings
from app.scheduler import should_recover_missed_run
from app.server import app
from app.storage import InboxStore


FIXTURES = Path(__file__).parent / "fixtures"


def make_client(tmp_path: Path) -> tuple[TestClient, InboxStore]:
    db_path = tmp_path / "content_inbox.db"
    store = InboxStore(db_path)
    app.state.store = store
    settings.database_path = db_path
    settings.enable_real_runs = True
    settings.scheduler_enabled = False
    return TestClient(app), store


def add_source(store: InboxStore, feed_url: str, *, source_id: str, priority: int = 3) -> None:
    store.create_rss_source(
        {
            "source_id": source_id,
            "source_name": source_id,
            "source_category": "Tests",
            "feed_url": feed_url,
            "status": "active",
            "priority": priority,
            "tags": [],
            "config": {"screen": False},
        }
    )


def test_registry_full_manual_run_summary_and_source_health(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_source(store, (FIXTURES / "rss_basic.xml").as_uri(), source_id="source-a")

    response = client.post(
        "/api/inbox-loop/runs",
        json={"run_synchronously": True, "limits": {"max_items_per_source": 2, "probe_limit": 2}},
    ).json()
    run_id = response["data"]["run_id"]
    summary = client.get(f"/api/inbox-loop/runs/{run_id}/summary").json()["data"]["summary"]
    source = store.get_rss_source("source-a")

    assert response["ok"] is True
    assert summary["active_sources"] == 1
    assert summary["succeeded_sources"] == 1
    assert summary["confidence"] == "high"
    assert source["last_success_at"] is not None
    assert source["last_incremental_decision"] == "new_source_initial_baseline"


def test_partial_success_confidence_and_diagnostics(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_source(store, (FIXTURES / "rss_basic.xml").as_uri(), source_id="source-ok")
    add_source(store, (FIXTURES / "missing-feed.xml").as_uri(), source_id="source-bad", priority=1)

    response = client.post(
        "/api/inbox-loop/runs",
        json={"run_synchronously": True, "force": True, "limits": {"max_items_per_source": 1, "probe_limit": 1}},
    ).json()
    run_id = response["data"]["run_id"]
    summary = client.get(f"/api/inbox-loop/runs/{run_id}/summary").json()["data"]
    diagnostics = client.get(f"/api/inbox-loop/runs/{run_id}/diagnostics").json()["data"]

    assert summary["run"]["status"] == "partial_success"
    assert summary["summary"]["confidence"] == "low"
    assert summary["summary"]["failed_source_digest"]
    assert diagnostics["failures"][0]["source_id"] == "source-bad"


def test_manual_recent_run_protection_and_force(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_source(store, (FIXTURES / "rss_basic.xml").as_uri(), source_id="source-a")

    first = client.post(
        "/api/inbox-loop/runs",
        json={"run_synchronously": True, "limits": {"max_items_per_source": 1, "probe_limit": 1}},
    ).json()
    skipped = client.post("/api/inbox-loop/runs", json={"run_synchronously": True}).json()
    forced = client.post("/api/inbox-loop/runs", json={"run_synchronously": True, "force": True}).json()

    assert first["data"]["status"] == "started"
    assert skipped["data"]["status"] == "skipped_recent"
    assert forced["data"]["status"] == "started"


def test_run_lock_blocks_duplicate_registry_full_runs(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    add_source(store, (FIXTURES / "rss_basic.xml").as_uri(), source_id="source-a")
    acquired, _lock = store.try_acquire_inbox_run_lock(run_id="external", owner="test")

    response = client.post("/api/inbox-loop/runs", json={"force": True}).json()

    assert acquired is True
    assert response["ok"] is False
    assert response["error"]["code"] == "INBOX_RUN_LOCKED"


def test_scheduler_missed_run_logic(tmp_path: Path) -> None:
    _client, store = make_client(tmp_path)
    settings.scheduler_enabled = True
    settings.daily_run_recover_missed = True
    settings.daily_run_time = "06:00"
    settings.daily_run_tz = "Asia/Shanghai"
    now = datetime(2026, 6, 11, 7, 0, tzinfo=ZoneInfo("Asia/Shanghai"))

    assert should_recover_missed_run(store, now=now) is True

    store.create_ingest_run(
        {
            "run_id": "inbox_scheduled_done",
            "trigger_type": "scheduled",
            "source_mode": "registry_full",
            "status": "success",
            "started_at": now.isoformat(),
            "finished_at": now.isoformat(),
            "selected_source_count": 1,
            "request": {},
            "summary": {},
        }
    )

    assert should_recover_missed_run(store, now=now) is False


def test_triage_packet_decision_ledger_and_context_pack(tmp_path: Path) -> None:
    client, store = make_client(tmp_path)
    now = datetime.now(ZoneInfo("UTC")).isoformat()
    store.create_ingest_run(
        {
            "run_id": "inbox_manual_test",
            "trigger_type": "manual",
            "source_mode": "registry_full",
            "status": "success",
            "started_at": now,
            "finished_at": now,
            "selected_source_count": 1,
            "success_source_count": 1,
            "request": {},
            "summary": {"confidence": "high"},
        }
    )
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO review_queue(review_type, target_type, target_id, status, suggestion_json, reason, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("merge_uncertain", "event", "event-x", "pending", '{"confidence":0.5}', "Needs agent decision", now, now),
        )

    packet = client.get("/api/inbox-loop/triage-packets?run_id=inbox_manual_test&limit=5").json()["data"]
    decision = client.post(
        "/api/inbox-loop/agent-decisions",
        json={
            "run_id": "inbox_manual_test",
            "packet_id": packet["packet_id"],
            "target_type": "event",
            "target_id": "event-x",
            "decision": "research",
            "confidence": 0.7,
            "reason_codes": ["merge_uncertain"],
            "evidence_ids": ["event-x"],
        },
    ).json()
    ledger = client.get("/api/inbox-loop/decision-ledger?run_id=inbox_manual_test").json()["data"]
    context = client.get("/api/context-packs/daily_brief?run_id=inbox_manual_test").json()["data"]["context_pack"]

    assert packet["stats"]["unbounded_raw_items_exposed"] is False
    assert packet["candidates"][0]["target_id"] == "event-x"
    assert decision["data"]["decision"]["decision"] == "research"
    assert ledger["decisions"][0]["target_id"] == "event-x"
    assert context["goal"] == "daily_brief"
    assert context["agent_queue"]

