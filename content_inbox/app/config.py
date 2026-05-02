from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from app.app_config import load_yaml_config

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


class Settings:
    def __init__(self) -> None:
        self.host = os.getenv("CONTENT_INBOX_HOST", "127.0.0.1")
        self.port = int(os.getenv("CONTENT_INBOX_PORT", "8787"))
        self.database_path = Path(
            os.getenv("CONTENT_INBOX_DB", BASE_DIR / "data" / "content_inbox.sqlite3")
        )
        self.request_timeout_seconds = float(os.getenv("CONTENT_INBOX_REQUEST_TIMEOUT", "20"))
        self.max_content_chars = int(os.getenv("CONTENT_INBOX_MAX_CONTENT_CHARS", "8000"))

        self.openai_api_key = os.getenv(
            "CONTENT_INBOX_DEEPSEEK_API_KEY",
            os.getenv("CONTENT_INBOX_OPENAI_API_KEY", ""),
        )
        self.openai_base_url = os.getenv(
            "CONTENT_INBOX_OPENAI_BASE_URL",
            os.getenv("CONTENT_INBOX_DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        ).rstrip("/")
        self.openai_model = os.getenv(
            "CONTENT_INBOX_OPENAI_MODEL",
            os.getenv("CONTENT_INBOX_DEEPSEEK_MODEL", "deepseek-v4-flash"),
        )
        self.openai_timeout_seconds = float(os.getenv("CONTENT_INBOX_OPENAI_TIMEOUT", "45"))
        self.ai_enabled = os.getenv("CONTENT_INBOX_AI_ENABLED", "1") not in {
            "0",
            "false",
            "False",
            "no",
        }
        self.config = load_yaml_config(BASE_DIR)
        self.llm = self.config["llm"]
        self.screening = self.config["screening"]
        self.score_policy = self.config["score_policy"]
        self.embedding = self.config["embedding"]
        self.clustering = self.config["clustering"]
        self.notification = self.config["notification"]

    def llm_api_key(self) -> str:
        env_name = self.llm.get("api_key_env", "CONTENT_INBOX_DEEPSEEK_API_KEY")
        return os.getenv(env_name) or self.openai_api_key

    def embedding_api_key(self) -> str:
        env_name = self.embedding.get("api_key_env", "CONTENT_INBOX_EMBEDDING_API_KEY")
        return os.getenv(env_name, "")


settings = Settings()
