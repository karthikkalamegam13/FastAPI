"""
Main FastAPI application instance and configuration.

This module creates the FastAPI application, includes routers,
sets up database tables, and configures static file serving.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import engine
from . import models
from .routers import post, comment

# Create database tables
# This will create all tables defined in models.py if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(
    title="FastAPI Blog Application",
    description="A complete blog application built with FastAPI, SQLAlchemy, and Jinja2 templates",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)

# Mount static files directory for CSS, JavaScript, images, etc.
# This allows serving static files from the /static URL path
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers for different parts of the application
# All post-related routes (homepage, post detail, CRUD operations)
app.include_router(post.router, tags=["posts"])

# All comment-related routes
app.include_router(comment.router, tags=["comments"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    
    Useful for monitoring and ensuring the application is running properly.
    
    Returns:
        dict: Status message indicating the application is healthy
    """
    return {"status": "healthy", "message": "FastAPI Blog Application is running"}


# Root API information endpoint
@app.get("/api")
async def api_info():
    """
    API information endpoint.
    
    Provides information about available API endpoints and their purposes.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "FastAPI Blog API",
        "version": "1.0.0",
        "endpoints": {
            "posts": {
                "GET /api/posts": "Get all posts",
                "GET /api/posts/{post_id}": "Get specific post with comments"
            },
            "comments": {
                "GET /api/posts/{post_id}/comments": "Get comments for a post",
                "POST /api/posts/{post_id}/comments": "Create new comment",
                "GET /api/comments/{comment_id}": "Get specific comment",
                "DELETE /comments/{comment_id}": "Delete comment"
            },
            "web_interface": {
                "GET /": "Homepage with all posts",
                "GET /post/{post_id}": "Post detail page",
                "GET /create-post": "Create post form",
                "POST /create-post": "Submit new post",
                "GET /edit-post/{post_id}": "Edit post form",
                "POST /edit-post/{post_id}": "Update post",
                "POST /delete-post/{post_id}": "Delete post",
                "POST /post/{post_id}/comment": "Add comment to post"
            }
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }


# Optional: Add startup event handler for any initialization tasks
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    This function runs when the application starts up.
    Useful for initialization tasks, logging, or setup operations.
    """
    print("🚀 FastAPI Blog Application started successfully!")
    print("📖 Access the application at: http://localhost:8000")
    print("📚 API Documentation available at: http://localhost:8000/docs")


# Optional: Add shutdown event handler for cleanup tasks
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    
    This function runs when the application shuts down.
    Useful for cleanup tasks, closing connections, or logging.
    """
    print("👋 FastAPI Blog Application shutting down...")


# Error handlers for common HTTP exceptions
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory="app/templates")

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 error handler.
    
    Returns a custom 404 page instead of the default JSON response
    for web browser requests.
    """
    # Check if request accepts HTML (from web browser)
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return templates.TemplateResponse(
            "404.html", 
            {"request": request}, 
            status_code=404
        )
    
    # For API requests, return JSON response
    return {"detail": "Not Found"}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Custom 500 error handler.
    
    Returns a custom error page for internal server errors.
    """
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return templates.TemplateResponse(
            "500.html", 
            {"request": request}, 
            status_code=500
        )
    
    return {"detail": "Internal Server Error"}


if __name__ == "__main__":
    import uvicorn
    
    # Run the application with uvicorn if this file is executed directly
    # This is useful for development and testing
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes during development
        log_level="info"
    )