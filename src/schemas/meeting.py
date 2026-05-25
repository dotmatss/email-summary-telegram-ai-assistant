from datetime import datetime

from pydantic import BaseModel, Field


class MeetingSummaryRequest(BaseModel):
    """Request schema for meeting summarization.

    Attributes:
        title: Meeting title.
        transcript: Meeting transcript.
    """

    title: str = Field(min_length=1)
    transcript: str = Field(min_length=1)


class MeetingSummaryResponse(BaseModel):
    """Response schema for meeting summarization.

    Attributes:
        title: Meeting title.
        summary: Generated meeting summary.
        action_items: Extracted action items.
    """

    title: str
    summary: str
    action_items: list[str]


class MeetingBriefRequest(BaseModel):
    """Request schema for pre-meeting brief generation.

    Attributes:
        title: Meeting title.
        starts_at: Meeting start time.
        attendee_emails: Attendee email addresses.
        agenda: Optional meeting agenda.
    """

    title: str = Field(min_length=1)
    starts_at: datetime
    attendee_emails: list[str] = Field(default_factory=list)
    agenda: str | None = None


class MeetingBriefResponse(BaseModel):
    """Response schema for pre-meeting brief generation.

    Attributes:
        title: Meeting title.
        brief: Generated pre-meeting brief.
        suggested_questions: Suggested questions for the meeting.
    """

    title: str
    brief: str
    suggested_questions: list[str]
