from src.application.domain.models import CredentialModel, RefreshCredentialModel
from src.application.services import AuthService
from src.infrastructure.repositories import AuthRepository
from src.presenters.controllers import AuthController
from pydantic import BaseModel
from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from src.main.middlewares import session_middleware


class LoginModel(BaseModel):
    username: str
    password: str


class Login(BaseModel):
    def __init__(self) -> None:
        pass


AUTH_ROUTER = APIRouter()


@AUTH_ROUTER.post("/login", response_model=RefreshCredentialModel)
@session_middleware
async def login(request: Request, data: CredentialModel):
    repository = AuthRepository(request.state.db_session)
    service = AuthService(repository)
    response = await AuthController(service).login(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )


@AUTH_ROUTER.post("/refresh_token", response_model=RefreshCredentialModel)
@session_middleware
async def refresh_token(request: Request, data: RefreshCredentialModel):
    repository = AuthRepository(request.state.db_session)
    service = AuthService(repository)
    response = await AuthController(service).refresh_token(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
