from src.application.domain.models import (
    CreateBookModel,
    UpdateBookModel,
    BookQueryModel,
)
from src.application.services import BookService


class BookController:
    def __init__(self, service: BookService):
        self.service = service

    async def create(self, book: CreateBookModel):
        result = await self.service.create(book)
        return result, 201, {}

    async def get_one(self, book_id: str):
        result = await self.service.get_one(book_id)
        return result, 200, {}

    async def get_all(self, query: BookQueryModel):
        result = await self.service.get_all(query)
        return result, 200, {}

    async def update_one(self, book_id: str, book: UpdateBookModel):
        result = await self.service.update_one(book_id, book)
        return result, 200, {}

    async def delete_one(self, book_id: str):
        await self.service.delete_one(book_id)
        return None, 204, {}
