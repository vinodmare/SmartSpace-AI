from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    phone: str | None
    avatar_url: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=160)
    phone: str | None = Field(default=None, max_length=32)
    avatar_url: str | None = None


class OwnerProfileRead(BaseModel):
    user_id: UUID
    business_name: str | None
    gst_number: str | None
    pan_number: str | None
    payout_enabled: bool
    verification_status: str

    model_config = {"from_attributes": True}

class OwnerProfileUpdate(BaseModel):
    business_name: str | None = Field(default=None, max_length=180)
    gst_number: str | None = Field(default=None, max_length=32)
    pan_number: str | None = Field(default=None, max_length=16)

