"""Dashboard route."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository
from app.repositories.file_runs import count_file_runs
from app.repositories.diagnostics import compute_warnings, get_db_diagnostics, get_outputs_diagnostics

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/dashboard", status_code=302)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    if not db_available:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "db_available": False,
            "db_path": str(settings.database_path),
            "active_page": "dashboard",
            "stats": {},
        })

    registered_sources = repo.count_sources(conn)
    observed_sources = repo.count_observed_sources(conn)
    db_runs = repo.count_runs(conn)
    file_runs = count_file_runs(settings.outputs_path)
    total_observed = max(registered_sources, observed_sources)

    stats = {
        "registered_sources": registered_sources,
        "observed_sources": observed_sources,
        "total_sources_display": registered_sources if registered_sources > 0 else observed_sources,
        "total_items": repo.count_items(conn),
        "items_24h": repo.count_items_last_24h(conn),
        "items_7d": repo.count_items_last_7d(conn),
        "db_runs": db_runs,
        "file_runs": file_runs,
        "total_runs_display": db_runs if db_runs > 0 else file_runs,
        "total_clusters": repo.count_clusters(conn),
        "sources_by_status": repo.count_sources_by_status(conn),
        "last_run": repo.get_last_run(conn),
        "items_by_category": repo.count_items_by_category(conn),
        "recent_items": repo.get_recent_items(conn, limit=20),
        "failed_sources": repo.get_recent_failed_sources(conn, limit=20),
        "db_size_bytes": repo.get_db_size(conn),
    }

    db_diag = get_db_diagnostics(settings.database_path)
    outputs_diag = get_outputs_diagnostics(settings.outputs_path)
    warnings = compute_warnings(db_diag, outputs_diag)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "db_available": True,
        "db_path": str(settings.database_path),
        "active_page": "dashboard",
        "stats": stats,
        "warnings": warnings,
        "last_run_status": stats["last_run"]["status"] if stats["last_run"] else None,
    })


@router.get("/api/dashboard/stats")
def dashboard_stats(
    request: Request,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    if not db_available:
        return {"error": "database unavailable", "db_available": False}

    settings = request.app.state.settings

    return {
        "db_available": True,
        "registered_sources": repo.count_sources(conn),
        "observed_sources": repo.count_observed_sources(conn),
        "total_items": repo.count_items(conn),
        "items_24h": repo.count_items_last_24h(conn),
        "items_7d": repo.count_items_last_7d(conn),
        "db_runs": repo.count_runs(conn),
        "file_runs": count_file_runs(settings.outputs_path),
        "total_clusters": repo.count_clusters(conn),
        "sources_by_status": repo.count_sources_by_status(conn),
        "db_size_bytes": repo.get_db_size(conn),
    }
