"""
Package initializer for the blog_api application.

This package contains all modules required to run the FastAPI-based
blog application. The application is designed as a teaching aid
for developers learning FastAPI and demonstrates how to structure
a typical project with routers, models, schemas and database
interaction using SQLAlchemy and SQLite.

To start the API server, run the ``main.py`` module with Uvicorn:

```
uvicorn blog_api.main:app --reload
```

The ``--reload`` flag automatically reloads the server when code
changes are detected, making development convenient during the
tutorial.
"""

from .main import app  # noqa: F401