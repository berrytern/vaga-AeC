from src.infrastructure.database.connection import get_session
from src.di import DI_CONTAINER
from src.background.tasks import CreateDefaultAdminTask
from src.utils.default import db_session_var
from src.utils.logger import logger
from asyncio import run


async def first_setup():
    async with get_session() as session:
        token = db_session_var.set(session)
        repository = DI_CONTAINER.repositories.auth_repository()
        await CreateDefaultAdminTask(repository, logger.background_logger).run()
        await session.commit()
        db_session_var.reset(token)


run(first_setup())
