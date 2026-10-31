from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.service import AppError


def error_response(status_code: int, code: str, message: str, details: object | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "error": {"code": code, "message": message, "details": details}},
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return error_response(exc.status_code, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(422, "validation_error", "Request validation failed", exc.errors())

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return error_response(exc.status_code, "http_error", str(exc.detail))

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
        return error_response(500, "internal_error", "Internal server error", {"type": type(exc).__name__})

