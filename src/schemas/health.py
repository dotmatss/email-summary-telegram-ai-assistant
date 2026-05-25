from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response schema.

    Attributes:
        status: Current service status.
    """

    status: str
