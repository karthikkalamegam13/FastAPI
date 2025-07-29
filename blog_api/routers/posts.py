"""
API router for blog post management.

This module defines endpoints under the ``/posts`` prefix to perform
create, read, update, and delete operations on blog posts. It uses
SQLAlchemy sessions and Pydantic schemas to ensure data integrity
and provide clear API responses.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, database


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    """Create a new blog post.

    Accepts a payload conforming to ``PostCreate`` and returns the
    created post including its generated ID and timestamps.
    """
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Retrieve a list of blog posts.

    Optional pagination parameters ``skip`` and ``limit`` allow the
    client to control which records are returned.
    """
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts


@router.get("/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(database.get_db)):
    """Retrieve a single post by its ID.

    Raises a 404 error if the post does not exist.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated: schemas.PostUpdate, db: Session = Depends(database.get_db)):
    """Update an existing post.

    Only fields provided in the request body will be updated. Returns the
    updated post or a 404 error if the post does not exist.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # Apply updates selectively
    if updated.title is not None:
        post.title = updated.title
    if updated.content is not None:
        post.content = updated.content
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(database.get_db)):
    """Delete a post by its ID.

    Returns 204 No Content on success. If the post does not exist a 404
    error is returned.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    # No content to return
    return None