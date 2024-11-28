from pydantic import BaseModel, StrictStr, Field, field_validator
from pydantic_core import PydanticCustomError
import re


class CreateAuthModel(BaseModel):
    username: StrictStr = Field(..., min_length=6)
    password: StrictStr = Field(
        ...,
        min_length=6,
        max_length=60,
    )

    @field_validator("password")
    @classmethod
    def v_password(cls, value: str) -> str:
        if re.search(
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$*&@#\!])[0-9a-zA-Z$*&@#\!]{8,}$",
            value,
        ):
            return value
        raise PydanticCustomError(
            "Invalid Password",
            "Minimum eight characters, at least one letter, one number and one special character",
            dict(wrong_value=value),
        )


class CredentialModel(BaseModel):
    login: StrictStr
    password: StrictStr


class RefreshCredentialModel(BaseModel):
    access_token: StrictStr
    refresh_token: StrictStr


class ResetCredentialModel(BaseModel):
    email: StrictStr
    old_password: StrictStr
    new_password: StrictStr
