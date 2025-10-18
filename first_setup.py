from src.infrastructure.database.connection import get_session
from src.infrastructure.repositories import AuthRepository
from src.background.tasks import CreateDefaultAdminTask
from src.utils.default import db_session_var
from src.utils.logger import logger
from asyncio import run



async def first_setup():
    async with get_session() as session:
        token = db_session_var.set(session)
        repository = AuthRepository()
        await CreateDefaultAdminTask(repository, logger.background_logger).run()
        await session.commit()
        db_session_var.reset(token)

run(first_setup())