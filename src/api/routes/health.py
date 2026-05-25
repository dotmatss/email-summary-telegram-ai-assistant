from fastapi import APIRouter

from src.schemas.health import HealthResponse


class HealthRoutes:
    """Registers health check routes."""

    def __init__(self) -> None:
        """Initializes the health router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "/health",
            self.health_check,
            methods=["GET"],
            response_model=HealthResponse,
        )

    def health_check(self) -> HealthResponse:
        """Returns the application health status.

        Returns:
            Health check response.
        """
        return HealthResponse(status="ok")


router = HealthRoutes().router
