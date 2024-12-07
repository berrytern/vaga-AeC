from src.application.domain.models import (
    AdminModel,
    AdminList,
    BookModel,
    BookList,
    FavoriteModel,
    FavoriteList,
    ReaderModel,
    ReaderList,
)
from src.application.services import (
    AuthService,
    AdminService,
    BookService,
    FavoriteService,
    ReaderService,
)
from src.infrastructure.database.schemas import (
    AdminSchema,
    BookSchema,
    FavoriteBookSchema,
    ReaderSchema,
)
from src.infrastructure.repositories import (
    AuthRepository,
    AdminRepository,
    BookRepository,
    FavoriteRepository,
    ReaderRepository,
)
from src.presenters.controllers import (
    AuthController,
    AdminController,
    BookController,
    ReaderController,
    FavoriteController,
)


class DI:
    @classmethod
    def auth_controller(cls, db_session) -> AuthController:
        repository = AuthRepository(db_session)
        service = AuthService(repository)
        return AuthController(service)

    @classmethod
    def admin_controller(cls, db_session) -> AdminController:
        repository = AdminRepository(db_session, AdminSchema, AdminModel, AdminList)
        auth_repository = AuthRepository(db_session)
        service = AdminService(repository, auth_repository)
        return AdminController(service)

    @classmethod
    def book_controller(cls, db_session) -> BookController:
        repository = BookRepository(db_session, BookSchema, BookModel, BookList)
        service = BookService(repository)
        return BookController(service)

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
