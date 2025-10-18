from src.application.domain.models import (
    CreateBookModel,
    UpdateBookModel,
    BookQueryModel,
)
from src.application.services import BookService
from uuid import UUID


class BookController:
    def __init__(self, service: BookService):
        self.service = service

    async def create(self, book: CreateBookModel):
        result = await self.service.create(book)
        return result, 201, {}

    async def get_one(self, book_id: UUID):
        result = await self.service.get_one(book_id)
        return result, 200, {}

    async def get_all(self, query: BookQueryModel):
        result, total_count = await self.service.get_all(query)
        return result, 200, {"X-Total-Count": str(total_count)}

    async def update_one(self, book_id: UUID, book: UpdateBookModel):
        result = await self.service.update_one(book_id, book)
        return result, 200, {}

    async def delete_one(self, book_id: UUID):
        await self.service.delete_one(book_id)
        return None, 204, {}
