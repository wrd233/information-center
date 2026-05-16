"""content_inbox_console -- FastAPI application factory."""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.repository import ConsoleRepository
from app.dependencies import verify_db_available
from app.routes import register_all_routers

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app() -> FastAPI:
    app = FastAPI(title="content-inbox-console", version="0.1.0")

    static_dir = BASE_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    templates_dir = BASE_DIR / "templates"
    templates = Jinja2Templates(directory=str(templates_dir))
    app.state.templates = templates

    repo = ConsoleRepository()
    app.state.repository = repo
    app.state.settings = settings

    db_available = verify_db_available()
    app.state.db_available = db_available
    if not db_available:
        logger.warning(
            "Database not available at %s -- pages will show error state until fixed.",
            settings.database_path,
        )
    else:
        logger.info("Database available at %s", settings.database_path)

    register_all_routers(app)
    return app


def main() -> None:
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    main()

app = create_app()
