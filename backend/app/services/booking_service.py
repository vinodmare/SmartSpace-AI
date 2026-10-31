from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictError, NotFoundError
from app.models.entities import Booking, BookingStatus, Space, SpaceStatus
from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate


class BookingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.bookings = BookingRepository(session)

    async def create_booking(self, customer_id: UUID, payload: BookingCreate) -> Booking:
        if payload.starts_at >= payload.ends_at:
            raise ConflictError("Booking start time must be before end time")

        space = await self.session.get(Space, payload.space_id)
        if space is None or space.status != SpaceStatus.approved:
            raise NotFoundError("Bookable space not found")
        if payload.guest_count > space.capacity:
            raise ConflictError("Guest count exceeds space capacity")

        duration_hours = (payload.ends_at - payload.starts_at).total_seconds() / 3600
        subtotal = round(duration_hours * space.hourly_price_inr)
        platform_fee = round(subtotal * 0.05)
        tax = round(subtotal * 0.18)
        total = subtotal + platform_fee + tax

        booking = Booking(
            customer_id=customer_id,
            space_id=space.id,
            owner_id=space.owner_id,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            guest_count=payload.guest_count,
            hourly_price_inr=space.hourly_price_inr,
            subtotal_inr=subtotal,
            tax_inr=tax,
            platform_fee_inr=platform_fee,
            total_inr=total,
            status=BookingStatus.pending,
        )
        await self.bookings.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def cancel_booking(self, booking_id: UUID, user_id: UUID, reason: str | None) -> Booking:
        booking = await self.bookings.get(booking_id)
        if booking is None:
            raise NotFoundError("Booking not found")
        booking.status = BookingStatus.cancelled
        booking.cancelled_by = user_id
        booking.cancelled_at = datetime.now(UTC)
        booking.cancellation_reason = reason
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

