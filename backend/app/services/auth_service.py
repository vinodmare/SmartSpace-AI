from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.exceptions import ConflictError, UnauthorizedError
from app.models.entities import CustomerProfile, OwnerProfile, User, UserRoleLink
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        existing = await self.users.get_by_email(payload.email)
        if existing:
            raise ConflictError("Email is already registered")

        user = User(
            email=payload.email.lower(),
            password_hash=get_password_hash(payload.password),
            full_name=payload.full_name,
        )
        await self.users.add(user)

        role = await self.users.get_role(payload.role)
        if role is None:
            raise ConflictError("Configured role does not exist")

        self.session.add(UserRoleLink(user_id=user.id, role_id=role.id))
        if payload.role == "customer":
            self.session.add(CustomerProfile(user_id=user.id))
        if payload.role == "owner":
            self.session.add(OwnerProfile(user_id=user.id))

        await self.session.commit()
        return self._tokens(user.id, [payload.role])

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self.users.get_by_email(payload.email.lower())
        if user is None or not verify_password(payload.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        roles = [link.role.name.value for link in user.roles]
        return self._tokens(user.id, roles)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token, refresh=True)
        user_id = UUID(payload["sub"])
        user = await self.users.get_with_roles(user_id)
        if user is None:
            raise UnauthorizedError("User no longer exists")
        roles = [link.role.name.value for link in user.roles]
        return self._tokens(user.id, roles)

    async def forgot_password(self, email: str) -> None:
        # Production implementation should send an expiring token by email.
        await self.users.get_by_email(email.lower())

    async def reset_password(self, token: str, new_password: str) -> None:
        # Placeholder until transactional password reset tokens are persisted.
        payload = decode_token(token)
        user = await self.users.get(UUID(payload["sub"]))
        if user is None:
            raise UnauthorizedError("Invalid reset token")
        user.password_hash = get_password_hash(new_password)
        await self.session.commit()

    def _tokens(self, user_id: UUID, roles: list[str]) -> TokenResponse:
        subject = str(user_id)
        return TokenResponse(
            access_token=create_access_token(subject, roles),
            refresh_token=create_refresh_token(subject),
        )

