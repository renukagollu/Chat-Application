"""
Group API routes.

Defines endpoints for creating and joining public groups.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_username, get_group_service
from app.domain.errors import NotFound
from app.schemas.groups import GroupCreate
from app.services.group_service import GroupService

router = APIRouter(tags=["groups"])


@router.post("/groups", status_code=201)
def create_group(
    payload: GroupCreate,
    db: Session = Depends(get_db),
    svc: GroupService = Depends(get_group_service),
) -> dict:
    """
    Create a new public group.

    Args:
        payload: Request payload containing the group name.
        db: Database session dependency.
        svc: Group service dependency.

    Returns:
        Created group representation.
    """
    return svc.create_group(db, payload.name)


@router.get("/groups")
def list_groups(
    db: Session = Depends(get_db),
    svc: GroupService = Depends(get_group_service),
) -> dict:
    """
    List all groups.

    Args:
        db: Database session dependency.
        svc: Group service dependency.

    Returns:
        A response wrapper containing groups.
    """
    return {"data": svc.list_groups(db)}


@router.post("/groups/{group_id}/join")
def join_group(
    group_id: int,
    username: str = Depends(get_username),
    db: Session = Depends(get_db),
    svc: GroupService = Depends(get_group_service),
) -> dict:
    """
    Join a public group.

    Args:
        group_id: Group ID path parameter.
        username: User identity extracted from request headers.
        db: Database session dependency.
        svc: Group service dependency.

    Returns:
        Confirmation payload.

    Raises:
        NotFound: Converted to HTTP 404 by main exception handler.
    """
    return svc.join_group(db, group_id, username)