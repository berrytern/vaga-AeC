from src.application.domain.models import (
    CredentialModel,
    RefreshCredentialModel,
    ResetCredentialModel,
    RecoverRequestModel,
    RecoverPasswordModel,
)
from src.application.services import AuthService
from http import HTTPStatus
from uuid import UUID


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    async def login(self, data: CredentialModel):
        result = await self.service.login(data)
        return result, HTTPStatus.OK, {}

    async def refresh_token(self, data: RefreshCredentialModel):
        result = await self.service.refresh_token(data)
        return result, HTTPStatus.OK, {}

    async def change_password(self, data: ResetCredentialModel, user_id: UUID):
        result = await self.service.change_password(data, user_id)
        return result, HTTPStatus.OK, {}

    async def request_password_reset(self, data: RecoverRequestModel):
        result = await self.service.request_password_reset(data)
        return result, HTTPStatus.OK, {}

    async def reset_password(self, data: RecoverPasswordModel):
        result = await self.service.reset_password(data)
        return result, HTTPStatus.OK, {}
