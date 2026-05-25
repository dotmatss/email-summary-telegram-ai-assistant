from typing import Protocol

from src.models.vector_document import VectorDocument


class VectorRepository(Protocol):
    """Repository contract for vector document storage and search."""

    def add(self, document: VectorDocument) -> VectorDocument:
        """Stores a vector-searchable document.

        Args:
            document: Vector document entity.

        Returns:
            Stored vector document entity.
        """
        ...

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
        ...
