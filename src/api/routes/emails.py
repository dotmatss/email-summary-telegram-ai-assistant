from fastapi import APIRouter, Depends, Query

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
)
from src.api.dependencies import dependency_provider
from src.operations.email_use_case import EmailUseCase


class EmailRoutes:
    """Registers email workflow routes."""

    def __init__(self) -> None:
        """Initializes the email router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "/classify",
            self.classify_email,
            methods=["POST"],
            response_model=EmailClassificationResponse,
        )
        self.router.add_api_route(
            "/draft-reply",
            self.draft_reply,
            methods=["POST"],
            response_model=DraftReplyResponse,
        )
        self.router.add_api_route(
            "/recent",
            self.list_recent_messages,
            methods=["GET"],
            response_model=list[EmailMessageResponse],
        )
        self.router.add_api_route(
            "/drafts",
            self.create_gmail_draft,
            methods=["POST"],
            response_model=GmailDraftResponse,
        )
        self.router.add_api_route(
            "/messages/{message_id}/draft-reply",
            self.draft_reply_for_message,
            methods=["POST"],
            response_model=DraftFromMessageResponse,
        )
        self.router.add_api_route(
            "/morning-review",
            self.run_morning_review,
            methods=["POST"],
            response_model=MorningEmailReviewResponse,
        )
        self.router.add_api_route(
            "/send",
            self.send_email,
            methods=["POST"],
            response_model=GmailSendResponse,
        )

    def classify_email(
        self,
        request: EmailClassificationRequest,
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> EmailClassificationResponse:
        """Classifies an email.

        Args:
            request: Email classification request.
            use_case: Email use case dependency.

        Returns:
            Email classification response.
        """
        return use_case.classify_email(request)

    def draft_reply(
        self,
        request: DraftReplyRequest,
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> DraftReplyResponse:
        """Creates an AI draft reply.

        Args:
            request: Draft reply request.
            use_case: Email use case dependency.

        Returns:
            Draft reply response.
        """
        return use_case.generate_draft_reply(request)

    def list_recent_messages(
        self,
        limit: int = Query(default=10, ge=1, le=50),
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> list[EmailMessageResponse]:
        """Lists recent Gmail inbox messages.

        Args:
            limit: Maximum number of messages to list.
            use_case: Email use case dependency.

        Returns:
            Recent Gmail message responses.
        """
        return use_case.list_recent_messages(limit=limit)

    def create_gmail_draft(
        self,
        request: GmailDraftCreate,
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> GmailDraftResponse:
        """Creates a real Gmail draft.

        Args:
            request: Gmail draft request.
            use_case: Email use case dependency.

        Returns:
            Created Gmail draft response.
        """
        return use_case.create_gmail_draft(request)

    def draft_reply_for_message(
        self,
        message_id: str,
        request: DraftFromMessageRequest,
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> DraftFromMessageResponse:
        """Creates a reviewable Gmail draft reply for an existing message.

        Args:
            message_id: Gmail message identifier.
            request: Draft options.
            use_case: Email use case dependency.

        Returns:
            Draft workflow response.
        """
        return use_case.draft_reply_for_message(message_id=message_id, request=request)

    def run_morning_review(
        self,
        request: MorningEmailReviewRequest,
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> MorningEmailReviewResponse:
        """Reviews recent inbox messages and creates reviewable Gmail drafts.

        Args:
            request: Morning review options.
            use_case: Email use case dependency.

        Returns:
            Morning review workflow response.
        """
        return use_case.run_morning_review(request)

    def send_email(
        self,
        request: GmailSendRequest,
        use_case: EmailUseCase = Depends(dependency_provider.get_email_use_case),
    ) -> GmailSendResponse:
        """Sends a real email through Gmail.

        Args:
            request: Gmail send request.
            use_case: Email use case dependency.

        Returns:
            Sent Gmail message response.
        """
        return use_case.send_email(request)


router = EmailRoutes().router
