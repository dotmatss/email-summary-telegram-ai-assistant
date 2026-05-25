import httpx

from src.config.config import settings
from src.integrations.telegram_service import TelegramSendResult


class TelegramClient:
    """Client boundary for Telegram Bot API operations."""

    def __init__(self, timeout_seconds: float = 10.0) -> None:
        """Initializes the Telegram client.

        Args:
            timeout_seconds: HTTP request timeout in seconds.
        """
        self._timeout_seconds = timeout_seconds

    def send_message(self, message: str, chat_id: str | None = None) -> TelegramSendResult:
        """Sends a Telegram message.

        Args:
            message: Message body.
            chat_id: Optional chat ID override.

        Returns:
            Telegram send result.
        """
        target_chat_id = chat_id or settings.telegram_default_chat_id
        if not settings.telegram_bot_token or not target_chat_id:
            return TelegramSendResult(delivered=False)

        response_data = self._post_message(message=message, chat_id=target_chat_id)
        result = response_data.get("result", {})
        message_id = result.get("message_id")
        return TelegramSendResult(
            delivered=bool(response_data.get("ok")),
            provider_message_id=str(message_id) if message_id is not None else None,
        )

    def _post_message(self, message: str, chat_id: str) -> dict:
        """Posts a message to the Telegram Bot API.

        Args:
            message: Message body.
            chat_id: Telegram chat ID.

        Returns:
            Telegram API response body.
        """
        url = f"{settings.telegram_api_base_url}/bot{settings.telegram_bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        try:
            response = httpx.post(url, json=payload, timeout=self._timeout_seconds)
            response.raise_for_status()
        except httpx.HTTPError:
            return {"ok": False}
        return response.json()
