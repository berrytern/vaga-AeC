from typing import TypedDict


class ReaderInterface(TypedDict):
    id: str
    name: str
    email: str
    birthday: str
    books_read_count: int
    created_at: str
    updated_at: str
