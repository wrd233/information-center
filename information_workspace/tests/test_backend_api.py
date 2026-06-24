from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def make_client(tmp_path: Path) -> TestClient:
    settings = Settings(
        db_path=tmp_path / "test.db",
        outputs_dir=tmp_path / "outputs",
        deepseek_api_key="",
        deepseek_model="deepseek-v4-flash",
        llm_provider="deepseek",
        api_host="127.0.0.1",
        api_port=8788,
    )
    return TestClient(create_app(settings))


def material(index: int, **overrides):
    data = {
        "title": f"Synthetic test material {index}",
        "content_text": (
            "This synthetic test material validates API upload, dedupe, light understanding, "
            "Event candidate generation, Topic structures, and export behavior."
        ),
        "source_name": "Pytest",
        "source_type": "api",
        "metadata": {
            "synthetic": True,
            "fixture_group": "multi_source_same_event",
            "test_purpose": ["api_smoke", "event_candidate"],
            "expected_behavior": "cluster into candidate event",
            "generated_by": "codex_goal_04",
            "event_key": "pytest_event",
        },
    }
    data.update(overrides)
    return data


def test_upload_process_search_detail_and_run_steps(tmp_path):
    client = make_client(tmp_path)
    response = client.post(
        "/api/materials/batch?allow_mock_llm=true",
        json={
            "items": [
                material(1),
                material(2, title="Synthetic test material 2", content_text="This second synthetic test material has distinct content for search and Event candidate grouping."),
            ],
            "auto_process": False,
        },
    )
    assert response.status_code == 200
    run_id = response.json()["run_id"]

    processed = client.post(f"/api/runs/{run_id}/process?allow_mock_llm=true")
    assert processed.status_code == 200
    assert processed.json()["status"] == "succeeded"

    run = client.get(f"/api/runs/{run_id}").json()
    assert [step["step_name"] for step in run["steps"]]
    assert all(step["status"] == "succeeded" for step in run["steps"])
    assert len(run["material_ids"]) == 2
    assert run["candidate_event_ids"]

    search = client.get("/api/materials?synthetic=true&include_noise=true").json()
    assert search["total"] == 2
    detail = client.get(f"/api/materials/{search['items'][0]['id']}").json()
    assert detail["no_original_link"] is True
    assert detail["light_understanding"]["content_facets"]


def test_batch_partial_validation_and_duplicate_compression(tmp_path):
    client = make_client(tmp_path)
    duplicate = material(1, title="Duplicate A")
    response = client.post(
        "/api/materials/batch",
        json={
            "items": [
                duplicate,
                {**duplicate, "title": "Duplicate B", "external_id": "duplicate-b"},
                {"title": "Bad", "content_text": "missing source fields"},
            ],
            "auto_process": False,
        },
    )
    run_id = response.json()["run_id"]
    processed = client.post(f"/api/runs/{run_id}/process?allow_mock_llm=true")
    assert processed.status_code == 200
    run = client.get(f"/api/runs/{run_id}").json()
    assert run["accepted_count"] == 2
    assert run["failed_count"] == 1
    assert run["duplicate_count"] == 1
    assert run["material_count"] == 1


def test_ignore_restore_event_topic_and_export(tmp_path):
    client = make_client(tmp_path)
    upload = client.post(
        "/api/materials/batch?allow_mock_llm=true",
        json={
            "items": [
                material(1),
                material(2, title="Second event material", content_text="A distinct second synthetic event material adds another source angle for Topic export validation."),
            ],
            "auto_process": True,
        },
    ).json()
    run_id = upload["id"] if "id" in upload else upload["run_id"]
    run = client.get(f"/api/runs/{run_id}").json()
    material_ids = run["material_ids"]

    noise_upload = client.post(
        "/api/materials?allow_mock_llm=true",
        json={
            **material(
                3,
                title="Noise material for ignore restore",
                content_text="Synthetic ad fragment for coupon noise. No useful context.",
                metadata={
                    "synthetic": True,
                    "fixture_group": "noise",
                    "test_purpose": ["noise_handling"],
                    "expected_behavior": "can be ignored and restored because it has no Event/Topic refs",
                    "generated_by": "codex_goal_04",
                },
            ),
            "auto_process": True,
        },
    ).json()
    noise_run = client.get(f"/api/runs/{noise_upload['id']}").json()
    noise_material_id = noise_run["material_ids"][0]
    ignored = client.post(f"/api/materials/{noise_material_id}/ignore")
    assert ignored.status_code == 200
    restored = client.post(f"/api/materials/{noise_material_id}/restore")
    assert restored.status_code == 200

    event = client.post(
        "/api/events/from-materials?allow_mock_llm=true",
        json={"material_ids": material_ids, "user_focus": "pytest focus"},
    )
    assert event.status_code == 200
    event_id = event.json()["id"]
    event_export = client.post(f"/api/exports/event/{event_id}").json()
    assert event_export["file_path"].endswith(".md")

    topic = client.post(
        "/api/topics",
        json={"title": "Pytest Topic", "goal": "Validate Topic flow", "organization": "Evidence first", "material_ids": material_ids, "event_ids": [event_id]},
    )
    assert topic.status_code == 200
    topic_id = topic.json()["id"]
    refreshed = client.post(
        f"/api/topics/{topic_id}/refresh-structure",
        json={"include_new_materials": True, "allow_mock_llm": True},
    )
    assert refreshed.status_code == 200
    confirmed = client.post(f"/api/topics/{topic_id}/confirm-candidate")
    assert confirmed.status_code == 200
    topic_export = client.post(f"/api/exports/topic/{topic_id}").json()
    assert topic_export["material_count"] >= 2


def test_business_llm_without_key_fails_clearly(tmp_path):
    client = make_client(tmp_path)
    upload = client.post("/api/materials", json={**material(1), "auto_process": False}).json()
    processed = client.post(f"/api/runs/{upload['run_id']}/process")
    assert processed.status_code == 200
    body = processed.json()
    assert body["status"] == "failed"
    assert "light_understanding" in body["failed_steps"]
