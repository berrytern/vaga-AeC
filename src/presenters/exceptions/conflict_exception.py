from typing import Optional
from .custom_exception import CustomHTTPException


class ConflictException(CustomHTTPException):
    message: str
    description: str

    def __init__(
        self, message: str = "Conflict error", description: Optional[str] = None
    ):
        super().__init__(status_code=409, message=message, description=description)
