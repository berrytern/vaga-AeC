from typing import Optional
from src.application.domain.utils import UserTypes
from src.infrastructure.cache import RedisClient
from src.utils import settings
from fastapi import Request, HTTPException
from typing import Callable
from functools import wraps
from jwt.exceptions import PyJWTError
import jwt


# This is a middleware function that checks for the presence of a valid JWT token in the Authorization header
def auth_middleware(scope: str, id_key: Optional[str] = None):
    """
    Creates a decorator that validates JWT tokens and checks for required scope.

    Args:
        scope (str): The required scope that must be present in the JWT token's payload.
        id_key (Optional[str]): The key in the endpoint's kwargs that contains the user ID.

    Returns:
        Callable: A decorator function that wraps API endpoints with JWT authentication.

    Example:
        ```python
        @auth_middleware("admin")
        async def protected_endpoint(request: Request):
            # Only users with "admin" scope can access this endpoint
            pass
        ```
    """

    def decorator(endpoint_func: Callable):
        @wraps(endpoint_func)
        async def wrapper(*args, request: Request, **kwargs):
            """
            Wraps an endpoint function with JWT authentication logic.

            Args:
                endpoint_func (Callable): The FastAPI endpoint function to be protected.

            Returns:
                Callable: The wrapped function with authentication checks.
            """
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(
                    status_code=401, detail="Authorization header missing"
                )
            try:
                # Remove 'Bearer ' prefix if present
                if token.startswith("Bearer "):
                    token = token.split(" ")[1]
                # Decode and validate the token
                if await RedisClient.get(token):
                    raise HTTPException(status_code=401, detail="Revoked token")
                payload = jwt.decode(
                    token, settings.JWT_SECRET, algorithms=["HS256"], verify=True
                )
                if scope not in payload["scope"]:
                    raise HTTPException(
                        status_code=401, detail="Invalid or expired token"
                    )
                if (
                    id_key
                    and kwargs[id_key] != payload["sub"]
                    and payload["type"] != UserTypes.ADMIN.value
                ):
                    raise HTTPException(
                        status_code=401, detail="Resource not owned by user"
                    )

                # Add the payload to the request state for use in the endpoint
                request.state.user = payload
                return await endpoint_func(*args, request=request, **kwargs)
            except PyJWTError:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

        return wrapper

    return decorator
