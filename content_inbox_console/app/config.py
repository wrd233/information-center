import os


class Settings:
    def __init__(self) -> None:
        self.host = os.getenv("CONTENT_INBOX_CONSOLE_HOST", "127.0.0.1")
        self.port = int(os.getenv("CONTENT_INBOX_CONSOLE_PORT", "8788"))
        self.page_size = int(os.getenv("CONTENT_INBOX_CONSOLE_PAGE_SIZE", "50"))
        self.api_base = os.getenv("CONTENT_INBOX_FRONTEND_API_BASE", "http://127.0.0.1:8787").rstrip("/")


settings = Settings()
