from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class VectorDocument:
    """Vector-searchable document domain entity.

    Attributes:
        id: Document identifier.
        namespace: Logical namespace for retrieval.
        content: Source text content.
        embedding: Numeric vector embedding.
        metadata: Additional document metadata.
    """

    id: UUID
    namespace: str
    content: str
    embedding: list[float]
    metadata: dict[str, str]
