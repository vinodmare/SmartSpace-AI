from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser
from app.permissions import require_roles

router = APIRouter()


@router.get("/me")
async def get_owner_profile(current: CurrentUser = Depends(require_roles("owner", "admin"))):
    return {"success": True, "data": {"user_id": str(current.id), "message": "Owner profile endpoint ready"}}


@router.post("/verification")
async def submit_owner_verification(current: CurrentUser = Depends(require_roles("owner", "admin"))):
    return {"success": True, "data": {"owner_id": str(current.id), "status": "pending"}}

