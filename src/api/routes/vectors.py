from fastapi import APIRouter, Depends

from src.api.dependencies import dependency_provider
from src.operations.vector_document_use_case import VectorDocumentUseCase
from src.schemas.vector import (
    VectorDocumentCreate,
    VectorDocumentResponse,
    VectorSearchRequest,
)


class VectorRoutes:
    """Registers vector document routes."""

    def __init__(self) -> None:
        """Initializes the vector router."""
        self.router = APIRouter()
        self.router.add_api_route(
            "/documents",
            self.add_document,
            methods=["POST"],
            response_model=VectorDocumentResponse,
        )
        self.router.add_api_route(
            "/search",
            self.search,
            methods=["POST"],
            response_model=list[VectorDocumentResponse],
        )

    def add_document(
        self,
        request: VectorDocumentCreate,
        use_case: VectorDocumentUseCase = Depends(
            dependency_provider.get_vector_document_use_case
        ),
    ) -> VectorDocumentResponse:
        """Stores a vector document.

        Args:
            request: Vector document creation request.
            use_case: Vector document use case dependency.

        Returns:
            Stored vector document response.
        """
        return use_case.add_document(request)

    def search(
        self,
        request: VectorSearchRequest,
        use_case: VectorDocumentUseCase = Depends(
            dependency_provider.get_vector_document_use_case
        ),
    ) -> list[VectorDocumentResponse]:
        """Searches vector documents.

        Args:
            request: Vector search request.
            use_case: Vector document use case dependency.

        Returns:
            Matching vector document responses.
        """
        return use_case.search(request)


router = VectorRoutes().router
