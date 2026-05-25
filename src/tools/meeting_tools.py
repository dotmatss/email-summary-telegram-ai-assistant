from datetime import datetime

from langchain_core.tools import BaseTool, tool

from src.agents.meeting_agent import MeetingAgent
from src.schemas.meeting import (
    MeetingBriefRequest,
    MeetingBriefResponse,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
)


class MeetingToolFactory:
    """Builds LangChain tools for meeting workflows.

    Args:
        meeting_agent: Agent used to summarize meetings and create briefs.
    """

    def __init__(self, meeting_agent: MeetingAgent | None = None) -> None:
        """Initializes the meeting tool factory.

        Args:
            meeting_agent: Optional meeting agent override.
        """
        self._meeting_agent = meeting_agent or MeetingAgent()

    def build(self) -> list[BaseTool]:
        """Creates the meeting tools.

        Returns:
            A list of LangChain tools for meeting summaries and briefs.
        """

        @tool("summarize_meeting", args_schema=MeetingSummaryRequest)
        def summarize_meeting(title: str, transcript: str) -> MeetingSummaryResponse:
            """Summarizes a meeting transcript and extracts action items.

            Args:
                title: Meeting title.
                transcript: Meeting transcript text.

            Returns:
                Meeting summary with extracted action items.
            """
            request = MeetingSummaryRequest(title=title, transcript=transcript)
            return self._meeting_agent.summarize(request)

        @tool("create_meeting_brief", args_schema=MeetingBriefRequest)
        def create_meeting_brief(
            title: str,
            starts_at: datetime,
            attendee_emails: list[str] | None = None,
            agenda: str | None = None,
        ) -> MeetingBriefResponse:
            """Creates a pre-meeting brief from calendar context.

            Args:
                title: Meeting title.
                starts_at: Scheduled meeting start time.
                attendee_emails: Attendee email addresses.
                agenda: Optional meeting agenda.

            Returns:
                Meeting brief with suggested questions.
            """
            request = MeetingBriefRequest(
                title=title,
                starts_at=starts_at,
                attendee_emails=attendee_emails or [],
                agenda=agenda,
            )
            return self._meeting_agent.create_brief(request)

        return [summarize_meeting, create_meeting_brief]

