from typing import Optional, Union, List
from .query_model import QueryModel
from src.application.domain.utils import TypeOpStr, TypeOpFloat
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    Field,
    field_serializer,
    validator,
    StrictStr,
    StrictFloat,
)
from uuid import UUID
from datetime import datetime


class CreateBookModel(BaseModel):
    """Model for creating a new book"""

    title: StrictStr = Field(..., max_length=60)
    description: StrictStr = Field(..., max_length=1500)
    author: StrictStr = Field(..., max_length=60)
    price: StrictFloat = Field(..., ge=0)


class UpdateBookModel(BaseModel):
    """Model for updating an existing book"""

    title: Optional[StrictStr] = Field(None, max_length=60)
    description: Optional[StrictStr] = Field(None, max_length=1500)
    author: Optional[StrictStr] = Field(None, max_length=60)
    price: Optional[StrictFloat] = Field(None, ge=0)


class BookModel(BaseModel):
    """Model for default response of a book"""

    id: Optional[UUID] = None
    title: Optional[StrictStr] = Field(None, max_length=60)
    description: Optional[StrictStr] = Field(None, max_length=1500)
    author: Optional[StrictStr] = Field(None, max_length=60)
    price: Optional[StrictFloat] = Field(None, ge=0)
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

    @field_serializer("id", check_fields=False)
    def serialize_id(self, id):
        return str(id)


class BookList(RootModel):
    """Model for default response of a list of books"""

    root: List[BookModel]


class BookQueryModel(QueryModel):
    id: Optional[List[UUID]] = None
    title: Optional[List[Union[TypeOpStr, StrictStr]]] = None
    description: Optional[List[Union[TypeOpStr, StrictStr]]] = None
    price: Optional[List[Union[TypeOpFloat, StrictStr]]] = None

    @staticmethod
    def integrate_regex(text: str) -> str:
        # text = f"^{text}" if text[0] != ["*"] else text.replace("*", ".*", 1)
        # text = f"{text}$" if text[-1] != ["*"] else text.replace("*", ".*", 1)

        return text  # .replace("*", ".*")

    @validator("title", "description")
    def str_validator(cls, v) -> List[Union[TypeOpStr, str]]:
        return [
            TypeOpStr(index)
            if TypeOpStr.validate_format(index)
            else cls.integrate_regex(index)
            for index in v
        ]

    @validator("price")
    def float_validator(cls, v) -> List[Union[TypeOpFloat, str]]:
        return [
            TypeOpFloat(index)
            if TypeOpFloat.validate_format(index)
            else cls.integrate_regex(index)
            for index in v
        ]
