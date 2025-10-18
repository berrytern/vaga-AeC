from fastapi import Request
from typing import Callable
from functools import wraps
from src.utils.default import get_or_set_db_session, db_session_var, aux_db_session_var


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
        token, session = get_or_set_db_session()
        async with session as db:
            try:
                response = await next(*args, request=request, **kwargs)
                # commit changes if no errors
                await db.commit()
                return response
            except BaseException as e:
                # Rollback only on errors
                await db.rollback()
                raise e
            finally:
                await db.close()
                if token:
                    db_session_var.reset(token)
                if aux_session := aux_db_session_var.get(None):
                    await aux_session.aclose()

    return wrapper
