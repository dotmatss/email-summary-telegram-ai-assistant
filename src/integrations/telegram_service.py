from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TelegramSendResult:
    """Represents the result of a Telegram send operation.

    Attributes:
        delivered: Whether the message was delivered.
        provider_message_id: Provider message identifier, when available.
    """

    delivered: bool
    provider_message_id: str | None = None


class TelegramService(Protocol):
    """Contract for Telegram notification delivery."""

    def send_message(self, message: str, chat_id: str | None = None) -> TelegramSendResult:
        """Sends a Telegram message.

        Args:
            message: Message body.
            chat_id: Optional chat ID override.

        Returns:
            Telegram send result.
        """
        ...
