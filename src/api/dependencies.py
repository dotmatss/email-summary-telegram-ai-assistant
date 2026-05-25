from functools import lru_cache

from src.agents.email_agent import EmailAgent
from src.agents.meeting_agent import MeetingAgent
from src.config.config import settings
from src.integrations.ai.langchain_openai_client import LangChainOpenAiClient
from src.integrations.calendar.calendar_client import CalendarClient
from src.integrations.gmail.gmail_client import GmailClient
from src.integrations.telegram.telegram_client import TelegramClient
from src.operations.chat_history_use_case import ChatHistoryUseCase
from src.operations.email_use_case import EmailUseCase
from src.operations.followup_use_case import FollowUpUseCase
from src.operations.meeting_use_case import MeetingUseCase
from src.operations.notification_use_case import NotificationUseCase
from src.operations.vector_document_use_case import VectorDocumentUseCase
from src.storage.memory_followup_repository import InMemoryFollowUpRepository
from src.storage.postgres_chat_history_repository import PostgresChatHistoryRepository
from src.storage.postgres_followup_repository import PostgresFollowUpRepository
from src.storage.postgres_vector_repository import PostgresVectorRepository


class DependencyProvider:
    """Provides shared dependencies for API routes."""

    @lru_cache
    def get_email_use_case(self) -> EmailUseCase:
        """Creates or returns the cached email use case.

        Returns:
            Email use case instance.
        """
        ai_service = (
            LangChainOpenAiClient()
            if settings.ai_provider.lower() == "openai"
            else None
        )
        return EmailUseCase(gmail_service=GmailClient(), email_agent=EmailAgent(ai_service))

    @lru_cache
    def get_meeting_use_case(self) -> MeetingUseCase:
        """Creates or returns the cached meeting use case.

        Returns:
            Meeting use case instance.
        """
        return MeetingUseCase(calendar_service=CalendarClient(), meeting_agent=MeetingAgent())

    @lru_cache
    def get_notification_use_case(self) -> NotificationUseCase:
        """Creates or returns the cached notification use case.

        Returns:
            Notification use case instance.
        """
        return NotificationUseCase(telegram_service=TelegramClient())

    @lru_cache
    def get_followup_use_case(self) -> FollowUpUseCase:
        """Creates or returns the cached follow-up use case.

        Returns:
            Follow-up use case instance.
        """
        if settings.followup_repository.lower() == "postgres":
            repository = PostgresFollowUpRepository()
        else:
            repository = InMemoryFollowUpRepository()
        return FollowUpUseCase(repository=repository)

    @lru_cache
    def get_chat_history_use_case(self) -> ChatHistoryUseCase:
        """Creates or returns the cached chat history use case.

        Returns:
            Chat history use case instance.
        """
        return ChatHistoryUseCase(repository=PostgresChatHistoryRepository())

    @lru_cache
    def get_vector_document_use_case(self) -> VectorDocumentUseCase:
        """Creates or returns the cached vector document use case.

        Returns:
            Vector document use case instance.
        """
        repository = PostgresVectorRepository(dimension=settings.vector_dimension)
        return VectorDocumentUseCase(repository=repository)


dependency_provider = DependencyProvider()
