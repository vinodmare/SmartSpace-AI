from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser
from app.permissions import require_roles

router = APIRouter()


@router.get("")
async def list_favorites(current: CurrentUser = Depends(require_roles("customer", "admin"))):
    return {"success": True, "data": [], "customer_id": str(current.id)}


@router.post("/{space_id}")
async def add_favorite(space_id: str, current: CurrentUser = Depends(require_roles("customer", "admin"))):
    return {"success": True, "data": {"user_id": str(current.id), "space_id": space_id}}


@router.delete("/{space_id}")
async def remove_favorite(space_id: str, current: CurrentUser = Depends(require_roles("customer", "admin"))):
    return {"success": True, "data": {"user_id": str(current.id), "space_id": space_id, "deleted": True}}

