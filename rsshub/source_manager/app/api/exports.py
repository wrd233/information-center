from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response

from app.api.deps import export_service
from app.services.export_service import ExportService


router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("/csv")
def export_csv(
    service: Annotated[ExportService, Depends(export_service)],
    mode: str = Query(default="clean", pattern="^(clean|full)$"),
) -> Response:
    return Response(
        service.csv(mode),
        media_type="text/csv; charset=utf-8",
        headers={"content-disposition": f'attachment; filename="sources-{mode}.csv"'},
    )


@router.get("/opml")
def export_opml(
    service: Annotated[ExportService, Depends(export_service)],
    profile: str = Query(default="local"),
) -> Response:
    return Response(
        service.opml(profile),
        media_type="text/x-opml; charset=utf-8",
        headers={"content-disposition": f'attachment; filename="sources-{profile}.opml"'},
    )

