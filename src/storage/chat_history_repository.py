from typing import Protocol
from uuid import UUID

from src.models.chat_message import ChatMessage


class ChatHistoryRepository(Protocol):
    """Repository contract for chat history storage."""

    def add(self, message: ChatMessage) -> ChatMessage:
        """Stores a chat message.

        Args:
            message: Chat message entity.

        Returns:
            Stored chat message entity.
        """
        ...

    def list_by_conversation(self, conversation_id: UUID) -> list[ChatMessage]:
        """Lists messages for a conversation.

        Args:
            conversation_id: Conversation identifier.

        Returns:
            Chat messages ordered by creation time.
        """
        ...
