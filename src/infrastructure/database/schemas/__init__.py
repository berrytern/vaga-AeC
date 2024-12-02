from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


from .auth_schema import AuthSchema
from .admin_schema import AdminSchema
from .book_schema import BookSchema
from .reader_schema import ReaderSchema
from .favorite_book_schema import FavoriteBookSchema

__all__ = [
    "Base",
    "AuthSchema",
    "AdminSchema",
    "BookSchema",
    "ReaderSchema",
    "FavoriteBookSchema",
]
