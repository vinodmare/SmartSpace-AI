from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import NotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def get_user(self, user_id: UUID):
        user = await self.users.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    async def update_user(self, user_id: UUID, payload: UserUpdate):
        user = await self.get_user(user_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

