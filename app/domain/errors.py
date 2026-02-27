"""
Domain-level exceptions.

Use these to keep business logic independent from FastAPI and HTTP concerns.
"""

from __future__ import annotations


class DomainError(Exception):
    """Base error for domain-level failures."""


class NotFound(DomainError):
    """Raised when an entity cannot be found."""


class Forbidden(DomainError):
    """Raised when an action is not allowed."""


class ValidationError(DomainError):
    """Raised when input violates business rules."""