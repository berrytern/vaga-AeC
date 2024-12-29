from typing import Callable
from src.infrastructure.cache import RedisClient
from fastapi import Request
from functools import wraps
from starlette.responses import JSONResponse
from uuid import uuid4


def rate_limit_middleware(limit: int, expiration_time: int, trust_proxy: bool = False):
    id = str(uuid4())

    def decorator(next: Callable):
        @wraps(next)
        async def wrapper(request: Request, *args, **kwargs):
            ip = request.client and request.client.host
            if trust_proxy:
                ip = request.headers.get("X-Forwarded-For", ip)
            key = f"limit-{ip}{id}"
            count = await RedisClient.get(key)
            if count is not None:
                count = int(count) + 1
                if count > limit:
                    return JSONResponse(
                        status_code=429,
                        content={"message": "Rate limit exceeded"},
                    )
                await RedisClient.set(key, count, True, True)
            else:
                await RedisClient.setex(key, expiration_time, 1)
            return await next(*args, request=request, **kwargs)

        return wrapper

    return decorator
