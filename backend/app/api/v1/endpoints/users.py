from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_user(current.id)


@router.patch("/me", response_model=UserRead)
async def update_me(
    payload: UserUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await UserService(db).update_user(current.id, payload)

