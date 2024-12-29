from typing import Dict, Any, Optional
from src.infrastructure.repositories import FavoriteRepository


class FavoriteService:
    def __init__(self, repository: FavoriteRepository):
        self.repository = repository

    async def create(self, reader_id: str, book_id: str) -> Optional[Dict[str, Any]]:
        return await self.repository.create(reader_id, book_id)

    async def get_one(self, reader_id: str, book_id: str) -> Optional[Dict[str, Any]]:
        return await self.repository.get_one(reader_id, book_id)

    async def get_all(self, query: Dict[str, Any]) -> Dict[str, Any]:
        return await self.repository.get_all(query)

    async def delete_one(self, reader_id: str, book_id: str) -> None:
        await self.repository.delete_one(reader_id, book_id)
