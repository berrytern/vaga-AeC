from typing import Optional
from .custom_exception import CustomHTTPException


class UnauthorizedException(CustomHTTPException):
    message: str
    description: str

    def __init__(
        self, message: str = "Unauthorized error", description: Optional[str] = None
    ):
        super().__init__(status_code=401, message=message, description=description)
