from collections.abc import Callable

from fastapi import Depends

from app.dependencies.auth import CurrentUser, get_current_user
from app.exceptions import ForbiddenError


def require_roles(*allowed_roles: str) -> Callable:
    async def dependency(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not set(current_user.roles).intersection(allowed_roles):
            raise ForbiddenError("You do not have permission to access this resource")
        return current_user

    return dependency

