from typing import Optional
from src.application.domain.models import (
    CredentialModel,
    RefreshCredentialModel,
    ResetCredentialModel,
    RecoverPasswordModel,
    RecoverRequestModel,
)
from src.application.domain.utils import UserTypes, UserScopes
from src.infrastructure.cache import RedisClient
from src.infrastructure.email import EmailClient
from src.infrastructure.repositories import AuthRepository
from src.presenters.exceptions import (
    ConflictException,
    UnauthorizedException,
    ValidationException,
)
from src.utils import settings, default
from http import HTTPStatus
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from email.mime.text import MIMEText
import bcrypt
import jwt


class AuthService:
    def __init__(self, repository: AuthRepository, email_client: EmailClient) -> None:
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
        return await self.repository.update_one(user_id, {"password": new_password})

    async def reset_password(self, data: RecoverPasswordModel):
        secret_hash: Optional[str] = await RedisClient.get(
            f"{default.RESET_PASSWD_PREFIX}{data.username}"
        )
        if secret_hash is None:
            raise ValidationException(HTTPStatus.BAD_REQUEST.phrase, "Invalid hash")

        result = await self.repository.get_one({"username": data.username})
        if result is None:
            raise ConflictException(
                HTTPStatus.CONFLICT.phrase, HTTPStatus.CONFLICT.description
            )
        new_password = bcrypt.hashpw(
            data.new_password.encode(), bcrypt.gensalt(settings.PASSWORD_SALT_ROUNDS)
        ).decode()
        await self.repository.update_one(result["id"], {"password": new_password})
        await RedisClient.delete(f"{default.RESET_PASSWD_PREFIX}{data.username}")

    async def request_password_reset(self, data: RecoverRequestModel):
        if (
            await RedisClient.get(f"{default.RESET_PASSWD_PREFIX}{data.username}")
            is not None
        ):
            raise ConflictException(
                HTTPStatus.CONFLICT.phrase, HTTPStatus.CONFLICT.description
            )
        result = await self.repository.get_one({"username": data.username})
        if result is None:
            raise ValidationException(
                HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST.description
            )
        id = str(uuid4())
        username = result["username"]
        email_body = [
            MIMEText(
                item[0].format(
                    name=username,
                    link=f"https://{settings.HOSTNAME}/v1/auth/password/username/{username}/hash/{id}",
                    support_email=settings.SMTP_USER,
                    exp_time=settings.RESET_PASSWD_EXP // 60,
                ),
                item[1],
                "utf-8",
            )
            for item in [
                (default.RESET_PASSWD_BODY_TEXT, "plain"),
                (default.RESET_PASSWD_BODY_HTML, "html"),
            ]
        ]
        response = await self.email_client.send_email(
            [result["email"]], default.RESET_PASSWD_SUBJECT, *email_body
        )
        await RedisClient.setex(
            f"{default.RESET_PASSWD_PREFIX}{data.username}",
            settings.RESET_PASSWD_EXP,
            id,
        )
        return response
