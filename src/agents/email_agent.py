from src.schemas.email import (
    DraftReplyRequest,
    DraftReplyResponse,
    EmailCategory,
    EmailClassificationRequest,
    EmailClassificationResponse,
)
from src.integrations.ai_service import AiService


class EmailAgent:
    """Handles email classification and draft reply generation."""

    def __init__(self, ai_service: AiService | None = None) -> None:
        """Initializes the email agent.

        Args:
            ai_service: Optional model-backed AI service.
        """
        self._ai_service = ai_service

    def classify(self, request: EmailClassificationRequest) -> EmailClassificationResponse:
        """Classifies an email by business priority.

        Args:
            request: Email classification request.

        Returns:
            Email classification result.
        """
        if self._ai_service:
            return self._classify_with_ai(request)
        return self._classify_deterministically(request)

    def draft_reply(self, request: DraftReplyRequest) -> DraftReplyResponse:
        """Creates a draft reply for an email.

        Args:
            request: Draft reply request.

        Returns:
            Draft reply response.
        """
        if self._ai_service:
            return self._draft_with_ai(request)
        return self._draft_deterministically(request)

    def _classify_with_ai(
        self,
        request: EmailClassificationRequest,
    ) -> EmailClassificationResponse:
        """Classifies an email using the configured AI provider."""
        result = self._ai_service.generate_json(
            instructions=(
                "Classify executive emails for triage. Use exactly one category: "
                "spam, fyi, important, urgent, or other. Urgent means immediate action "
                "or deadline pressure. Important means requires thoughtful attention but "
                "not immediate action. FYI means informational. Spam means marketing, "
                "phishing, or irrelevant bulk mail."
            ),
            prompt=(
                f"Sender: {request.sender}\n"
                f"Subject: {request.subject}\n"
                f"Body:\n{request.body[:6000]}"
            ),
            schema={
                "name": "email_classification",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["spam", "fyi", "important", "urgent", "other"],
                        },
                        "confidence": {"type": "number"},
                        "rationale": {"type": "string"},
                    },
                    "required": ["category", "confidence", "rationale"],
                },
            },
        )
        return EmailClassificationResponse(**result)

    def _draft_with_ai(self, request: DraftReplyRequest) -> DraftReplyResponse:
        """Drafts an email reply using the configured AI provider."""
        samples = "\n\n---\n\n".join(request.writing_style_samples[:5])
        style_context = samples or "No writing samples were provided. Use a concise executive tone."
        result = self._ai_service.generate_json(
            instructions=(
                "Draft an email reply for an executive assistant workflow. Match the "
                "provided writing samples when present. Keep the reply concise, specific, "
                "and ready for human review. Do not invent commitments or facts not in "
                "the source email."
            ),
            prompt=(
                f"Desired tone: {request.tone}\n\n"
                f"Writing style samples:\n{style_context[:6000]}\n\n"
                f"Original sender: {request.sender}\n"
                f"Original subject: {request.subject}\n"
                f"Original body:\n{request.body[:6000]}"
            ),
            schema={
                "name": "email_draft_reply",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "subject": {"type": "string"},
                        "body": {"type": "string"},
                        "needs_review": {"type": "boolean"},
                    },
                    "required": ["subject", "body", "needs_review"],
                },
            },
        )
        return DraftReplyResponse(**result)

    @staticmethod
    def _classify_deterministically(
        request: EmailClassificationRequest,
    ) -> EmailClassificationResponse:
        """Classifies an email with local deterministic rules."""
        text = f"{request.sender} {request.subject} {request.body}".lower()

        marketing_keywords = ("unsubscribe", "newsletter", "promo", "limited time")
        if any(keyword in text for keyword in marketing_keywords):
            return EmailClassificationResponse(
                category=EmailCategory.spam,
                confidence=0.78,
                rationale="The email contains marketing or bulk-mail cues.",
            )

        if any(keyword in text for keyword in ("urgent", "asap", "immediately", "deadline")):
            return EmailClassificationResponse(
                category=EmailCategory.urgent,
                confidence=0.84,
                rationale="The email contains urgency cues.",
            )

        if any(keyword in text for keyword in ("approval", "decision", "contract", "invoice")):
            return EmailClassificationResponse(
                category=EmailCategory.important,
                confidence=0.76,
                rationale="The email appears to require executive attention.",
            )

        if any(keyword in text for keyword in ("fyi", "for your information", "update", "digest")):
            return EmailClassificationResponse(
                category=EmailCategory.fyi,
                confidence=0.72,
                rationale="The email appears informational.",
            )

        return EmailClassificationResponse(
            category=EmailCategory.other,
            confidence=0.55,
            rationale="No strong priority-specific signals were found.",
        )

    @staticmethod
    def _draft_deterministically(request: DraftReplyRequest) -> DraftReplyResponse:
        """Creates a local deterministic draft reply."""
        subject = (
            request.subject
            if request.subject.lower().startswith("re:")
            else f"Re: {request.subject}"
        )
        body = (
            "Hi,\n\n"
            f"Thanks for your note. I reviewed your message about \"{request.subject}\" "
            "and will follow up with the right next steps shortly.\n\n"
            "Best,\n"
        )
        return DraftReplyResponse(subject=subject, body=body, needs_review=True)
