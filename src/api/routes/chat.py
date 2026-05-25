from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import dependency_provider
from src.operations.chat_history_use_case import ChatHistoryUseCase
from src.schemas.chat import ChatMessageCreate, ChatMessageResponse


class ChatRoutes:
    """Registers chat history routes."""

    def __init__(self) -> None:
        """Initializes the chat router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "/messages",
            self.add_message,
            methods=["POST"],
            response_model=ChatMessageResponse,
        )
        self.router.add_api_route(
            "/conversations/{conversation_id}/messages",
            self.list_messages,
            methods=["GET"],
            response_model=list[ChatMessageResponse],
        )

    def add_message(
        self,
        request: ChatMessageCreate,
        use_case: ChatHistoryUseCase = Depends(
            dependency_provider.get_chat_history_use_case
        ),
    ) -> ChatMessageResponse:
        """Stores a chat message.

        Args:
            request: Chat message creation request.
            use_case: Chat history use case dependency.

        Returns:
            Stored chat message response.
        """
        return use_case.add_message(request)

    def list_messages(
        self,
        conversation_id: UUID,
        use_case: ChatHistoryUseCase = Depends(
            dependency_provider.get_chat_history_use_case
        ),
    ) -> list[ChatMessageResponse]:
        """Lists messages for a conversation.

        Args:
            conversation_id: Conversation identifier.
            use_case: Chat history use case dependency.

        Returns:
            Chat message responses.
        """
        return use_case.list_messages(conversation_id)


router = ChatRoutes().router
