from src.application.models import CredentialModel
from src.application.utils import UserTypes, UserScopes
from src.infrastructure.database import get_db
from src.infrastructure.repositories import AuthRepository
from src.utils import settings, default
from http import HTTPStatus
from datetime import datetime, timedelta
import bcrypt
import jwt


class AuthController:
    @staticmethod
    def getScopeByUserType(type: str):
        try:
            UserTypes(type)
            return UserScopes[type.upper()].value
        except ValueError:
            raise Exception("event not listed in events")

    @classmethod
    async def login(cls, data: CredentialModel):

        response = None
        async with get_db() as session:
            repo = AuthRepository(session)
            result = await repo.get_one_by_username(data.login)
            if result is not None:
                result = result[0]
                # result = await repo.update_one(aluno_id, aluno.model_dump(exclude_none=True))
                if not bcrypt.checkpw(data.password.encode(), result.password.encode()):
                    return None, HTTPStatus.UNAUTHORIZED, {}
                current = datetime.utcnow()
                token = jwt.encode(
                    {
                        "sub": str(result.id),
                        "iss": settings.ISSUER,
                        "type": result.user_type,
                        "iat": current,
                        "scope": str(cls.getScopeByUserType(result.user_type)),
                        "exp": current + timedelta(seconds=default.TOKEN_EXP_TIME),
                    },
                    settings.JWT_SECRET,
                )
                response = {
                    "access_token": token,
                    "refresh_token": bcrypt.hashpw(
                        token.encode("utf8"), bcrypt.gensalt(12)
                    ).decode("utf8"),
                }
                await repo.update_one(
                    str(result.id),
                    {
                        "refresh_token": response["refresh_token"],
                        "last_login": datetime.now(),
                    },
                )
                return response, HTTPStatus.OK, {}
        return response, HTTPStatus.UNAUTHORIZED, {}
