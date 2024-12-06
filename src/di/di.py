from src.application.domain.models import ReaderModel, ReaderList
from src.application.services.reader_service import ReaderService
from src.infrastructure.database.schemas import ReaderSchema
from src.infrastructure.repositories import AuthRepository, ReaderRepository
from src.presenters.controllers.reader_controller import ReaderController


class DI:
    @classmethod
    def reader_controller(cls, db_session) -> ReaderController:
        repository = ReaderRepository(db_session, ReaderSchema, ReaderModel, ReaderList)
        auth_repository = AuthRepository(db_session)
        service = ReaderService(repository, auth_repository)
        return ReaderController(service)
