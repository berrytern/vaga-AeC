from src.infrastructure.database.connection import get_session
from src.infrastructure.repositories import AuthRepository
from src.background.tasks import CreateDefaultAdminTask
from src.utils.logger import logger
from asyncio import run



async def first_setup():
    async with get_session() as session:
        repository = AuthRepository(session)
        await CreateDefaultAdminTask(repository, logger.background_logger).run()
        await session.commit()

run(first_setup())