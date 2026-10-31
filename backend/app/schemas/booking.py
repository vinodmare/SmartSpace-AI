from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    space_id: UUID
    starts_at: datetime
    ends_at: datetime
    guest_count: int = Field(gt=0)


class BookingRead(BaseModel):
    id: UUID
    customer_id: UUID
    space_id: UUID
    owner_id: UUID
    starts_at: datetime
    ends_at: datetime
    guest_count: int
    hourly_price_inr: int
    subtotal_inr: int
    tax_inr: int
    platform_fee_inr: int
    total_inr: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BookingCancelRequest(BaseModel):
    reason: str | None = None

