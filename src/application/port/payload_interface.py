from typing import TypedDict
from src.application.domain.utils import UserTypes


class PayloadInterface(TypedDict):
    sub: str
    type: UserTypes
    iss: str
    iat: str
    scope: int
    exp: int
