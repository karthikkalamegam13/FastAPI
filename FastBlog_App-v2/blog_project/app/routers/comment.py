"""
Comment-related routes for the blog application.

This module handles comment operations including:
- Adding new comments to posts
- API endpoints for comment management
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# Create router instance for comment-related routes
router = APIRouter()


@router.post("/post/{post_id}/comment")
async def add_comment(
    post_id: int,
    name: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handle comment form submission for a specific post.
    
    Creates a new comment associated with the given post and redirects
    back to the post detail page to show the new comment.
    
    Args:
        post_id: ID of the post to comment on
        name: Commenter's name from form
        content: Comment content from form
        db: Database session dependency
        
    Returns:
        RedirectResponse: Redirect to post detail page after comment creation
        
    Raises:
        HTTPException: 404 if post not found
    """
    # Verify that the post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create new comment instance
    new_comment = models.Comment(
        name=name,
        content=content,
        post_id=post_id
    )
    
    # Add to database session and commit
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Redirect back to the post detail page to show the new comment
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)


@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific comment.
    
    This endpoint allows deletion of individual comments.
    Useful for moderation or if users want to remove their comments.
    
    Args:
        comment_id: ID of the comment to delete
        db: Database session dependency
        
    Returns:
        dict: Success message with deleted comment ID
        
    Raises:
        HTTPException: 404 if comment not found
    """
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Store post_id for potential redirect before deleting
    post_id = comment.post_id
    
    # Delete comment
    db.delete(comment)
    db.commit()
    
    return {"message": f"Comment {comment_id} deleted successfully", "post_id": post_id}


# API endpoints for JSON responses

@router.get("/api/posts/{post_id}/comments", response_model=List[schemas.Comment])
async def get_comments_api(post_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get all comments for a specific post as JSON.
    
    Args:
        post_id: ID of the post to get comments for
        db: Database session dependency
        
    Returns:
        List[Comment]: List of comments for the specified post
        
    Raises:
        HTTPException: 404 if post not found
    """
    # Verify post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get comments ordered by creation date (oldest first for reading flow)
    comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id
    ).order_by(models.Comment.created_at.asc()).all()
    
    return comments


@router.post("/api/posts/{post_id}/comments", response_model=schemas.Comment)
async def create_comment_api(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    """
    API endpoint to create a new comment via JSON.
    
    This endpoint allows programmatic creation of comments using JSON data
    instead of form submission.
    
    Args:
        post_id: ID of the post to comment on
        comment: Comment data from request body
        db: Database session dependency
        
    Returns:
        Comment: The created comment with all fields
        
    Raises:
        HTTPException: 404 if post not found
    """
    # Verify that the post exists
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create new comment instance from Pydantic model
    new_comment = models.Comment(
        name=comment.name,
        content=comment.content,
        post_id=post_id
    )
    
    # Add to database session and commit
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment


@router.get("/api/comments/{comment_id}", response_model=schemas.Comment)
async def get_comment_api(comment_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a specific comment as JSON.
    
    Args:
        comment_id: ID of the comment to retrieve
        db: Database session dependency
        
    Returns:
        Comment: The requested comment data
        
    Raises:
        HTTPException: 404 if comment not found
    """
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment