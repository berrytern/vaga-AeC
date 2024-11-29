from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.application.models import (
    CreateAdminModel,
    AdminModel,
    AdminQueryModel,
    AdminList,
)
from src.presenters.controllers import AdminController
from src.main.middlewares import auth_middleware

ADMIN_ROUTER = APIRouter()


@ADMIN_ROUTER.post("/", response_model=AdminModel)
@auth_middleware("ad:c")
async def create_new_admin(request: Request, admin: CreateAdminModel):
    response = await AdminController().create(admin)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.get("/", response_model=AdminList)
@auth_middleware("ad:ra")
async def get_all_admins(request: Request):
    query_params = dict(request.query_params)
    query = AdminQueryModel(**query_params).query_dict()
    response = await AdminController().get_all(query)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.get("/{admin_id}", response_model=AdminModel)
@auth_middleware("ad:r")
async def get_one_admin(request: Request, admin_id: str):
    response = await AdminController().get_one(admin_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.put("/{admin_id}", response_model=AdminModel)
@auth_middleware("ad:u")
async def update_admin_info(request: Request, admin_id: str, admin: AdminModel):
    response = await AdminController().update_one(admin)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@ADMIN_ROUTER.delete("/{admin_id}", response_model=bool)
@auth_middleware("ad:d")
async def delete_admin_info(request: Request, admin_id: str):
    response = await AdminController().delete_one(admin_id)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
