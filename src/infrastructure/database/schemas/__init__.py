from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


from .auth_schema import AuthSchema
from .admin_schema import AdminSchema
from .book_schema import BookSchema
from .reader_schema import ReaderSchema
