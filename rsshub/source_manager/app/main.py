from __future__ import annotations

import subprocess
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
from app.utils.time import utc_now


APP_NAME = "RSS Source Manager"
APP_VERSION = "0.2.1"


def git_commit(root_dir) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root_dir,
            capture_output=True,
            check=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip() or None
    except Exception:
        return None


def create_app(config: AppConfig | None = None) -> FastAPI:
    config = config or settings
    database = Database(config.database_path)
    source_service = SourceService(database, config)
    app = FastAPI(title=APP_NAME, version=APP_VERSION)
    dist = config.root_dir / "frontend" / "dist"
    app.state.config = config
    app.state.database = database
    app.state.app_metadata = {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "started_at": utc_now(),
        "git_commit": git_commit(config.root_dir),
        "frontend_static_dir": str(dist),
    }
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
        return {
            "ok": True,
            **app.state.app_metadata,
            "db_path": str(config.database_path),
            "database_path": str(config.database_path),
            "config_path": str(config.config_path),
            "api": "/api/v1",
        }

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
