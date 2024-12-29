from src.application.domain.models import (
    CredentialModel,
    RefreshCredentialModel,
    RevokeCredentialModel,
)
from src.application.services import AuthService
from src.di import DI
from src.infrastructure.cache import RedisClient
from src.main.middlewares import (
    rate_limit_middleware,
    session_middleware,
)
from pydantic import BaseModel
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime


class LoginModel(BaseModel):
    username: str
    password: str


class Login(BaseModel):
    def __init__(self) -> None:
        pass


AUTH_ROUTER = APIRouter()


@AUTH_ROUTER.post("/login", response_model=RefreshCredentialModel)
@rate_limit_middleware(5, 60)
@session_middleware
async def login(request: Request, data: CredentialModel):
    response = await DI.auth_controller(request.state.db_session).login(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/refresh_token", response_model=RefreshCredentialModel)
@session_middleware
async def refresh_token(request: Request, data: RefreshCredentialModel):
    response = await DI.auth_controller(request.state.db_session).refresh_token(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/revoke_token")
async def revoke_token(data: RevokeCredentialModel):
    if await RedisClient.get(data.access_token):
        return JSONResponse(
            "Token was already revoked",
        )
    payload = AuthService.decode_token(data.access_token)
    remaining_time = payload["exp"] - datetime.utcnow().timestamp()
    await RedisClient.setex(data.access_token, int(remaining_time), "true")
    return JSONResponse("Token has been revoked")
