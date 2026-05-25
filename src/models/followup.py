from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class FollowUp:
    """Follow-up reminder domain entity.

    Attributes:
        id: Follow-up identifier.
        subject: Follow-up subject.
        recipient: Follow-up recipient email address.
        due_at: Follow-up due datetime.
        notes: Optional notes.
        completed: Whether the follow-up is complete.
    """

    id: UUID
    subject: str
    recipient: str
    due_at: datetime
    notes: str | None = None
    completed: bool = False
