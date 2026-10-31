from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.authentication.security import decode_token
from app.exceptions import UnauthorizedError

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class CurrentUser:
    id: UUID
    roles: list[str]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    if credentials is None:
        raise UnauthorizedError("Authentication required")
    payload = decode_token(credentials.credentials)
    subject = payload.get("sub")
    if not subject:
        raise UnauthorizedError("Invalid token subject")
    return CurrentUser(id=UUID(subject), roles=list(payload.get("roles", [])))
