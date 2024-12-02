from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    CreateReaderModel,
    UpdateReaderModel,
    ReaderModel,
    ReaderQueryModel,
    ReaderList,
)
from src.application.services import ReaderService
from src.infrastructure.repositories import ReaderRepository, AuthRepository
from src.presenters.controllers import ReaderController
from src.main.middlewares import auth_middleware, session_middleware

READER_ROUTER = APIRouter()


@READER_ROUTER.post("/", response_model=ReaderModel)
@auth_middleware("rd:c")
@session_middleware
async def create_new_reader(request: Request, reader: CreateReaderModel):
    repository = ReaderRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = ReaderService(repository, auth_repository)
    response = await ReaderController(service).create(reader)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.get("/", response_model=ReaderList)
@auth_middleware("rd:ra")
@session_middleware
async def get_all_readers(request: Request):
    query_params = dict(request.query_params)
    query = ReaderQueryModel(**query_params).query_dict()

    repository = ReaderRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = ReaderService(repository, auth_repository)
    response = await ReaderController(service).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.get("/{reader_id}", response_model=ReaderModel)
@auth_middleware("rd:r")
@session_middleware
async def get_one_reader(request: Request, reader_id: str):
    repository = ReaderRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = ReaderService(repository, auth_repository)
    response = await ReaderController(service).get_one(reader_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.put("/{reader_id}", response_model=ReaderModel)
@auth_middleware("rd:u")
@session_middleware
async def update_reader_info(
    request: Request, reader_id: str, reader: UpdateReaderModel
):
    repository = ReaderRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = ReaderService(repository, auth_repository)
    response = await ReaderController(service).update_one(reader_id, reader)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@READER_ROUTER.delete("/{reader_id}", response_model=bool)
@auth_middleware("rd:d")
@session_middleware
async def delete_reader_info(request: Request, reader_id: str):
    repository = ReaderRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = ReaderService(repository, auth_repository)
    response = await ReaderController(service).delete_one(reader_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
