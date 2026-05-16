"""Diagnostics route for debugging database and outputs state."""

import sqlite3

from fastapi import APIRouter, Request, Depends

from app.dependencies import get_db_connection
from app.config import settings
from app.repositories.diagnostics import (
    get_db_diagnostics,
    get_outputs_diagnostics,
    compute_warnings,
)

router = APIRouter()


@router.get("/api/diagnostics")
def api_diagnostics(request: Request):
    db_diag = get_db_diagnostics(settings.database_path)
    outputs_diag = get_outputs_diagnostics(settings.outputs_path)
    warnings = compute_warnings(db_diag, outputs_diag)

    return {
        "database": db_diag,
        "outputs": outputs_diag,
        "warnings": warnings,
    }
