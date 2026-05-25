"""Compatibility exports for routes now located in src.api.routes."""

from src.api.routes.chat import ChatRoutes
from src.api.routes.emails import EmailRoutes
from src.api.routes.followups import FollowUpRoutes
from src.api.routes.health import HealthRoutes
from src.api.routes.meetings import MeetingRoutes
from src.api.routes.notifications import NotificationRoutes
from src.api.routes.vectors import VectorRoutes

__all__ = [
    "ChatRoutes",
    "EmailRoutes",
    "FollowUpRoutes",
    "HealthRoutes",
    "MeetingRoutes",
    "NotificationRoutes",
    "VectorRoutes",
]
