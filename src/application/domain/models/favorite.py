from .query import QueryModel
from datetime import datetime
from typing import Optional, List
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
    field_serializer,
)
from uuid import UUID


class CreateFavoriteModel(BaseModel):
    reader_id: UUID
    book_id: UUID


class FavoriteModel(BaseModel):
    id: Optional[UUID] = None
    reader_id: Optional[UUID] = None
    book_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True, from_attributes=True
    )

    @field_serializer("created_at", "updated_at")
    def serialize_datetimes(self, dt: Optional[datetime]) -> Optional[str]:
        if dt is None:
            return None
        return dt.replace(microsecond=0).isoformat() + "Z"


class FavoriteQueryModel(QueryModel):
    reader_id: Optional[UUID] = None
    book_id: Optional[UUID] = None


class FavoriteList(RootModel):
    root: List[FavoriteModel]
