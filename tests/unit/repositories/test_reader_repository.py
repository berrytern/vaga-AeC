import pytest
from unittest.mock import AsyncMock, Mock, MagicMock
from src.infrastructure.repositories import ReaderRepository
from tests.unit.mocks.reader_data import READER_DATA
from uuid import UUID


@pytest.mark.asyncio
async def test_reader_repository_initialization(session_mock):
    schema, model, list_model = Mock(), Mock(), Mock()
    repository = ReaderRepository(
        session=session_mock, schema=schema, model=model, list_model=list_model
    )

    assert repository.session == session_mock
    assert repository.schema == schema
    assert repository.model == model
    assert repository.list_model == list_model


@pytest.mark.asyncio
async def test_create_reader(reader_repository, session_mock):
    # Prepare test data
    input_data = {
        "name": READER_DATA["name"],
        "birthday": READER_DATA["birthday"],
        "books_read_count": READER_DATA["books_read_count"],
    }

    # Mock the execute result
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (
        READER_DATA["id"],
        READER_DATA["name"],
        READER_DATA["birthday"],
        READER_DATA["books_read_count"],
        READER_DATA["created_at"],
        READER_DATA["updated_at"],
    )
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await reader_repository.create(input_data)

    # Assertions
    assert result is not None
    assert isinstance(result, dict)
    assert result["id"] == str(READER_DATA["id"])
    assert result["name"] == READER_DATA["name"]
    assert (
        result["created_at"]
        == READER_DATA["created_at"].replace(microsecond=0).isoformat() + "Z"
    )
    assert (
        result["updated_at"]
        == READER_DATA["updated_at"].replace(microsecond=0).isoformat() + "Z"
    )
    session_mock.execute.assert_called_once()
    mock_result.fetchone.assert_called_once()


@pytest.mark.asyncio
async def test_get_one_reader(reader_repository, session_mock):
    # Prepare test data
    search_fields = {"id": READER_DATA["id"]}

    # Mock the execute result
    mock_result = MagicMock()
    mock_schema = MagicMock()
    for key, value in READER_DATA.items():
        setattr(mock_schema, key, value)
    mock_result.fetchone.return_value = (mock_schema,)
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await reader_repository.get_one(search_fields)

    # Assertions
    assert result is not None
    assert isinstance(result, dict)
    assert result["id"] == str(READER_DATA["id"])
    assert result["name"] == READER_DATA["name"]
    assert (
        result["created_at"]
        == READER_DATA["created_at"].replace(microsecond=0).isoformat() + "Z"
    )
    assert (
        result["updated_at"]
        == READER_DATA["updated_at"].replace(microsecond=0).isoformat() + "Z"
    )
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_readers(reader_repository, session_mock):
    # Prepare test data
    filters = {"query": {}, "limit": 10}

    # Mock the stream_scalars result
    mock_schema = MagicMock()
    for key, value in READER_DATA.items():
        setattr(mock_schema, key, value)

    async def mock_stream():
        yield mock_schema

    session_mock.stream_scalars.return_value = mock_stream()

    # Execute the method
    result = await reader_repository.get_all(filters)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == str(READER_DATA["id"])
    assert result[0]["name"] == READER_DATA["name"]
    assert (
        result[0]["created_at"]
        == READER_DATA["created_at"].replace(microsecond=0).isoformat() + "Z"
    )
    assert (
        result[0]["updated_at"]
        == READER_DATA["updated_at"].replace(microsecond=0).isoformat() + "Z"
    )
    session_mock.stream_scalars.assert_called_once()


@pytest.mark.asyncio
async def test_update_one_reader(reader_repository, session_mock):
    # Prepare test data
    reader_id = str(READER_DATA["id"])
    update_data = {"name": "Jane Doe"}

    # Mock the execute result
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (
        READER_DATA["id"],
        "Jane Doe",
        READER_DATA["birthday"],
        READER_DATA["books_read_count"],
        READER_DATA["created_at"],
        READER_DATA["updated_at"],
    )
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await reader_repository.update_one(reader_id, update_data)

    # Assertions
    assert result["id"] == str(READER_DATA["id"])
    assert result["name"] == "Jane Doe"
    assert (
        result["created_at"]
        == READER_DATA["created_at"].replace(microsecond=0).isoformat() + "Z"
    )
    assert (
        result["updated_at"]
        == READER_DATA["updated_at"].replace(microsecond=0).isoformat() + "Z"
    )
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_books_read_count(reader_repository, session_mock):
    # Prepare test data
    reader_id = str(READER_DATA["id"])
    count_increment = 1

    # Mock the execute result
    mock_result = MagicMock()
    updated_count = READER_DATA["books_read_count"] + count_increment
    mock_result.fetchone.return_value = (
        READER_DATA["id"],
        READER_DATA["name"],
        READER_DATA["birthday"],
        updated_count,
        READER_DATA["created_at"],
        READER_DATA["updated_at"],
    )
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await reader_repository.update_books_read_count(reader_id, count_increment)

    # Assertions
    assert result is not None
    assert isinstance(result, dict)
    assert result["id"] == str(READER_DATA["id"])
    assert result["books_read_count"] == updated_count
    assert (
        result["created_at"]
        == READER_DATA["created_at"].replace(microsecond=0).isoformat() + "Z"
    )
    assert (
        result["updated_at"]
        == READER_DATA["updated_at"].replace(microsecond=0).isoformat() + "Z"
    )
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_delete_one_reader(
    reader_repository: ReaderRepository, session_mock: AsyncMock
):
    # Prepare test data
    reader_id = str(READER_DATA["id"])

    # Execute the method
    result = await reader_repository.delete_one(reader_id)

    # Assertions
    assert result is None
    session_mock.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_one_reader_not_found(reader_repository, session_mock):
    # Prepare test data
    search_fields = {"id": UUID("12345678-1234-5678-1234-567812345678")}

    # Mock the execute result to return None
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None
    session_mock.execute.return_value = mock_result

    # Execute the method
    result = await reader_repository.get_one(search_fields)

    # Assertions
    assert result is None
    session_mock.execute.assert_called_once()
