from src.application.domain.models import (
    CredentialModel,
    RefreshCredentialModel,
    RevokeCredentialModel,
    ResetCredentialModel,
    RecoverRequestModel,
    RecoverPasswordModel,
)
from src.application.services import AuthService
from src.di import DI
from src.infrastructure.cache import RedisClient
from src.main.middlewares import (
    auth_middleware,
    rate_limit_middleware,
    session_middleware,
)
from src.utils import settings
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from uuid import UUID


AUTH_ROUTER = APIRouter()

templates = Jinja2Templates(directory="templates")


@AUTH_ROUTER.post("/login", response_model=RefreshCredentialModel)
@rate_limit_middleware(5, 5 * 60)
@session_middleware
async def login(request: Request, data: CredentialModel):
    response = await DI.auth_controller(request.state.db_session).login(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/refresh-token", response_model=RefreshCredentialModel)
@rate_limit_middleware(2, 10 * 60)
@session_middleware
async def refresh_token(request: Request, data: RefreshCredentialModel):
    response = await DI.auth_controller(request.state.db_session).refresh_token(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/revoke-token")
@rate_limit_middleware(2, 60)
async def revoke_token(data: RevokeCredentialModel):
    if await RedisClient.get(data.access_token):
        return JSONResponse(
            "Token was already revoked",
        )
    payload = AuthService.decode_token(data.access_token)
    remaining_time = payload["exp"] - datetime.utcnow().timestamp()
    await RedisClient.setex(data.access_token, int(remaining_time), "true")
    return JSONResponse("Token has been revoked")


@AUTH_ROUTER.post("/users/{user_id}/change-password")
@auth_middleware(None, "user_id")
@rate_limit_middleware(2, 5 * 60)
async def change_password(request: Request, data: ResetCredentialModel, user_id: UUID):
    response = await DI.auth_controller(request.state.db_session).change_password(
        data, user_id
    )
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/password/reset-request")
@rate_limit_middleware(1, 10 * 60)
@session_middleware
async def request_password_reset(request: Request, data: RecoverRequestModel):
    response = await DI.auth_controller(
        request.state.db_session
    ).request_password_reset(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/password/reset")
@rate_limit_middleware(1, 60)
@session_middleware
async def reset_password(request: Request, data: RecoverPasswordModel):
    response = await DI.auth_controller(request.state.db_session).reset_password(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.get(
    "/password/username/{username}/hash/{hash}", response_class=HTMLResponse
)
@rate_limit_middleware(2, settings.RESET_PASSWD_EXP)
async def get_password_reset_page(request: Request, username: str, hash: str):
    return templates.TemplateResponse(
        request=request,
        name="reset_password.html",
        context={"username": username, "hash": hash},
    )


@AUTH_ROUTER.get("/password/reset/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse(request=request, name="reset_success.html")
