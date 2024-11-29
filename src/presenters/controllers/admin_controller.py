from src.application.models import (
    AuthModel,
    AdminQueryModel,
    AdminModel,
    CreateAdminModel,
)
from src.application.utils import UserTypes
from src.infrastructure.database import get_db
from src.infrastructure.repositories import AuthRepository, AdminRepository
import bcrypt


class AdminController:
    async def create(self, admin: CreateAdminModel):
        result = None
        async with get_db() as session:
            repo = AdminRepository(session)
            try:
                result = await repo.create(
                    admin.model_dump(
                        exclude_none=True,
                        exclude={"id", "username", "password"},
                    ),
                    commit=False,
                )
                admin.password = bcrypt.hashpw(
                    admin.password.encode(), bcrypt.gensalt(13)
                ).decode()
                auth = AuthModel(
                    **{
                        **admin.model_dump(exclude_none=True, exclude={"id"}),
                        **{
                            "user_type": UserTypes.CLIENT.value,
                            "refresh_token": None,
                            "last_login": None,
                            "foreign_id": str(result["id"]),
                        },
                    }
                )
                auth_repo = AuthRepository(session)
                await auth_repo.create(auth.model_dump(exclude_none=True), False)
                await session.commit()
                return result, 201, {}
            except BaseException:
                await session.rollback()
                return (
                    {
                        "message": "Already exist",
                        "description": "email/username already used",
                    },
                    409,
                    {},
                )

    async def get_one(self, admin_id: str):
        async with get_db() as session:
            repo = AdminRepository(session)
            return await repo.get_one({"id": admin_id}), 200, {}

    async def get_all(self, query: AdminQueryModel):
        async with get_db() as session:
            repo = AdminRepository(session)
            return (await repo.get_all(query)), 200, {}

    async def update_one(self, admin: AdminModel):
        async with get_db() as session:
            repo = AdminRepository(session)
            return (
                await repo.update_one(id, admin.model_dump(exclude_none=True)),
                200,
                {},
            )

    async def delete_one(self, admin_id: str):
        async with get_db() as session:
            repo = AdminRepository(session)
            await repo.delete_one(admin_id), 200, {}
