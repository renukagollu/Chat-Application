"""
Message API routes.

Defines endpoints for sending and listing messages within a group.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_username, get_message_service
from app.schemas.messages import MessageCreate
from app.services.message_service import MessageService

router = APIRouter(tags=["messages"])


@router.post("/groups/{group_id}/messages", status_code=201)
def send_message(
    group_id: int,
    payload: MessageCreate,
    username: str = Depends(get_username),
    db: Session = Depends(get_db),
    svc: MessageService = Depends(get_message_service),
) -> dict:
    """
    Send a message to a group.

    Args:
        group_id: Group ID path parameter.
        payload: Message body.
        username: User identity from headers.
        db: Database session.
        svc: Message service.

    Returns:
        Message creation metadata.
    """
    return svc.send_message(db, group_id, username, payload.content)


@router.get("/groups/{group_id}/messages")
def list_messages(
    group_id: int,
    limit: int = Query(50, ge=1, le=200),
    after: str | None = Query(None),
    db: Session = Depends(get_db),
    svc: MessageService = Depends(get_message_service),
) -> dict:
    """
    List messages for a group.

    Args:
        group_id: Group ID path parameter.
        limit: Maximum number of messages to return (1..200).
        after: ISO timestamp to fetch messages strictly after it.
        db: Database session.
        svc: Message service.

    Returns:
        A response wrapper containing messages.
    """
    return {"data": svc.list_messages(db, group_id, limit, after)}