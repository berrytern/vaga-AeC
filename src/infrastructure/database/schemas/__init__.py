from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


from .auth import AuthSchema
from .admin import AdminSchema
from .book import BookSchema
from .reader import ReaderSchema
from .favorite_book import FavoriteBookSchema

__all__ = [
    "Base",
    "AuthSchema",
    "AdminSchema",
    "BookSchema",
    "ReaderSchema",
    "FavoriteBookSchema",
]
