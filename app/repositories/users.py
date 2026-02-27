"""
UserRepository.

Provides persistence operations for User entities.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository for user persistence operations."""

    def get_or_create(self, db: Session, username: str) -> User:
        """
        Fetch an existing user by username or create a new one.

        Args:
            db: SQLAlchemy session.
            username: Unique user identifier.

        Returns:
            The existing or newly created User.
        """
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if user:
            return user

        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user