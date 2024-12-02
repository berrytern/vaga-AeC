import pytest
from unittest.mock import AsyncMock, patch
from src.main.middlewares import session_middleware
from uuid import uuid4


@pytest.mark.asyncio
async def test_session_middleware(request_mock):
    # Create mock session
    db_session_mock = AsyncMock()

    excepted_answer = uuid4()

    # Create mock for next function
    async def next_mock(*args, **kwargs):
        return excepted_answer

    # Mock get_db to return our session mock
    with patch(
        "src.main.middlewares.session_middleware.get_db", return_value=db_session_mock
    ):
        # Verify that the middleware is a callable function
        assert callable(session_middleware)
        assert callable(session_middleware(next_mock))
        middleware = session_middleware(next_mock)
        # Apply and execute middleware
        response = await middleware(request_mock)

        # Verify response
        assert response == excepted_answer
        # Verify if the session was injected into the request state
        assert db_session_mock == request_mock.state.db_session

        # Verify commit was called
        db_session_mock.commit.assert_called_once()


@pytest.mark.asyncio
async def test_session_middleware_error_handling(request_mock):
    # Create mock session
    db_session_mock = AsyncMock()

    # Create next function that raises error
    async def next_mock(request, *args, **kwargs):
        raise ValueError("Test error")

    with patch(
        "src.main.middlewares.session_middleware.get_db", return_value=db_session_mock
    ):
        middleware = session_middleware(next_mock)

        with pytest.raises(ValueError, match="Test error"):
            await middleware(request_mock)

        db_session_mock.commit.assert_not_called()
