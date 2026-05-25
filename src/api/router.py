from fastapi import APIRouter

from src.api.routes.chat import ChatRoutes
from src.api.routes.emails import EmailRoutes
from src.api.routes.followups import FollowUpRoutes
from src.api.routes.health import HealthRoutes
from src.api.routes.meetings import MeetingRoutes
from src.api.routes.notifications import NotificationRoutes
from src.api.routes.vectors import VectorRoutes


class ApiRouterFactory:
    """Builds the top-level API router."""

    def build(self) -> APIRouter:
        """Creates the API router and mounts feature routers.

        Returns:
            Configured API router.
        """
        router = APIRouter()
        router.include_router(HealthRoutes().router, tags=["health"])
        router.include_router(EmailRoutes().router, prefix="/emails", tags=["emails"])
        router.include_router(MeetingRoutes().router, prefix="/meetings", tags=["meetings"])
        router.include_router(ChatRoutes().router, prefix="/chat", tags=["chat"])
        router.include_router(VectorRoutes().router, prefix="/vectors", tags=["vectors"])
        router.include_router(
            NotificationRoutes().router,
            prefix="/notifications",
            tags=["notifications"],
        )
        router.include_router(FollowUpRoutes().router, prefix="/followups", tags=["followups"])
        return router


api_router = ApiRouterFactory().build()
