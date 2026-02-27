"""
Message request/response schemas.

Includes pagination query parameters via API routes.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """Request payload for sending a message."""

    content: str = Field(min_length=1, max_length=2000)


class MessageOut(BaseModel):
    """Response payload for a message."""

    id: int
    content: str
    created_at: datetime
    username: str