"""
Database setup for the blog API.

This module exposes a SQLAlchemy ``SessionLocal`` factory for
creating database sessions and a ``Base`` class for model
declarations. It uses an SQLite database stored in a local file,
which keeps the tutorial self‑contained and easy to run without
needing a separate database server.

Whenever you perform database operations within a request, you
should depend on the ``get_db`` dependency defined here to
automatically create and clean up sessions.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL. The ``check_same_thread`` flag must be set to
# False because SQLAlchemy creates a pool of connections which will
# be shared across threads by FastAPI. Without this flag SQLite
# restricts connections to a single thread.
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Create the SQLAlchemy engine. The connect_args argument is
# necessary only for SQLite. For other databases such as PostgreSQL
# or MySQL you can omit this argument and instead provide user,
# password and host information in the URL.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ``sessionmaker`` returns a new Session class when called.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models. All ORM models should inherit
# from this class.
Base = declarative_base()


def get_db():
    """Provide a transactional scope around a series of operations.

    This dependency yields a database session to request handlers
    and closes it automatically after the request is complete.

    Usage in a FastAPI path operation:

    ```
    @app.get("/items/")
    def read_items(db: Session = Depends(get_db)):
        # use db here
        ...
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()