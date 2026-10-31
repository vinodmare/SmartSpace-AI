from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Booking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Booking)

    async def list_for_customer(self, customer_id: UUID, offset: int, limit: int) -> list[Booking]:
        result = await self.session.execute(
            select(Booking)
            .where(Booking.customer_id == customer_id, Booking.deleted_at.is_(None))
            .order_by(Booking.starts_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def list_for_owner(self, owner_id: UUID, offset: int, limit: int) -> list[Booking]:
        result = await self.session.execute(
            select(Booking)
            .where(Booking.owner_id == owner_id, Booking.deleted_at.is_(None))
            .order_by(Booking.starts_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
