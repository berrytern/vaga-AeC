from .custom_exception import CustomHTTPException
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from asyncpg.exceptions import PostgresError
from http import HTTPStatus
from src.utils.logger import logger


class APIExceptionManager:
    @staticmethod
    def register_error_handling(app: FastAPI):
        @app.exception_handler(Exception)
        async def handle_unknow_exceptions(request, exc: Exception):
            logger.api_logger.exception(exc)
            error = CustomHTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
                HTTPStatus.INTERNAL_SERVER_ERROR.name,
                HTTPStatus.INTERNAL_SERVER_ERROR.description,
            )
            return JSONResponse(error.to_json(), status_code=error.status_code)

        @app.exception_handler(CustomHTTPException)
        async def handle_custom_exceptions(request, exc: CustomHTTPException):
            return JSONResponse(exc.to_json(), status_code=exc.status_code)

        @app.exception_handler(PostgresError)
        async def handle_database_exceptions(request, exc: PostgresError):
            logger.api_logger.exception(exc)
            error = CustomHTTPException(
                500,
                "database error",
                "An error occurred while doing some database operation",
            )
            return JSONResponse(error.to_json(), status_code=error.status_code)
