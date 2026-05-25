from uuid import UUID

from pydantic import BaseModel, Field


class VectorDocumentCreate(BaseModel):
    """Request schema for storing a vector document.

    Attributes:
        namespace: Logical document namespace.
        content: Source text content.
        embedding: Numeric vector embedding.
        metadata: Additional document metadata.
    """

    namespace: str = Field(min_length=1)
    content: str = Field(min_length=1)
    embedding: list[float]
    metadata: dict[str, str] = Field(default_factory=dict)


class VectorSearchRequest(BaseModel):
    """Request schema for vector search.

    Attributes:
        namespace: Logical document namespace.
        embedding: Query embedding.
        limit: Maximum number of matches.
    """

    namespace: str = Field(min_length=1)
    embedding: list[float]
    limit: int = Field(default=5, ge=1, le=50)


class VectorDocumentResponse(BaseModel):
    """Response schema for a vector document.

    Attributes:
        id: Document identifier.
        namespace: Logical document namespace.
        content: Source text content.
        metadata: Additional document metadata.
    """

    id: UUID
    namespace: str
    content: str
    metadata: dict[str, str]
