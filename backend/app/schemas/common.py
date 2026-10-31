from uuid import UUID

from pydantic import BaseModel, Field


class IdResponse(BaseModel):
    id: UUID


class MessageResponse(BaseModel):
    message: str


class ListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: str | None = None
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")

