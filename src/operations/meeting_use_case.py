from src.agents.meeting_agent import MeetingAgent
from src.integrations.calendar_service import CalendarService
from src.schemas.meeting import (
    MeetingBriefRequest,
    MeetingBriefResponse,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
)


class MeetingUseCase:
    """Coordinates meeting use cases."""

    def __init__(self, calendar_service: CalendarService, meeting_agent: MeetingAgent) -> None:
        """Initializes the meeting use case."""
        self._calendar_service = calendar_service
        self._meeting_agent = meeting_agent

    def create_summary(self, request: MeetingSummaryRequest) -> MeetingSummaryResponse:
        """Creates a meeting summary."""
        return self._meeting_agent.summarize(request)

    def create_pre_meeting_brief(self, request: MeetingBriefRequest) -> MeetingBriefResponse:
        """Creates a pre-meeting brief."""
        return self._meeting_agent.create_brief(request)
