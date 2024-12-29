from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    CreateReaderModel,
    UpdateReaderModel,
    ReaderModel,
    ReaderQueryModel,
    ReaderList,
)
from src.di import DI
from src.main.middlewares import (
    authenticate_middleware,
    cache_middleware,
    rate_limit_middleware,
    session_middleware,
)
from uuid import UUID

READER_ROUTER = APIRouter()


@READER_ROUTER.post("/", response_model=ReaderModel)
@rate_limit_middleware(5, 60)
@authenticate_middleware("rd:c")
@session_middleware
async def create_new_reader(request: Request, reader: CreateReaderModel):
    response = await DI.reader_controller(request.state.db_session).create(reader)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.get("/", response_model=ReaderList)
@rate_limit_middleware(5, 60)
@authenticate_middleware("rd:ra")
@cache_middleware(5)
@session_middleware
async def get_all_readers(request: Request):
    query_params = dict(request.query_params)
    query = ReaderQueryModel(**query_params).query_dict()

    response = await DI.reader_controller(request.state.db_session).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.get("/{reader_id}", response_model=ReaderModel)
@rate_limit_middleware(5, 60)
@authenticate_middleware("rd:r", "reader_id")
@cache_middleware(5)
@session_middleware
async def get_one_reader(request: Request, reader_id: UUID):
    response = await DI.reader_controller(request.state.db_session).get_one(reader_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.put("/{reader_id}", response_model=ReaderModel)
@rate_limit_middleware(5, 60)
@authenticate_middleware("rd:u", "reader_id")
@session_middleware
async def update_reader_info(
    request: Request, reader_id: UUID, reader: UpdateReaderModel
):
    response = await DI.reader_controller(request.state.db_session).update_one(
        reader_id, reader
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.delete("/{reader_id}", response_model=bool)
@rate_limit_middleware(5, 60)
@authenticate_middleware("rd:d", "reader_id")
@session_middleware
async def delete_reader_info(request: Request, reader_id: UUID):
    response = await DI.reader_controller(request.state.db_session).delete_one(
        reader_id
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
