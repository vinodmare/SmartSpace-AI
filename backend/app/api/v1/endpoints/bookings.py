from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.permissions import require_roles
from app.schemas.booking import BookingCancelRequest, BookingCreate, BookingRead
from app.services.booking_service import BookingService

router = APIRouter()


@router.post("", response_model=BookingRead)
async def create_booking(
    payload: BookingCreate,
    current: CurrentUser = Depends(require_roles("customer", "admin")),
    db: AsyncSession = Depends(get_db),
):
    return await BookingService(db).create_booking(current.id, payload)


@router.patch("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_booking(
    booking_id: UUID,
    payload: BookingCancelRequest,
    current: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await BookingService(db).cancel_booking(booking_id, current.id, payload.reason)

