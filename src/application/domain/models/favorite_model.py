from .query_model import QueryModel
from datetime import datetime
from typing import Optional, List
from pydantic import (
    BaseModel,
    RootModel,
    ConfigDict,
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
        populate_by_name=True,
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.replace(microsecond=0).isoformat() + "Z"
        },
    )


class FavoriteQueryModel(QueryModel):
    reader_id: Optional[UUID] = None
    book_id: Optional[UUID] = None


class FavoriteList(RootModel):
    root: List[FavoriteModel]
