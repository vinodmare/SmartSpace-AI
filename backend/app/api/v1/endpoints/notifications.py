from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser, get_current_user

router = APIRouter()


@router.get("")
async def list_notifications(current: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": [], "user_id": str(current.id)}


@router.patch("/{notification_id}/read")
async def mark_read(notification_id: str, current: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": {"notification_id": notification_id, "user_id": str(current.id)}}


@router.patch("/read-all")
async def mark_all_read(current: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": {"user_id": str(current.id), "updated": True}}

