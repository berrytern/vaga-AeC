from src.application.domain.models import (
    CredentialModel,
    RefreshCredentialModel,
    ResetCredentialModel,
)
from src.application.domain.utils import UserTypes, UserScopes
from src.infrastructure.cache import RedisClient
from src.infrastructure.repositories import AuthRepository
from src.presenters.exceptions import UnauthorizedException
from src.utils import settings, default
from http import HTTPStatus
from datetime import datetime, timedelta
from aiosmtplib import SMTP
from uuid import UUID
import bcrypt
import jwt


class AuthService:
    def __init__(self, repository: AuthRepository, email_client: SMTP) -> None:
        self.repository = repository
        self.email_client = email_client

    @staticmethod
    def _getScopeByUserType(type: str):
        try:
            UserTypes(type)
            return UserScopes[type.upper()].value
        except ValueError:
            raise Exception("event not listed in events")

    async def login(self, data: CredentialModel):
        result = await self.repository.get_one({"username": data.login})
        if result is None:  # User not found, return unauthorized
            raise UnauthorizedException(
                HTTPStatus.UNAUTHORIZED.phrase, HTTPStatus.UNAUTHORIZED.description
            )
        if not bcrypt.checkpw(data.password.encode(), result["password"].encode()):
            raise UnauthorizedException(
                HTTPStatus.UNAUTHORIZED.phrase, HTTPStatus.UNAUTHORIZED.description
            )
        current = datetime.utcnow()
        payload = {
            "sub": str(result["foreign_id"]),
            "iss": settings.ISSUER,
            "type": result["user_type"],
            "iat": current,
            "scope": str(self._getScopeByUserType(result["user_type"])),
            "exp": current + timedelta(seconds=default.TOKEN_EXP_TIME),
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm="HS256",
        )
        response = {
            "access_token": token,
            "refresh_token": bcrypt.hashpw(
                token.encode("utf8"), bcrypt.gensalt(settings.PASSWORD_SALT_ROUNDS)
            ).decode("utf8"),
        }
        await self.repository.update_one(
            str(result["id"]),
            {
                "refresh_token": response["refresh_token"],
                "last_login": datetime.now(),
            },
        )
        return response

    @staticmethod
    def decode_token(access_token: str):
        return jwt.decode(
            access_token.encode("utf8"),
            settings.JWT_SECRET,
            algorithms="HS256",
            verify=True,
        )

    async def refresh_token(self, data: RefreshCredentialModel):
        result = await self.repository.get_one({"refresh_token": data.refresh_token})
        if result is None:
            raise UnauthorizedException(
                HTTPStatus.UNAUTHORIZED.phrase, HTTPStatus.UNAUTHORIZED.description
            )
        if await RedisClient.get(data.access_token):
            raise UnauthorizedException(HTTPStatus.UNAUTHORIZED.phrase, "Revoked token")
        current = datetime.utcnow()
        _ = self.decode_token(data.access_token)
        if not bcrypt.checkpw(
            data.access_token.encode("utf8"), data.refresh_token.encode("utf8")
        ):
            raise UnauthorizedException(
                HTTPStatus.UNAUTHORIZED.phrase, HTTPStatus.UNAUTHORIZED.description
            )

        token = jwt.encode(
            {
                "sub": str(result["id"]),
                "iss": settings.ISSUER,
                "type": result["user_type"],
                "iat": current,
                "scope": str(self._getScopeByUserType(result["user_type"])),
                "exp": current + timedelta(seconds=default.REFRESH_TOKEN_EXP_TIME),
            },
            settings.JWT_SECRET,
            algorithm="HS256",
        )
        response = {
            "access_token": token,
            "refresh_token": bcrypt.hashpw(
                token.encode("utf8"), bcrypt.gensalt(12)
            ).decode("utf8"),
        }
        await self.repository.update_one(
            str(result["id"]),
            {
                "refresh_token": response["refresh_token"],
                "last_login": datetime.now(),
            },
        )
        return response

    async def change_password(self, data: ResetCredentialModel, user_id: UUID):
        result = await self.repository.get_one({"foreign_id": user_id})
        if not bcrypt.checkpw(data.old_password.encode(), result["password"].encode()):
            raise UnauthorizedException(
                HTTPStatus.UNAUTHORIZED.phrase, HTTPStatus.UNAUTHORIZED.description
            )
        new_password = bcrypt.hashpw(
            data.new_password.encode(), bcrypt.gensalt(settings.PASSWORD_SALT_ROUNDS)
        ).decode()
        return await self.repository.update_one(
            user_id, {"password": new_password}
        )
