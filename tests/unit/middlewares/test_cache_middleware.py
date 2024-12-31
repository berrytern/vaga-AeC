import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.main.middlewares import cache_middleware
from fastapi import Request, Response
from uuid import uuid4
from json import dumps
from random import randint


@pytest.mark.asyncio
async def test_cache_middleware_with_empty_cache(request_mock):
    exp = randint(100, 599)
    method, path = str(uuid4()), str(uuid4())
    request_mock.method = method
    request_mock.url = Mock()
    request_mock.url.path = path
    request_mock.query_params = Mock()
    query_params_sorted = sorted(
        [(str(uuid4()), str(uuid4())), (str(uuid4()), str(uuid4()))]
    )
    query_params_unsorted = query_params_sorted[::-1]
    request_mock.query_params.items = Mock(return_value=query_params_unsorted)
    key = f"{method}-{path}" + str(query_params_sorted)
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)
    redis_mock.setex = AsyncMock()

    expected_response = Response(
        content=str(uuid4()),
        status_code=randint(100, 599),
        headers={str(uuid4()): str(uuid4())},
    )
    expected_cache = dumps(
        {
            "body": expected_response.body.decode(),
            "status_code": expected_response.status_code,
            "headers": {
                item[0].decode(): item[1].decode()
                for item in expected_response.raw_headers
            },
        }
    )

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.cache.RedisClient", redis_mock) as _:
        wrapper = cache_middleware(exp)
        assert callable(cache_middleware)
        assert callable(wrapper)
        assert callable(wrapper(next_mock))
        middleware = wrapper(next_mock)
        response = await middleware(request=request_mock)

        redis_mock.get.assert_called_with(key)
        redis_mock.setex.assert_called_with(key, exp, expected_cache)

        assert response == expected_response


@pytest.mark.asyncio
async def test_cache_middleware_with_cache(request_mock):
    exp = randint(100, 599)
    method, path = str(uuid4()), str(uuid4())
    request_mock.method = method
    request_mock.url = Mock()
    request_mock.url.path = path
    request_mock.query_params = Mock()
    query_params_sorted = sorted(
        [(str(uuid4()), str(uuid4())), (str(uuid4()), str(uuid4()))]
    )
    query_params_unsorted = query_params_sorted[::-1]
    request_mock.query_params.items = Mock(return_value=query_params_unsorted)
    key = f"{method}-{path}" + str(query_params_sorted)

    expected_response = Response(
        content=str(uuid4()),
        status_code=randint(100, 599),
        headers={str(uuid4()): str(uuid4())},
    )
    expected_cache = dumps(
        {
            "body": expected_response.body.decode(),
            "status_code": expected_response.status_code,
            "headers": {
                item[0].decode(): item[1].decode()
                for item in expected_response.raw_headers
            },
        }
    )

    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=expected_cache)
    redis_mock.setex = AsyncMock()

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.cache.RedisClient", redis_mock) as _:
        wrapper = cache_middleware(exp)
        assert callable(cache_middleware)
        assert callable(wrapper)
        assert callable(wrapper(next_mock))
        middleware = wrapper(next_mock)
        response = await middleware(request=request_mock)

        redis_mock.get.assert_called_with(key)
        redis_mock.setex.assert_not_called()

        assert response.status_code == expected_response.status_code
        assert response.body == expected_response.body
        assert response.headers == expected_response.headers
