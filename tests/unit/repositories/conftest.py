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
from src.utils.default import db_session_var, aux_db_session_var


@pytest.fixture
def session_mock():
    session = AsyncMock(spec=AsyncSession)
    token = db_session_var.set(session)
    yield session
    db_session_var.reset(token)


@pytest.fixture
def aux_session_mock():
    session = AsyncMock(spec=AsyncSession)
    token = aux_db_session_var.set(session)
    yield session
    aux_db_session_var.reset(token)


@pytest.fixture
def reader_repository(session_mock):
    return ReaderRepository(
        schema=ReaderSchema,
        model=ReaderModel,
        list_model=ReaderList,
    )


@pytest.fixture
def admin_repository(session_mock):
    return AdminRepository(schema=AdminSchema, model=AdminModel, list_model=AdminList)
