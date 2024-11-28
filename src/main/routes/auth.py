from src.application.models import CredentialModel, RefreshCredentialModel
from src.presenters.controllers import AuthController
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse


class LoginModel(BaseModel):
    username: str
    password: str


class Login(BaseModel):
    def __init__(self) -> None:
        pass


AUTH_ROUTER = APIRouter()


@AUTH_ROUTER.post("/login")
async def login(data: CredentialModel, response_model=RefreshCredentialModel):
    response = await AuthController().login(data)
    return JSONResponse(
        content=response[0], status_code=response[1], headers=response[2]
    )
