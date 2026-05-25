from langchain_core.tools import BaseTool

from src.agents.email_agent import EmailAgent
from src.agents.meeting_agent import MeetingAgent
from src.operations.notification_use_case import NotificationUseCase
from src.tools.email_tools import EmailToolFactory
from src.tools.meeting_tools import MeetingToolFactory
from src.tools.notification_tools import NotificationToolFactory


class AssistantToolRegistry:
    """Builds the full set of LangChain tools for the assistant.

    Args:
        email_agent: Agent used by email tools.
        meeting_agent: Agent used by meeting tools.
        notification_use_case: Use case used by notification tools.
    """

    def __init__(
        self,
        email_agent: EmailAgent | None = None,
        meeting_agent: MeetingAgent | None = None,
        notification_use_case: NotificationUseCase | None = None,
    ) -> None:
        """Initializes the tool registry.

        Args:
            email_agent: Optional email agent override.
            meeting_agent: Optional meeting agent override.
            notification_use_case: Optional notification use case override.
        """
        self._email_agent = email_agent
        self._meeting_agent = meeting_agent
        self._notification_use_case = notification_use_case

    def build(self) -> list[BaseTool]:
        """Creates all assistant tools.

        Returns:
            A combined list of LangChain tools.
        """
        return [
            *EmailToolFactory(email_agent=self._email_agent).build(),
            *MeetingToolFactory(meeting_agent=self._meeting_agent).build(),
            *NotificationToolFactory(
                notification_use_case=self._notification_use_case
            ).build(),
        ]
