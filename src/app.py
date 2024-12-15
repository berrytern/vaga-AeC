from src.background.tasks import CreateDefaultAdminTask
from src.infrastructure.database.connection import init_models, get_db
from src.infrastructure.repositories import AuthRepository
from src.presenters.exceptions.api_exception_manager import APIExceptionManager
from src.main.middlewares import register_track_middleware
from src.main.routes import (
    ADMIN_ROUTER,
    AUTH_ROUTER,
    BOOK_ROUTER,
    READER_FAVORITE_ROUTER,
    READER_ROUTER,
)
from src.utils import settings
from src.utils.logger import logger
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager


http_app = FastAPI(
    title="Proxy API",
    version="1.0",
    description="Redirects to book store API.",
)

https_app = FastAPI(
    title="Book Store API",
    version="1.0",
    description="A simple CRUD API for managing books in a bookstore.",
)


@http_app.middleware("http")
async def redirect_to_https(request: Request, _):
    url = request.url.replace(scheme="https", port=settings.HTTPS_PORT)
    return RedirectResponse(
        url=url,
        status_code=301,  # Permanent redirect
    )


# Add the CORS middleware if needed
https_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
# register the track middleware | It can be used to get the graphic of the requests using prometheus + grafana
register_track_middleware(https_app)

https_app.include_router(AUTH_ROUTER, prefix="/v1/auth", tags=["auth"])
https_app.include_router(ADMIN_ROUTER, prefix="/v1/admins", tags=["admin"])
https_app.include_router(
    READER_FAVORITE_ROUTER, prefix="/v1/readers", tags=["reader-favorite"]
)
https_app.include_router(READER_ROUTER, prefix="/v1/readers", tags=["reader"])
https_app.include_router(BOOK_ROUTER, prefix="/v1/books", tags=["book"])


# This is a context manager that will run before the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # use Background service layer if it grows in complexity
    await init_models()
    # Create the admin user if it does not exist
    async with get_db() as session:
        repository = AuthRepository(session)
        await CreateDefaultAdminTask(repository, logger.background_logger).run()
        await session.commit()
    yield


# Set the lifespan context
https_app.router.lifespan_context = lifespan

# Register the error handling
APIExceptionManager.register_error_handling(https_app)
