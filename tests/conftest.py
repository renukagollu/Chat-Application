"""
Test configuration.

Provides a FastAPI TestClient for integration-style tests.
"""

from fastapi.testclient import TestClient
from app.main import create_app


def test_client() -> TestClient:
    """
    Create a TestClient for the FastAPI app.

    Returns:
        A configured TestClient instance.
    """
    app = create_app()
    return TestClient(app)