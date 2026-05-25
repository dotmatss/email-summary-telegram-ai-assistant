from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class FollowUpCreate(BaseModel):
    """Request schema for creating a follow-up reminder.

    Attributes:
        subject: Follow-up subject.
        recipient: Recipient email address.
        due_at: Due datetime.
        notes: Optional follow-up notes.
    """

    subject: str = Field(min_length=1)
    recipient: EmailStr
    due_at: datetime
    notes: str | None = None


class FollowUpResponse(BaseModel):
    """Response schema for a follow-up reminder.

    Attributes:
        id: Follow-up identifier.
        subject: Follow-up subject.
        recipient: Recipient email address.
        due_at: Due datetime.
        notes: Optional follow-up notes.
        completed: Whether the follow-up is complete.
    """

    id: UUID
    subject: str
    recipient: EmailStr
    due_at: datetime
    notes: str | None = None
    completed: bool
