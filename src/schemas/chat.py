from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChatMessageCreate(BaseModel):
    """Request schema for storing a chat message.

    Attributes:
        conversation_id: Conversation identifier.
        role: Message role.
        content: Message content.
    """

    conversation_id: UUID
    role: str = Field(min_length=1)
    content: str = Field(min_length=1)


class ChatMessageResponse(BaseModel):
    """Response schema for a chat message.

    Attributes:
        id: Message identifier.
        conversation_id: Conversation identifier.
        role: Message role.
        content: Message content.
        created_at: Creation timestamp.
    """

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
