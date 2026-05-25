from mcp.server.fastmcp import FastMCP

from src.api.dependencies import dependency_provider
from src.schemas.email import (
    DraftFromMessageRequest,
    DraftReplyRequest,
    EmailClassificationRequest,
    MorningEmailReviewRequest,
)
from src.schemas.meeting import MeetingBriefRequest, MeetingSummaryRequest
from src.schemas.notification import TelegramNotificationRequest

mcp = FastMCP("Email AI Assistant")


@mcp.tool()
def classify_email(sender: str, subject: str, body: str) -> dict:
    """Classify an email into spam, fyi, important, urgent, or other."""
    request = EmailClassificationRequest(sender=sender, subject=subject, body=body)
    return dependency_provider.get_email_use_case().classify_email(request).model_dump()


@mcp.tool()
def draft_email_reply(
    sender: str,
    subject: str,
    body: str,
    tone: str = "professional",
    writing_style_samples: list[str] | None = None,
) -> dict:
    """Generate a reply draft using optional writing style samples."""
    request = DraftReplyRequest(
        sender=sender,
        subject=subject,
        body=body,
        tone=tone,
        writing_style_samples=writing_style_samples or [],
    )
    return dependency_provider.get_email_use_case().generate_draft_reply(request).model_dump()


@mcp.tool()
def run_morning_email_review(
    limit: int = 10,
    tone: str = "professional",
    create_gmail_drafts: bool = True,
    writing_style_samples: list[str] | None = None,
) -> dict:
    """Review recent Gmail inbox messages and create drafts for actionable emails."""
    request = MorningEmailReviewRequest(
        limit=limit,
        tone=tone,
        create_gmail_drafts=create_gmail_drafts,
        writing_style_samples=writing_style_samples or [],
    )
    return dependency_provider.get_email_use_case().run_morning_review(request).model_dump()


@mcp.tool()
def draft_reply_for_gmail_message(
    message_id: str,
    tone: str = "professional",
    create_gmail_draft: bool = True,
    writing_style_samples: list[str] | None = None,
) -> dict:
    """Create a reviewable reply draft for an existing Gmail message."""
    request = DraftFromMessageRequest(
        tone=tone,
        create_gmail_draft=create_gmail_draft,
        writing_style_samples=writing_style_samples or [],
    )
    return dependency_provider.get_email_use_case().draft_reply_for_message(
        message_id=message_id,
        request=request,
    ).model_dump()


@mcp.tool()
def summarize_meeting(title: str, transcript: str) -> dict:
    """Summarize a meeting transcript and extract action items."""
    request = MeetingSummaryRequest(title=title, transcript=transcript)
    return dependency_provider.get_meeting_use_case().create_summary(request).model_dump()


@mcp.tool()
def create_meeting_brief(
    title: str,
    starts_at: str,
    attendee_emails: list[str] | None = None,
    agenda: str | None = None,
) -> dict:
    """Create a pre-meeting brief from calendar-style context."""
    request = MeetingBriefRequest(
        title=title,
        starts_at=starts_at,
        attendee_emails=attendee_emails or [],
        agenda=agenda,
    )
    return dependency_provider.get_meeting_use_case().create_pre_meeting_brief(request).model_dump()


@mcp.tool()
def send_telegram_notification(message: str, chat_id: str | None = None) -> dict:
    """Send a Telegram notification."""
    request = TelegramNotificationRequest(message=message, chat_id=chat_id)
    return dependency_provider.get_notification_use_case().send_telegram_notification(
        request
    ).model_dump()


if __name__ == "__main__":
    mcp.run()
