"""
SQLAlchemy ORM models for the blog application.

This module defines the database models for blog posts and comments,
including their relationships and table structures.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Post(Base):
    """
    Blog Post model representing a single blog post.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        title: Post title, required string up to 200 characters
        content: Post content, text field for longer content
        author: Author name, required string up to 100 characters
        created_at: Timestamp when post was created, auto-generated
        updated_at: Timestamp when post was last updated, auto-updated
        comments: Relationship to associated comments
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with comments - cascade delete ensures comments are deleted when post is deleted
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', author='{self.author}')>"


class Comment(Base):
    """
    Comment model representing comments on blog posts.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        name: Commenter's name, required string up to 100 characters
        content: Comment content, text field
        created_at: Timestamp when comment was created, auto-generated
        post_id: Foreign key referencing the associated post
        post: Relationship to the parent post
    """
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign key to link comment to a specific post
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    # Relationship back to the post
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, name='{self.name}', post_id={self.post_id})>"