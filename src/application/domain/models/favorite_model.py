from .query_model import QueryModel
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
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


class FavoriteQueryModel(QueryModel):
    reader_id: Optional[List[UUID]] = None
    book_id: Optional[List[UUID]] = None


class FavoriteList(BaseModel):
    root: list[FavoriteModel]
