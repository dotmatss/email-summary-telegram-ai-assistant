from uuid import UUID, uuid4

from src.config.datetime import DateTimeProvider
from src.models.chat_message import ChatMessage
from src.schemas.chat import ChatMessageCreate, ChatMessageResponse
from src.storage.chat_history_repository import ChatHistoryRepository


class ChatHistoryUseCase:
    """Coordinates chat history application use cases."""

    def __init__(
        self,
        repository: ChatHistoryRepository,
        datetime_provider: DateTimeProvider | None = None,
    ) -> None:
        """Initializes the chat history use case.

        Args:
            repository: Chat history repository.
            datetime_provider: Date/time provider.
        """
        self._repository = repository
        self._datetime_provider = datetime_provider or DateTimeProvider()

    def add_message(self, request: ChatMessageCreate) -> ChatMessageResponse:
        """Stores a chat message.

        Args:
            request: Chat message creation request.

        Returns:
            Stored chat message response.
        """
        message = ChatMessage(
            id=uuid4(),
            conversation_id=request.conversation_id,
            role=request.role,
            content=request.content,
            created_at=self._datetime_provider.utc_now(),
        )
        return self._to_response(self._repository.add(message))

    def list_messages(self, conversation_id: UUID) -> list[ChatMessageResponse]:
        """Lists messages for a conversation.

        Args:
            conversation_id: Conversation identifier.

        Returns:
            Chat message responses.
        """
        messages = self._repository.list_by_conversation(conversation_id)
        return [self._to_response(message) for message in messages]

    @staticmethod
    def _to_response(message: ChatMessage) -> ChatMessageResponse:
        """Converts a chat message entity into a response schema.

        Args:
            message: Chat message entity.

        Returns:
            Chat message response.
        """
        return ChatMessageResponse(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )
