from src.application.domain.models import (
    FavoriteModel,
    FavoriteList,
    ReaderModel,
    ReaderList,
)
from src.application.services import FavoriteService, ReaderService
from src.infrastructure.database.schemas import (
    FavoriteBookSchema,
    ReaderSchema,
)
from src.infrastructure.repositories import (
    AuthRepository,
    FavoriteRepository,
    ReaderRepository,
)
from src.presenters.controllers import (
    ReaderController,
    FavoriteController,
)


class DI:
    @classmethod
    def reader_controller(cls, db_session) -> ReaderController:
        repository = ReaderRepository(db_session, ReaderSchema, ReaderModel, ReaderList)
        auth_repository = AuthRepository(db_session)
        service = ReaderService(repository, auth_repository)
        return ReaderController(service)

    @classmethod
    def reader_favorite_controller(cls, db_session) -> FavoriteController:
        reader_repository = ReaderRepository(
            db_session, ReaderSchema, ReaderModel, ReaderList
        )
        repository = FavoriteRepository(
            db_session,
            FavoriteBookSchema,
            FavoriteModel,
            FavoriteList,
            reader_repository,
        )
        service = FavoriteService(repository)
        return FavoriteController(service)
