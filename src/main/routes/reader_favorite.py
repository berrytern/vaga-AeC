from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    FavoriteModel,
    FavoriteList,
    FavoriteQueryModel,
)
from src.di import DI
from src.main.middlewares import (
    auth_middleware,
    cache_middleware,
    rate_limit_middleware,
    session_middleware,
)
from uuid import UUID

READER_FAVORITE_ROUTER = APIRouter()


@READER_FAVORITE_ROUTER.post(
    "/{reader_id}/favorites/{book_id}", response_model=FavoriteModel
)
@rate_limit_middleware(5, 60)
@auth_middleware("bkf:c", "reader_id")
@session_middleware
async def set_book_as_favorite(request: Request, reader_id: UUID, book_id: UUID):
    response = await DI.reader_favorite_controller(request.state.db_session).create(
        reader_id, book_id
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_FAVORITE_ROUTER.get("/{reader_id}/favorites", response_model=FavoriteList)
@rate_limit_middleware(5, 60)
@auth_middleware("bkf:r", "reader_id")
@cache_middleware(5)
@session_middleware
async def get_all_favorite_books_of_reader(request: Request, reader_id: UUID):
    query_params = dict(request.query_params)
    query = FavoriteQueryModel(**{**query_params, "reader_id": reader_id}).query_dict()

    response = await DI.reader_favorite_controller(request.state.db_session).get_all(
        query
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_FAVORITE_ROUTER.get(
    "/{reader_id}/favorites/{book_id}", response_model=FavoriteModel
)
@rate_limit_middleware(5, 60)
@auth_middleware("bkf:r", "reader_id")
@cache_middleware(5)
@session_middleware
async def get_one_favorite_book_of_reader(
    request: Request, reader_id: UUID, book_id: UUID
):

    response = await DI.reader_favorite_controller(request.state.db_session).get_one(
        reader_id, book_id
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_FAVORITE_ROUTER.delete("/{reader_id}/favorites/{book_id}", response_model=None)
@rate_limit_middleware(5, 60)
@auth_middleware("bkf:d", "reader_id")
@session_middleware
async def delete_one_favorite_book_of_reader(
    request: Request, reader_id: UUID, book_id: UUID
):

    response = await DI.reader_favorite_controller(request.state.db_session).delete_one(
        reader_id, book_id
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
