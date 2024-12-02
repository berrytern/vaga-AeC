import pytest
from unittest.mock import Mock


@pytest.fixture(scope="function")
def request_mock():
    from fastapi import Request

    request = Mock(spec=Request)
    yield request
