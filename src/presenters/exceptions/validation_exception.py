from typing import Optional
from .custom_exception import CustomHTTPException


class ValidationException(CustomHTTPException):
    message: str
    description: str

    def __init__(
        self, message: str = "Validation error", description: Optional[str] = None
    ):
        super().__init__(status_code=400, message=message, description=description)
