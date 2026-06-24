from __future__ import annotations

from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR, Settings
from .schemas import (
    BatchUploadRequest,
    EventFromMaterialsRequest,
    ExportMaterialRequest,
    PromptEvalRequest,
    SingleUploadRequest,
    TopicAddMaterialsRequest,
    TopicCreateRequest,
    TopicLocalRefreshRequest,
    TopicRefreshRequest,
)
from .service import WorkspaceService


def _error(exc: Exception) -> HTTPException:
    message = str(exc)
    status_code = 404 if message.startswith("Unknown ") else 400
    return HTTPException(status_code=status_code, detail=message)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    service = WorkspaceService(settings)
    app = FastAPI(title="information_workspace", version="0.1.0")
    app.state.service = service

    @app.get("/api/health")
    @app.get("/health")
    def health() -> dict[str, Any]:
        return service.health()

    @app.post("/api/materials")
    def upload_material(payload: SingleUploadRequest, allow_mock_llm: bool = Query(False)) -> dict[str, Any]:
        try:
            data = payload.model_dump(exclude={"auto_process"})
            result = service.create_run([data], source="single_upload", auto_process=payload.auto_process)
            if payload.auto_process:
                service.process_run(result["run_id"], allow_mock_llm=allow_mock_llm)
                result = service.get_run(result["run_id"])
            return result
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/materials/batch")
    def upload_materials(payload: BatchUploadRequest, allow_mock_llm: bool = Query(False)) -> dict[str, Any]:
        try:
            result = service.create_run(payload.items, source=payload.source, auto_process=payload.auto_process)
            if payload.auto_process:
                service.process_run(result["run_id"], allow_mock_llm=allow_mock_llm)
                result = service.get_run(result["run_id"])
            return result
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, Any]:
        try:
            return service.get_run(run_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.get("/api/runs")
    def list_runs(limit: int = 20) -> list[dict[str, Any]]:
        return service.list_runs(limit=limit)

    @app.post("/api/runs/{run_id}/process")
    def process_run(run_id: str, allow_mock_llm: bool = Query(False)) -> dict[str, Any]:
        try:
            return service.process_run(run_id, allow_mock_llm=allow_mock_llm)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/runs/{run_id}/reprocess-light")
    def reprocess_run(run_id: str, allow_mock_llm: bool = Query(False), debug: bool = Query(False)) -> dict[str, Any]:
        try:
            return service.reprocess_run(run_id, allow_mock_llm=allow_mock_llm, debug=debug)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.get("/api/materials")
    def search_materials(
        q: str | None = None,
        run_id: str | None = None,
        include_ignored: bool = False,
        include_noise: bool = False,
        synthetic: bool | None = None,
        source_type: str | None = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        return service.search_materials(
            q=q,
            run_id=run_id,
            include_ignored=include_ignored,
            include_noise=include_noise,
            synthetic=synthetic,
            source_type=source_type,
            limit=limit,
        )

    @app.get("/api/materials/{material_id}")
    def get_material(material_id: str) -> dict[str, Any]:
        try:
            return service.get_material(material_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/materials/{material_id}/ignore")
    def ignore_material(material_id: str) -> dict[str, Any]:
        try:
            return service.ignore_material(material_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/materials/{material_id}/restore")
    def restore_material(material_id: str) -> dict[str, Any]:
        try:
            return service.restore_material(material_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/materials/{material_id}/reprocess-light")
    def reprocess_material(material_id: str, allow_mock_llm: bool = Query(False), debug: bool = Query(False)) -> dict[str, Any]:
        try:
            return service.reprocess_material(material_id, allow_mock_llm=allow_mock_llm, debug=debug)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.get("/api/events")
    def list_events(status: str | None = None, include_sleeping: bool = False) -> list[dict[str, Any]]:
        return service.list_events(status=status, include_sleeping=include_sleeping)

    @app.get("/api/events/{event_id}")
    def get_event(event_id: str) -> dict[str, Any]:
        try:
            return service.get_event(event_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/events/from-materials")
    def create_event(payload: EventFromMaterialsRequest, allow_mock_llm: bool = Query(False)) -> dict[str, Any]:
        try:
            return service.create_event_from_materials(
                payload.material_ids,
                title=payload.title,
                user_focus=payload.user_focus,
                allow_mock_llm=allow_mock_llm,
            )
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/events/{event_id}/promote")
    def promote_event(event_id: str, user_focus: str | None = None, allow_mock_llm: bool = Query(False)) -> dict[str, Any]:
        try:
            return service.promote_event(event_id, user_focus=user_focus, allow_mock_llm=allow_mock_llm)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/events/{event_id}/ignore-candidate")
    def ignore_candidate(event_id: str) -> dict[str, Any]:
        try:
            return service.ignore_candidate_event(event_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.get("/api/topics")
    def list_topics() -> list[dict[str, Any]]:
        return service.list_topics()

    @app.post("/api/topics")
    def create_topic(payload: TopicCreateRequest) -> dict[str, Any]:
        try:
            return service.create_topic(payload.title, payload.goal, payload.organization, payload.material_ids, payload.event_ids)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.get("/api/topics/{topic_id}")
    def get_topic(topic_id: str) -> dict[str, Any]:
        try:
            return service.get_topic(topic_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/topics/{topic_id}/materials")
    def add_topic_materials(topic_id: str, payload: TopicAddMaterialsRequest) -> dict[str, Any]:
        try:
            return service.add_topic_materials(topic_id, payload.material_ids, payload.event_ids)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/topics/{topic_id}/refresh-structure")
    def refresh_topic(topic_id: str, payload: TopicRefreshRequest) -> dict[str, Any]:
        try:
            return service.refresh_topic_structure(topic_id, include_new_materials=payload.include_new_materials, allow_mock_llm=payload.allow_mock_llm)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/topics/{topic_id}/confirm-candidate")
    def confirm_topic(topic_id: str) -> dict[str, Any]:
        try:
            return service.confirm_topic_candidate(topic_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/topics/{topic_id}/local-refresh")
    def local_refresh(topic_id: str, payload: TopicLocalRefreshRequest) -> dict[str, Any]:
        try:
            return service.local_refresh_topic(
                topic_id,
                payload.node_id,
                payload.instruction,
                include_new_materials=payload.include_new_materials,
                allow_mock_llm=payload.allow_mock_llm,
            )
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/exports/material")
    def export_material(payload: ExportMaterialRequest) -> dict[str, Any]:
        try:
            return service.export_materials(payload.material_ids)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/exports/event/{event_id}")
    def export_event(event_id: str) -> dict[str, Any]:
        try:
            return service.export_event(event_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/exports/topic/{topic_id}")
    def export_topic(topic_id: str) -> dict[str, Any]:
        try:
            return service.export_topic(topic_id)
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/prompt-eval")
    def prompt_eval(payload: PromptEvalRequest) -> dict[str, Any]:
        try:
            return service.prompt_eval(
                task=payload.task,
                material_ids=payload.material_ids,
                run_id=payload.run_id,
                fixture_file=payload.fixture_file,
                fixture_group=payload.fixture_group,
                test_purpose=payload.test_purpose,
                limit=payload.limit,
                allow_mock_llm=payload.allow_mock_llm,
            )
        except Exception as exc:  # noqa: BLE001
            raise _error(exc) from exc

    @app.post("/api/admin/cleanup-synthetic")
    def cleanup_synthetic() -> dict[str, Any]:
        return service.cleanup_synthetic()

    @app.get("/files/{file_path:path}")
    def safe_file(file_path: str) -> FileResponse:
        requested = (BASE_DIR / file_path).resolve()
        if not str(requested).startswith(str(BASE_DIR)):
            raise HTTPException(status_code=404, detail="File not allowed")
        relative = requested.relative_to(BASE_DIR)
        parts = relative.parts
        allowed = (
            relative.as_posix() in {"README.md", "STATUS.md"}
            or (parts and parts[0] == "docs")
            or relative.as_posix() == "fixtures/synthetic_materials/REPORT.md"
            or (parts and parts[0] == "outputs" and len(parts) > 1 and parts[1] in {"test_runs", "prompt_evals", "exports"})
        )
        blocked = any(part.startswith(".env") for part in parts) or (parts and parts[0] == "data")
        if not allowed or blocked or not requested.exists() or not requested.is_file():
            raise HTTPException(status_code=404, detail="File not allowed")
        return FileResponse(requested)

    frontend_dir = BASE_DIR / "frontend"
    if frontend_dir.exists():
        app.mount("/assets", StaticFiles(directory=frontend_dir), name="frontend-assets")

        @app.get("/")
        def index() -> FileResponse:
            return FileResponse(frontend_dir / "index.html")

        @app.get("/{path:path}")
        def spa(path: str) -> FileResponse:
            target = frontend_dir / path
            if target.exists() and target.is_file():
                return FileResponse(target)
            return FileResponse(frontend_dir / "index.html")

    return app


app = create_app()


def main() -> None:
    settings = Settings.from_env()
    uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port, reload=False)


if __name__ == "__main__":
    main()
