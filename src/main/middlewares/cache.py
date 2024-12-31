from typing import Callable
from src.infrastructure.cache import RedisClient
from fastapi import Request, Response
from functools import wraps
from json import loads, dumps


def cache_middleware(expiration_time: int):
    def decorator(next: Callable):
        @wraps(next)
        async def wrapper(request: Request, *args, **kwargs):
            key = f"{request.method}-{request.url.path}" + str(
                sorted(request.query_params.items())
            )
            cached_data = await RedisClient.get(key)
            if cached_data:
                cached_response = loads(cached_data)
                return Response(
                    content=cached_response["body"],
                    status_code=cached_response["status_code"],
                    headers=cached_response["headers"],
                )
            response: Response = await next(*args, request=request, **kwargs)
            cached_response = {
                "body": response.body.decode(),
                "status_code": response.status_code,
                "headers": {
                    item[0].decode(): item[1].decode() for item in response.raw_headers
                },
            }
            await RedisClient.setex(key, expiration_time, dumps(cached_response))
            return response

        return wrapper

    return decorator
