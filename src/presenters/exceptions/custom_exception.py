from typing import Optional


class CustomHTTPException(Exception):
    status_code: int
    message: str
    description: Optional[str]

    def __init__(
        self,
        status_code: int,
        message: str,
        description: Optional[str],
    ):
        self.status_code = status_code
        self.message = message
        self.description = description

    def to_json(self) -> dict:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "description": self.description,
        }
