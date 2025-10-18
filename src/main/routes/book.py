from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    CreateBookModel,
    UpdateBookModel,
    BookModel,
    BookQueryModel,
    BookList,
)
from src.di import DI
from src.main.middlewares import (
    auth_middleware,
    cache_middleware,
    CORSMiddleware,
    rate_limit_middleware,
    session_middleware,
)
from uuid import UUID

BOOK_ROUTER = APIRouter()

router_cors = CORSMiddleware(BOOK_ROUTER, "*")


@(
    router_cors.set_path("")
    .allow_headers("Content-Type", "Authorization")
    .post(response_model=BookModel)
)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:c")
@session_middleware
async def create_new_book(request: Request, book: CreateBookModel):
    response = await DI.book_controller().create(book)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("")
    .allow_headers("Content-Type", "Authorization")
    .get(response_model=BookList)
)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:ra")
@cache_middleware(5)
@session_middleware
async def get_all_books(request: Request):
    query_params = dict(request.query_params)
    query = BookQueryModel(**query_params).query_dict()

    response = await DI.book_controller().get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("{book_id}")
    .allow_headers("Content-Type", "Authorization")
    .get(response_model=BookModel)
)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:r")
@cache_middleware(5)
@session_middleware
async def get_one_book(request: Request, book_id: UUID):
    response = await DI.book_controller().get_one(book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("{book_id}")
    .allow_headers("Content-Type", "Authorization")
    .put(response_model=BookModel)
)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:u")
@session_middleware
async def update_book_info(request: Request, book_id: UUID, book: UpdateBookModel):
    response = await DI.book_controller().update_one(
        book_id, book
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("{book_id}")
    .allow_headers("Content-Type", "Authorization")
    .delete(response_model=bool)
)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:d")
@session_middleware
async def delete_book_info(request: Request, book_id: UUID):
    response = await DI.book_controller().delete_one(book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
