from typing import Optional, List
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    field_serializer,
    Field,
    StrictStr,
)
from uuid import UUID
from datetime import datetime


class BookModel(BaseModel):
    id: Optional[UUID] = None
    title: StrictStr = Field(..., max_length=60)
    description: StrictStr = Field(..., max_length=400)
    author: StrictStr = Field(..., max_length=60)
    price: float = Field(..., ge=0)
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


class BookList(RootModel):
    root: List[BookModel]
