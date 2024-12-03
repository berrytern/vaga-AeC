from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    CreateBookModel,
    UpdateBookModel,
    BookModel,
    BookQueryModel,
    BookList,
)
from src.application.services import BookService
from src.infrastructure.repositories import BookRepository
from src.presenters.controllers import BookController
from src.main.middlewares import auth_middleware, session_middleware

BOOK_ROUTER = APIRouter()


@BOOK_ROUTER.post("/", response_model=BookModel)
@auth_middleware("bk:c")
@session_middleware
async def create_new_book(request: Request, book: CreateBookModel):
    repository = BookRepository(request.state.db_session)
    service = BookService(repository)
    response = await BookController(service).create(book)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.get("/", response_model=BookList)
@auth_middleware("bk:ra")
@session_middleware
async def get_all_books(request: Request):
    query_params = dict(request.query_params)
    query = BookQueryModel(**query_params).query_dict()

    repository = BookRepository(request.state.db_session)
    service = BookService(repository)
    response = await BookController(service).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.get("/{book_id}", response_model=BookModel)
@auth_middleware("bk:r")
@session_middleware
async def get_one_book(request: Request, book_id: str):
    repository = BookRepository(request.state.db_session)
    service = BookService(repository)
    response = await BookController(service).get_one(book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.put("/{book_id}", response_model=BookModel)
@auth_middleware("bk:u")
@session_middleware
async def update_book_info(request: Request, book_id: str, book: UpdateBookModel):
    repository = BookRepository(request.state.db_session)
    service = BookService(repository)
    response = await BookController(service).update_one(book_id, book)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@BOOK_ROUTER.delete("/{book_id}", response_model=bool)
@auth_middleware("bk:d")
@session_middleware
async def delete_book_info(request: Request, book_id: str):
    repository = BookRepository(request.state.db_session)
    service = BookService(repository)
    response = await BookController(service).delete_one(book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
