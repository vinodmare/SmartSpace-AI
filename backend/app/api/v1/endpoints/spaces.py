from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.permissions import require_roles
from app.schemas.space import SpaceCreate, SpaceRead, SpaceSearchParams, SpaceUpdate
from app.services.space_service import SpaceService

router = APIRouter()


@router.post("", response_model=SpaceRead)
async def create_space(
    payload: SpaceCreate,
    current: CurrentUser = Depends(require_roles("owner", "admin")),
    db: AsyncSession = Depends(get_db),
):
    return await SpaceService(db).create_space(current.id, payload)


@router.get("", response_model=list[SpaceRead])
async def list_spaces(
    query: str | None = None,
    city: str | None = None,
    capacity: int | None = None,
    budget_inr: int | None = None,
    category_id: int | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    params = SpaceSearchParams(
        query=query, city=city, capacity=capacity, budget_inr=budget_inr, category_id=category_id
    )
    return await SpaceService(db).search_spaces(params, page, page_size)


@router.get("/{space_id}", response_model=SpaceRead)
async def get_space(space_id: UUID, db: AsyncSession = Depends(get_db)):
    return await SpaceService(db).get_space(space_id)


@router.patch("/{space_id}", response_model=SpaceRead)
async def update_space(
    space_id: UUID,
    payload: SpaceUpdate,
    _: CurrentUser = Depends(require_roles("owner", "admin")),
    db: AsyncSession = Depends(get_db),
):
    return await SpaceService(db).update_space(space_id, payload)


@router.patch("/{space_id}/submit", response_model=SpaceRead)
async def submit_space(
    space_id: UUID,
    _: CurrentUser = Depends(require_roles("owner", "admin")),
    db: AsyncSession = Depends(get_db),
):
    return await SpaceService(db).submit_for_approval(space_id)

