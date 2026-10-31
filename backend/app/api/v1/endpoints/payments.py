from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser, get_current_user

router = APIRouter()


@router.post("/create-order")
async def create_payment_order(payload: dict, _: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": {"provider": "razorpay", "status": "pending", "payload": payload}}


@router.post("/webhook")
async def payment_webhook(payload: dict):
    return {"success": True, "data": {"received": True, "payload": payload}}

