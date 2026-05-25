from src.integrations.telegram_service import TelegramService
from src.schemas.notification import (
    TelegramNotificationRequest,
    TelegramNotificationResponse,
)


class NotificationUseCase:
    """Coordinates notification use cases."""

    def __init__(self, telegram_service: TelegramService) -> None:
        """Initializes the notification use case."""
        self._telegram_service = telegram_service

    def send_telegram_notification(
        self,
        request: TelegramNotificationRequest,
    ) -> TelegramNotificationResponse:
        """Sends a Telegram notification."""
        result = self._telegram_service.send_message(
            message=request.message,
            chat_id=request.chat_id,
        )
        return TelegramNotificationResponse(
            delivered=result.delivered,
            provider_message_id=result.provider_message_id,
        )
