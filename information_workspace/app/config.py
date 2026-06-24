from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[1]


def _read_local_env() -> dict[str, str]:
    env_path = BASE_DIR / ".env"
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name) or _read_local_env().get(name, default)


def _resolve_workspace_path(value: str, default: str) -> Path:
    raw = value or default
    path = Path(raw)
    if not path.is_absolute():
        path = BASE_DIR / path
    return path.resolve()


@dataclass(frozen=True)
class Settings:
    db_path: Path
    outputs_dir: Path
    deepseek_api_key: str
    deepseek_model: str
    llm_provider: str
    api_host: str
    api_port: int

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            db_path=_resolve_workspace_path(
                _env("INFORMATION_WORKSPACE_DB_PATH"),
                "./data/information_workspace.db",
            ),
            outputs_dir=_resolve_workspace_path(
                _env("INFORMATION_WORKSPACE_OUTPUTS_DIR"),
                "./outputs",
            ),
            deepseek_api_key=_env("DEEPSEEK_API_KEY"),
            deepseek_model=_env("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            llm_provider=_env("INFORMATION_WORKSPACE_LLM_PROVIDER", "deepseek"),
            api_host=_env("INFORMATION_WORKSPACE_API_HOST", "127.0.0.1"),
            api_port=int(_env("INFORMATION_WORKSPACE_API_PORT", "8788")),
        )

    def with_mock_llm(self) -> "Settings":
        return replace(self, llm_provider="mock", deepseek_api_key="")

    @property
    def deepseek_configured(self) -> bool:
        return bool(self.deepseek_api_key)

    def ensure_dirs(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        for child in ["test_runs", "prompt_evals", "llm_traces", "exports"]:
            (self.outputs_dir / child).mkdir(parents=True, exist_ok=True)
