from uuid import UUID

from src.models.chat_message import ChatMessage
from src.storage.database.postgres import (
    PostgresConnectionManager,
    postgres_connection_manager,
)


class PostgresChatHistoryRepository:
    """Stores chat history messages in PostgreSQL."""

    def __init__(
        self,
        connection_manager: PostgresConnectionManager | None = None,
    ) -> None:
        """Initializes the repository.

        Args:
            connection_manager: PostgreSQL connection manager.
        """
        self._connection_manager = connection_manager or postgres_connection_manager
        self._schema_initialized = False

    def add(self, message: ChatMessage) -> ChatMessage:
        """Stores a chat message.

        Args:
            message: Chat message entity.

        Returns:
            Stored chat message entity.
        """
        self._ensure_schema()
        statement = """
        INSERT INTO chat_messages (id, conversation_id, role, content, created_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, conversation_id, role, content, created_at;
        """
        params = (
            message.id,
            message.conversation_id,
            message.role,
            message.content,
            message.created_at,
        )
        with self._connection_manager.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, params)
                row = cursor.fetchone()
            connection.commit()
        return self._to_entity(row)

    def list_by_conversation(self, conversation_id: UUID) -> list[ChatMessage]:
        """Lists messages for a conversation.

        Args:
            conversation_id: Conversation identifier.

        Returns:
            Chat messages ordered by creation time.
        """
        self._ensure_schema()
        statement = """
        SELECT id, conversation_id, role, content, created_at
        FROM chat_messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC;
        """
        with self._connection_manager.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, (conversation_id,))
                rows = cursor.fetchall()
        return [self._to_entity(row) for row in rows]

    def _ensure_schema(self) -> None:
        """Initializes the repository schema once per repository instance."""
        if self._schema_initialized:
            return
        self._connection_manager.initialize_chat_history_schema()
        self._schema_initialized = True

    @staticmethod
    def _to_entity(row: dict | None) -> ChatMessage:
        """Converts a database row into a chat message entity.

        Args:
            row: Chat message database row.

        Returns:
            Chat message entity.
        """
        if row is None:
            raise RuntimeError("Expected chat message row was not returned by PostgreSQL.")
        return ChatMessage(
            id=row["id"],
            conversation_id=row["conversation_id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"],
        )
