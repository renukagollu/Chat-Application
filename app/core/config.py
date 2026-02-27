"""
Application configuration.

This module defines the Settings object used to configure runtime behavior.
The settings are loaded from environment variables when present.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Strongly-typed application settings.

    Attributes:
        app_name: Name of the application (used in OpenAPI docs).
        database_url: SQLAlchemy database URL. Defaults to a local SQLite file.
        debug: Enables more verbose error output.
    """

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    app_name: str = "Chat Backend"
    database_url: str = "sqlite:///./chat.db"
    debug: bool = False


settings = Settings()