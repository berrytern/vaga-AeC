import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.main.middlewares import rate_limit_middleware
from fastapi import Request
from fastapi.responses import JSONResponse
from uuid import uuid4


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "limit,exp",
    [
        (0, 10),
        (10, 12),
        (100, 23),
    ],
)
async def test_rate_limit_middleware_first_count(request_mock, limit: int, exp: int):
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)
    redis_mock.set = AsyncMock()
    redis_mock.setex = AsyncMock()
    middleware_instance_id = str(uuid4())
    client_ip = str(uuid4())
    key = f"limit-{client_ip}{middleware_instance_id}"
    gen_uuid4_mock = Mock(return_value=middleware_instance_id)
    request_mock.client = Mock()
    request_mock.client.host = client_ip

    expected_response = str(uuid4())

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.rate_limit.RedisClient", redis_mock), patch(
        "src.main.middlewares.rate_limit.uuid4", gen_uuid4_mock
    ) as _:
        wrapper = rate_limit_middleware(limit + 1, exp)
        assert callable(rate_limit_middleware)
        assert callable(wrapper)
        assert callable(wrapper(next_mock))
        middleware = wrapper(next_mock)
        response = await middleware(request=request_mock)

        assert request_mock.client.host == client_ip
        redis_mock.get.assert_called_with(key)
        redis_mock.set.assert_not_called()
        redis_mock.setex.assert_called_with(key, exp, 1)

        assert response == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "limit",
    [
        0,
        10,
        100,
    ],
)
async def test_rate_limit_middleware_last_count(request_mock, limit):
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=limit)
    redis_mock.set = AsyncMock()
    redis_mock.setex = AsyncMock()
    middleware_instance_id = str(uuid4())
    client_ip = str(uuid4())
    key = f"limit-{client_ip}{middleware_instance_id}"
    gen_uuid4_mock = Mock(return_value=middleware_instance_id)
    request_mock.client = Mock()
    request_mock.client.host = client_ip

    expected_response = str(uuid4())

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.rate_limit.RedisClient", redis_mock), patch(
        "src.main.middlewares.rate_limit.uuid4", gen_uuid4_mock
    ) as _:
        wrapper = rate_limit_middleware(limit + 1, 10)
        assert callable(rate_limit_middleware)
        assert callable(wrapper)
        assert callable(wrapper(next_mock))
        middleware = wrapper(next_mock)
        response = await middleware(request=request_mock)

        assert request_mock.client.host == client_ip
        redis_mock.get.assert_called_with(key)
        redis_mock.set.assert_called_with(key, limit + 1, True, True)
        redis_mock.setex.assert_not_called()

        assert response == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "limit",
    [
        0,
        10,
        100,
    ],
)
async def test_rate_limit_middleware_out_of_limit(request_mock, limit):
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=limit)
    redis_mock.set = AsyncMock()
    middleware_instance_id = str(uuid4())
    client_ip = str(uuid4())
    key = f"limit-{client_ip}{middleware_instance_id}"
    gen_uuid4_mock = Mock(return_value=middleware_instance_id)
    request_mock.client = Mock()
    request_mock.client.host = client_ip

    expected_response = str(uuid4())

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.rate_limit.RedisClient", redis_mock), patch(
        "src.main.middlewares.rate_limit.uuid4", gen_uuid4_mock
    ) as _:
        wrapper = rate_limit_middleware(limit, 10)
        assert callable(rate_limit_middleware)
        assert callable(wrapper)
        assert callable(wrapper(next_mock))
        middleware = wrapper(next_mock)
        response = await middleware(request=request_mock)

        assert request_mock.client.host == client_ip
        redis_mock.get.assert_called_with(key)
        redis_mock.set.assert_not_called()
        redis_mock.setex.assert_not_called()

        assert isinstance(response, JSONResponse)
        assert response.status_code == 429
        assert response.body == b'{"message":"Rate limit exceeded"}'
