from typing import Dict, Any, Tuple, Optional
from src.application.services import FavoriteService
from uuid import UUID


class FavoriteController:
    def __init__(self, service: FavoriteService):
        self.service = service

    async def create(
        self, reader_id: UUID, book_id: UUID
    ) -> Tuple[Dict[str, Any], int, Dict[str, Any]]:
        result = await self.service.create(reader_id, book_id)
        return result, 201, {}

    async def get_one(
        self, reader_id: UUID, book_id: UUID
    ) -> Tuple[Optional[Dict[str, Any]], int, Dict[str, Any]]:
        result = await self.service.get_one(reader_id, book_id)
        return result, 200, {}

    async def get_all(
        self, query: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], int, Dict[str, Any]]:
        result = await self.service.get_all(query)
        return result, 200, {}

    async def delete_one(
        self, reader_id: UUID, book_id: UUID
    ) -> Tuple[None, int, Dict[str, Any]]:
        await self.service.delete_one(reader_id, book_id)
        return None, 204, {}
