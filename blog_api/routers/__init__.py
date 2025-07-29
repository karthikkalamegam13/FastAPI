"""
Package for API routers.

This package groups the separate routers used by the application
(e.g., posts and comments). By organizing the endpoints into distinct
modules you keep the codebase modular and easier to navigate. New
routers can be added here as the project grows.
"""

from . import posts, comments  # noqa: F401