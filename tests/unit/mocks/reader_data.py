from datetime import datetime
from uuid import UUID


READER_DATA = {
    "id": UUID("12345678-1234-5678-1234-567812345678"),
    "name": "John Doe",
    "email": "john@example.com",
    "birthday": datetime(1990, 1, 1),
    "books_read_count": 5,
    "created_at": datetime(2024, 1, 1),
    "updated_at": datetime(2024, 1, 1),
}
