import pytest
from unittest.mock import AsyncMock, Mock, MagicMock, patch
from src.main.middlewares import auth_middleware
from tests.unit.mocks.auth_payload import (
    ADMIN_PAYLOAD,
    ADMIN_SCOPE,
    READER_PAYLOAD,
    READER_SCOPE,
)
from fastapi import HTTPException, Request
from jwt.exceptions import PyJWTError
from uuid import uuid4
import jwt


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,scope",
    [
        (
            ADMIN_PAYLOAD,
            ADMIN_SCOPE[0],
        ),
        (
            READER_PAYLOAD,
            READER_SCOPE[0],
        ),
    ],
)
async def test_auth_middleware(request_mock, payload, scope):
    jwt_secret = str(uuid4())  # Create a random jwt secret
    token = jwt.encode(payload, "secret")
    # Setup request mock
    request_mock.headers.get = MagicMock(return_value=token)
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)

    expected_response = str(uuid4())  # Create a random string

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.auth.RedisClient", redis_mock), patch(
        "src.main.middlewares.auth.settings.JWT_SECRET", jwt_secret
    ), patch(
        "src.main.middlewares.auth.jwt.decode", return_value=payload
    ) as decode_mock:
        assert callable(auth_middleware)
        assert callable(auth_middleware(scope))
        assert callable(auth_middleware(scope)(next_mock))
        middleware = auth_middleware(scope)(next_mock)
        response = await middleware(request=request_mock)
        request_mock.headers.get.assert_called_with("Authorization")
        decode_mock.assert_called_with(
            token, jwt_secret, algorithms=["HS256"], verify=True
        )
        redis_mock.get.assert_called_with(token)
        # Test success cases
        assert response == expected_response
        assert hasattr(request_mock.state, "user")
        assert request_mock.state.user == payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,scope",
    [
        (
            ADMIN_PAYLOAD,
            ADMIN_SCOPE[0],
        ),
        (
            READER_PAYLOAD,
            READER_SCOPE[0],
        ),
    ],
)
async def test_auth_middleware_with_revoked_token(request_mock, payload, scope):
    jwt_secret = str(uuid4())  # Create a random jwt secret
    token = jwt.encode(payload, "secret")
    # Setup request mock
    request_mock.headers.get = MagicMock(return_value=token)
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=token)

    expected_response = str(uuid4())  # Create a random string

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.auth.RedisClient", redis_mock), patch(
        "src.main.middlewares.auth.settings.JWT_SECRET", jwt_secret
    ), patch(
        "src.main.middlewares.auth.jwt.decode", return_value=payload
    ) as decode_mock:
        assert callable(auth_middleware)
        assert callable(auth_middleware(scope))
        assert callable(auth_middleware(scope)(next_mock))
        with pytest.raises(HTTPException) as exc_info:
            middleware = auth_middleware(scope)(next_mock)
            await middleware(request=request_mock)
        # Test failure cases
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Revoked token"
        request_mock.headers.get.assert_called_with("Authorization")
        decode_mock.assert_not_called()
        redis_mock.get.assert_called_with(token)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,scope",
    [
        (
            ADMIN_PAYLOAD,
            "vs:2",
        ),
        (
            READER_PAYLOAD,
            "ad:c",
        ),
    ],
)
async def test_auth_middleware_without_permission(request_mock, payload, scope):
    jwt_secret = str(uuid4())  # Create a random jwt secret
    token = jwt.encode(payload, "secret")
    # Setup request mock
    request_mock.headers.get = MagicMock(return_value=token)
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)

    expected_response = str(uuid4())  # Create a random string

    # Create mock for next function
    async def next_mock(*args, **kwargs):
        return expected_response

    with patch("src.main.middlewares.auth.RedisClient", redis_mock), patch(
        "src.main.middlewares.auth.settings.JWT_SECRET", jwt_secret
    ), patch(
        "src.main.middlewares.auth.jwt.decode", return_value=payload
    ) as decode_mock:
        assert callable(auth_middleware)
        assert callable(auth_middleware(scope))
        assert callable(auth_middleware(scope)(next_mock))
        middleware = auth_middleware(scope)(next_mock)
        with pytest.raises(HTTPException) as exc_info:
            await middleware(request=request_mock)
        request_mock.headers.get.assert_called_with("Authorization")
        decode_mock.assert_called_with(
            token, jwt_secret, algorithms=["HS256"], verify=True
        )
        # Test failure cases
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid or expired token"


@pytest.mark.asyncio
async def test_auth_middleware_with_invalid_jwt_secret(request_mock):
    """Additional test for JWT secret validation"""
    request_mock.headers.get = MagicMock(return_value="Bearer invalid_token")
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)

    # Create mock for next function
    async def next_mock(*args, **kwargs):
        return ""

    with patch("src.main.middlewares.auth.RedisClient", redis_mock), patch(
        "src.main.middlewares.auth.jwt.decode",
        side_effect=PyJWTError("Invalid signature"),
    ):
        middleware = auth_middleware("admin")(next_mock)

        with pytest.raises(HTTPException) as exc_info:
            await middleware(request=request_mock)

        request_mock.headers.get.assert_called_with("Authorization")
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid or expired token"


@pytest.mark.asyncio
async def test_auth_middleware_without_authorization_header(request_mock):
    scope = "vr:c"
    jwt_secret = str(uuid4())  # Create a random jwt secret
    token = None
    # Setup request mock
    request_mock.headers.get = MagicMock(return_value=token)
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)

    expected_response = str(uuid4())  # Create a random string

    # Create mock for next function
    async def next_mock(*args, **kwargs):
        return expected_response

    with patch("src.main.middlewares.auth.RedisClient", redis_mock), patch(
        "src.main.middlewares.auth.settings.JWT_SECRET", jwt_secret
    ), patch("src.main.middlewares.auth.jwt.decode", return_value=token) as decode_mock:
        assert callable(auth_middleware)
        assert callable(auth_middleware(scope))
        assert callable(auth_middleware(scope)(next_mock))
        middleware = auth_middleware(scope)(next_mock)
        with pytest.raises(HTTPException) as exc_info:
            await middleware(request=request_mock)
        request_mock.headers.get.assert_called_with("Authorization")
        decode_mock.assert_not_called()
        # Test failure cases
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Authorization header missing"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,scope,authorized",
    [
        (
            ADMIN_PAYLOAD,
            ADMIN_SCOPE[0],
            True,
        ),
        (
            READER_PAYLOAD,
            READER_SCOPE[0],
            False,
        ),
    ],
)
async def test_auth_middleware_not_owned(
    request_mock, payload, scope, authorized: bool
):
    id_key = str(uuid4())
    id_value = str(uuid4())
    jwt_secret = str(uuid4())  # Create a random jwt secret
    token = jwt.encode(payload, "secret")
    # Setup request mock
    request_mock.headers.get = MagicMock(return_value=token)
    redis_mock = Mock()
    redis_mock.get = AsyncMock(return_value=None)

    expected_response = str(uuid4())  # Create a random string

    # Create mock for next function
    async def next_mock(*args, request: Request, **kwargs):
        return expected_response

    with patch("src.main.middlewares.auth.RedisClient", redis_mock), patch(
        "src.main.middlewares.auth.settings.JWT_SECRET", jwt_secret
    ), patch(
        "src.main.middlewares.auth.jwt.decode", return_value=payload
    ) as decode_mock:
        assert callable(auth_middleware)
        wrapper = auth_middleware(scope, id_key)
        assert callable(wrapper)
        assert callable(wrapper(next_mock))
        middleware = wrapper(next_mock)
        if authorized:
            response = await middleware(request=request_mock, **{id_key: id_value})
            assert response == expected_response
            request_mock.headers.get.assert_called_with("Authorization")
            decode_mock.assert_called_with(
                token, jwt_secret, algorithms=["HS256"], verify=True
            )
            redis_mock.get.assert_called_with(token)

            # Test success cases
            assert hasattr(request_mock.state, "user")
            assert request_mock.state.user == payload
        else:
            with pytest.raises(HTTPException) as exc_info:
                await middleware(request=request_mock, **{id_key: id_value})
            # Test failure cases
            assert exc_info.value.status_code == 401
            assert exc_info.value.detail == "Resource not owned by user"
