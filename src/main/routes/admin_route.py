from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    CreateAdminModel,
    AdminModel,
    AdminQueryModel,
    AdminList,
)
from src.application.services import AdminService
from src.infrastructure.repositories import AdminRepository, AuthRepository
from src.presenters.controllers import AdminController
from src.main.middlewares import auth_middleware, session_middleware

ADMIN_ROUTER = APIRouter()


@ADMIN_ROUTER.post("/", response_model=AdminModel)
@auth_middleware("ad:c")
@session_middleware
async def create_new_admin(request: Request, admin: CreateAdminModel):
    repository = AdminRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).create(admin)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.get("/", response_model=AdminList)
@auth_middleware("ad:ra")
@session_middleware
async def get_all_admins(request: Request):
    query_params = dict(request.query_params)
    query = AdminQueryModel(**query_params).query_dict()

    repository = AdminRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.get("/{admin_id}", response_model=AdminModel)
@auth_middleware("ad:r")
@session_middleware
async def get_one_admin(request: Request, admin_id: str):
    repository = AdminRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).get_one(admin_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.put("/{admin_id}", response_model=AdminModel)
@auth_middleware("ad:u")
@session_middleware
async def update_admin_info(request: Request, admin_id: str, admin: AdminModel):
    repository = AdminRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).update_one(admin_id, admin)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.delete("/{admin_id}", response_model=bool)
@auth_middleware("ad:d")
@session_middleware
async def delete_admin_info(request: Request, admin_id: str):
    repository = AdminRepository(request.state.db_session)
    auth_repository = AuthRepository(request.state.db_session)
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).delete_one(admin_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
