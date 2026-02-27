"""
FastAPI application entrypoint.

This module creates the FastAPI app, wires routes, initializes the database schema,
and maps domain errors to HTTP responses.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.db import Base, engine
from app.domain.errors import NotFound, Forbidden, ValidationError
from app.api.routes_groups import router as groups_router
from app.api.routes_messages import router as messages_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        A configured FastAPI app instance.
    """
    app = FastAPI(title=settings.app_name)

    # Create tables (simple approach for assignments; for prod use migrations)
    Base.metadata.create_all(bind=engine)

    # Routes
    app.include_router(groups_router)
    app.include_router(messages_router)

    # Domain error mapping
    @app.exception_handler(NotFound)
    async def not_found_handler(_, exc: NotFound):
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(Forbidden)
    async def forbidden_handler(_, exc: Forbidden):
        return JSONResponse(status_code=403, content={"error": str(exc)})

    @app.exception_handler(ValidationError)
    async def validation_handler(_, exc: ValidationError):
        return JSONResponse(status_code=400, content={"error": str(exc)})

    return app


app = create_app()