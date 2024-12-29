from pydantic import BaseModel, StrictStr, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError
import re


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
        if re.search(
            (
                r"^(?=.*\d)"  # At least one number
                r"(?=.*[a-z])"  # At least one lowercase letter
                r"(?=.*[A-Z])"  # At least one uppercase letter
                r"(?=.*[\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])"  # At least one special character
                # Only valid characters
                r"[a-zA-Z0-9áàâãéèêíïóôõöúüçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇÑ\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]"
                r"{8,}$"  # at least 8 characters long
            ),
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


class RevokeCredentialModel(BaseModel):
    access_token: StrictStr


class RecoverPasswordModel(BaseModel):
    email: EmailStr = Field(..., min_length=10, max_length=250)
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
        if re.search(
            (
                r"^(?=.*\d)"  # At least one number
                r"(?=.*[a-z])"  # At least one lowercase letter
                r"(?=.*[A-Z])"  # At least one uppercase letter
                r"(?=.*[\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])"  # At least one special character
                # Only valid characters
                r"[a-zA-Z0-9áàâãéèêíïóôõöúüçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇÑ\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]"
                r"{8,}$"  # at least 8 characters long
            ),
            value,
        ):
            return value
        raise PydanticCustomError(
            "Invalid Password",
            "Minimum eight characters, at least one letter, one number and one special character",
            dict(wrong_value=value),
        )


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
        if re.search(
            (
                r"^(?=.*\d)"  # At least one number
                r"(?=.*[a-z])"  # At least one lowercase letter
                r"(?=.*[A-Z])"  # At least one uppercase letter
                r"(?=.*[\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])"  # At least one special character
                # Only valid characters
                r"[a-zA-Z0-9áàâãéèêíïóôõöúüçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇÑ\!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]"
                r"{8,}$"  # at least 8 characters long
            ),
            value,
        ):
            return value
        raise PydanticCustomError(
            "Invalid Password",
            "Minimum eight characters, at least one letter, one number and one special character",
            dict(wrong_value=value),
        )
