from __future__ import annotations

import sqlite3
from pathlib import Path

from app.config import settings
from app.storage.schema import connect, ensure_schema


class Database:
    def __init__(self, path: Path | None = None):
        self.path = path or settings.database_path
        ensure_schema(self.path)

    def connect(self) -> sqlite3.Connection:
        return connect(self.path)

