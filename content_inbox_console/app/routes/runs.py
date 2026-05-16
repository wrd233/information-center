"""Runs routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
import sqlite3

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository

router = APIRouter()


@router.get("/runs", response_class=HTMLResponse)
def list_runs(
    request: Request,
    page: int = 1,
    page_size: int = 30,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    filters = {
        "page": max(1, page),
        "page_size": min(max(1, page_size), 200),
    }

    if not db_available:
        return templates.TemplateResponse("runs/list.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "runs", "runs": [], "total_runs": 0, "filters": filters,
        })

    runs, total = repo.list_runs(
        conn, limit=filters["page_size"], offset=(filters["page"] - 1) * filters["page_size"],
    )

    return templates.TemplateResponse("runs/list.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "runs", "runs": runs, "total_runs": total, "filters": filters,
    })


@router.get("/runs/rows", response_class=HTMLResponse)
def list_runs_rows(
    request: Request,
    page: int = 1,
    page_size: int = 30,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)

    page = max(1, page)
    page_size = min(max(1, page_size), 200)

    if not db_available:
        return templates.TemplateResponse("runs/_rows.html", {
            "request": request, "runs": [],
        })

    runs, _ = repo.list_runs(
        conn, limit=page_size, offset=(page - 1) * page_size,
    )

    return templates.TemplateResponse("runs/_rows.html", {
        "request": request, "runs": runs,
    })


@router.get("/runs/{run_id}", response_class=HTMLResponse)
def run_detail(
    request: Request,
    run_id: str,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    if not db_available:
        return templates.TemplateResponse("runs/detail.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "runs", "run": None,
        })

    run = repo.get_run(conn, run_id)
    if not run:
        return templates.TemplateResponse("runs/detail.html", {
            "request": request, "db_available": True, "db_path": str(settings.database_path),
            "active_page": "runs", "run": None, "not_found": True, "run_id": run_id,
        }, status_code=404)

    run_sources = repo.get_run_sources(conn, run_id)

    return templates.TemplateResponse("runs/detail.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "runs", "run": run, "run_sources": run_sources,
        "status": run.get("status", ""),
    })
