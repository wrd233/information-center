"""Route registration."""

from fastapi import FastAPI


def register_all_routers(app: FastAPI) -> None:
    from app.routes.dashboard import router as dashboard_router
    from app.routes.items import router as items_router
    from app.routes.sources import router as sources_router
    from app.routes.runs import router as runs_router
    from app.routes.clusters import router as clusters_router

    app.include_router(dashboard_router)
    app.include_router(items_router)
    app.include_router(sources_router)
    app.include_router(runs_router)
    app.include_router(clusters_router)
