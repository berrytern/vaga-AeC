from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.domain.models import (
    CreateAdminModel,
    UpdateAdminModel,
    AdminModel,
    AdminQueryModel,
    AdminList,
)
from src.application.services import AdminService
from src.infrastructure.database.schemas import AdminSchema
from src.infrastructure.repositories import AdminRepository, AuthRepository
from src.presenters.controllers import AdminController
from src.main.middlewares import (
    auth_middleware,
    cache_middleware,
    CORSMiddleware,
    rate_limit_middleware,
    session_middleware,
)
from uuid import UUID

ADMIN_ROUTER = APIRouter()

router_cors = CORSMiddleware(ADMIN_ROUTER, "*")


@(
    router_cors.set_path("login")
    .allow_headers("Content-Type", "Authorization")
    .post(response_model=AdminModel)
)
@rate_limit_middleware(2, 60)
@auth_middleware("ad:c")
@session_middleware
async def create_new_admin(request: Request, admin: CreateAdminModel):
    repository = AdminRepository(
        AdminSchema, AdminModel, AdminList
    )
    auth_repository = AuthRepository()
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).create(admin)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("")
    .allow_headers("Content-Type", "Authorization")
    .get(response_model=AdminList)
)
@rate_limit_middleware(2, 60)
@auth_middleware("ad:ra")
@cache_middleware(5)
@session_middleware
async def get_all_admins(request: Request):
    query_params = dict(request.query_params)
    query = AdminQueryModel(**query_params).query_dict()

    repository = AdminRepository(
        AdminSchema, AdminModel, AdminList
    )
    auth_repository = AuthRepository()
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("{admin_id}")
    .allow_headers("Content-Type", "Authorization")
    .get(response_model=AdminModel)
)
@rate_limit_middleware(5, 60)
@auth_middleware("ad:r")
@cache_middleware(5)
@session_middleware
async def get_one_admin(request: Request, admin_id: UUID):
    repository = AdminRepository(
        AdminSchema, AdminModel, AdminList
    )
    auth_repository = AuthRepository()
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).get_one(admin_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("{admin_id}")
    .allow_headers("Content-Type", "Authorization")
    .put(response_model=AdminModel)
)
@rate_limit_middleware(2, 60)
@auth_middleware("ad:u")
@session_middleware
async def update_admin_info(request: Request, admin_id: UUID, admin: UpdateAdminModel):
    repository = AdminRepository(
        AdminSchema, AdminModel, AdminList
    )
    auth_repository = AuthRepository()
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).update_one(admin_id, admin)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@(
    router_cors.set_path("{admin_id}")
    .allow_headers("Content-Type", "Authorization")
    .delete(response_model=bool)
)
@rate_limit_middleware(2, 60)
@auth_middleware("ad:d")
@session_middleware
async def delete_admin_info(request: Request, admin_id: UUID):
    repository = AdminRepository(
        AdminSchema, AdminModel, AdminList
    )
    auth_repository = AuthRepository()
    service = AdminService(repository, auth_repository)
    response = await AdminController(service).delete_one(admin_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
