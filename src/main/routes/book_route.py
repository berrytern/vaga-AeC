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
    rate_limit_middleware,
    session_middleware,
)

BOOK_ROUTER = APIRouter()


@BOOK_ROUTER.post("/", response_model=BookModel)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:c")
@session_middleware
async def create_new_book(request: Request, book: CreateBookModel):
    response = await DI.book_controller(request.state.db_session).create(book)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.get("/", response_model=BookList)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:ra")
@cache_middleware(5)
@session_middleware
async def get_all_books(request: Request):
    query_params = dict(request.query_params)
    query = BookQueryModel(**query_params).query_dict()

    response = await DI.book_controller(request.state.db_session).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.get("/{book_id}", response_model=BookModel)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:r")
@cache_middleware(5)
@session_middleware
async def get_one_book(request: Request, book_id: str):
    response = await DI.book_controller(request.state.db_session).get_one(book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.put("/{book_id}", response_model=BookModel)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:u")
@session_middleware
async def update_book_info(request: Request, book_id: str, book: UpdateBookModel):
    response = await DI.book_controller(request.state.db_session).update_one(
        book_id, book
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.delete("/{book_id}", response_model=bool)
@rate_limit_middleware(5, 60)
@auth_middleware("bk:d")
@session_middleware
async def delete_book_info(request: Request, book_id: str):
    response = await DI.book_controller(request.state.db_session).delete_one(book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
