from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser, get_current_user
from app.permissions import require_roles

router = APIRouter()


@router.get("/spaces/{space_id}")
async def get_space_availability(space_id: str):
    return {"success": True, "data": {"space_id": space_id, "rules": [], "blackouts": []}}


@router.put("/spaces/{space_id}/rules")
async def update_availability_rules(
    space_id: str,
    payload: list[dict],
    _: CurrentUser = Depends(require_roles("owner", "admin")),
):
    return {"success": True, "data": {"space_id": space_id, "rules": payload}}


@router.post("/spaces/{space_id}/blackouts")
async def create_blackout(
    space_id: str,
    payload: dict,
    _: CurrentUser = Depends(require_roles("owner", "admin")),
):
    return {"success": True, "data": {"space_id": space_id, "blackout": payload}}

