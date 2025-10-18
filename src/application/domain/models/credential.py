from pydantic import BaseModel, StrictStr, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError
import re


# Define the password validation regex pattern once
PASSWORD_PATTERN = (
    r"^(?=.*\d)"  # At least one number
    r"(?=.*[a-z])"  # At least one lowercase letter
    r"(?=.*[A-Z])"  # At least one uppercase letter
    r"(?=.*[\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])"  # At least one special character
    # Only valid characters
    r"[a-zA-Z0-9áàâãéèêíïóôõöúüçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇÑ\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]"
    r"{8,72}\Z"  # at least 8 characters long
)


# Define a reusable password validator function
def validate_password(value: str) -> str:
    """
    Validates if a password meets the security requirements.

    Requirements:
    - At least 8 characters long
    - At least one special character
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit

    Args:
        value: The password to be validated

    Returns:
        str: The validated password

    Raises:
        PydanticCustomError: If password doesn't meet requirements
    """
    if re.search(PASSWORD_PATTERN, value):
        return value
    raise PydanticCustomError(
        "Invalid Password",
        "Minimum eight characters, at least one letter, one number and one special character",
        dict(wrong_value=value),
    )


USERNAME_PATTERN = (
    r"(?=.*[a-z])"  # At least one lowercase letter
    # Only valid characters
    r"[a-z0-9_.]{6,}\Z"
)


def validate_username(value: str) -> str:
    if re.search(USERNAME_PATTERN, value):
        return value
    raise PydanticCustomError(
        "Invalid Username",
        "Minimum six characters",
        dict(wrong_value=value),
    )


class CreateAuthModel(BaseModel):
    username: StrictStr = Field(..., min_length=6)
    email: EmailStr = Field(..., min_length=10, max_length=250)
    password: StrictStr = Field(
        ...,
        min_length=6,
        max_length=60,
    )

    @field_validator("password")
    @classmethod
    def v_password(cls, value: str) -> str:
        return validate_password(value)

    @field_validator("username")
    @classmethod
    def v_username(cls, value: str) -> str:
        return validate_username(value)

    @field_validator("email")
    @classmethod
    def v_email(cls, value: str) -> str:
        return value.lower()


class CredentialModel(BaseModel):
    login: StrictStr
    password: StrictStr = Field(..., max_length=72)


class RefreshCredentialModel(BaseModel):
    access_token: StrictStr
    refresh_token: StrictStr


class RevokeCredentialModel(BaseModel):
    access_token: StrictStr


class RecoverPasswordModel(BaseModel):
    username: StrictStr
    security_hash: StrictStr
    new_password: StrictStr = Field(
        ...,
        min_length=6,
        max_length=60,
    )

    @field_validator("new_password")
    @classmethod
    def v_password(cls, value: str) -> str:
        """
        Validates if a password meets the security requirements.

        Requirements:
        - At least 8 characters long
        - At least one special character
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number

        Args:
            password: The password to validate

        Returns:
            str
        """
        return validate_password(value)


class RecoverRequestModel(BaseModel):
    username: StrictStr


class ResetCredentialModel(BaseModel):
    old_password: StrictStr
    new_password: StrictStr = Field(
        ...,
        min_length=6,
        max_length=60,
    )

    @field_validator("new_password")
    @classmethod
    def v_password(cls, value: str) -> str:
        """
        Validates if a password meets the security requirements.

        Requirements:
        - At least 8 characters long
        - At least one special character
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number

        Args:
            password: The password to validate

        Returns:
            str
        """
        return validate_password(value)
