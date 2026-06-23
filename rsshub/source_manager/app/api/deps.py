from __future__ import annotations

from fastapi import Request

from app.services.check_service import CheckService
from app.services.batch_run_service import BatchRunService
from app.services.export_service import ExportService
from app.services.fetch_service import FetchService
from app.services.import_service import ImportService
from app.services.rating_service import RatingService
from app.services.source_service import SourceService


def source_service(request: Request) -> SourceService:
    return request.app.state.source_service


def check_service(request: Request) -> CheckService:
    return request.app.state.check_service


def fetch_service(request: Request) -> FetchService:
    return request.app.state.fetch_service


def batch_run_service(request: Request) -> BatchRunService:
    return request.app.state.batch_run_service


def import_service(request: Request) -> ImportService:
    return request.app.state.import_service


def export_service(request: Request) -> ExportService:
    return request.app.state.export_service


def rating_service(request: Request) -> RatingService:
    return request.app.state.rating_service
