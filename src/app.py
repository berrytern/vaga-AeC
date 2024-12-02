from src.background.tasks import CreateDefaultAdminTask
from src.infrastructure.database.connection import init_models, get_db
from src.infrastructure.repositories import AuthRepository
from src.presenters.exceptions.api_exception_manager import APIExceptionManager
from src.main.routes import ADMIN_ROUTER, AUTH_ROUTER
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

app.include_router(AUTH_ROUTER, prefix="/auth", tags=["auth"])
app.include_router(ADMIN_ROUTER, prefix="/admins", tags=["auth"])


# This is a context manager that will run before the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # use Background service layer if it grows in complexity
    from asyncio import sleep

    retry = 5
    # Try to initialize the models
    for try_count in range(1, retry + 1):
        try:
            await init_models()
            break
        except BaseException:
            await sleep(try_count**2)
    # Create the admin user if it does not exist
    async with get_db() as session:
        repository = AuthRepository(session)
        await CreateDefaultAdminTask(repository, logger.background_logger).run()
    yield


# Set the lifespan context
app.router.lifespan_context = lifespan

# Register the error handling
APIExceptionManager.register_error_handling(app)
