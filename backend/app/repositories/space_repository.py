from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Address, Space, SpaceAmenity, SpaceStatus
from app.repositories.base import BaseRepository
from app.schemas.space import SpaceSearchParams


class SpaceRepository(BaseRepository[Space]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Space)

    async def search(self, params: SpaceSearchParams, offset: int, limit: int) -> list[Space]:
        statement = select(Space).join(Address).where(Space.deleted_at.is_(None))
        if params.city:
            statement = statement.where(Address.city.ilike(f"%{params.city}%"))
        if params.capacity:
            statement = statement.where(Space.capacity >= params.capacity)
        if params.budget_inr:
            statement = statement.where(Space.hourly_price_inr <= params.budget_inr)
        if params.category_id:
            statement = statement.where(Space.category_id == params.category_id)
        if params.query:
            like = f"%{params.query}%"
            statement = statement.where(or_(Space.name.ilike(like), Space.description.ilike(like), Address.locality.ilike(like)))
        statement = statement.where(Space.status == SpaceStatus.approved).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def add_amenities(self, space_id: UUID, amenity_ids: list[int]) -> None:
        for amenity_id in set(amenity_ids):
            self.session.add(SpaceAmenity(space_id=space_id, amenity_id=amenity_id))

