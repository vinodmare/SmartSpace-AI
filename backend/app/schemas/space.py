from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field


class AddressCreate(BaseModel):
    line1: str = Field(max_length=255)
    line2: str | None = Field(default=None, max_length=255)
    locality: str = Field(max_length=140)
    city: str = Field(max_length=120)
    state: str = Field(max_length=120)
    postal_code: str | None = Field(default=None, max_length=16)
    latitude: float | None = None
    longitude: float | None = None


class SpaceCreate(BaseModel):
    name: str = Field(max_length=180)
    category_id: int
    address: AddressCreate
    description: str | None = None
    capacity: int = Field(gt=0)
    size_sqft: int | None = Field(default=None, gt=0)
    hourly_price_inr: int = Field(ge=0)
    daily_price_inr: int | None = Field(default=None, ge=0)
    minimum_booking_hours: float = Field(default=1, gt=0)
    amenity_ids: list[int] = Field(default_factory=list)


class SpaceUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=180)
    description: str | None = None
    capacity: int | None = Field(default=None, gt=0)
    size_sqft: int | None = Field(default=None, gt=0)
    hourly_price_inr: int | None = Field(default=None, ge=0)
    daily_price_inr: int | None = Field(default=None, ge=0)
    minimum_booking_hours: float | None = Field(default=None, gt=0)


class SpaceRead(BaseModel):
    id: UUID
    owner_id: UUID
    category_id: int
    address_id: UUID
    name: str
    slug: str
    description: str | None
    capacity: int
    size_sqft: int | None
    hourly_price_inr: int
    daily_price_inr: int | None
    rating_average: float
    rating_count: int
    demand_score: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SpaceSearchParams(BaseModel):
    query: str | None = None
    city: str | None = None
    capacity: int | None = Field(default=None, gt=0)
    budget_inr: int | None = Field(default=None, ge=0)
    category_id: int | None = None


class AvailabilityRuleCreate(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    opens_at: time
    closes_at: time
    is_available: bool = True

