from .base_task import BaseTask
from src.application.domain.utils import UserTypes
from src.infrastructure.repositories import AuthRepository
from src.utils.logger import logger
from src.utils import settings
from logging import Logger
import bcrypt


class CreateDefaultAdminTask(BaseTask):
    def __init__(self, repository: AuthRepository, logger: Logger) -> None:
        self.repository = repository
        self.logger = logger

    async def run(self):
        self.logger.debug("Create default Administrator task started")
        try:
            if not await self.repository.get_one({"user_type": UserTypes.ADMIN.value}):
                password = bcrypt.hashpw(
                    settings.ADMIN_PASSWORD.encode(),
                    bcrypt.gensalt(settings.PASSWORD_SALT_ROUNDS),
                ).decode()
                await self.repository.create(
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
