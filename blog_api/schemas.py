"""
Pydantic models for request and response validation.

These classes enforce the shape of data sent to and returned from the
API endpoints. They also serve as a form of documentation for the
expected payloads when building API clients.

Each model using ``orm_mode = True`` allows FastAPI to read data
returned by SQLAlchemy ORM objects directly.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Post Schemas
class PostBase(BaseModel):
    title: str = Field(..., title="Post title", max_length=255)
    content: str = Field(..., title="Post content")


class PostCreate(PostBase):
    """Schema for creating a new blog post."""

    pass


class PostUpdate(BaseModel):
    """Schema for updating an existing blog post.

    All fields are optional; only provided fields will be updated.
    """

    title: Optional[str] = Field(None, max_length=255, title="Updated title")
    content: Optional[str] = Field(None, title="Updated content")


class CommentBase(BaseModel):
    content: str = Field(..., title="Comment content")


class CommentCreate(CommentBase):
    """Schema for creating a new comment on a post."""

    pass


class Comment(CommentBase):
    """Schema for returning comment details."""

    id: int
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    """Schema for returning post details, including comments."""

    id: int
    created_at: datetime
    updated_at: datetime
    comments: List[Comment] = []

    class Config:
        orm_mode = True