from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser, get_current_user

router = APIRouter()


@router.post("")
async def create_review(payload: dict, current: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": {"customer_id": str(current.id), "payload": payload}}


@router.patch("/{review_id}/reply")
async def reply_to_review(review_id: str, payload: dict, current: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": {"review_id": review_id, "owner_id": str(current.id), "payload": payload}}

