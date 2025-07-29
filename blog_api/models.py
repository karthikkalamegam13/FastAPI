"""
SQLAlchemy models for the blog API.

These classes map to database tables and define the schema for
blog posts and comments. Relationships between posts and comments
are established via foreign keys and SQLAlchemy relationships.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    """Represents a blog post entry."""

    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(255), nullable=False)
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship to comments. When a post is deleted, cascade the delete to
    # its comments to maintain referential integrity.
    comments: List["Comment"] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class Comment(Base):
    """Represents a comment on a blog post."""

    __tablename__ = "comments"

    id: int = Column(Integer, primary_key=True, index=True)
    post_id: int = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationship back to the post. The back_populates argument
    # must match the attribute name used in the Post model.
    post: Post = relationship("Post", back_populates="comments")