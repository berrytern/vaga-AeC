from .admin import ADMIN_ROUTER
from .auth import AUTH_ROUTER
from .book import BOOK_ROUTER
from .reader_favorite import READER_FAVORITE_ROUTER
from .reader import READER_ROUTER

__all__ = [
    "ADMIN_ROUTER",
    "AUTH_ROUTER",
    "BOOK_ROUTER",
    "READER_FAVORITE_ROUTER",
    "READER_ROUTER",
]
