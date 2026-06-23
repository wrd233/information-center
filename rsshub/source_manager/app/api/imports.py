from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import import_service, source_service
from app.models.schemas import ImportCommitRequest, ImportPreviewRequest
from app.services.import_service import ImportService
from app.services.source_service import SourceService


router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/csv/preview")
def csv_preview(
    service: Annotated[ImportService, Depends(import_service)],
    payload: ImportPreviewRequest,
) -> dict:
    return service.preview("csv", payload.content, payload.filename)


@router.post("/csv/commit")
def csv_commit(
    service: Annotated[ImportService, Depends(import_service)],
    payload: ImportCommitRequest,
) -> dict:
    return service.commit("csv", payload.content, filename=payload.filename, strategy=payload.strategy)


@router.post("/opml/preview")
def opml_preview(
    service: Annotated[ImportService, Depends(import_service)],
    payload: ImportPreviewRequest,
) -> dict:
    return service.preview("opml", payload.content, payload.filename)


@router.post("/opml/commit")
def opml_commit(
    service: Annotated[ImportService, Depends(import_service)],
    payload: ImportCommitRequest,
) -> dict:
    return service.commit("opml", payload.content, filename=payload.filename, strategy=payload.strategy)


@router.get("/history")
def import_history(service: Annotated[SourceService, Depends(source_service)]) -> dict:
    return {"ok": True, "import_runs": service.runs.list_import_runs()}
