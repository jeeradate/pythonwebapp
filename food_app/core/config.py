"""Configuration management module for Food Order App.

Parses environment variables and dynamic system configurations using Pydantic Settings.
Fully compliant with PEP 8 standards and strict type annotations.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings schema."""

    # Application Metadata
    APP_TITLE: str = "Food Order App - Learning Platform"
    APP_VERSION: str = "0.1.0"

    # Network & Server Settings (Supports Cloud Dynamic Environment Variables)
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8080"))
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1", "t")

    # Directory Structure Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Database Settings
    DATABASE_URL_ENV: Optional[str] = os.getenv("DATABASE_URL")
    DATABASE_FILE: str = "food_order_app.db"

    @property
    def DATABASE_URL(self) -> str:
        """Computes and returns the appropriate SQLModel/SQLAlchemy connection URL.

        Returns:
            str: Connection string for PostgreSQL if defined; otherwise local SQLite URL.
        """
        if self.DATABASE_URL_ENV:
            # Fix legacy 'postgres://' scheme to 'postgresql://' for SQLAlchemy 2.0+ compatibility
            if self.DATABASE_URL_ENV.startswith("postgres://"):
                return self.DATABASE_URL_ENV.replace("postgres://", "postgresql://", 1)
            return self.DATABASE_URL_ENV

        db_path: Path = self.BASE_DIR / self.DATABASE_FILE
        return f"sqlite:///{db_path}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Single shared instance for system-wide access
settings: Settings = Settings()
