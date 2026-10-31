from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    message: str | None = None


class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    meta: PageMeta

