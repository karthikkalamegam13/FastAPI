"""
Post-related routes for the blog application.

This module handles all post-related operations including:
- Homepage with post listings
- Individual post detail pages
- Post creation, updating, and deletion
- Template rendering for frontend views
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# Create router instance for post-related routes
router = APIRouter()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


# Utility function to create post summary for listing pages
def create_post_summary(post: models.Post) -> str:
    """
    Create a short summary from post content for listing pages.
    
    Args:
        post: Post model instance
        
    Returns:
        str: Truncated summary of the post content
    """
    # Limit summary to first 150 characters and add ellipsis if truncated
    if len(post.content) > 150:
        return post.content[:150] + "..."
    return post.content


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    """
    Homepage route displaying all blog posts.
    
    Fetches all posts from the database and renders them in a list format
    with title, author, and summary for each post.
    
    Args:
        request: FastAPI request object for template context
        db: Database session dependency
        
    Returns:
        HTMLResponse: Rendered homepage template with posts list
    """
    # Fetch all posts ordered by creation date (newest first)
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    
    # Create post summaries for the homepage
    post_summaries = []
    for post in posts:
        post_summaries.append({
            "id": post.id,
            "title": post.title,
            "author": post.author,
            "created_at": post.created_at,
            "summary": create_post_summary(post)
        })
    
    return templates.TemplateResponse(
        "home.html", 
        {"request": request, "posts": post_summaries}
    )


@router.get("/post/{post_id}", response_class=HTMLResponse)
async def post_detail(request: Request, post_id: int, db: Session = Depends(get_db)):
    """
    Post detail page showing full post content and comments.
    
    Args:
        request: FastAPI request object for template context
        post_id: ID of the post to display
        db: Database session dependency
        
    Returns:
        HTMLResponse: Rendered post detail template
        
    Raises:
        HTTPException: 404 if post not found
    """
    # Fetch post with comments using eager loading
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return templates.TemplateResponse(
        "post_detail.html",
        {"request": request, "post": post}
    )


@router.get("/create-post", response_class=HTMLResponse)
async def create_post_form(request: Request):
    """
    Display the create post form.
    
    Args:
        request: FastAPI request object for template context
        
    Returns:
        HTMLResponse: Rendered create post form template
    """
    return templates.TemplateResponse(
        "create_post.html",
        {"request": request}
    )


@router.post("/create-post")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handle post creation form submission.
    
    Creates a new blog post with the provided data and redirects to homepage.
    
    Args:
        title: Post title from form
        content: Post content from form
        author: Post author from form
        db: Database session dependency
        
    Returns:
        RedirectResponse: Redirect to homepage after successful creation
    """
    # Create new post instance
    new_post = models.Post(
        title=title,
        content=content,
        author=author
    )
    
    # Add to database session and commit
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # Redirect to homepage after successful creation
    return RedirectResponse(url="/", status_code=303)


@router.get("/edit-post/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
    """
    Display the edit post form with existing post data.
    
    Args:
        request: FastAPI request object for template context
        post_id: ID of the post to edit
        db: Database session dependency
        
    Returns:
        HTMLResponse: Rendered edit post form template
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return templates.TemplateResponse(
        "edit_post.html",
        {"request": request, "post": post}
    )


@router.post("/edit-post/{post_id}")
async def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handle post update form submission.
    
    Updates an existing blog post with new data and redirects to the post detail page.
    
    Args:
        post_id: ID of the post to update
        title: Updated post title from form
        content: Updated post content from form
        author: Updated post author from form
        db: Database session dependency
        
    Returns:
        RedirectResponse: Redirect to updated post detail page
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Update post fields
    post.title = title
    post.content = content
    post.author = author
    
    # Commit changes to database
    db.commit()
    
    # Redirect to the updated post detail page
    return RedirectResponse(url=f"/post/{post_id}", status_code=303)


@router.post("/delete-post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Handle post deletion.
    
    Deletes a blog post and all associated comments, then redirects to homepage.
    
    Args:
        post_id: ID of the post to delete
        db: Database session dependency
        
    Returns:
        RedirectResponse: Redirect to homepage after deletion
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Delete post (comments will be cascade deleted due to relationship configuration)
    db.delete(post)
    db.commit()
    
    # Redirect to homepage after deletion
    return RedirectResponse(url="/", status_code=303)


# API endpoints for JSON responses (useful for future API integration)

@router.get("/api/posts", response_model=List[schemas.PostSummary])
async def get_posts_api(db: Session = Depends(get_db)):
    """
    API endpoint to get all posts as JSON.
    
    Returns:
        List[PostSummary]: List of post summaries in JSON format
    """
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    
    post_summaries = []
    for post in posts:
        post_summaries.append(schemas.PostSummary(
            id=post.id,
            title=post.title,
            author=post.author,
            created_at=post.created_at,
            summary=create_post_summary(post)
        ))
    
    return post_summaries


@router.get("/api/posts/{post_id}", response_model=schemas.Post)
async def get_post_api(post_id: int, db: Session = Depends(get_db)):
    """
    API endpoint to get a single post as JSON.
    
    Args:
        post_id: ID of the post to retrieve
        db: Database session dependency
        
    Returns:
        Post: Complete post data including comments
        
    Raises:
        HTTPException: 404 if post not found
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post