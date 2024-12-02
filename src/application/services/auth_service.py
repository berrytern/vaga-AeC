from src.application.domain.models import CredentialModel, RefreshCredentialModel
from src.application.domain.utils import UserTypes, UserScopes
from src.infrastructure.repositories import AuthRepository
from src.presenters.exceptions import UnauthorizedException
from src.utils import settings, default
from http import HTTPStatus
from datetime import datetime, timedelta
import bcrypt
import jwt


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

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
            return None, HTTPStatus.UNAUTHORIZED, {}
        current = datetime.utcnow()
        token = jwt.encode(
            {
                "sub": str(result["id"]),
                "iss": settings.ISSUER,
                "type": result["user_type"],
                "iat": current,
                "scope": str(self._getScopeByUserType(result["user_type"])),
                "exp": current + timedelta(seconds=default.TOKEN_EXP_TIME),
            },
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

    async def refresh_token(self, data: RefreshCredentialModel):
        result = await self.repository.get_one({"refresh_token": data.refresh_token})
        if result is None:
            raise UnauthorizedException(
                HTTPStatus.UNAUTHORIZED.phrase, HTTPStatus.UNAUTHORIZED.description
            )
        current = datetime.utcnow()
        _ = jwt.decode(
            data.access_token.encode("utf8"),
            settings.JWT_SECRET,
            algorithms="HS256",
            verify=True,
        )
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
