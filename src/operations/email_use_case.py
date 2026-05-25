from email.utils import parseaddr

from src.agents.email_agent import EmailAgent
from src.schemas.email import (
    DraftFromMessageRequest,
    DraftFromMessageResponse,
    DraftReplyRequest,
    DraftReplyResponse,
    EmailClassificationRequest,
    EmailClassificationResponse,
    EmailMessageResponse,
    GmailDraftCreate,
    GmailDraftResponse,
    GmailSendRequest,
    GmailSendResponse,
    MorningEmailReviewRequest,
    MorningEmailReviewResponse,
    ReviewedEmailResponse,
)
from src.integrations.gmail_service import GmailService
from src.workflows.email_review_graph import EmailReviewGraphBuilder


class EmailUseCase:
    """Coordinates email application use cases."""

    def __init__(self, gmail_service: GmailService, email_agent: EmailAgent) -> None:
        """Initializes the email use case.

        Args:
            gmail_service: Gmail provider service.
            email_agent: Email agent.
        """
        self._gmail_service = gmail_service
        self._email_agent = email_agent

    def classify_email(self, request: EmailClassificationRequest) -> EmailClassificationResponse:
        """Classifies an email.

        Args:
            request: Email classification request.

        Returns:
            Email classification response.
        """
        return self._email_agent.classify(request)

    def generate_draft_reply(self, request: DraftReplyRequest) -> DraftReplyResponse:
        """Generates a draft email reply.

        Args:
            request: Draft reply request.

        Returns:
            Draft reply response.
        """
        return self._email_agent.draft_reply(request)

    def list_recent_messages(self, limit: int = 10) -> list[EmailMessageResponse]:
        """Lists recent Gmail messages.

        Args:
            limit: Maximum number of messages to return.

        Returns:
            Gmail message responses.
        """
        messages = self._gmail_service.list_recent_messages(limit=limit)
        return [EmailMessageResponse(**message) for message in messages]

    def draft_reply_for_message(
        self,
        message_id: str,
        request: DraftFromMessageRequest,
    ) -> DraftFromMessageResponse:
        """Generates a reply for a Gmail message and optionally creates a Gmail draft.

        Args:
            message_id: Gmail message identifier.
            request: Draft options.

        Returns:
            Draft-from-message workflow response.
        """
        message = EmailMessageResponse(**self._gmail_service.get_message(message_id))
        classification = self.classify_email(
            EmailClassificationRequest(
                sender=self._extract_email(message.sender),
                subject=message.subject or "(no subject)",
                body=message.body or message.snippet or "(empty)",
            )
        )
        draft = self.generate_draft_reply(
            DraftReplyRequest(
                sender=self._extract_email(message.sender),
                subject=message.subject or "(no subject)",
                body=message.body or message.snippet or "(empty)",
                tone=request.tone,
                writing_style_samples=request.writing_style_samples,
            )
        )
        gmail_draft = None
        if request.create_gmail_draft:
            gmail_draft = self.create_gmail_draft(
                GmailDraftCreate(
                    to=self._extract_email(message.sender),
                    subject=draft.subject,
                    body=draft.body,
                )
            )
        return DraftFromMessageResponse(
            message=message,
            classification=classification,
            draft=draft,
            gmail_draft=gmail_draft,
        )

    def run_morning_review(
        self,
        request: MorningEmailReviewRequest,
    ) -> MorningEmailReviewResponse:
        """Reviews recent inbox messages and creates drafts for actionable emails.

        Args:
            request: Morning review options.

        Returns:
            Morning review workflow response.
        """
        reviewed_items = []
        graph = EmailReviewGraphBuilder(
            gmail_service=self._gmail_service,
            email_agent=self._email_agent,
        ).build()
        state = graph.invoke({"request": request})

        for raw_message, raw_classification, raw_draft, raw_gmail_draft in zip(
            state["messages"],
            state["classifications"],
            state["drafts"],
            state["gmail_drafts"],
            strict=False,
        ):
            message = EmailMessageResponse(**raw_message)
            reviewed_items.append(
                ReviewedEmailResponse(
                    message=message,
                    classification=EmailClassificationResponse(**raw_classification),
                    draft=DraftReplyResponse(**raw_draft) if raw_draft else None,
                    gmail_draft=GmailDraftResponse(**raw_gmail_draft)
                    if raw_gmail_draft
                    else None,
                )
            )

        return MorningEmailReviewResponse(
            processed_count=len(reviewed_items),
            draft_count=sum(1 for item in reviewed_items if item.gmail_draft),
            items=reviewed_items,
        )

    def create_gmail_draft(self, request: GmailDraftCreate) -> GmailDraftResponse:
        """Creates a Gmail draft.

        Args:
            request: Draft creation request.

        Returns:
            Created Gmail draft response.
        """
        draft = self._gmail_service.create_draft(
            to=str(request.to),
            subject=request.subject,
            body=request.body,
        )
        return GmailDraftResponse(**draft)

    def send_email(self, request: GmailSendRequest) -> GmailSendResponse:
        """Sends an email through Gmail.

        Args:
            request: Send email request.

        Returns:
            Sent Gmail message response.
        """
        sent_message = self._gmail_service.send_email(
            to=str(request.to),
            subject=request.subject,
            body=request.body,
        )
        return GmailSendResponse(**sent_message)

    @staticmethod
    def _extract_email(value: str) -> str:
        """Extracts an email address from a header value."""
        _, address = parseaddr(value)
        return address or value
