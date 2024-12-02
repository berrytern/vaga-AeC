from src.application.domain.utils import UserTypes
from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories import AuthRepository
from src.utils.logger import logger
from src.utils import settings
import bcrypt


class CreateDefaultAdminTask:
    @staticmethod
    async def run():
        logger.background_logger.debug("Create default Administrator task started")
        try:
            async with get_db() as session:
                repo = AuthRepository(session)
                if not await repo.get_one_by_username(settings.ADMIN_USERNAME):
                    password = bcrypt.hashpw(
                        settings.ADMIN_PASSWORD.encode(),
                        bcrypt.gensalt(settings.PASSWORD_SALT_ROUNDS),
                    ).decode()
                    await repo.create(
                        {
                            "username": settings.ADMIN_USERNAME,
                            "password": password,
                            "user_type": UserTypes.ADMIN.value,
                        }
                    )
                    logger.background_logger.info(
                        "Administrator account created successfully"
                    )
        except BaseException:
            logger.background_logger.exception(
                "An Error occourred while creating the admin user"
            )
