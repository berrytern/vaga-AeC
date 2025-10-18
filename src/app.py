from src.presenters.exceptions.api_exception_manager import APIExceptionManager
from src.main.middlewares import register_track_middleware
from src.main.routes import (
    ADMIN_ROUTER,
    AUTH_ROUTER,
    BOOK_ROUTER,
    READER_FAVORITE_ROUTER,
    READER_ROUTER,
)
from src.utils import settings
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


http_app = FastAPI(
    title="Proxy API",
    version="1.0",
    description="Redirects to book store API.",
)

https_app = FastAPI(
    title="Book Store API",
    version="1.0",
    description="A simple CRUD API for managing books in a bookstore.",
)


@http_app.middleware("http")
async def redirect_to_https(request: Request, _):
    url = request.url.replace(scheme="https", port=settings.HTTPS_PORT)
    return RedirectResponse(
        url=url,
        status_code=301,  # Permanent redirect
    )


# register the track middleware | It can be used to get the graphic of the requests using prometheus + grafana
register_track_middleware(https_app)

https_app.include_router(AUTH_ROUTER, prefix="/v1/auth", tags=["auth"])
https_app.include_router(ADMIN_ROUTER, prefix="/v1/admins", tags=["admin"])
https_app.include_router(
    READER_FAVORITE_ROUTER, prefix="/v1/readers", tags=["reader-favorite"]
)
https_app.include_router(READER_ROUTER, prefix="/v1/readers", tags=["reader"])
https_app.include_router(BOOK_ROUTER, prefix="/v1/books", tags=["book"])


# Register the error handling
APIExceptionManager.register_error_handling(https_app)
