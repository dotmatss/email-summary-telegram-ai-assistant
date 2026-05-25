from uuid import uuid4

from src.models.followup import FollowUp
from src.schemas.followup import FollowUpCreate, FollowUpResponse
from src.storage.followup_repository import FollowUpRepository


class FollowUpUseCase:
    """Coordinates follow-up reminder application use cases."""

    def __init__(self, repository: FollowUpRepository) -> None:
        """Initializes the follow-up use case.

        Args:
            repository: Follow-up repository.
        """
        self._repository = repository

    def create_followup(self, request: FollowUpCreate) -> FollowUpResponse:
        """Creates a follow-up reminder.

        Args:
            request: Follow-up creation request.

        Returns:
            Created follow-up response.
        """
        followup = FollowUp(
            id=uuid4(),
            subject=request.subject,
            recipient=str(request.recipient),
            due_at=request.due_at,
            notes=request.notes,
        )
        return self._to_response(self._repository.add(followup))

    def list_followups(self) -> list[FollowUpResponse]:
        """Lists follow-up reminders.

        Returns:
            Follow-up responses ordered by due date.
        """
        return [self._to_response(item) for item in self._repository.list()]

    @staticmethod
    def _to_response(followup: FollowUp) -> FollowUpResponse:
        """Converts a follow-up domain entity into a response schema.

        Args:
            followup: Follow-up domain entity.

        Returns:
            Follow-up response schema.
        """
        return FollowUpResponse(
            id=followup.id,
            subject=followup.subject,
            recipient=followup.recipient,
            due_at=followup.due_at,
            notes=followup.notes,
            completed=followup.completed,
        )
