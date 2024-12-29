from typing import Optional, List
from .credential import CreateAuthModel
from .query import QueryModel
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    Field,
    field_serializer,
    StrictStr,
)
from uuid import UUID
from datetime import date, datetime


class CreateReaderModel(CreateAuthModel):
    name: StrictStr = Field(..., min_length=10, max_length=60)
    birthday: date = Field(..., description="Format: YYYY-MM-DD")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            date: lambda dt: dt.strftime("%Y-%m-%d"),
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z",
        },
    )


class UpdateReaderModel(BaseModel):
    name: Optional[StrictStr] = None
    birthday: Optional[date] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            date: lambda dt: dt.strftime("%Y-%m-%d"),
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z",
        },
    )


class ReaderModel(BaseModel):
    id: Optional[UUID] = None
    name: Optional[StrictStr] = None
    birthday: Optional[date] = None
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
            date: lambda dt: dt.strftime("%Y-%m-%d"),
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z",
        },
    )

    @field_serializer("id")
    def serialize_id(self, id):
        return str(id)


class ReaderList(RootModel):
    root: List[ReaderModel]


class ReaderQueryModel(QueryModel):
    id: Optional[UUID] = None
    name: Optional[StrictStr] = None
    birthday: Optional[StrictStr] = None
