"""
Group request/response schemas.

These define the API contracts while keeping ORM models internal.
"""

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    """Request payload to create a new group."""

    name: str = Field(min_length=1, max_length=100)


class GroupOut(BaseModel):
    """Response payload for a group."""

    id: int
    name: str

    model_config = {"from_attributes": True}