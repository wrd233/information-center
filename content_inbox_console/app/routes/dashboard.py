"""Dashboard route."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository

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

    stats = {
        "total_sources": repo.count_sources(conn),
        "total_items": repo.count_items(conn),
        "items_24h": repo.count_items_last_24h(conn),
        "items_7d": repo.count_items_last_7d(conn),
        "total_runs": repo.count_runs(conn),
        "total_clusters": repo.count_clusters(conn),
        "sources_by_status": repo.count_sources_by_status(conn),
        "last_run": repo.get_last_run(conn),
        "items_by_category": repo.count_items_by_category(conn),
        "recent_items": repo.get_recent_items(conn, limit=20),
        "failed_sources": repo.get_recent_failed_sources(conn, limit=20),
        "db_size_bytes": repo.get_db_size(conn),
    }

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "db_available": True,
        "db_path": str(settings.database_path),
        "active_page": "dashboard",
        "stats": stats,
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

    return {
        "db_available": True,
        "total_sources": repo.count_sources(conn),
        "total_items": repo.count_items(conn),
        "items_24h": repo.count_items_last_24h(conn),
        "items_7d": repo.count_items_last_7d(conn),
        "total_runs": repo.count_runs(conn),
        "total_clusters": repo.count_clusters(conn),
        "sources_by_status": repo.count_sources_by_status(conn),
        "db_size_bytes": repo.get_db_size(conn),
    }
