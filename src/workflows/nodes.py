from typing import Any

from src.agents.email_agent import EmailAgent
from src.schemas.email import EmailClassificationRequest


class EmailProcessingNodes:
    """Provides node callables for the email processing workflow."""

    def __init__(self, email_agent: EmailAgent | None = None) -> None:
        """Initializes email workflow nodes.

        Args:
            email_agent: Optional email agent override.
        """
        self._email_agent = email_agent or EmailAgent()

    def classify(self, state: dict[str, Any]) -> dict[str, Any]:
        """Classifies the email held in graph state.

        Args:
            state: Graph state containing an email payload.

        Returns:
            Graph state update with classification details.
        """
        request = EmailClassificationRequest(**state["email"])
        return {"classification": self._email_agent.classify(request).model_dump()}
