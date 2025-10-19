from typing import cast
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
from src.infrastructure.email import EmailClient
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
from src.utils import settings, logger
from dependency_injector import containers, providers


class RepositoryContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    auth_repository = providers.Singleton(AuthRepository)
    admin_repository = providers.Singleton(
        AdminRepository,
        schema=AdminSchema,
        model=AdminModel,
        list_model=AdminList,
    )
    book_repository = providers.Singleton(
        BookRepository,
        schema=BookSchema,
        model=BookModel,
        list_model=BookList,
    )
    reader_repository = providers.Singleton(
        ReaderRepository,
        schema=ReaderSchema,
        model=ReaderModel,
        list_model=ReaderList,
    )
    favorite_repository = providers.Singleton(
        FavoriteRepository,
        schema=FavoriteBookSchema,
        model=FavoriteModel,
        list_model=FavoriteList,
    )


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = cast(RepositoryContainer, providers.DependenciesContainer())

    auth_service = providers.Singleton(
        AuthService,
        repository=repositories.auth_repository,
        email_client=EmailClient(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
        ),
    )
    admin_service = providers.Singleton(
        AdminService,
        repository=repositories.admin_repository,
        auth_repository=repositories.auth_repository,
    )
    book_service = providers.Singleton(
        BookService, repository=repositories.book_repository
    )
    reader_service = providers.Singleton(
        ReaderService,
        repository=repositories.reader_repository,
        auth_repository=repositories.auth_repository,
    )
    favorite_service = providers.Singleton(
        FavoriteService,
        repository=repositories.favorite_repository,
    )


class ControllerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    services = cast(ServiceContainer, providers.DependenciesContainer())

    auth_controller = providers.Singleton(
        AuthController,
        service=services.auth_service,
    )
    admin_controller = providers.Singleton(
        AdminController,
        service=services.admin_service,
    )
    book_controller = providers.Singleton(
        BookController,
        service=services.book_service,
    )
    reader_controller = providers.Singleton(
        ReaderController,
        service=services.reader_service,
    )
    favorite_controller = providers.Singleton(
        FavoriteController,
        service=services.favorite_service,
    )


class LoggerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Singleton(logger.Logger)


class IoC:
    config = providers.Configuration("config")
    logger = providers.Container(LoggerContainer)
    repositories = RepositoryContainer()
    services = ServiceContainer(repositories=repositories)
    controllers = ControllerContainer(services=services)


DI_CONTAINER = IoC()
