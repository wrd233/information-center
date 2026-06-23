from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.deps import check_service, fetch_service, rating_service, source_service
from app.models.schemas import (
    BatchRunRequest,
    BatchUpdateRequest,
    FetchRequest,
    RatingAdjustmentRequest,
    SourceCreate,
    SourceDetailResponse,
    SourceListResponse,
    SourceResponse,
    SourceUpdate,
)
from app.services.check_service import CheckService
from app.services.fetch_service import FetchService
from app.services.rating_service import RatingService
from app.services.source_service import SourceService


router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=SourceListResponse)
def list_sources(
    service: Annotated[SourceService, Depends(source_service)],
    search: str | None = None,
    source_type: str | None = None,
    category: str | None = None,
    status: str | None = None,
    rating_min: int | None = Query(default=None, ge=0, le=100),
    rating_max: int | None = Query(default=None, ge=0, le=100),
    include_disabled: bool = False,
    sort: str | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
) -> SourceListResponse:
    sources, total, stats = service.list(
        search=search,
        source_type=source_type,
        category=category,
        status=status,
        rating_min=rating_min,
        rating_max=rating_max,
        include_disabled=include_disabled,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    return SourceListResponse(sources=sources, total=total, stats=stats)


@router.post("", response_model=SourceResponse)
def create_source(payload: SourceCreate, service: Annotated[SourceService, Depends(source_service)]) -> SourceResponse:
    try:
        return service.create(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.patch("/batch", response_model=list[SourceResponse])
def batch_update_sources(
    payload: BatchUpdateRequest,
    service: Annotated[SourceService, Depends(source_service)],
) -> list[SourceResponse]:
    updates = payload.model_dump(exclude={"source_ids"}, exclude_none=True)
    return service.batch_update(payload.source_ids, updates)


@router.post("/check-batch")
def check_batch(
    payload: BatchRunRequest,
    service: Annotated[CheckService, Depends(check_service)],
) -> dict:
    statuses = payload.statuses or ["active", "broken"]
    if payload.include_paused and "paused" not in statuses:
        statuses.append("paused")
    return service.check_batch(statuses=statuses, source_ids=payload.source_ids)


@router.post("/fetch-batch")
def fetch_batch(
    payload: BatchRunRequest,
    service: Annotated[FetchService, Depends(fetch_service)],
) -> dict:
    statuses = payload.statuses or ["active"]
    if payload.include_broken and "broken" not in statuses:
        statuses.append("broken")
    if payload.include_paused and "paused" not in statuses:
        statuses.append("paused")
    return service.fetch_batch(
        statuses=statuses,
        source_ids=payload.source_ids,
        include_raw=payload.include_raw,
        max_concurrent_sources=payload.max_concurrent_sources,
    )


@router.get("/{source_id}", response_model=SourceDetailResponse)
def get_source(source_id: str, service: Annotated[SourceService, Depends(source_service)]) -> SourceDetailResponse:
    detail = service.detail(source_id)
    if not detail:
        raise HTTPException(status_code=404, detail="source not found")
    return SourceDetailResponse(**detail)


@router.patch("/{source_id}", response_model=SourceResponse)
def update_source(
    source_id: str,
    payload: SourceUpdate,
    service: Annotated[SourceService, Depends(source_service)],
) -> SourceResponse:
    try:
        source = service.update(source_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not source:
        raise HTTPException(status_code=404, detail="source not found")
    return source


@router.delete("/{source_id}", response_model=SourceResponse)
def delete_source(source_id: str, service: Annotated[SourceService, Depends(source_service)]) -> SourceResponse:
    source = service.delete(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="source not found")
    return source


@router.post("/{source_id}/check")
def check_source(source_id: str, service: Annotated[CheckService, Depends(check_service)]):
    result = service.check_one(source_id)
    if not result:
        raise HTTPException(status_code=404, detail="source not found")
    return result


@router.post("/{source_id}/fetch")
def fetch_source(
    source_id: str,
    payload: FetchRequest,
    service: Annotated[FetchService, Depends(fetch_service)],
):
    result = service.fetch_one(source_id, include_raw=payload.include_raw)
    if not result:
        raise HTTPException(status_code=404, detail="source not found")
    return result


@router.post("/{source_id}/rating-adjustments", response_model=SourceResponse)
def adjust_rating(
    source_id: str,
    payload: RatingAdjustmentRequest,
    service: Annotated[RatingService, Depends(rating_service)],
) -> SourceResponse:
    result = service.adjust(source_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="source not found")
    return result

