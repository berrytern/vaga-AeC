import pytest
from unittest.mock import Mock, MagicMock
from src.infrastructure.repositories.admin_repository import AdminRepository
from tests.unit.mocks.admin_data import ADMIN_DATA
from uuid import UUID


@pytest.mark.asyncio
async def test_repository_initialization(session_mock):
    schema, model, list_model = Mock(), Mock(), Mock()
    repository = AdminRepository(
        session=session_mock, schema=schema, model=model, list_model=list_model
    )

    assert repository.session == session_mock


@pytest.mark.asyncio
async def test_create_admin(admin_repository, session_mock):
    # Prepare test data
    input_data = {"name": ADMIN_DATA["name"], "email": ADMIN_DATA["email"]}

    # Mock the execute result
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (
        ADMIN_DATA["id"],
        ADMIN_DATA["name"],
        ADMIN_DATA["email"],
        ADMIN_DATA["created_at"],
        ADMIN_DATA["updated_at"],
    )
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await admin_repository.create(input_data)

    # Assertions
    assert isinstance(result, dict)
    assert result["id"] == str(ADMIN_DATA["id"])
    assert result["name"] == ADMIN_DATA["name"]
    assert result["email"] == ADMIN_DATA["email"]
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_one_admin(admin_repository, session_mock):
    # Prepare test data
    search_fields = {"id": ADMIN_DATA["id"]}

    # Mock the execute result
    mock_result = MagicMock()
    mock_schema = MagicMock()
    for key, value in ADMIN_DATA.items():
        setattr(mock_schema, key, value)
    mock_result.fetchone.return_value = (mock_schema,)
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await admin_repository.get_one(search_fields)

    # Assertions
    assert isinstance(result, dict)
    assert result["id"] == str(ADMIN_DATA["id"])
    assert result["name"] == ADMIN_DATA["name"]
    assert result["email"] == ADMIN_DATA["email"]
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_admins(admin_repository, session_mock):
    # Prepare test data
    filters = {"query": {}, "limit": 10}

    # Mock the stream_scalars result
    mock_schema = MagicMock()
    for key, value in ADMIN_DATA.items():
        setattr(mock_schema, key, value)

    async def mock_stream():
        yield mock_schema

    session_mock.stream_scalars.return_value = mock_stream()

    # Execute the method
    result = await admin_repository.get_all(filters)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == str(ADMIN_DATA["id"])
    assert result[0]["name"] == ADMIN_DATA["name"]
    session_mock.stream_scalars.assert_called_once()


@pytest.mark.asyncio
async def test_update_one_admin(admin_repository, session_mock):
    # Prepare test data
    admin_id = str(ADMIN_DATA["id"])
    update_data = {"name": "Updated Admin"}

    # Mock the execute result
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (
        ADMIN_DATA["id"],
        "Updated Admin",
        ADMIN_DATA["email"],
        ADMIN_DATA["created_at"],
        ADMIN_DATA["updated_at"],
    )
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await admin_repository.update_one(admin_id, update_data)

    # Assertions
    assert isinstance(result, dict)
    assert result["id"] == str(ADMIN_DATA["id"])
    assert result["name"] == "Updated Admin"
    assert result["email"] == ADMIN_DATA["email"]
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_delete_one_admin(admin_repository, session_mock):
    # Prepare test data
    admin_id = str(ADMIN_DATA["id"])

    # Execute the method
    result = await admin_repository.delete_one(admin_id)

    # Assertions
    assert result is None
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_one_admin_not_found(admin_repository, session_mock):
    # Prepare test data
    search_fields = {"id": UUID("12345678-1234-5678-1234-567812345678")}

    # Mock the execute result to return None
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await admin_repository.get_one(search_fields)

    # Assertions
    assert result is None
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_admin_failure(admin_repository, session_mock):
    # Prepare test data
    input_data = {"name": "Test Admin", "email": "test@example.com"}

    # Mock the execute result to return None
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await admin_repository.create(input_data)

    # Assertions
    assert result is None
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_one_admin_not_found(admin_repository, session_mock):
    # Prepare test data
    admin_id = str(UUID("12345678-1234-5678-1234-567812345678"))
    update_data = {"name": "Updated Admin"}

    # Mock the execute result to return None
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await admin_repository.update_one(admin_id, update_data)

    # Assertions
    assert result is None
    session_mock.execute.assert_called_once()
