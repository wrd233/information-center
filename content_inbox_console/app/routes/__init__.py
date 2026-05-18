"""Route registration."""

from fastapi import FastAPI


def register_all_routers(app: FastAPI) -> None:
    from app.routes.ops import router as ops_router

    app.include_router(ops_router)
