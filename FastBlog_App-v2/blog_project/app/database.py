"""
Database configuration and session management for the FastAPI blog application.

This module sets up SQLAlchemy with SQLite database connection and provides
database session management for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL - creates a file named 'blog.db' in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Create SQLite engine with check_same_thread=False to allow multiple threads
# This is needed for FastAPI's async nature
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a SessionLocal class for database sessions
# autocommit=False: transactions need to be explicitly committed
# autoflush=False: changes aren't automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    
    This function creates a new database session for each request
    and ensures it's properly closed after the request is completed.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()