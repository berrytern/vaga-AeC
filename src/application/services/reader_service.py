from typing import Optional, Dict, List, Any
from src.application.domain.models import (
    AuthModel,
    ReaderQueryModel,
    UpdateReaderModel,
    CreateReaderModel,
)
from src.application.domain.utils import UserTypes
from src.application.port import ReaderInterface
from src.infrastructure.repositories import AuthRepository, ReaderRepository
import bcrypt


class ReaderService:
    def __init__(self, repository: ReaderRepository, auth_repository: AuthRepository):
        self.repository = repository
        self.auth_repository = auth_repository

    async def create(self, reader: CreateReaderModel) -> ReaderInterface:
        result = await self.repository.create(
            reader.model_dump(
                exclude_none=True,
                exclude={"id", "username", "password", "email"},
            )
        )
        reader.password = bcrypt.hashpw(
            reader.password.encode(), bcrypt.gensalt(13)
        ).decode()
        auth = AuthModel(
            **{
                **reader.model_dump(exclude_none=True, exclude={"id"}),
                **{
                    "user_type": UserTypes.READER.value,
                    "refresh_token": None,
                    "last_login": None,
                    "foreign_id": str(result["id"]),
                },
            }
        )

        await self.auth_repository.create(auth.model_dump(exclude_none=True))
        return result

    async def get_one(self, reader_id: str):
        return await self.repository.get_one({"id": reader_id})

    async def get_all(self, query: ReaderQueryModel) -> List[Dict[str, Any]]:
        return await self.repository.get_all(query)

    async def update_one(
        self, reader_id: str, reader: UpdateReaderModel
    ) -> Optional[Any]:
        return await self.repository.update_one(
            reader_id, reader.model_dump(exclude_none=True)
        )

    async def delete_one(self, reader_id: str) -> None:
        await self.repository.delete_one(reader_id)
