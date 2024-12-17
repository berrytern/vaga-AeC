from typing import Optional, Dict, List, Any
from src.application.domain.models import (
    AuthModel,
    AdminQueryModel,
    UpdateAdminModel,
    CreateAdminModel,
)
from src.application.domain.utils import UserTypes
from src.infrastructure.repositories import AuthRepository, AdminRepository
import bcrypt


class AdminService:
    def __init__(
        self, repository: AdminRepository, auth_repository: AuthRepository
    ) -> None:
        self.repository = repository
        self.auth_repository = auth_repository

    async def create(self, admin: CreateAdminModel) -> Dict[str, Any]:
        result = await self.repository.create(
            admin.model_dump(
                exclude_none=True,
                exclude={"id", "username", "password", "email"},
            )
        )
        admin.password = bcrypt.hashpw(
            admin.password.encode(), bcrypt.gensalt(13)
        ).decode()
        auth = AuthModel(
            **{
                **admin.model_dump(exclude_none=True, exclude={"id"}),
                **{
                    "user_type": UserTypes.ADMIN.value,
                    "refresh_token": None,
                    "last_login": None,
                    "foreign_id": str(result["id"]),
                },
            }
        )

        await self.auth_repository.create(auth.model_dump(exclude_none=True))
        return result

    async def get_one(self, admin_id: str):
        return await self.repository.get_one({"id": admin_id})

    async def get_all(self, query: AdminQueryModel) -> List[Dict[str, Any]]:
        return await self.repository.get_all(query)

    async def update_one(self, admin_id: str, admin: UpdateAdminModel) -> Optional[Any]:
        return await self.repository.update_one(
            admin_id, admin.model_dump(exclude_none=True)
        )

    async def delete_one(self, admin_id: str) -> None:
        await self.repository.delete_one(admin_id)
