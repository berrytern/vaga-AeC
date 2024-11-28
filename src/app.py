from src.application.utils import UserTypes
from src.infrastructure.database.connection import init_models, get_db
from src.infrastructure.repositories import AuthRepository
from src.main.routes import AUTH_ROUTER
from src.utils import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import bcrypt


app = FastAPI(
    title="Book Store API",
    version="1.0",
    description="A simple CRUD API for managing books in a bookstore.",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(AUTH_ROUTER, prefix="/auth", tags=["auth"])


# This is a context manager that will run before the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    from asyncio import sleep

    try_count, retry = 0, 5
    # Try to initialize the models
    while True:
        try:
            await init_models()
            break
        except BaseException:
            if try_count >= retry:
                break
            try_count += 1
            await sleep(try_count**2)
    # Create the admin user if it does not exist
    async with get_db() as session:
        repo = AuthRepository(session)
        print("on admin creation", flush=True)
        if not await repo.get_one_by_username(settings.ADMIN_USERNAME):
            password = bcrypt.hashpw(
                settings.ADMIN_PASSWORD.encode(), bcrypt.gensalt(13)
            ).decode()
            await repo.create(
                {
                    "username": settings.ADMIN_USERNAME,
                    "password": password,
                    "user_type": UserTypes.ADMIN.value,
                }
            )
    yield


# Set the lifespan context
app.router.lifespan_context = lifespan
