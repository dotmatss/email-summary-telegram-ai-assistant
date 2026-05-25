from fastapi import APIRouter, Depends

from src.api.dependencies import dependency_provider
from src.operations.followup_use_case import FollowUpUseCase
from src.schemas.followup import FollowUpCreate, FollowUpResponse


class FollowUpRoutes:
    """Registers follow-up routes."""

    def __init__(self) -> None:
        """Initializes the follow-up router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "",
            self.create_followup,
            methods=["POST"],
            response_model=FollowUpResponse,
        )
        self.router.add_api_route(
            "",
            self.list_followups,
            methods=["GET"],
            response_model=list[FollowUpResponse],
        )

    def create_followup(
        self,
        request: FollowUpCreate,
        use_case: FollowUpUseCase = Depends(dependency_provider.get_followup_use_case),
    ) -> FollowUpResponse:
        """Creates a follow-up reminder.

        Args:
            request: Follow-up creation request.
            use_case: Follow-up use case dependency.

        Returns:
            Created follow-up response.
        """
        return use_case.create_followup(request)

    def list_followups(
        self,
        use_case: FollowUpUseCase = Depends(dependency_provider.get_followup_use_case),
    ) -> list[FollowUpResponse]:
        """Lists follow-up reminders.

        Args:
            use_case: Follow-up use case dependency.

        Returns:
            Follow-up responses ordered by due date.
        """
        return use_case.list_followups()


router = FollowUpRoutes().router
