import os
from pathlib import Path


class Settings:
    def __init__(self) -> None:
        self.host = os.getenv("CONTENT_INBOX_CONSOLE_HOST", "127.0.0.1")
        self.port = int(os.getenv("CONTENT_INBOX_CONSOLE_PORT", "8788"))
        self.page_size = int(os.getenv("CONTENT_INBOX_CONSOLE_PAGE_SIZE", "50"))
        self.db_timeout = int(os.getenv("CONTENT_INBOX_CONSOLE_DB_TIMEOUT", "5"))

        raw_db = os.getenv(
            "CONTENT_INBOX_CONSOLE_DB",
            str(Path(__file__).resolve().parent.parent.parent / "content_inbox" / "data" / "content_inbox.sqlite3"),
        )
        self.database_path = Path(raw_db)
        if not self.database_path.is_absolute():
            self.database_path = Path(__file__).resolve().parent.parent.parent / self.database_path

        raw_outputs = os.getenv("CONTENT_INBOX_CONSOLE_OUTPUTS", "")
        if raw_outputs:
            self.outputs_path = Path(raw_outputs)
            if not self.outputs_path.is_absolute():
                self.outputs_path = Path(__file__).resolve().parent.parent.parent / self.outputs_path
        else:
            self.outputs_path = self.database_path.parent.parent / "outputs" / "runs"


settings = Settings()
