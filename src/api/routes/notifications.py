from fastapi import APIRouter, Depends

from src.api.dependencies import dependency_provider
from src.operations.notification_use_case import NotificationUseCase
from src.schemas.notification import (
    TelegramNotificationRequest,
    TelegramNotificationResponse,
)


class NotificationRoutes:
    """Registers notification routes."""

    def __init__(self) -> None:
        """Initializes the notification router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "/telegram",
            self.send_telegram_notification,
            methods=["POST"],
            response_model=TelegramNotificationResponse,
        )

    def send_telegram_notification(
        self,
        request: TelegramNotificationRequest,
        use_case: NotificationUseCase = Depends(
            dependency_provider.get_notification_use_case
        ),
    ) -> TelegramNotificationResponse:
        """Sends a Telegram notification.

        Args:
            request: Telegram notification request.
            use_case: Notification use case dependency.

        Returns:
            Telegram notification delivery response.
        """
        return use_case.send_telegram_notification(request)


router = NotificationRoutes().router
