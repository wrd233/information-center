"""Clusters routes."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
import sqlite3

from app.dependencies import get_db_connection, get_settings
from app.config import Settings
from app.repository import ConsoleRepository

router = APIRouter()


@router.get("/clusters", response_class=HTMLResponse)
def list_clusters(
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
        return templates.TemplateResponse("clusters/list.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "clusters", "clusters": [], "total_clusters": 0, "filters": filters,
        })

    clusters, total = repo.list_clusters(
        conn, limit=filters["page_size"], offset=(filters["page"] - 1) * filters["page_size"],
    )

    return templates.TemplateResponse("clusters/list.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "clusters", "clusters": clusters, "total_clusters": total,
        "filters": filters,
    })


@router.get("/clusters/{cluster_id}", response_class=HTMLResponse)
def cluster_detail(
    request: Request,
    cluster_id: str,
    conn: sqlite3.Connection = Depends(get_db_connection),
):
    templates = request.app.state.templates
    repo: ConsoleRepository = request.app.state.repository
    db_available: bool = getattr(request.app.state, "db_available", False)
    settings: Settings = request.app.state.settings

    if not db_available:
        return templates.TemplateResponse("clusters/detail.html", {
            "request": request, "db_available": False, "db_path": str(settings.database_path),
            "active_page": "clusters", "cluster": None,
        })

    cluster = repo.get_cluster(conn, cluster_id)
    if not cluster:
        return templates.TemplateResponse("clusters/detail.html", {
            "request": request, "db_available": True, "db_path": str(settings.database_path),
            "active_page": "clusters", "cluster": None, "not_found": True,
            "cluster_id": cluster_id,
        }, status_code=404)

    cluster_items = repo.get_cluster_items(conn, cluster_id, limit=50)

    return templates.TemplateResponse("clusters/detail.html", {
        "request": request, "db_available": True, "db_path": str(settings.database_path),
        "active_page": "clusters", "cluster": cluster, "cluster_items": cluster_items,
    })
