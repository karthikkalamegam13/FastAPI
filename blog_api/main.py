"""
Entry point for the blog API.

This module creates the FastAPI application instance, sets up the
database tables, and includes API routers for posts and comments. It
also defines a simple root endpoint for health checking or providing
basic information about the API.

To run the development server, install the required dependencies and
execute the following command in your terminal:

```
uvicorn blog_api.main:app --reload
```

The ``--reload`` flag reloads the server automatically when code
changes are detected, making it ideal for iterative development in a
video tutorial.
"""

from __future__ import annotations

from fastapi import FastAPI

from .database import Base, engine
from .routers import posts, comments


# Create all database tables. In a larger application you may want to
# manage migrations with a tool like Alembic instead of calling
# ``create_all`` at import time.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", version="1.0.0", description="A simple blog API built with FastAPI")


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """Root endpoint returning a friendly greeting.

    This can be used as a simple health check or landing point for the
    API. It returns a short message describing the purpose of the API.
    """
    return {"message": "Welcome to the Blog API! Use /docs for API documentation."}


# Include routers for posts and comments. The order of inclusion does
# not matter, but grouping them in a dedicated routers package keeps
# the application modular and easy to maintain.
app.include_router(posts.router)
app.include_router(comments.router)