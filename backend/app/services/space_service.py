from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from app.models.entities import Address, Space, SpaceStatus
from app.repositories.space_repository import SpaceRepository
from app.schemas.space import SpaceCreate, SpaceSearchParams, SpaceUpdate
from app.utils.slug import slugify


class SpaceService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.spaces = SpaceRepository(session)

    async def create_space(self, owner_id: UUID, payload: SpaceCreate) -> Space:
        address = Address(**payload.address.model_dump())
        self.session.add(address)
        await self.session.flush()

        space = Space(
            owner_id=owner_id,
            category_id=payload.category_id,
            address_id=address.id,
            name=payload.name,
            slug=slugify(payload.name),
            description=payload.description,
            capacity=payload.capacity,
            size_sqft=payload.size_sqft,
            hourly_price_inr=payload.hourly_price_inr,
            daily_price_inr=payload.daily_price_inr,
            minimum_booking_hours=payload.minimum_booking_hours,
            status=SpaceStatus.draft,
        )
        await self.spaces.add(space)
        await self.spaces.add_amenities(space.id, payload.amenity_ids)
        await self.session.commit()
        await self.session.refresh(space)
        return space

    async def get_space(self, space_id: UUID) -> Space:
        space = await self.spaces.get(space_id)
        if space is None or space.deleted_at is not None:
            raise NotFoundError("Space not found")
        return space

    async def update_space(self, space_id: UUID, payload: SpaceUpdate) -> Space:
        space = await self.get_space(space_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(space, key, value)
        await self.session.commit()
        await self.session.refresh(space)
        return space

    async def search_spaces(self, params: SpaceSearchParams, page: int, page_size: int) -> list[Space]:
        return await self.spaces.search(params, offset=(page - 1) * page_size, limit=page_size)

    async def submit_for_approval(self, space_id: UUID) -> Space:
        space = await self.get_space(space_id)
        space.status = SpaceStatus.pending_approval
        await self.session.commit()
        await self.session.refresh(space)
        return space

