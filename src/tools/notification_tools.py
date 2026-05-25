from langchain_core.tools import BaseTool, tool

from src.operations.notification_use_case import NotificationUseCase
from src.schemas.notification import (
    TelegramNotificationRequest,
    TelegramNotificationResponse,
)
from src.integrations.telegram.telegram_client import TelegramClient


class NotificationToolFactory:
    """Builds LangChain tools for notification workflows.

    Args:
        notification_use_case: Use case used to deliver notifications.
    """

    def __init__(self, notification_use_case: NotificationUseCase | None = None) -> None:
        """Initializes the notification tool factory.

        Args:
            notification_use_case: Optional notification use case override.
        """
        self._notification_use_case = notification_use_case or NotificationUseCase(
            telegram_service=TelegramClient()
        )

    def build(self) -> list[BaseTool]:
        """Creates the notification tools.

        Returns:
            A list of LangChain tools for notification delivery.
        """

        @tool("send_telegram_notification", args_schema=TelegramNotificationRequest)
        def send_telegram_notification(
            message: str,
            chat_id: str | None = None,
        ) -> TelegramNotificationResponse:
            """Sends a Telegram notification.

            Args:
                message: Notification message body.
                chat_id: Optional Telegram chat ID override.

            Returns:
                Delivery status and provider message ID, when available.
            """
            request = TelegramNotificationRequest(message=message, chat_id=chat_id)
            return self._notification_use_case.send_telegram_notification(request)

        return [send_telegram_notification]
