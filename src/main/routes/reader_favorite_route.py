from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    BookModel,
    FavoriteQueryModel,
    BookList,
)
from src.application.services import FavoriteService
from src.infrastructure.repositories import FavoriteRepository
from src.presenters.controllers import FavoriteController
from src.main.middlewares import auth_middleware, session_middleware

READER_FAVORITE_ROUTER = APIRouter()


@READER_FAVORITE_ROUTER.post(
    "/{reader_id}/favorites/{book_id}", response_model=BookModel
)
@auth_middleware("bkf:c")
@session_middleware
async def set_book_as_favorite(request: Request, reader_id: str, book_id: str):
    repository = FavoriteRepository(request.state.db_session)
    service = FavoriteService(repository)
    response = await FavoriteController(service).create(reader_id, book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_FAVORITE_ROUTER.get("/{reader_id}/favorites", response_model=BookList)
@auth_middleware("bkf:r")
@session_middleware
async def get_all_favorite_books_of_reader(request: Request, reader_id: str):
    query_params = dict(request.query_params)
    query = FavoriteQueryModel(**{**query_params, "reader_id": reader_id}).query_dict()

    repository = FavoriteRepository(request.state.db_session)
    service = FavoriteService(repository)
    response = await FavoriteController(service).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_FAVORITE_ROUTER.get(
    "/{reader_id}/favorites/{book_id}", response_model=BookModel
)
@auth_middleware("bkf:r")
@session_middleware
async def get_one_favorite_book_of_reader(
    request: Request, reader_id: str, book_id: str
):
    repository = FavoriteRepository(request.state.db_session)
    service = FavoriteService(repository)
    response = await FavoriteController(service).get_one(reader_id, book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_FAVORITE_ROUTER.delete("/{reader_id}/favorites/{book_id}", response_model=bool)
@auth_middleware("bkf:d")
@session_middleware
async def delete_one_favorite_book_of_reader(
    request: Request, reader_id: str, book_id: str
):
    repository = FavoriteRepository(request.state.db_session)
    service = FavoriteService(repository)
    response = await FavoriteController(service).delete_one(reader_id, book_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
