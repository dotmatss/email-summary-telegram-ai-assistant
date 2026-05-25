from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class EmailCategory(StrEnum):
    """Supported email classification categories."""

    spam = "spam"
    fyi = "fyi"
    important = "important"
    urgent = "urgent"
    other = "other"


class EmailClassificationRequest(BaseModel):
    """Request schema for email classification.

    Attributes:
        sender: Sender email address.
        subject: Email subject.
        body: Email body.
    """

    sender: EmailStr
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)


class EmailClassificationResponse(BaseModel):
    """Response schema for email classification.

    Attributes:
        category: Classified email category.
        confidence: Classification confidence score.
        rationale: Short classification rationale.
    """

    category: EmailCategory
    confidence: float = Field(ge=0, le=1)
    rationale: str


class DraftReplyRequest(BaseModel):
    """Request schema for draft reply generation.

    Attributes:
        sender: Sender email address.
        subject: Email subject.
        body: Email body.
        tone: Desired reply tone.
    """

    sender: EmailStr
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)
    tone: str = "professional"
    writing_style_samples: list[str] = Field(default_factory=list)


class DraftReplyResponse(BaseModel):
    """Response schema for draft reply generation.

    Attributes:
        subject: Draft reply subject.
        body: Draft reply body.
        needs_review: Whether the draft needs human review.
    """

    subject: str
    body: str
    needs_review: bool = True


class EmailMessageResponse(BaseModel):
    """Response schema for a Gmail message.

    Attributes:
        id: Gmail message identifier.
        thread_id: Gmail thread identifier.
        sender: Message sender.
        to: Message recipient header.
        subject: Message subject.
        snippet: Gmail snippet preview.
        body: Plain text body preview.
    """

    id: str
    thread_id: str
    sender: str = ""
    to: str = ""
    subject: str = ""
    snippet: str = ""
    body: str = ""


class GmailDraftCreate(BaseModel):
    """Request schema for creating a Gmail draft.

    Attributes:
        to: Recipient email address.
        subject: Email subject.
        body: Email body.
    """

    to: EmailStr
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)


class GmailDraftResponse(BaseModel):
    """Response schema for a created Gmail draft.

    Attributes:
        id: Gmail draft identifier.
        message_id: Gmail message identifier inside the draft.
    """

    id: str
    message_id: str = ""


class DraftFromMessageRequest(BaseModel):
    """Request schema for drafting a reply to a Gmail message.

    Attributes:
        tone: Desired reply tone.
        writing_style_samples: Sample sent emails used to mimic writing style.
        create_gmail_draft: Whether to create the draft in Gmail.
    """

    tone: str = "professional"
    writing_style_samples: list[str] = Field(default_factory=list)
    create_gmail_draft: bool = True


class DraftFromMessageResponse(BaseModel):
    """Response schema for a generated Gmail message reply draft.

    Attributes:
        message: Source Gmail message.
        classification: Email classification result.
        draft: Generated draft reply.
        gmail_draft: Created Gmail draft metadata when requested.
    """

    message: EmailMessageResponse
    classification: EmailClassificationResponse
    draft: DraftReplyResponse
    gmail_draft: GmailDraftResponse | None = None


class MorningEmailReviewRequest(BaseModel):
    """Request schema for morning email review automation.

    Attributes:
        limit: Maximum number of recent inbox messages to process.
        tone: Desired reply tone.
        writing_style_samples: Sample sent emails used to mimic writing style.
        create_gmail_drafts: Whether to create Gmail drafts for actionable emails.
    """

    limit: int = Field(default=10, ge=1, le=50)
    tone: str = "professional"
    writing_style_samples: list[str] = Field(default_factory=list)
    create_gmail_drafts: bool = True


class ReviewedEmailResponse(BaseModel):
    """Response schema for one reviewed inbox email.

    Attributes:
        message: Source Gmail message.
        classification: Email classification result.
        draft: Draft reply for actionable emails.
        gmail_draft: Created Gmail draft metadata when requested.
    """

    message: EmailMessageResponse
    classification: EmailClassificationResponse
    draft: DraftReplyResponse | None = None
    gmail_draft: GmailDraftResponse | None = None


class MorningEmailReviewResponse(BaseModel):
    """Response schema for the morning email review workflow.

    Attributes:
        processed_count: Number of emails reviewed.
        draft_count: Number of Gmail drafts created.
        items: Reviewed email results.
    """

    processed_count: int
    draft_count: int
    items: list[ReviewedEmailResponse]


class GmailSendRequest(BaseModel):
    """Request schema for sending email through Gmail.

    Attributes:
        to: Recipient email address.
        subject: Email subject.
        body: Email body.
    """

    to: EmailStr
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)


class GmailSendResponse(BaseModel):
    """Response schema for sent Gmail messages.

    Attributes:
        id: Gmail message identifier.
        thread_id: Gmail thread identifier.
        label_ids: Gmail labels attached to the sent message.
    """

    id: str
    thread_id: str = ""
    label_ids: list[str] = Field(default_factory=list)
