from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ChatMessage:
    """Chat message domain entity.

    Attributes:
        id: Message identifier.
        conversation_id: Conversation identifier.
        role: Message role such as user, assistant, or system.
        content: Message text content.
        created_at: Creation timestamp.
    """

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
