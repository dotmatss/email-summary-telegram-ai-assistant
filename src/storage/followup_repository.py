from typing import Protocol

from src.models.followup import FollowUp


class FollowUpRepository(Protocol):
    """Repository contract for follow-up storage."""

    def add(self, followup: FollowUp) -> FollowUp:
        """Adds a follow-up reminder.

        Args:
            followup: Follow-up domain entity.

        Returns:
            Stored follow-up entity.
        """
        ...

    def list(self) -> list[FollowUp]:
        """Lists follow-up reminders.

        Returns:
            Follow-up entities.
        """
        ...
