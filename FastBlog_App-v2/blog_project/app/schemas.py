"""
Pydantic schemas for request and response data validation.

This module defines the data validation schemas used for API requests
and responses, ensuring data integrity and providing automatic
API documentation.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    """Base schema for comment data."""
    name: str = Field(..., min_length=1, max_length=100, description="Commenter's name")
    content: str = Field(..., min_length=1, description="Comment content")


class CommentCreate(CommentBase):
    """Schema for creating a new comment."""
    pass


class Comment(CommentBase):
    """
    Schema for comment response data.
    
    Includes all comment fields plus metadata like ID and creation timestamp.
    """
    id: int
    created_at: datetime
    post_id: int
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class PostBase(BaseModel):
    """Base schema for post data."""
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, description="Post content")
    author: str = Field(..., min_length=1, max_length=100, description="Post author")


class PostCreate(PostBase):
    """Schema for creating a new post."""
    pass


class PostUpdate(BaseModel):
    """Schema for updating an existing post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1, max_length=100)


class Post(PostBase):
    """
    Schema for post response data.
    
    Includes all post fields plus metadata like ID, timestamps, and associated comments.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[Comment] = []
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class PostSummary(BaseModel):
    """
    Schema for post summary data used in list views.
    
    Contains only essential fields for displaying posts in lists,
    without the full content and comments.
    """
    id: int
    title: str
    author: str
    created_at: datetime
    summary: str = Field(..., description="Short summary of the post content")
    
    class Config:
        from_attributes = True