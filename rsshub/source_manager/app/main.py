from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.batch_runs import router as batch_runs_router
from app.api.exports import router as exports_router
from app.api.imports import router as imports_router
from app.api.settings import router as settings_router
from app.api.sources import router as sources_router
from app.config import AppConfig, settings
from app.services.batch_run_service import BatchRunService
from app.services.check_service import CheckService
from app.services.export_service import ExportService
from app.services.fetch_service import FetchService
from app.services.import_service import ImportService
from app.services.rating_service import RatingService
from app.services.source_service import SourceService
from app.storage.db import Database


def create_app(config: AppConfig | None = None) -> FastAPI:
    config = config or settings
    database = Database(config.database_path)
    source_service = SourceService(database, config)
    app = FastAPI(title="RSS Source Manager", version="0.1.0")
    app.state.config = config
    app.state.database = database
    app.state.source_service = source_service
    app.state.check_service = CheckService(source_service)
    app.state.fetch_service = FetchService(source_service, config)
    app.state.batch_run_service = BatchRunService(
        source_service,
        app.state.check_service,
        app.state.fetch_service,
        config,
    )
    app.state.batch_run_service.recover_incomplete()
    app.state.import_service = ImportService(source_service, config)
    app.state.export_service = ExportService(source_service, config)
    app.state.rating_service = RatingService(source_service)

    api_prefix = "/api/v1"
    app.include_router(sources_router, prefix=api_prefix)
    app.include_router(batch_runs_router, prefix=api_prefix)
    app.include_router(imports_router, prefix=api_prefix)
    app.include_router(exports_router, prefix=api_prefix)
    app.include_router(settings_router, prefix=api_prefix)

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"ok": True, "database_path": str(config.database_path), "api": "/api/v1"}

    dist = config.root_dir / "frontend" / "dist"
    if dist.exists():
        assets = dist / "assets"
        if assets.exists():
            app.mount("/assets", StaticFiles(directory=assets), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def frontend(path: str = "") -> FileResponse:
            target = dist / path
            if path and target.exists() and target.is_file():
                return FileResponse(target)
            return FileResponse(dist / "index.html")

    return app


app = create_app()
