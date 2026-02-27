"""
FastAPI dependencies.

This module exposes dependency providers used by route handlers.
It wires database sessions and application services via FastAPI's Depends.
"""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.repositories.users import UserRepository
from app.repositories.groups import GroupRepository
from app.repositories.memberships import MembershipRepository
from app.repositories.messages import MessageRepository
from app.services.group_service import GroupService
from app.services.message_service import MessageService


def get_db() -> Session:
    """
    Provide a transactional SQLAlchemy session.

    Yields:
        A SQLAlchemy session that is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_username(x_user: str = Header(..., alias="X-User")) -> str:
    """
    Extract and validate the user identity from request headers.

    Args:
        x_user: The value of the `X-User` header.

    Returns:
        A normalized username string.

    Raises:
        HTTPException: If missing or invalid format.
    """
    username = (x_user or "").strip()
    if not username:
        raise HTTPException(status_code=400, detail="Missing X-User header")

    if len(username) > 50:
        raise HTTPException(status_code=400, detail="X-User too long")

    # Simple allowlist (adjust if you need spaces)
    import re
    if not re.match(r"^[a-zA-Z0-9._-]+$", username):
        raise HTTPException(status_code=400, detail="Invalid X-User format")

    return username


def get_group_service() -> GroupService:
    """
    Provide GroupService with its repositories.

    Returns:
        A fully-wired GroupService instance.
    """
    return GroupService(
        groups=GroupRepository(),
        users=UserRepository(),
        memberships=MembershipRepository(),
    )


def get_message_service() -> MessageService:
    """
    Provide MessageService with its repositories.

    Returns:
        A fully-wired MessageService instance.
    """
    return MessageService(
        groups=GroupRepository(),
        users=UserRepository(),
        memberships=MembershipRepository(),
        messages=MessageRepository(),
    )