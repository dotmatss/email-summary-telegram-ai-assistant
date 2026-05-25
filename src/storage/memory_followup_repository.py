from uuid import UUID

from src.models.followup import FollowUp


class InMemoryFollowUpRepository:
    """Stores follow-up reminders in memory."""

    def __init__(self) -> None:
        """Initializes the repository."""
        self._items: dict[UUID, FollowUp] = {}

    def add(self, followup: FollowUp) -> FollowUp:
        """Adds a follow-up reminder.

        Args:
            followup: Follow-up domain entity.

        Returns:
            Stored follow-up entity.
        """
        self._items[followup.id] = followup
        return followup

    def list(self) -> list[FollowUp]:
        """Lists follow-up reminders ordered by due date.

        Returns:
            Follow-up entities.
        """
        return sorted(self._items.values(), key=lambda item: item.due_at)
