from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from src.config.config import settings


class PostgresConnectionManager:
    """Creates PostgreSQL connections and initializes schemas."""

    @contextmanager
    def connection(self) -> Generator[psycopg.Connection, None, None]:
        """Yields a PostgreSQL connection.

        Yields:
            Active PostgreSQL connection.
        """
        with psycopg.connect(settings.database_url, row_factory=dict_row) as connection:
            yield connection

    def initialize_followup_schema(self) -> None:
        """Creates follow-up tables."""
        statements = [
            """
            CREATE TABLE IF NOT EXISTS followups (
                id UUID PRIMARY KEY,
                subject TEXT NOT NULL,
                recipient TEXT NOT NULL,
                due_at TIMESTAMPTZ NOT NULL,
                notes TEXT,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """
        ]
        self._execute_schema_statements(statements)

    def initialize_chat_history_schema(self) -> None:
        """Creates chat history tables."""
        statements = [
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id UUID PRIMARY KEY,
                conversation_id UUID NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL
            );
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_created
            ON chat_messages (conversation_id, created_at);
            """,
        ]
        self._execute_schema_statements(statements)

    def initialize_vector_schema(self, dimension: int) -> None:
        """Creates pgvector extension and vector document table.

        Args:
            dimension: Embedding dimension.
        """
        statements = [
            "CREATE EXTENSION IF NOT EXISTS vector;",
            f"""
            CREATE TABLE IF NOT EXISTS vector_documents (
                id UUID PRIMARY KEY,
                namespace TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding vector({dimension}) NOT NULL,
                metadata JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_vector_documents_namespace
            ON vector_documents (namespace);
            """,
        ]
        self._execute_schema_statements(statements)

    def _execute_schema_statements(self, statements: list[str]) -> None:
        """Executes schema statements in a transaction.

        Args:
            statements: SQL schema statements.
        """
        with psycopg.connect(settings.database_url) as connection:
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)
            connection.commit()


postgres_connection_manager = PostgresConnectionManager()
