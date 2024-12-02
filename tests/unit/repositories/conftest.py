import pytest
from unittest.mock import AsyncMock
from src.infrastructure.repositories import ReaderRepository
from src.application.domain.models import ReaderModel, ReaderList
from src.infrastructure.database.schemas import ReaderSchema
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def reader_repository(mock_session):
    return ReaderRepository(
        session=mock_session,
        schema=ReaderSchema,
        model=ReaderModel,
        list_model=ReaderList,
    )
