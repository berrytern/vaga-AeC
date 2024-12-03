from .custom_exception import CustomHTTPException
from src.utils.logger import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from asyncpg.exceptions import PostgresError
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus


# It does the rollback of the database session if erros occur
async def session_rollback(request: Request):
    if hasattr(request.state, "db_session"):
        await request.state.db_session.rollback()


# Handles all the exceptions that can occur in the API
class APIExceptionManager:
    @staticmethod
    def register_error_handling(app: FastAPI):
        @app.exception_handler(Exception)
        async def handle_unknow_exceptions(request: Request, exc: Exception):
            await session_rollback(request)
            logger.api_logger.exception(exc)
            error = CustomHTTPException(
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
                HTTPStatus.INTERNAL_SERVER_ERROR.name,
                HTTPStatus.INTERNAL_SERVER_ERROR.description,
            )
            return JSONResponse(error.to_json(), status_code=error.status_code)

        @app.exception_handler(IntegrityError)
        async def handle_unique_violation_exceptions(request, exc: IntegrityError):
            await session_rollback(request)
            error = CustomHTTPException(
                HTTPStatus.CONFLICT.value,
                HTTPStatus.CONFLICT.name,
                HTTPStatus.CONFLICT.description,
            )
            return JSONResponse(error.to_json(), status_code=error.status_code)

        @app.exception_handler(CustomHTTPException)
        async def handle_custom_exceptions(request, exc: CustomHTTPException):
            await session_rollback(request)
            return JSONResponse(exc.to_json(), status_code=exc.status_code)

        @app.exception_handler(PostgresError)
        async def handle_database_exceptions(request, exc: PostgresError):
            await session_rollback(request)
            logger.api_logger.exception(exc)
            error = CustomHTTPException(
                500,
                "database error",
                "An error occurred while doing some database operation",
            )
            return JSONResponse(error.to_json(), status_code=error.status_code)
