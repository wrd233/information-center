from __future__ import annotations

import csv
import io
from typing import Any


def normalize_header(value: str) -> str:
    return (value or "").strip().lower().replace(" ", "_").replace("-", "_")


def parse_csv(text: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(text.lstrip("\ufeff")))
    rows = []
    for raw in reader:
        rows.append({normalize_header(key): (value or "").strip() for key, value in raw.items() if key is not None})
    return rows


def write_csv(rows: list[dict[str, Any]], fields: list[str]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()

