from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
import hashlib
import json
import re
import sqlite3
import uuid

from pydantic import ValidationError

from .config import BASE_DIR, Settings
from .db import SCHEMA_VERSION, connect, ensure_schema, schema_version
from .llm import LLMClient
from .schemas import MaterialUpload, RUN_STEPS
from .time_utils import timestamp_slug, utc_now


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _loads(value: str | None, default: Any) -> Any:
    if value is None or value == "":
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def _norm_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _sha(value: str) -> str:
    return hashlib.sha256(_norm_text(value).encode("utf-8")).hexdigest()


def _material_hash(item: MaterialUpload) -> str:
    return _sha(item.content_text)


def _title_hash(item: MaterialUpload) -> str:
    return _sha(item.title)


def _row(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _parse_material(row: sqlite3.Row) -> dict[str, Any]:
    item = dict(row)
    item["tags_from_source"] = _loads(item.pop("tags_from_source_json"), [])
    item["metadata"] = _loads(item.pop("metadata_json"), {})
    item["raw_payload"] = _loads(item.pop("raw_payload_json"), {})
    item["light_understanding"] = _loads(item.pop("light_understanding_json"), None)
    item["synthetic"] = bool(item["synthetic"])
    item["ignored"] = bool(item["ignored"])
    item["is_duplicate"] = bool(item["is_duplicate"])
    return item


def _current_status_from_status_doc() -> str:
    status_path = BASE_DIR / "STATUS.md"
    try:
        for line in status_path.read_text(encoding="utf-8").splitlines()[:20]:
            match = re.match(r"## Current Status:\s*(.+)", line.strip())
            if match:
                return match.group(1).strip()
    except OSError:
        pass
    return "UNKNOWN; see STATUS.md"


def _material_snippet(material: dict[str, Any], length: int = 260) -> str:
    text = material.get("content_text") or ""
    return text[:length] + ("..." if len(text) > length else "")


class WorkspaceService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.settings.ensure_dirs()
        with self.connect() as conn:
            ensure_schema(conn)

    def connect(self) -> sqlite3.Connection:
        return connect(self.settings.db_path)

    def health(self) -> dict[str, Any]:
        with self.connect() as conn:
            run_count = conn.execute("SELECT COUNT(*) AS count FROM ingest_runs").fetchone()["count"]
            material_count = conn.execute("SELECT COUNT(*) AS count FROM materials").fetchone()["count"]
        return {
            "app": "information_workspace",
            "version": "0.1.0",
            "database_path": str(self.settings.db_path),
            "outputs_path": str(self.settings.outputs_dir),
            "schema_version": SCHEMA_VERSION,
            "schema_version_in_db": schema_version(self.connect()),
            "deepseek_model": self.settings.deepseek_model,
            "deepseek_configured": self.settings.deepseek_configured,
            "llm_provider": self.settings.llm_provider,
            "started_at": utc_now(),
            "status_summary": {
                "runs": run_count,
                "materials": material_count,
                "current_status": _current_status_from_status_doc(),
            },
        }

    def create_run(self, raw_items: list[dict[str, Any]], *, source: str, auto_process: bool = False) -> dict[str, Any]:
        now = utc_now()
        run_id = _id("run")
        synthetic = any(bool((item.get("metadata") or {}).get("synthetic")) for item in raw_items)
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO ingest_runs(
                  id, status, source, auto_process, synthetic, item_count,
                  accepted_count, failed_count, created_at, updated_at
                ) VALUES (?, 'uploaded', ?, ?, ?, ?, 0, 0, ?, ?)
                """,
                (run_id, source, int(auto_process), int(synthetic), len(raw_items), now, now),
            )
            for step in RUN_STEPS:
                conn.execute(
                    """
                    INSERT INTO run_steps(id, run_id, step_name, status)
                    VALUES (?, ?, ?, 'pending')
                    """,
                    (_id("step"), run_id, step),
                )
            for raw in raw_items:
                clean = dict(raw)
                clean.pop("auto_process", None)
                conn.execute(
                    """
                    INSERT INTO ingest_run_items(id, run_id, raw_json, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (_id("item"), run_id, _json(clean), now),
                )
            self._log(conn, run_id, "upload", "info", f"Created ingest run with {len(raw_items)} items", {"source": source})
            conn.commit()
        return {
            "run_id": run_id,
            "item_count": len(raw_items),
            "accepted_count": 0,
            "failed_count": 0,
            "status": "uploaded",
        }

    def process_run(self, run_id: str, *, allow_mock_llm: bool = False) -> dict[str, Any]:
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        material_ids: list[str] = []
        candidate_event_ids: list[str] = []
        failed_steps: list[str] = []
        with self.connect() as conn:
            run = self._get_run_row(conn, run_id)
            if not run:
                raise ValueError(f"Unknown run_id {run_id}")
            conn.execute("UPDATE ingest_runs SET status='processing', updated_at=? WHERE id=?", (utc_now(), run_id))
            conn.commit()

            valid_items = self._step_validate_input(conn, run_id)
            if self._step_failed(conn, run_id, "validate_input"):
                failed_steps.append("validate_input")
                self._finalize_failed(conn, run_id, failed_steps)
                return self._process_response(conn, run_id, material_ids, candidate_event_ids, failed_steps)

            dedupe_decisions = self._step_dedupe(conn, run_id, valid_items)
            material_ids = self._step_persist(conn, run_id, dedupe_decisions)
            if self._step_failed(conn, run_id, "persist_materials"):
                failed_steps.append("persist_materials")
                self._finalize_failed(conn, run_id, failed_steps)
                return self._process_response(conn, run_id, material_ids, candidate_event_ids, failed_steps)

            light_ok = self._step_light_understanding(conn, run_id, material_ids, llm)
            if not light_ok:
                failed_steps.append("light_understanding")
                self._mark_step(conn, run_id, "similarity_marking", "skipped", 0, 0, 0, 0, "Skipped because light understanding failed")
                self._mark_step(conn, run_id, "candidate_events", "skipped", 0, 0, 0, 0, "Skipped because light understanding failed")
                self._mark_step(conn, run_id, "active_event_matching", "skipped", 0, 0, 0, 0, "Skipped because light understanding failed")
                self._finalize_failed(conn, run_id, failed_steps)
                return self._process_response(conn, run_id, material_ids, candidate_event_ids, failed_steps)

            self._step_similarity(conn, run_id, material_ids)
            candidate_event_ids = self._step_candidate_events(conn, run_id, material_ids, llm)
            self._step_active_event_matching(conn, run_id, material_ids)
            self._step_finalize(conn, run_id, material_ids, candidate_event_ids)
            return self._process_response(conn, run_id, material_ids, candidate_event_ids, failed_steps)

    def get_run(self, run_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            run = self._get_run_row(conn, run_id)
            if not run:
                raise ValueError(f"Unknown run_id {run_id}")
            steps = [dict(row) for row in conn.execute("SELECT * FROM run_steps WHERE run_id=? ORDER BY rowid", (run_id,))]
            logs = [dict(row) for row in conn.execute("SELECT * FROM run_logs WHERE run_id=? ORDER BY id", (run_id,))]
            items = [
                dict(row)
                for row in conn.execute(
                    "SELECT id, validation_status, error, material_id, created_at FROM ingest_run_items WHERE run_id=?",
                    (run_id,),
                )
            ]
            material_ids = [row["material_id"] for row in items if row["material_id"]]
            candidate_ids = [
                row["id"]
                for row in conn.execute(
                    """
                    SELECT DISTINCT e.id FROM events e
                    JOIN event_materials em ON em.event_id=e.id
                    WHERE e.status='candidate' AND em.material_id IN (
                      SELECT material_id FROM ingest_run_items WHERE run_id=? AND material_id IS NOT NULL
                    )
                    """,
                    (run_id,),
                )
            ]
        data = dict(run)
        data["trace_paths"] = _loads(data.pop("trace_paths_json"), [])
        data["report_paths"] = _loads(data.pop("report_paths_json"), [])
        data["steps"] = steps
        data["logs"] = logs
        data["items"] = items
        data["material_ids"] = material_ids
        data["candidate_event_ids"] = candidate_ids
        data["synthetic"] = bool(data["synthetic"])
        data["auto_process"] = bool(data["auto_process"])
        return data

    def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM ingest_runs ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        runs = []
        for row in rows:
            data = dict(row)
            data["trace_paths"] = _loads(data.pop("trace_paths_json"), [])
            data["report_paths"] = _loads(data.pop("report_paths_json"), [])
            data["synthetic"] = bool(data["synthetic"])
            data["auto_process"] = bool(data["auto_process"])
            runs.append(data)
        return runs

    def search_materials(
        self,
        *,
        q: str | None = None,
        run_id: str | None = None,
        include_ignored: bool = False,
        include_noise: bool = False,
        synthetic: bool | None = None,
        source_type: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        clauses = []
        params: list[Any] = []
        if q:
            clauses.append("(title LIKE ? OR content_text LIKE ? OR summary_from_source LIKE ?)")
            like = f"%{q}%"
            params.extend([like, like, like])
        if not include_ignored:
            clauses.append("ignored=0")
        if synthetic is not None:
            clauses.append("synthetic=?")
            params.append(int(synthetic))
        if source_type:
            clauses.append("source_type=?")
            params.append(source_type)
        if run_id:
            clauses.append("id IN (SELECT material_id FROM ingest_run_items WHERE run_id=? AND material_id IS NOT NULL)")
            params.append(run_id)
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM materials {where} ORDER BY created_at DESC LIMIT ?",
                (*params, limit),
            ).fetchall()
        items = []
        for row in rows:
            material = _parse_material(row)
            light = material.get("light_understanding") or {}
            facets = light.get("content_facets", [])
            if not include_noise and "noise" in facets:
                continue
            material["snippet"] = _material_snippet(material)
            material["noise"] = "noise" in facets
            material["no_original_link"] = not bool(material.get("url"))
            items.append(material)
        return {"items": items, "total": len(items)}

    def get_material(self, material_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM materials WHERE id=?", (material_id,)).fetchone()
            if not row:
                raise ValueError(f"Unknown material_id {material_id}")
            material = _parse_material(row)
            material["relations"] = [
                dict(rel)
                for rel in conn.execute(
                    """
                    SELECT * FROM material_relations
                    WHERE primary_material_id=? OR related_material_id=?
                    ORDER BY created_at DESC
                    """,
                    (material_id, material_id),
                )
            ]
            material["events"] = [
                dict(event)
                for event in conn.execute(
                    """
                    SELECT e.id, e.title, e.status, em.role
                    FROM events e JOIN event_materials em ON em.event_id=e.id
                    WHERE em.material_id=?
                    ORDER BY e.updated_at DESC
                    """,
                    (material_id,),
                )
            ]
            material["topics"] = [
                dict(topic)
                for topic in conn.execute(
                    """
                    SELECT t.id, t.title, tm.entry_type
                    FROM topics t JOIN topic_materials tm ON tm.topic_id=t.id
                    WHERE tm.material_id=?
                    ORDER BY t.updated_at DESC
                    """,
                    (material_id,),
                )
            ]
            run_row = conn.execute(
                "SELECT run_id FROM ingest_run_items WHERE material_id=? ORDER BY created_at DESC LIMIT 1",
                (material_id,),
            ).fetchone()
        material["run_id"] = run_row["run_id"] if run_row else None
        material["no_original_link"] = not bool(material.get("url"))
        return material

    def ignore_material(self, material_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            refs = conn.execute(
                """
                SELECT
                  (SELECT COUNT(*) FROM event_materials WHERE material_id=?) AS event_refs,
                  (SELECT COUNT(*) FROM topic_materials WHERE material_id=?) AS topic_refs
                """,
                (material_id, material_id),
            ).fetchone()
            if refs["event_refs"] or refs["topic_refs"]:
                raise ValueError("Cannot ignore a material already referenced by Event or Topic")
            conn.execute("UPDATE materials SET ignored=1, updated_at=? WHERE id=?", (utc_now(), material_id))
            conn.commit()
        return self.get_material(material_id)

    def restore_material(self, material_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            conn.execute("UPDATE materials SET ignored=0, updated_at=? WHERE id=?", (utc_now(), material_id))
            conn.commit()
        return self.get_material(material_id)

    def reprocess_material(self, material_id: str, *, allow_mock_llm: bool = False, debug: bool = False) -> dict[str, Any]:
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM materials WHERE id=?", (material_id,)).fetchone()
            if not row:
                raise ValueError(f"Unknown material_id {material_id}")
            material = _parse_material(row)
            before = material.get("light_understanding")
            result = self._run_light_for_material(conn, None, material, llm, trace_mode="debug_full" if debug else "business_summary")
            if result["status"] != "succeeded":
                raise ValueError(result["error_summary"])
            report_path = None
            if debug:
                report_path = self._write_reprocess_compare(material_id, before, result["parsed_json"])
            conn.commit()
        refreshed = self.get_material(material_id)
        refreshed["compare_report_path"] = report_path
        return refreshed

    def reprocess_run(self, run_id: str, *, allow_mock_llm: bool = False, debug: bool = False) -> dict[str, Any]:
        run = self.get_run(run_id)
        reports = []
        for material_id in run["material_ids"]:
            reports.append(self.reprocess_material(material_id, allow_mock_llm=allow_mock_llm, debug=debug))
        return {"run_id": run_id, "material_count": len(reports), "reports": reports}

    def list_events(self, *, status: str | None = None, include_sleeping: bool = False) -> list[dict[str, Any]]:
        clauses = []
        params: list[Any] = []
        if status:
            clauses.append("status=?")
            params.append(status)
        elif not include_sleeping:
            clauses.append("status != 'sleeping'")
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM events {where} ORDER BY pinned DESC, updated_at DESC",
                params,
            ).fetchall()
        return [self._parse_event(row) for row in rows]

    def get_event(self, event_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
            if not row:
                raise ValueError(f"Unknown event_id {event_id}")
            event = self._parse_event(row)
            event["materials"] = [
                {**dict(rel), "material": _parse_material(material)}
                for rel, material in [
                    (
                        rel,
                        conn.execute("SELECT * FROM materials WHERE id=?", (rel["material_id"],)).fetchone(),
                    )
                    for rel in conn.execute("SELECT * FROM event_materials WHERE event_id=? ORDER BY created_at", (event_id,))
                ]
                if material
            ]
            event["updates"] = [
                {**dict(row), "update": _loads(row["update_json"], {})}
                for row in conn.execute("SELECT * FROM event_updates WHERE event_id=? ORDER BY created_at DESC", (event_id,))
            ]
            event["topics"] = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT t.id, t.title FROM topics t
                    JOIN topic_materials tm ON tm.topic_id=t.id
                    WHERE tm.event_id=?
                    """,
                    (event_id,),
                )
            ]
        return event

    def create_event_from_materials(
        self,
        material_ids: list[str],
        *,
        title: str | None = None,
        user_focus: str | None = None,
        allow_mock_llm: bool = False,
        status: str = "official",
    ) -> dict[str, Any]:
        if not material_ids:
            raise ValueError("Event requires at least one material")
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        with self.connect() as conn:
            materials = [self._material_for_llm(conn, mid) for mid in material_ids]
            result = llm.run_json_task(
                task_name="event_update",
                prompt_file="event_update_v1.md",
                input_data={"event": {"title": title or materials[0]["title"]}, "current_center_description": {}, "new_materials": materials, "user_focus": user_focus},
                input_material_ids=material_ids,
            )
            if result["status"] != "succeeded":
                raise ValueError(result["error_summary"] or "Event center generation failed")
            event_id = _id("event")
            now = utc_now()
            center = result["parsed_json"]["center_description"]
            event_title = title or self._event_title_from_materials(materials)
            conn.execute(
                """
                INSERT INTO events(id, title, status, center_description_json, user_focus, created_at, updated_at, last_meaningful_update_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (event_id, event_title, status, _json(center), user_focus, now, now, now if status == "official" else None),
            )
            for mid in material_ids:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO event_materials(id, event_id, material_id, role, note, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (_id("em"), event_id, mid, "core_update" if status == "official" else "candidate_support", "created from selected materials", now),
                )
            self._insert_llm_summary(conn, "event_update", result, material_ids[0], None)
            conn.commit()
        return self.get_event(event_id)

    def promote_event(self, event_id: str, *, user_focus: str | None = None, allow_mock_llm: bool = False) -> dict[str, Any]:
        event = self.get_event(event_id)
        if event["status"] != "candidate":
            raise ValueError("Only candidate Events can be promoted")
        material_ids = [item["material_id"] for item in event["materials"]]
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        with self.connect() as conn:
            materials = [self._material_for_llm(conn, mid) for mid in material_ids]
            result = llm.run_json_task(
                task_name="event_update",
                prompt_file="event_update_v1.md",
                input_data={"event": event, "current_center_description": {}, "new_materials": materials, "user_focus": user_focus or event.get("user_focus")},
                input_material_ids=material_ids,
            )
            if result["status"] != "succeeded":
                raise ValueError(result["error_summary"] or "Event promotion failed")
            now = utc_now()
            conn.execute(
                """
                UPDATE events
                SET status='official', center_description_json=?, user_focus=COALESCE(?, user_focus),
                    updated_at=?, last_meaningful_update_at=?
                WHERE id=?
                """,
                (_json(result["parsed_json"]["center_description"]), user_focus, now, now, event_id),
            )
            conn.execute(
                "UPDATE event_materials SET role='core_update', note='promoted candidate support' WHERE event_id=?",
                (event_id,),
            )
            self._insert_llm_summary(conn, "event_update", result, material_ids[0] if material_ids else None, None)
            conn.commit()
        return self.get_event(event_id)

    def ignore_candidate_event(self, event_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            conn.execute(
                "UPDATE events SET ignored_candidate=1, status='sleeping', sleeping_reason='candidate ignored', updated_at=? WHERE id=? AND status='candidate'",
                (utc_now(), event_id),
            )
            conn.commit()
        return self.get_event(event_id)

    def create_topic(self, title: str, goal: str, organization: str, material_ids: list[str], event_ids: list[str]) -> dict[str, Any]:
        topic_id = _id("topic")
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO topics(id, title, goal, organization, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (topic_id, title, goal, organization, now, now),
            )
            self._add_topic_links(conn, topic_id, material_ids, event_ids)
            conn.commit()
        return self.get_topic(topic_id)

    def list_topics(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM topics ORDER BY pinned DESC, updated_at DESC").fetchall()
        return [self._parse_topic(row) for row in rows]

    def get_topic(self, topic_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM topics WHERE id=?", (topic_id,)).fetchone()
            if not row:
                raise ValueError(f"Unknown topic_id {topic_id}")
            topic = self._parse_topic(row)
            links = conn.execute("SELECT * FROM topic_materials WHERE topic_id=? ORDER BY added_at DESC", (topic_id,)).fetchall()
            materials = []
            events = []
            for link in links:
                data = dict(link)
                if link["material_id"]:
                    mat = conn.execute("SELECT * FROM materials WHERE id=?", (link["material_id"],)).fetchone()
                    if mat:
                        data["material"] = _parse_material(mat)
                        materials.append(data)
                if link["event_id"]:
                    ev = conn.execute("SELECT * FROM events WHERE id=?", (link["event_id"],)).fetchone()
                    if ev:
                        data["event"] = self._parse_event(ev)
                        events.append(data)
            topic["materials"] = materials
            topic["events"] = events
            topic["unincorporated_material_count"] = sum(1 for item in materials if not item["referenced_by_current_structure"])
        return topic

    def add_topic_materials(self, topic_id: str, material_ids: list[str], event_ids: list[str]) -> dict[str, Any]:
        with self.connect() as conn:
            self._add_topic_links(conn, topic_id, material_ids, event_ids)
            conn.execute("UPDATE topics SET updated_at=? WHERE id=?", (utc_now(), topic_id))
            conn.commit()
        return self.get_topic(topic_id)

    def refresh_topic_structure(self, topic_id: str, *, include_new_materials: bool = True, allow_mock_llm: bool = False) -> dict[str, Any]:
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        topic = self.get_topic(topic_id)
        materials = [self._material_for_llm_dict(item["material"]) for item in topic["materials"]]
        result = llm.run_json_task(
            task_name="topic_structure",
            prompt_file="topic_structure_v1.md",
            input_data={
                "topic": {"id": topic_id, "title": topic["title"], "goal": topic["goal"], "organization": topic["organization"]},
                "current_structure": topic["current_structure"],
                "materials": materials,
                "new_materials_since_refresh": materials if include_new_materials else [],
                "referenced_events": [item.get("event") for item in topic["events"]],
                "user_constraints": topic["node_constraints"],
            },
            input_material_ids=[item["material"]["id"] for item in topic["materials"]],
        )
        if result["status"] != "succeeded":
            raise ValueError(result["error_summary"] or "Topic structure refresh failed")
        with self.connect() as conn:
            conn.execute(
                "UPDATE topics SET candidate_structure_json=?, last_structure_refresh_at=?, updated_at=? WHERE id=?",
                (_json(result["parsed_json"]["structure"]), utc_now(), utc_now(), topic_id),
            )
            self._insert_llm_summary(conn, "topic_structure", result, None, None)
            conn.commit()
        return self.get_topic(topic_id)

    def confirm_topic_candidate(self, topic_id: str) -> dict[str, Any]:
        with self.connect() as conn:
            topic = conn.execute("SELECT candidate_structure_json FROM topics WHERE id=?", (topic_id,)).fetchone()
            if not topic:
                raise ValueError(f"Unknown topic_id {topic_id}")
            candidate = _loads(topic["candidate_structure_json"], {})
            if not candidate:
                raise ValueError("No candidate structure to confirm")
            referenced_ids = self._collect_structure_material_ids(candidate)
            conn.execute(
                "UPDATE topics SET current_structure_json=?, candidate_structure_json='{}', updated_at=? WHERE id=?",
                (_json(candidate), utc_now(), topic_id),
            )
            conn.execute("UPDATE topic_materials SET referenced_by_current_structure=0 WHERE topic_id=?", (topic_id,))
            for mid in referenced_ids:
                conn.execute(
                    "UPDATE topic_materials SET referenced_by_current_structure=1 WHERE topic_id=? AND material_id=?",
                    (topic_id, mid),
                )
            conn.commit()
        return self.get_topic(topic_id)

    def local_refresh_topic(self, topic_id: str, node_id: str, instruction: str, *, include_new_materials: bool = True, allow_mock_llm: bool = False) -> dict[str, Any]:
        topic = self.get_topic(topic_id)
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        materials = [self._material_for_llm_dict(item["material"]) for item in topic["materials"]]
        result = llm.run_json_task(
            task_name="topic_local_refresh",
            prompt_file="topic_local_refresh_v1.md",
            input_data={
                "topic": {"id": topic_id, "title": topic["title"], "goal": topic["goal"]},
                "node": {"id": node_id},
                "node_constraint": instruction,
                "include_new_materials": include_new_materials,
                "materials": materials,
            },
            input_material_ids=[item["material"]["id"] for item in topic["materials"]],
        )
        if result["status"] != "succeeded":
            raise ValueError(result["error_summary"] or "Topic local refresh failed")
        candidate = topic["candidate_structure"] or topic["current_structure"] or {"title": topic["title"], "nodes": []}
        candidate.setdefault("nodes", []).append(result["parsed_json"]["structure"]["nodes"][0])
        with self.connect() as conn:
            constraints = topic["node_constraints"]
            constraints[node_id] = instruction
            conn.execute(
                "UPDATE topics SET candidate_structure_json=?, node_constraints_json=?, updated_at=? WHERE id=?",
                (_json(candidate), _json(constraints), utc_now(), topic_id),
            )
            self._insert_llm_summary(conn, "topic_local_refresh", result, None, None)
            conn.commit()
        return self.get_topic(topic_id)

    def export_materials(self, material_ids: list[str]) -> dict[str, Any]:
        materials = [self.get_material(mid) for mid in material_ids]
        title = "materials_" + timestamp_slug()
        return self._write_export("material", "multiple", title, self._render_material_export(materials), len(materials))

    def export_event(self, event_id: str) -> dict[str, Any]:
        event = self.get_event(event_id)
        materials = [item["material"] for item in event["materials"]]
        return self._write_export("event", event_id, event["title"], self._render_event_export(event, materials), len(materials))

    def export_topic(self, topic_id: str) -> dict[str, Any]:
        topic = self.get_topic(topic_id)
        materials = [item["material"] for item in topic["materials"]]
        for event_link in topic["events"]:
            event = self.get_event(event_link["event_id"])
            materials.extend(item["material"] for item in event["materials"])
        seen = {}
        for mat in materials:
            seen[mat["id"]] = mat
        return self._write_export("topic", topic_id, topic["title"], self._render_topic_export(topic, list(seen.values())), len(seen))

    def prompt_eval(
        self,
        *,
        task: str,
        material_ids: list[str] | None = None,
        run_id: str | None = None,
        fixture_file: str | None = None,
        fixture_group: str | None = None,
        test_purpose: str | None = None,
        limit: int | None = None,
        allow_mock_llm: bool = False,
        concurrency: int = 1,
    ) -> dict[str, Any]:
        settings = self.settings.with_mock_llm() if allow_mock_llm else self.settings
        llm = LLMClient(settings)
        run_dir = self.settings.outputs_dir / "prompt_evals" / timestamp_slug()
        trace_dir = run_dir / "llm_traces"
        run_dir.mkdir(parents=True, exist_ok=True)
        trace_dir.mkdir(parents=True, exist_ok=True)
        samples = self._prompt_eval_samples(material_ids or [], run_id, fixture_file, fixture_group, test_purpose)
        expected_count = len(samples)
        if limit is not None:
            samples = samples[:limit]
        results = []
        def run_light_sample(sample: dict[str, Any]) -> dict[str, Any]:
            return llm.run_json_task(
                task_name="light_understanding",
                prompt_file="light_understanding_v1.md",
                input_data=sample,
                input_material_ids=[sample.get("id")] if sample.get("id") else [],
                trace_mode="prompt_eval_full",
                trace_dir=trace_dir,
            )

        if task == "light_understanding" and concurrency > 1 and len(samples) > 1:
            with ThreadPoolExecutor(max_workers=max(1, min(concurrency, 12))) as executor:
                future_to_sample = {executor.submit(run_light_sample, sample): sample for sample in samples}
                for future in as_completed(future_to_sample):
                    try:
                        results.append(future.result())
                    except Exception as exc:  # noqa: BLE001
                        results.append(
                            {
                                "status": "failed",
                                "error_summary": str(exc),
                                "provider": settings.llm_provider,
                                "model": settings.deepseek_model,
                                "prompt_file": "light_understanding_v1.md",
                                "prompt_version": "unknown",
                            }
                        )
        else:
            for sample in samples:
                if task == "light_understanding":
                    input_data = sample
                    prompt_file = "light_understanding_v1.md"
                    task_name = "light_understanding"
                elif task == "event_candidate":
                    input_data = {"run_id": run_id or "prompt_eval", "materials": samples, "active_events": []}
                    prompt_file = "event_candidate_v1.md"
                    task_name = "event_candidate"
                    results.append(
                        llm.run_json_task(
                            task_name=task_name,
                            prompt_file=prompt_file,
                            input_data=input_data,
                            input_material_ids=[item["id"] for item in samples if item.get("id")],
                            trace_mode="prompt_eval_full",
                            trace_dir=trace_dir,
                        )
                    )
                    break
                else:
                    input_data = {
                        "topic": {"title": "Prompt eval synthetic topic", "goal": "Evaluate structure quality"},
                        "current_structure": {},
                        "materials": samples,
                        "new_materials_since_refresh": samples,
                        "referenced_events": [],
                        "user_constraints": {},
                    }
                    prompt_file = "topic_structure_v1.md"
                    task_name = "topic_structure"
                    results.append(
                        llm.run_json_task(
                            task_name=task_name,
                            prompt_file=prompt_file,
                            input_data=input_data,
                            input_material_ids=[item["id"] for item in samples if item.get("id")],
                            trace_mode="prompt_eval_full",
                            trace_dir=trace_dir,
                        )
                    )
                    break
                results.append(
                    llm.run_json_task(
                        task_name=task_name,
                        prompt_file=prompt_file,
                        input_data=input_data,
                        input_material_ids=[sample.get("id")] if sample.get("id") else [],
                        trace_mode="prompt_eval_full",
                        trace_dir=trace_dir,
                    )
                )
        succeeded = sum(1 for item in results if item["status"] == "succeeded")
        failed = len(results) - succeeded
        coverage = {
            "expected_count": expected_count,
            "actual_count": len(samples),
            "task_invocations": len(results),
            "fixture_group": fixture_group,
            "test_purpose": test_purpose,
            "provider": settings.llm_provider,
        }
        summary_path = run_dir / "summary.md"
        compare_path = run_dir / "compare.md"
        summary_path.write_text(
            "\n".join(
                [
                    f"# Prompt Eval {task}",
                    "",
                    f"- Created: {utc_now()}",
                    f"- Provider: {settings.llm_provider}",
                    f"- Model: {settings.deepseek_model}",
                    f"- Expected coverage: {expected_count}",
                    f"- Actual sample count: {len(samples)}",
                    f"- Task invocations: {len(results)}",
                    f"- Succeeded: {succeeded}",
                    f"- Failed: {failed}",
                    f"- Trace dir: {trace_dir}",
                    "",
                    "## Semantic Quality Notes",
                    "",
                    "This report records schema and semantic checks from each trace. Mock provider results are test-only and cannot count as final READY validation." if settings.llm_provider == "mock" else "Real DeepSeek output must be reviewed for faithfulness, classification quality, and over-invention.",
                ]
            ),
            encoding="utf-8",
        )
        compare_path.write_text(
            "# Compare\n\nNo prompt revision comparison was performed in this run.\n",
            encoding="utf-8",
        )
        return {
            "task": task,
            "summary_path": str(summary_path),
            "compare_path": str(compare_path),
            "trace_dir": str(trace_dir),
            "coverage": coverage,
            "succeeded": succeeded,
            "failed": failed,
        }

    def cleanup_synthetic(self) -> dict[str, Any]:
        with self.connect() as conn:
            synthetic_ids = [row["id"] for row in conn.execute("SELECT id FROM materials WHERE synthetic=1")]
            protected_topic_refs = conn.execute(
                "SELECT COUNT(*) AS count FROM topic_materials WHERE material_id IN (SELECT id FROM materials WHERE synthetic=1)"
            ).fetchone()["count"]
            protected_event_refs = conn.execute(
                "SELECT COUNT(*) AS count FROM event_materials WHERE material_id IN (SELECT id FROM materials WHERE synthetic=1)"
            ).fetchone()["count"]
            conn.execute("DELETE FROM exports WHERE object_id IN (SELECT id FROM materials WHERE synthetic=1)")
            conn.execute("DELETE FROM material_relations WHERE primary_material_id IN (SELECT id FROM materials WHERE synthetic=1) OR related_material_id IN (SELECT id FROM materials WHERE synthetic=1)")
            conn.execute("DELETE FROM event_materials WHERE material_id IN (SELECT id FROM materials WHERE synthetic=1)")
            conn.execute("DELETE FROM topic_materials WHERE material_id IN (SELECT id FROM materials WHERE synthetic=1)")
            conn.execute("DELETE FROM materials WHERE synthetic=1")
            conn.execute("DELETE FROM ingest_runs WHERE synthetic=1")
            conn.commit()
        return {
            "deleted_material_count": len(synthetic_ids),
            "removed_topic_refs": protected_topic_refs,
            "removed_event_refs": protected_event_refs,
        }

    def _get_run_row(self, conn: sqlite3.Connection, run_id: str) -> sqlite3.Row | None:
        return conn.execute("SELECT * FROM ingest_runs WHERE id=?", (run_id,)).fetchone()

    def _log(self, conn: sqlite3.Connection, run_id: str, step_name: str | None, level: str, message: str, details: dict[str, Any] | None = None) -> None:
        conn.execute(
            """
            INSERT INTO run_logs(run_id, step_name, level, message, details_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (run_id, step_name, level, message, _json(details or {}), utc_now()),
        )

    def _mark_step(
        self,
        conn: sqlite3.Connection,
        run_id: str,
        step_name: str,
        status: str,
        input_count: int,
        output_count: int,
        skipped_count: int,
        failed_count: int,
        message: str,
        error_summary: str | None = None,
    ) -> None:
        now = utc_now()
        conn.execute(
            """
            UPDATE run_steps
            SET status=?, started_at=COALESCE(started_at, ?), finished_at=?,
                input_count=?, output_count=?, skipped_count=?, failed_count=?,
                message=?, error_summary=?
            WHERE run_id=? AND step_name=?
            """,
            (status, now, now, input_count, output_count, skipped_count, failed_count, message, error_summary, run_id, step_name),
        )
        if status in {"failed", "skipped"}:
            self._log(conn, run_id, step_name, "warning" if status == "skipped" else "error", message, {"error_summary": error_summary})
        else:
            self._log(conn, run_id, step_name, "info", message, {"input_count": input_count, "output_count": output_count})
        conn.commit()

    def _step_failed(self, conn: sqlite3.Connection, run_id: str, step_name: str) -> bool:
        row = conn.execute("SELECT status FROM run_steps WHERE run_id=? AND step_name=?", (run_id, step_name)).fetchone()
        return bool(row and row["status"] == "failed")

    def _step_validate_input(self, conn: sqlite3.Connection, run_id: str) -> list[tuple[str, MaterialUpload]]:
        rows = conn.execute("SELECT * FROM ingest_run_items WHERE run_id=? ORDER BY created_at", (run_id,)).fetchall()
        valid: list[tuple[str, MaterialUpload]] = []
        failed = 0
        for row in rows:
            raw = _loads(row["raw_json"], {})
            try:
                item = MaterialUpload.model_validate(raw)
                valid.append((row["id"], item))
                conn.execute("UPDATE ingest_run_items SET validation_status='valid', error=NULL WHERE id=?", (row["id"],))
            except ValidationError as exc:
                failed += 1
                conn.execute(
                    "UPDATE ingest_run_items SET validation_status='invalid', error=? WHERE id=?",
                    (str(exc), row["id"]),
                )
                self._log(conn, run_id, "validate_input", "error", "Item validation failed", {"item_id": row["id"], "error": str(exc)})
        status = "succeeded" if valid else "failed"
        self._mark_step(conn, run_id, "validate_input", status, len(rows), len(valid), 0, failed, f"Validated {len(valid)} of {len(rows)} items", None if valid else "No valid items")
        conn.execute("UPDATE ingest_runs SET accepted_count=?, failed_count=?, updated_at=? WHERE id=?", (len(valid), failed, utc_now(), run_id))
        conn.commit()
        return valid

    def _step_dedupe(self, conn: sqlite3.Connection, run_id: str, valid_items: list[tuple[str, MaterialUpload]]) -> list[dict[str, Any]]:
        decisions: list[dict[str, Any]] = []
        seen_hashes: dict[str, str] = {}
        duplicate_count = 0
        for item_id, item in valid_items:
            content_hash = _material_hash(item)
            url = item.url or item.source_url
            existing = None
            if url:
                existing = conn.execute("SELECT id FROM materials WHERE url=? LIMIT 1", (url,)).fetchone()
            if not existing and item.external_id:
                existing = conn.execute("SELECT id FROM materials WHERE external_id=? LIMIT 1", (item.external_id,)).fetchone()
            if not existing:
                existing = conn.execute("SELECT id FROM materials WHERE content_hash=? LIMIT 1", (content_hash,)).fetchone()
            primary_item_id = seen_hashes.get(content_hash)
            primary_id = existing["id"] if existing else None
            same_run_duplicate = bool(primary_item_id and not primary_id)
            duplicate_target = primary_id or primary_item_id
            is_duplicate = bool(duplicate_target)
            if is_duplicate:
                duplicate_count += 1
                self._log(conn, run_id, "dedupe_compress", "info", "Duplicate item linked to primary material", {"item_id": item_id, "primary_material_id": primary_id, "content_hash": content_hash})
            else:
                seen_hashes[content_hash] = item_id
            decisions.append(
                {
                    "item_id": item_id,
                    "item": item,
                    "content_hash": content_hash,
                    "duplicate_of": primary_id,
                    "duplicate_of_item_id": primary_item_id if same_run_duplicate else None,
                    "is_duplicate": is_duplicate,
                }
            )
        self._mark_step(conn, run_id, "dedupe_compress", "succeeded", len(valid_items), len(valid_items) - duplicate_count, duplicate_count, 0, f"Detected {duplicate_count} exact duplicates")
        conn.execute("UPDATE ingest_runs SET duplicate_count=?, updated_at=? WHERE id=?", (duplicate_count, utc_now(), run_id))
        conn.commit()
        return decisions

    def _step_persist(self, conn: sqlite3.Connection, run_id: str, decisions: list[dict[str, Any]]) -> list[str]:
        material_ids: list[str] = []
        item_to_material: dict[str, str] = {}
        failed = 0
        for decision in decisions:
            item: MaterialUpload = decision["item"]
            primary_id = decision.get("duplicate_of")
            if not primary_id and decision.get("duplicate_of_item_id"):
                primary_id = item_to_material.get(decision["duplicate_of_item_id"])
            if primary_id:
                conn.execute("UPDATE ingest_run_items SET material_id=? WHERE id=?", (primary_id, decision["item_id"]))
                conn.execute(
                    """
                    INSERT OR IGNORE INTO material_relations(id, primary_material_id, related_material_id, relation_type, reason, score, run_id, created_at)
                    VALUES (?, ?, ?, 'exact_duplicate', ?, 1.0, ?, ?)
                    """,
                    (_id("rel"), primary_id, primary_id, "duplicate upload item points to existing primary material", run_id, utc_now()),
                )
                material_ids.append(primary_id)
                item_to_material[decision["item_id"]] = primary_id
                continue
            material_id = _id("mat")
            if not decision["duplicate_of"]:
                decision["content_hash"] = decision["content_hash"]
            metadata = dict(item.metadata or {})
            synthetic = bool(metadata.get("synthetic"))
            raw_payload = item.raw_payload or {}
            if not raw_payload:
                raw_payload = item.model_dump(exclude={"metadata", "raw_payload"})
            now = utc_now()
            url = item.url or item.source_url
            try:
                conn.execute(
                    """
                    INSERT INTO materials(
                      id, title, content_text, source_name, source_type, url, external_id,
                      author, published_at, fetched_at, language, content_html,
                      summary_from_source, tags_from_source_json, upstream_score, upstream_reason,
                      metadata_json, raw_payload_json, content_hash, title_hash, synthetic,
                      created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        material_id,
                        item.title,
                        item.content_text,
                        item.source_name,
                        item.source_type,
                        url,
                        item.external_id,
                        item.author,
                        item.published_at,
                        item.fetched_at,
                        item.language,
                        item.content_html,
                        item.summary_from_source,
                        _json(item.tags_from_source),
                        item.upstream_score,
                        item.upstream_reason,
                        _json(metadata),
                        _json(raw_payload),
                        decision["content_hash"],
                        _title_hash(item),
                        int(synthetic),
                        now,
                        now,
                    ),
                )
                conn.execute("UPDATE ingest_run_items SET material_id=? WHERE id=?", (material_id, decision["item_id"]))
                material_ids.append(material_id)
                item_to_material[decision["item_id"]] = material_id
            except sqlite3.Error as exc:
                failed += 1
                conn.execute("UPDATE ingest_run_items SET validation_status='persist_failed', error=? WHERE id=?", (str(exc), decision["item_id"]))
                self._log(conn, run_id, "persist_materials", "error", "Material persist failed", {"item_id": decision["item_id"], "error": str(exc)})
        unique_ids = sorted(set(material_ids))
        status = "succeeded" if not failed else "failed"
        self._mark_step(conn, run_id, "persist_materials", status, len(decisions), len(unique_ids), 0, failed, f"Persisted or linked {len(unique_ids)} materials", None if not failed else "One or more materials failed to persist")
        conn.execute("UPDATE ingest_runs SET material_count=?, updated_at=? WHERE id=?", (len(unique_ids), utc_now(), run_id))
        conn.commit()
        return unique_ids

    def _step_light_understanding(self, conn: sqlite3.Connection, run_id: str, material_ids: list[str], llm: LLMClient) -> bool:
        failed = 0
        noise = 0
        traces: list[str] = []
        materials = [self._material_for_llm(conn, material_id) for material_id in material_ids]
        pending_materials = [material for material in materials if material.get("light_understanding_status") != "succeeded"]
        results: list[tuple[dict[str, Any], dict[str, Any]]] = []

        if llm.provider == "deepseek" and len(pending_materials) > 1:
            with ThreadPoolExecutor(max_workers=min(6, len(pending_materials))) as executor:
                future_to_material = {
                    executor.submit(self._run_light_task, material, llm, "business_summary"): material
                    for material in pending_materials
                }
                for future in as_completed(future_to_material):
                    material = future_to_material[future]
                    try:
                        result = future.result()
                    except Exception as exc:  # noqa: BLE001
                        result = {
                            "status": "failed",
                            "parsed_json": None,
                            "trace_path": None,
                            "semantic_check": {"status": "failed", "notes": [str(exc)], "checked_at": utc_now()},
                            "error_summary": str(exc),
                            "provider": llm.provider,
                            "model": llm.model,
                            "prompt_file": "light_understanding_v1.md",
                            "prompt_version": "unknown",
                        }
                    results.append((material, result))
        else:
            for material in pending_materials:
                results.append((material, self._run_light_task(material, llm, "business_summary")))

        for material, result in results:
            self._persist_light_result(conn, run_id, material, result)
            traces.append(result.get("trace_path") or "")
            if result["status"] != "succeeded":
                failed += 1
                self._log(conn, run_id, "light_understanding", "error", "Light understanding failed", {"material_id": material["id"], "error": result["error_summary"]})
                break
            facets = result["parsed_json"].get("content_facets", [])
            if "noise" in facets:
                noise += 1
        if failed:
            self._mark_step(conn, run_id, "light_understanding", "failed", len(material_ids), len(material_ids) - failed, 0, failed, "Light understanding failed", "DeepSeek/mock task failed; no fake business result was written")
            conn.execute("UPDATE ingest_runs SET trace_paths_json=?, noise_count=?, updated_at=? WHERE id=?", (_json([item for item in traces if item]), noise, utc_now(), run_id))
            conn.commit()
            return False
        self._mark_step(conn, run_id, "light_understanding", "succeeded", len(material_ids), len(material_ids), 0, 0, f"Light understanding completed for {len(material_ids)} materials")
        conn.execute("UPDATE ingest_runs SET trace_paths_json=?, noise_count=?, updated_at=? WHERE id=?", (_json([item for item in traces if item]), noise, utc_now(), run_id))
        conn.commit()
        return True

    def _run_light_for_material(self, conn: sqlite3.Connection, run_id: str | None, material: dict[str, Any], llm: LLMClient, trace_mode: str = "business_summary") -> dict[str, Any]:
        result = self._run_light_task(material, llm, trace_mode)
        self._persist_light_result(conn, run_id, material, result)
        conn.commit()
        return result

    def _run_light_task(self, material: dict[str, Any], llm: LLMClient, trace_mode: str) -> dict[str, Any]:
        input_data = {
            "material_id": material["id"],
            "title": material["title"],
            "source_name": material["source_name"],
            "source_type": material["source_type"],
            "published_at": material.get("published_at"),
            "content_text": material["content_text"],
            "upstream_score": material.get("upstream_score"),
            "upstream_reason": material.get("upstream_reason"),
            "metadata": material.get("metadata") or {},
        }
        result = llm.run_json_task(
            task_name="light_understanding",
            prompt_file="light_understanding_v1.md",
            input_data=input_data,
            input_material_ids=[material["id"]],
            trace_mode=trace_mode,
        )
        return result

    def _persist_light_result(self, conn: sqlite3.Connection, run_id: str | None, material: dict[str, Any], result: dict[str, Any]) -> None:
        if result["status"] == "succeeded":
            conn.execute(
                """
                UPDATE materials
                SET light_understanding_json=?, light_understanding_status='succeeded', llm_trace_path=?, updated_at=?
                WHERE id=?
                """,
                (_json(result["parsed_json"]), result["trace_path"], utc_now(), material["id"]),
            )
        else:
            conn.execute(
                "UPDATE materials SET light_understanding_status='failed', llm_trace_path=?, updated_at=? WHERE id=?",
                (result["trace_path"], utc_now(), material["id"]),
            )
        self._insert_llm_summary(conn, "light_understanding", result, material["id"], run_id)

    def _step_similarity(self, conn: sqlite3.Connection, run_id: str, material_ids: list[str]) -> None:
        created = 0
        materials = [
            _parse_material(row)
            for row in conn.execute(
                "SELECT * FROM materials WHERE id IN (%s)" % ",".join("?" for _ in material_ids),
                material_ids,
            )
        ] if material_ids else []
        by_event_key: dict[str, list[dict[str, Any]]] = {}
        for material in materials:
            key = (material.get("metadata") or {}).get("event_key")
            if key:
                by_event_key.setdefault(str(key), []).append(material)
        for group in by_event_key.values():
            for left in group:
                for right in group:
                    if left["id"] >= right["id"]:
                        continue
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO material_relations(id, primary_material_id, related_material_id, relation_type, reason, score, run_id, created_at)
                        VALUES (?, ?, ?, 'near_duplicate', ?, 0.74, ?, ?)
                        """,
                        (_id("rel"), left["id"], right["id"], "shared synthetic event key or similar incident thread", run_id, utc_now()),
                    )
                    created += 1
        self._mark_step(conn, run_id, "similarity_marking", "succeeded", len(material_ids), created, 0, 0, f"Marked {created} near-similar relationships")
        conn.commit()

    def _step_candidate_events(self, conn: sqlite3.Connection, run_id: str, material_ids: list[str], llm: LLMClient) -> list[str]:
        materials = [self._material_for_llm(conn, mid) for mid in material_ids]
        active_events = [self._parse_event(row) for row in conn.execute("SELECT * FROM events WHERE status='official'")]
        result = llm.run_json_task(
            task_name="event_candidate",
            prompt_file="event_candidate_v1.md",
            input_data={"run_id": run_id, "materials": materials, "active_events": active_events},
            input_material_ids=material_ids,
        )
        if result["status"] != "succeeded":
            self._mark_step(conn, run_id, "candidate_events", "failed", len(material_ids), 0, 0, 1, "Candidate Event generation failed", result["error_summary"])
            self._insert_llm_summary(conn, "event_candidate", result, material_ids[0] if material_ids else None, run_id)
            conn.commit()
            return []
        event_ids: list[str] = []
        for candidate in result["parsed_json"].get("candidates", []):
            mids = [mid for mid in candidate.get("material_ids", []) if mid in material_ids]
            if not mids:
                continue
            event_id = _id("event")
            now = utc_now()
            center = {
                "main_thread": candidate.get("title", "Candidate event"),
                "known_facts": [candidate.get("reason", "")],
                "recent_changes": [],
                "open_questions": candidate.get("doubts", []),
            }
            conn.execute(
                """
                INSERT INTO events(id, title, status, center_description_json, user_focus, created_at, updated_at)
                VALUES (?, ?, 'candidate', ?, NULL, ?, ?)
                """,
                (event_id, candidate.get("title", "Candidate event"), _json(center), now, now),
            )
            for mid in mids:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO event_materials(id, event_id, material_id, role, note, created_at)
                    VALUES (?, ?, ?, 'candidate_support', ?, ?)
                    """,
                    (_id("em"), event_id, mid, candidate.get("reason", ""), now),
                )
            event_ids.append(event_id)
        self._insert_llm_summary(conn, "event_candidate", result, material_ids[0] if material_ids else None, run_id)
        self._mark_step(conn, run_id, "candidate_events", "succeeded", len(material_ids), len(event_ids), 0, 0, f"Generated {len(event_ids)} candidate Events")
        conn.execute("UPDATE ingest_runs SET candidate_event_count=?, updated_at=? WHERE id=?", (len(event_ids), utc_now(), run_id))
        conn.commit()
        return event_ids

    def _step_active_event_matching(self, conn: sqlite3.Connection, run_id: str, material_ids: list[str]) -> None:
        official_events = conn.execute("SELECT * FROM events WHERE status='official'").fetchall()
        matched = 0
        if not official_events:
            self._mark_step(conn, run_id, "active_event_matching", "succeeded", len(material_ids), 0, 0, 0, "No active official Events to match")
            return
        for material_id in material_ids:
            material = self._material_for_llm(conn, material_id)
            material_key = (material.get("metadata") or {}).get("event_key")
            if not material_key:
                continue
            for event_row in official_events:
                event = self._parse_event(event_row)
                if material_key.lower() in event["title"].lower():
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO event_materials(id, event_id, material_id, role, note, created_at)
                        VALUES (?, ?, ?, 'supporting_no_new_info', ?, ?)
                        """,
                        (_id("em"), event["id"], material_id, "matched by event key; no center update in deterministic pass", utc_now()),
                    )
                    matched += 1
        self._mark_step(conn, run_id, "active_event_matching", "succeeded", len(material_ids), matched, 0, 0, f"Matched {matched} materials to active Events")
        conn.commit()

    def _step_finalize(self, conn: sqlite3.Connection, run_id: str, material_ids: list[str], candidate_event_ids: list[str]) -> None:
        self._mark_step(conn, run_id, "finalize_run", "succeeded", len(material_ids), len(material_ids), 0, 0, "Run finalized")
        conn.execute(
            "UPDATE ingest_runs SET status='succeeded', material_count=?, candidate_event_count=?, updated_at=? WHERE id=?",
            (len(material_ids), len(candidate_event_ids), utc_now(), run_id),
        )
        conn.commit()

    def _finalize_failed(self, conn: sqlite3.Connection, run_id: str, failed_steps: list[str]) -> None:
        conn.execute(
            "UPDATE ingest_runs SET status='failed', error_summary=?, updated_at=? WHERE id=?",
            (", ".join(failed_steps), utc_now(), run_id),
        )
        conn.commit()

    def _process_response(self, conn: sqlite3.Connection, run_id: str, material_ids: list[str], candidate_event_ids: list[str], failed_steps: list[str]) -> dict[str, Any]:
        row = self._get_run_row(conn, run_id)
        return {
            "run_id": run_id,
            "status": row["status"] if row else "unknown",
            "material_ids": sorted(set(material_ids)),
            "candidate_event_ids": candidate_event_ids,
            "failed_steps": failed_steps,
        }

    def _insert_llm_summary(self, conn: sqlite3.Connection, task_name: str, result: dict[str, Any], material_id: str | None, run_id: str | None) -> None:
        conn.execute(
            """
            INSERT INTO llm_call_summaries(
              id, task_name, provider, model, prompt_file, prompt_version, status,
              material_id, run_id, trace_path, semantic_check_json, error_summary, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _id("llm"),
                task_name,
                result.get("provider", "unknown"),
                result.get("model", ""),
                result.get("prompt_file", ""),
                result.get("prompt_version", ""),
                result.get("status", "failed"),
                material_id,
                run_id,
                result.get("trace_path"),
                _json(result.get("semantic_check") or {}),
                result.get("error_summary"),
                utc_now(),
            ),
        )

    def _material_for_llm(self, conn: sqlite3.Connection, material_id: str) -> dict[str, Any]:
        row = conn.execute("SELECT * FROM materials WHERE id=?", (material_id,)).fetchone()
        if not row:
            raise ValueError(f"Unknown material_id {material_id}")
        return self._material_for_llm_dict(_parse_material(row))

    def _material_for_llm_dict(self, material: dict[str, Any]) -> dict[str, Any]:
        light = material.get("light_understanding") or {}
        return {
            "id": material["id"],
            "title": material["title"],
            "source_name": material["source_name"],
            "source_type": material["source_type"],
            "published_at": material.get("published_at"),
            "url": material.get("url"),
            "content_text": material["content_text"],
            "content_snippet": _material_snippet(material, 500),
            "content_facets": light.get("content_facets", []),
            "summary": light.get("summary"),
            "metadata": material.get("metadata") or {},
            "ignored": material.get("ignored", False),
        }

    def _event_title_from_materials(self, materials: list[dict[str, Any]]) -> str:
        if not materials:
            return "Untitled Event"
        key = (materials[0].get("metadata") or {}).get("event_key")
        if key:
            return f"Synthetic event: {str(key).replace('_', ' ')}"
        return materials[0]["title"][:120]

    def _parse_event(self, row: sqlite3.Row) -> dict[str, Any]:
        event = dict(row)
        event["center_description"] = _loads(event.pop("center_description_json"), {})
        event["pinned"] = bool(event["pinned"])
        event["favorite"] = bool(event["favorite"])
        event["ignored_candidate"] = bool(event["ignored_candidate"])
        return event

    def _parse_topic(self, row: sqlite3.Row) -> dict[str, Any]:
        topic = dict(row)
        topic["current_structure"] = _loads(topic.pop("current_structure_json"), {})
        topic["candidate_structure"] = _loads(topic.pop("candidate_structure_json"), {})
        topic["node_constraints"] = _loads(topic.pop("node_constraints_json"), {})
        topic["pinned"] = bool(topic["pinned"])
        return topic

    def _add_topic_links(self, conn: sqlite3.Connection, topic_id: str, material_ids: list[str], event_ids: list[str]) -> None:
        now = utc_now()
        for mid in material_ids:
            conn.execute(
                """
                INSERT INTO topic_materials(id, topic_id, material_id, entry_type, added_at)
                VALUES (?, ?, ?, 'material', ?)
                """,
                (_id("tm"), topic_id, mid, now),
            )
        for eid in event_ids:
            conn.execute(
                """
                INSERT INTO topic_materials(id, topic_id, event_id, entry_type, added_at)
                VALUES (?, ?, ?, 'event', ?)
                """,
                (_id("tm"), topic_id, eid, now),
            )

    def _collect_structure_material_ids(self, structure: dict[str, Any]) -> set[str]:
        found: set[str] = set()

        def walk(node: dict[str, Any]) -> None:
            for item in node.get("items", []) or []:
                for mid in item.get("material_ids", []) or []:
                    if mid:
                        found.add(mid)
            for child in node.get("children", []) or []:
                if isinstance(child, dict):
                    walk(child)

        for node in structure.get("nodes", []) or []:
            if isinstance(node, dict):
                walk(node)
        return found

    def _write_reprocess_compare(self, material_id: str, before: Any, after: Any) -> str:
        out_dir = self.settings.outputs_dir / "test_runs" / timestamp_slug()
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"reprocess_compare_{material_id}.md"
        path.write_text(
            "# Reprocess Compare\n\n"
            f"- Material: `{material_id}`\n"
            f"- Created: {utc_now()}\n\n"
            "## Before\n\n```json\n"
            + json.dumps(before, ensure_ascii=False, indent=2)
            + "\n```\n\n## After\n\n```json\n"
            + json.dumps(after, ensure_ascii=False, indent=2)
            + "\n```\n",
            encoding="utf-8",
        )
        return str(path)

    def _write_export(self, object_type: str, object_id: str, title: str, markdown: str, material_count: int) -> dict[str, Any]:
        out_dir = self.settings.outputs_dir / "exports" / timestamp_slug()
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_title = re.sub(r"[^A-Za-z0-9_.-]+", "_", title)[:80].strip("_") or object_type
        path = out_dir / f"{object_type}_{safe_title}.md"
        path.write_text(markdown, encoding="utf-8")
        export_id = _id("export")
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO exports(id, object_type, object_id, file_path, material_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (export_id, object_type, object_id, str(path), material_count, utc_now()),
            )
            conn.commit()
        return {"export_id": export_id, "object_type": object_type, "object_id": object_id, "file_path": str(path), "material_count": material_count}

    def _render_material_export(self, materials: list[dict[str, Any]]) -> str:
        lines = self._export_header("Material", "multiple", len(materials))
        lines.append("## Material Index\n")
        for index, material in enumerate(materials, start=1):
            lines.append(f"[M{index}] {material['title']} ({material['source_name']})")
        lines.append("\n## Complete Source Appendix\n")
        for index, material in enumerate(materials, start=1):
            lines.extend(self._material_appendix(index, material))
        return "\n".join(lines)

    def _render_event_export(self, event: dict[str, Any], materials: list[dict[str, Any]]) -> str:
        lines = self._export_header("Event", event["title"], len(materials))
        lines.append("## Center Description\n")
        center = event.get("center_description") or {}
        for key in ["main_thread", "known_facts", "recent_changes", "open_questions"]:
            value = center.get(key, [])
            lines.append(f"### {key.replace('_', ' ').title()}")
            if isinstance(value, list):
                lines.extend(f"- {item}" for item in value)
            else:
                lines.append(str(value))
        lines.append("\n## Material References\n")
        for index, material in enumerate(materials, start=1):
            lines.append(f"- [M{index}] {material['title']}")
        lines.append("\n## Complete Source Appendix\n")
        for index, material in enumerate(materials, start=1):
            lines.extend(self._material_appendix(index, material))
        return "\n".join(lines)

    def _render_topic_export(self, topic: dict[str, Any], materials: list[dict[str, Any]]) -> str:
        lines = self._export_header("Topic", topic["title"], len(materials))
        lines.append("## Topic Goal\n")
        lines.append(topic["goal"])
        lines.append("\n## Organization Requirements\n")
        lines.append(topic["organization"] or "No additional organization requirements.")
        lines.append("\n## Current Structure\n")
        lines.append("```json")
        lines.append(json.dumps(topic.get("current_structure") or {}, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("\n## Unreferenced Supplemental Materials\n")
        referenced = self._collect_structure_material_ids(topic.get("current_structure") or {})
        for index, material in enumerate(materials, start=1):
            if material["id"] not in referenced:
                lines.append(f"- [M{index}] {material['title']} (low-weight supplemental evidence)")
        lines.append("\n## Complete Source Appendix\n")
        for index, material in enumerate(materials, start=1):
            lines.extend(self._material_appendix(index, material))
        return "\n".join(lines)

    def _export_header(self, object_type: str, name: str, material_count: int) -> list[str]:
        return [
            "# information_workspace Evidence Package",
            "",
            "## AI Use Instructions",
            "",
            "Use this package as context and evidence. Treat user judgments as high-weight direction, not unquestionable fact. Verify claims against cited materials. Treat unreferenced materials as lower-weight supplemental evidence. De-duplicate repeated background and preserve uncertainty.",
            "",
            "## Export Snapshot",
            "",
            f"- Exported at: {utc_now()}",
            f"- Object type: {object_type}",
            f"- Object name: {name}",
            f"- Material count: {material_count}",
            "",
            "## Duplicate And Similarity Handling",
            "",
            "Exact duplicates should rely on the primary material. Near-similar materials are included when available but should be weighted as repeated background unless they add facts.",
            "",
        ]

    def _material_appendix(self, index: int, material: dict[str, Any]) -> list[str]:
        light = material.get("light_understanding") or {}
        url = material.get("url") or "No original link"
        return [
            f"### [M{index}] {material['title']}",
            "",
            f"- Source: {material['source_name']} ({material['source_type']})",
            f"- URL: {url}",
            f"- Published: {material.get('published_at') or 'unknown'}",
            f"- Facets: {', '.join(light.get('content_facets', [])) or 'none'}",
            f"- Summary: {light.get('summary') or 'not available'}",
            "",
            "```text",
            material["content_text"],
            "```",
            "",
        ]

    def _prompt_eval_samples(
        self,
        material_ids: list[str],
        run_id: str | None,
        fixture_file: str | None,
        fixture_group: str | None,
        test_purpose: str | None,
    ) -> list[dict[str, Any]]:
        samples: list[dict[str, Any]] = []
        if fixture_file:
            path = Path(fixture_file)
            if not path.is_absolute():
                path = self.settings.db_path.parents[1] / fixture_file
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                item = json.loads(line)
                metadata = item.get("metadata") or {}
                if fixture_group and metadata.get("fixture_group") != fixture_group:
                    continue
                if test_purpose and test_purpose not in metadata.get("test_purpose", []):
                    continue
                item["id"] = item.get("external_id") or _sha(item["title"])[:16]
                samples.append(item)
            return samples
        ids = list(material_ids)
        if run_id:
            run = self.get_run(run_id)
            ids.extend(run.get("material_ids", []))
        with self.connect() as conn:
            for mid in dict.fromkeys(ids):
                samples.append(self._material_for_llm(conn, mid))
        return samples
