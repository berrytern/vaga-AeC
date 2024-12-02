from src.application.domain.models import CredentialModel, RefreshCredentialModel
from src.application.services import AuthService
from http import HTTPStatus


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    async def login(self, data: CredentialModel):
        result = await self.service.login(data)
        print(result, flush=True)
        return result, HTTPStatus.OK, {}

    async def refresh_token(self, data: RefreshCredentialModel):
        result = await self.service.refresh_token(data)
        return result, HTTPStatus.OK, {}
