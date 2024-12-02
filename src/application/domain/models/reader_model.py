from typing import Optional, List, Union
from .credential_model import CreateAuthModel
from .query_model import QueryModel
from src.application.domain.utils import TypeOpStr, TypeOpDate
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    EmailStr,
    StrictStr,
)
from uuid import UUID
from datetime import datetime


class CreateReaderModel(CreateAuthModel):
    name: StrictStr = Field(..., min_length=10, max_length=60)
    email: EmailStr = Field(..., min_length=10, max_length=250)
    birthday: datetime = Field(..., description="Format: YYYY-MM-DD")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z"
        },
    )


class UpdateReaderModel(BaseModel):
    name: Optional[StrictStr] = None
    email: Optional[EmailStr] = None
    birthday: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z"
        },
    )


class ReaderModel(BaseModel):
    id: Optional[UUID] = None
    name: Optional[StrictStr] = None
    email: Optional[EmailStr] = None
    birthday: Optional[datetime] = None
    books_read_count: Optional[int] = Field(None, ge=0)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now().replace(microsecond=0)
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z"
        },
    )

    @field_serializer("id")
    def serialize_id(self, id):
        return str(id)


class ReaderList(RootModel):
    root: List[ReaderModel]


class ReaderQueryModel(QueryModel):
    id: Optional[List[UUID]] = None
    name: Optional[List[Union[TypeOpStr, StrictStr]]] = None
    email: Optional[List[Union[TypeOpStr, StrictStr]]] = None
    birthday: Optional[List[Union[TypeOpDate, StrictStr]]] = None

    @staticmethod
    def integrate_regex(text: str) -> str:
        # text = f"^{text}" if text[0] != ["*"] else text.replace("*", ".*", 1)
        # text = f"{text}$" if text[-1] != ["*"] else text.replace("*", ".*", 1)

        return text  # .replace("*", ".*")

    @field_validator("name", "email")
    def str_validator(cls, v) -> List[Union[TypeOpStr, str]]:
        return [
            TypeOpStr(index)
            if TypeOpStr.validate_format(index)
            else cls.integrate_regex(index)
            for index in v
        ]

    @field_validator("birthday")
    def date_validator(cls, v) -> List[Union[TypeOpDate, str]]:
        return [
            TypeOpDate(index)
            if TypeOpDate.validate_format(index)
            else cls.integrate_regex(index)
            for index in v
        ]
