from __future__ import annotations

from typing import Any

import httpx

from app.config import settings


class BackendClient:
    def __init__(self, api_base: str | None = None) -> None:
        self.api_base = (api_base or settings.api_base).rstrip("/")

    def request(self, method: str, path: str, *, params: dict[str, Any] | None = None, json: Any = None) -> dict[str, Any]:
        url = f"{self.api_base}{path}"
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.request(method, url, params=params, json=json)
            data = response.json()
            if response.status_code >= 400 and data.get("ok") is not False:
                return self.error("BACKEND_HTTP_ERROR", f"Backend returned HTTP {response.status_code}", {"response": data})
            return data
        except Exception as exc:
            return self.error("BACKEND_UNAVAILABLE", str(exc), {"api_base": self.api_base, "path": path})

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request("GET", path, params=params)

    def post(self, path: str, payload: Any | None = None) -> dict[str, Any]:
        return self.request("POST", path, json=payload or {})

    def patch(self, path: str, payload: Any | None = None) -> dict[str, Any]:
        return self.request("PATCH", path, json=payload or {})

    def delete(self, path: str) -> dict[str, Any]:
        return self.request("DELETE", path)

    @staticmethod
    def error(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
        return {"ok": False, "data": None, "error": {"code": code, "message": message, "details": details or {}}, "meta": {}}


def data(response: dict[str, Any], default: Any = None) -> Any:
    if response.get("ok"):
        return response.get("data", default)
    return default
