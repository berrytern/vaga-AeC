from typing import Tuple, Dict, Any
from src.application.domain.models import (
    CreateReaderModel,
    UpdateReaderModel,
    ReaderQueryModel,
)
from src.application.port import ReaderInterface
from src.application.services import ReaderService


class ReaderController:
    def __init__(self, service: ReaderService):
        self.service = service

    async def create(
        self, reader: CreateReaderModel
    ) -> Tuple[ReaderInterface, int, Dict[str, Any]]:
        result = await self.service.create(reader)
        return result, 201, {}

    async def get_one(self, reader_id: str):
        result = await self.service.get_one(reader_id)
        return result, 200, {}

    async def get_all(self, query: ReaderQueryModel):
        result = await self.service.get_all(query)
        return result, 200, {}

    async def update_one(self, reader_id: str, reader: UpdateReaderModel):
        result = await self.service.update_one(reader_id, reader)
        return result, 200, {}

    async def delete_one(self, reader_id: str):
        await self.service.delete_one(reader_id)
        return None, 204, {}
