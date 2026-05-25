from psycopg.types.json import Jsonb

from src.models.vector_document import VectorDocument
from src.storage.database.postgres import (
    PostgresConnectionManager,
    postgres_connection_manager,
)


class PostgresVectorRepository:
    """Stores and searches vector documents using PostgreSQL pgvector."""

    def __init__(
        self,
        dimension: int,
        connection_manager: PostgresConnectionManager | None = None,
    ) -> None:
        """Initializes the repository.

        Args:
            dimension: Embedding dimension.
            connection_manager: PostgreSQL connection manager.
        """
        self._dimension = dimension
        self._connection_manager = connection_manager or postgres_connection_manager
        self._schema_initialized = False

    def add(self, document: VectorDocument) -> VectorDocument:
        """Stores a vector-searchable document.

        Args:
            document: Vector document entity.

        Returns:
            Stored vector document entity.
        """
        self._ensure_schema()
        self._validate_embedding(document.embedding)
        statement = """
        INSERT INTO vector_documents (id, namespace, content, embedding, metadata)
        VALUES (%s, %s, %s, %s::vector, %s)
        RETURNING id, namespace, content, embedding::text, metadata;
        """
        params = (
            document.id,
            document.namespace,
            document.content,
            self._format_vector(document.embedding),
            Jsonb(document.metadata),
        )
        with self._connection_manager.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, params)
                row = cursor.fetchone()
            connection.commit()
        return self._to_entity(row)

    def search(
        self,
        namespace: str,
        embedding: list[float],
        limit: int = 5,
    ) -> list[VectorDocument]:
        """Searches documents by vector similarity.

        Args:
            namespace: Logical document namespace.
            embedding: Query embedding vector.
            limit: Maximum number of matches.

        Returns:
            Similar vector documents.
        """
        self._ensure_schema()
        self._validate_embedding(embedding)
        statement = """
        SELECT id, namespace, content, embedding::text, metadata
        FROM vector_documents
        WHERE namespace = %s
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
        """
        with self._connection_manager.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, (namespace, self._format_vector(embedding), limit))
                rows = cursor.fetchall()
        return [self._to_entity(row) for row in rows]

    def _ensure_schema(self) -> None:
        """Initializes the repository schema once per repository instance."""
        if self._schema_initialized:
            return
        self._connection_manager.initialize_vector_schema(self._dimension)
        self._schema_initialized = True

    def _validate_embedding(self, embedding: list[float]) -> None:
        """Validates the embedding dimension before database operations.

        Args:
            embedding: Numeric embedding values.

        Raises:
            ValueError: If the embedding dimension does not match configuration.
        """
        if len(embedding) != self._dimension:
            raise ValueError(
                f"Expected embedding dimension {self._dimension}, got {len(embedding)}."
            )

    @staticmethod
    def _format_vector(embedding: list[float]) -> str:
        """Formats an embedding for pgvector.

        Args:
            embedding: Numeric embedding values.

        Returns:
            pgvector-compatible string representation.
        """
        values = ",".join(str(value) for value in embedding)
        return f"[{values}]"

    @classmethod
    def _to_entity(cls, row: dict | None) -> VectorDocument:
        """Converts a database row into a vector document entity.

        Args:
            row: Vector document database row.

        Returns:
            Vector document entity.
        """
        if row is None:
            raise RuntimeError("Expected vector document row was not returned by PostgreSQL.")
        return VectorDocument(
            id=row["id"],
            namespace=row["namespace"],
            content=row["content"],
            embedding=cls._parse_vector(row["embedding"]),
            metadata=dict(row["metadata"]),
        )

    @staticmethod
    def _parse_vector(value: str) -> list[float]:
        """Parses a pgvector text value.

        Args:
            value: pgvector text representation.

        Returns:
            Numeric embedding values.
        """
        stripped = value.strip("[]")
        if not stripped:
            return []
        return [float(item) for item in stripped.split(",")]
