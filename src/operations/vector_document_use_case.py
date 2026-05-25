from uuid import uuid4

from src.models.vector_document import VectorDocument
from src.schemas.vector import (
    VectorDocumentCreate,
    VectorDocumentResponse,
    VectorSearchRequest,
)
from src.storage.vector_repository import VectorRepository


class VectorDocumentUseCase:
    """Coordinates vector document application use cases."""

    def __init__(self, repository: VectorRepository) -> None:
        """Initializes the vector document use case.

        Args:
            repository: Vector repository.
        """
        self._repository = repository

    def add_document(self, request: VectorDocumentCreate) -> VectorDocumentResponse:
        """Stores a vector document.

        Args:
            request: Vector document creation request.

        Returns:
            Stored vector document response.
        """
        document = VectorDocument(
            id=uuid4(),
            namespace=request.namespace,
            content=request.content,
            embedding=request.embedding,
            metadata=request.metadata,
        )
        return self._to_response(self._repository.add(document))

    def search(self, request: VectorSearchRequest) -> list[VectorDocumentResponse]:
        """Searches vector documents.

        Args:
            request: Vector search request.

        Returns:
            Matching vector document responses.
        """
        documents = self._repository.search(
            namespace=request.namespace,
            embedding=request.embedding,
            limit=request.limit,
        )
        return [self._to_response(document) for document in documents]

    @staticmethod
    def _to_response(document: VectorDocument) -> VectorDocumentResponse:
        """Converts a vector document entity into a response schema.

        Args:
            document: Vector document entity.

        Returns:
            Vector document response.
        """
        return VectorDocumentResponse(
            id=document.id,
            namespace=document.namespace,
            content=document.content,
            metadata=document.metadata,
        )
