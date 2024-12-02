from src.infrastructure.database import get_db
from fastapi import Request
from typing import Callable
from functools import wraps


# injects a database session into the request state
def session_middleware(next: Callable):
    """
    Creates a database session that injects a database session into the request state.

    Args:
        Callable: The FastAPI endpoint function that need database access or another middleware.
    Returns:
        Callable: A decorator function that wraps API endpoints with JWT authentication.

    Example:
        ```python
        @session_middleware
        async def db_action_endpoint(request: Request):
            # Enable use of the database session in the endpoint
            request.state.db_session
        ```
    """

    @wraps(next)
    async def wrapper(request: Request, *args, **kwargs):
        """
        Wraps an endpoint function with database session access.

        Args:
            next (Callable): The FastAPI endpoint function that need database access.

        Returns:
            Callable: The wrapped function  with database session access.
        """
        request.state.db_session = get_db()
        return await next(*args, request=request, **kwargs)

    return wrapper
