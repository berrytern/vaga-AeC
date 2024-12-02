import pytest
from unittest.mock import AsyncMock
from src.infrastructure.repositories import (
    AdminRepository,
    ReaderRepository,
)
from src.application.domain.models import (
    AdminModel,
    AdminList,
    ReaderModel,
    ReaderList,
)
from src.infrastructure.database.schemas import (
    AdminSchema,
    ReaderSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def session_mock():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def reader_repository(session_mock):
    return ReaderRepository(
        session=session_mock,
        schema=ReaderSchema,
        model=ReaderModel,
        list_model=ReaderList,
    )


@pytest.fixture
def admin_repository(session_mock):
    return AdminRepository(
        session=session_mock, schema=AdminSchema, model=AdminModel, list_model=AdminList
    )
