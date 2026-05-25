from fastapi import FastAPI

from src.api.router import ApiRouterFactory
from src.config.config import settings


class ApplicationFactory:
    """Creates the FastAPI application instance."""

    def create(self) -> FastAPI:
        """Builds and configures the FastAPI app.

        Returns:
            Configured FastAPI application.
        """
        fastapi_app = FastAPI(title=settings.app_name)
        fastapi_app.include_router(ApiRouterFactory().build(), prefix="/api/v1")
        return fastapi_app


app = ApplicationFactory().create()
