from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import batch_run_service
from app.models.schemas import BatchRunItemResponse, BatchRunResponse
from app.services.batch_run_service import BatchRunService


router = APIRouter(prefix="/batch-runs", tags=["batch-runs"])


@router.get("/{batch_run_id}", response_model=BatchRunResponse)
def get_batch_run(
    batch_run_id: str,
    service: Annotated[BatchRunService, Depends(batch_run_service)],
) -> BatchRunResponse:
    run = service.get_run(batch_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="batch run not found")
    return BatchRunResponse(**run)


@router.get("/{batch_run_id}/items", response_model=list[BatchRunItemResponse])
def list_batch_run_items(
    batch_run_id: str,
    service: Annotated[BatchRunService, Depends(batch_run_service)],
) -> list[BatchRunItemResponse]:
    items = service.list_items(batch_run_id)
    if items is None:
        raise HTTPException(status_code=404, detail="batch run not found")
    return [BatchRunItemResponse(**item) for item in items]


@router.post("/{batch_run_id}/cancel", response_model=BatchRunResponse)
def cancel_batch_run(
    batch_run_id: str,
    service: Annotated[BatchRunService, Depends(batch_run_service)],
) -> BatchRunResponse:
    run = service.cancel(batch_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="batch run not found")
    return BatchRunResponse(**run)
