from src.models.followup import FollowUp
from src.storage.database.postgres import (
    PostgresConnectionManager,
    postgres_connection_manager,
)


class PostgresFollowUpRepository:
    """Stores follow-up reminders in PostgreSQL."""

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

    def add(self, followup: FollowUp) -> FollowUp:
        """Adds a follow-up reminder.

        Args:
            followup: Follow-up domain entity.

        Returns:
            Stored follow-up entity.
        """
        self._ensure_schema()
        statement = """
        INSERT INTO followups (id, subject, recipient, due_at, notes, completed)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, subject, recipient, due_at, notes, completed;
        """
        params = (
            followup.id,
            followup.subject,
            followup.recipient,
            followup.due_at,
            followup.notes,
            followup.completed,
        )
        with self._connection_manager.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, params)
                row = cursor.fetchone()
            connection.commit()
        return self._to_entity(row)

    def list(self) -> list[FollowUp]:
        """Lists follow-up reminders ordered by due date.

        Returns:
            Follow-up entities.
        """
        self._ensure_schema()
        statement = """
        SELECT id, subject, recipient, due_at, notes, completed
        FROM followups
        ORDER BY due_at ASC;
        """
        with self._connection_manager.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement)
                rows = cursor.fetchall()
        return [self._to_entity(row) for row in rows]

    def _ensure_schema(self) -> None:
        """Initializes the repository schema once per repository instance."""
        if self._schema_initialized:
            return
        self._connection_manager.initialize_followup_schema()
        self._schema_initialized = True

    @staticmethod
    def _to_entity(row: dict | None) -> FollowUp:
        """Converts a database row into a follow-up entity."""
        if row is None:
            raise RuntimeError("Expected follow-up row was not returned by PostgreSQL.")
        return FollowUp(
            id=row["id"],
            subject=row["subject"],
            recipient=row["recipient"],
            due_at=row["due_at"],
            notes=row["notes"],
            completed=row["completed"],
        )
