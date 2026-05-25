from fastapi import APIRouter, Depends

from src.api.dependencies import dependency_provider
from src.operations.meeting_use_case import MeetingUseCase
from src.schemas.meeting import (
    MeetingBriefRequest,
    MeetingBriefResponse,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
)


class MeetingRoutes:
    """Registers meeting workflow routes."""

    def __init__(self) -> None:
        """Initializes the meeting router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "/summaries",
            self.summarize_meeting,
            methods=["POST"],
            response_model=MeetingSummaryResponse,
        )
        self.router.add_api_route(
            "/briefs",
            self.create_meeting_brief,
            methods=["POST"],
            response_model=MeetingBriefResponse,
        )

    def summarize_meeting(
        self,
        request: MeetingSummaryRequest,
        use_case: MeetingUseCase = Depends(dependency_provider.get_meeting_use_case),
    ) -> MeetingSummaryResponse:
        """Creates a meeting summary.

        Args:
            request: Meeting summary request.
            use_case: Meeting use case dependency.

        Returns:
            Meeting summary response.
        """
        return use_case.create_summary(request)

    def create_meeting_brief(
        self,
        request: MeetingBriefRequest,
        use_case: MeetingUseCase = Depends(dependency_provider.get_meeting_use_case),
    ) -> MeetingBriefResponse:
        """Creates a pre-meeting brief.

        Args:
            request: Meeting brief request.
            use_case: Meeting use case dependency.

        Returns:
            Meeting brief response.
        """
        return use_case.create_pre_meeting_brief(request)


router = MeetingRoutes().router
