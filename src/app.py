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
from src.utils.logger import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


app = FastAPI(
    title="Book Store API",
    version="1.0",
    description="A simple CRUD API for managing books in a bookstore.",
)


# Add the CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
# register the track middleware | It can be used to get the graphic of the requests using prometheus + grafana
register_track_middleware(app)

app.include_router(AUTH_ROUTER, prefix="/auth", tags=["auth"])
app.include_router(ADMIN_ROUTER, prefix="/admins", tags=["admin"])
app.include_router(READER_FAVORITE_ROUTER, prefix="/readers", tags=["reader-favorite"])
app.include_router(READER_ROUTER, prefix="/readers", tags=["reader"])
app.include_router(BOOK_ROUTER, prefix="/books", tags=["book"])


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
app.router.lifespan_context = lifespan

# Register the error handling
APIExceptionManager.register_error_handling(app)
