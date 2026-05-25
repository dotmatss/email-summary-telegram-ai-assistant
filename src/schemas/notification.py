from pydantic import BaseModel, Field


class TelegramNotificationRequest(BaseModel):
    """Request schema for Telegram notification delivery.

    Attributes:
        message: Notification message body.
        chat_id: Optional Telegram chat ID override.
    """

    message: str = Field(min_length=1)
    chat_id: str | None = None


class TelegramNotificationResponse(BaseModel):
    """Response schema for Telegram notification delivery.

    Attributes:
        delivered: Whether the notification was delivered.
        provider_message_id: Provider message identifier, when available.
    """

    delivered: bool
    provider_message_id: str | None = None
