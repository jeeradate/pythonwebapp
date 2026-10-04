"""Database initialization and session context management module.

Handles SQLModel engine configuration and SQLite Foreign Key enforcement.
Fully compliant with PEP 8 standards and type-safety rules.
"""

from typing import Any, Generator
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from food_app.core.config import settings

# Configure SQLite specific runtime connection arguments
connect_args: dict[str, bool] = (
    {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Initialize SQLModel Database Engine instance
engine: Engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG_MODE,
    connect_args=connect_args,
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection: Any, connection_record: Any) -> None:
    """Enforces SQLite Foreign Key constraint checking on every new connection.

    Args:
        dbapi_connection (Any): Active underlying DBAPI connection object.
        connection_record (Any): SQLAlchemy connection record wrapper.
    """
    if "sqlite" in settings.DATABASE_URL:
        # Using Any type annotation prevents Mypy/Pylance 'no attribute cursor' warnings
        cursor: Any = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_db_and_tables() -> None:
    """Creates all database schema tables registered in SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Provides a transactional database session generator for application requests.

    Yields:
        Generator[Session, None, None]: Active SQLModel Session instance.
    """
    with Session(engine) as session:
        yield session