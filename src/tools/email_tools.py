from langchain_core.tools import BaseTool, tool

from src.agents.email_agent import EmailAgent
from src.schemas.email import (
    DraftReplyRequest,
    DraftReplyResponse,
    EmailClassificationRequest,
    EmailClassificationResponse,
)


class EmailToolFactory:
    """Builds LangChain tools for email workflows.

    Args:
        email_agent: Agent used to classify emails and draft replies.
    """

    def __init__(self, email_agent: EmailAgent | None = None) -> None:
        """Initializes the email tool factory.

        Args:
            email_agent: Optional email agent override.
        """
        self._email_agent = email_agent or EmailAgent()

    def build(self) -> list[BaseTool]:
        """Creates the email tools.

        Returns:
            A list of LangChain tools for email classification and reply drafting.
        """

        @tool("classify_email", args_schema=EmailClassificationRequest)
        def classify_email(
            sender: str,
            subject: str,
            body: str,
        ) -> EmailClassificationResponse:
            """Classifies an email by urgency and intent.

            Args:
                sender: Email address of the sender.
                subject: Email subject line.
                body: Email body content.

            Returns:
                Email classification with category, confidence, and rationale.
            """
            request = EmailClassificationRequest(sender=sender, subject=subject, body=body)
            return self._email_agent.classify(request)

        @tool("draft_email_reply", args_schema=DraftReplyRequest)
        def draft_email_reply(
            sender: str,
            subject: str,
            body: str,
            tone: str = "professional",
            writing_style_samples: list[str] | None = None,
        ) -> DraftReplyResponse:
            """Creates a draft reply for an email.

            Args:
                sender: Email address of the original sender.
                subject: Original email subject line.
                body: Original email body content.
                tone: Desired reply tone.
                writing_style_samples: Sample sent emails used to mimic writing style.

            Returns:
                Draft reply subject and body.
            """
            request = DraftReplyRequest(
                sender=sender,
                subject=subject,
                body=body,
                tone=tone,
                writing_style_samples=writing_style_samples or [],
            )
            return self._email_agent.draft_reply(request)

        return [classify_email, draft_email_reply]
