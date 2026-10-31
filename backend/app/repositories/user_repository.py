from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.entities import Role, User, UserRole, UserRoleLink
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).options(selectinload(User.roles).selectinload(UserRoleLink.role)).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_with_roles(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).options(selectinload(User.roles).selectinload(UserRoleLink.role)).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_role(self, role_name: str) -> Role | None:
        result = await self.session.execute(select(Role).where(Role.name == UserRole(role_name)))
        return result.scalar_one_or_none()

