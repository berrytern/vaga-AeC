from src.application.utils import UserTypes
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories import AuthRepository
from src.utils import settings
import bcrypt


class CreateDefaultAdminTask:
    @staticmethod
    async def run():
        async with get_db() as session:
            repo = AuthRepository(session)
            print("on admin creation", flush=True)
            if not await repo.get_one_by_username(settings.ADMIN_USERNAME):
                try:
                    password = bcrypt.hashpw(
                        settings.ADMIN_PASSWORD.encode(), bcrypt.gensalt(13)
                    ).decode()
                    await repo.create(
                        {
                            "username": settings.ADMIN_USERNAME,
                            "password": password,
                            "user_type": UserTypes.ADMIN.value,
                        }
                    )
                except BaseException as err:
                    print(
                        f"An Error occourred while creating the admin user: {err}",
                        flush=True,
                    )
