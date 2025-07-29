"""
API router for comment management.

This module defines endpoints under the ``/posts/{post_id}/comments``
prefix to create new comments on blog posts and retrieve existing
comments. Comments are associated with posts via a foreign key
relationship defined in the models.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, database


# Using a dynamic prefix to capture the parent post's ID. This allows
# grouping all comment-related routes under the relevant post.
router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


@router.post("/", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
):
    """Create a new comment on a specific post.

    A 404 error is returned if the referenced post does not exist.
    """
    parent = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db_comment = models.Comment(post_id=post_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/", response_model=List[schemas.Comment])
def read_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
):
    """Retrieve comments for a specific post.

    Supports optional pagination via ``skip`` and ``limit`` query
    parameters. Returns an empty list if no comments exist or if the
    post does not exist. Clients should treat the absence of
    comments and non‑existence of the post differently based on
    their needs; this API returns an empty list for both cases.
    """
    # Optionally verify the post exists; returning an empty list if not.
    comments_query = (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return comments_query