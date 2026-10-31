from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser
from app.permissions import require_roles

router = APIRouter()


@router.get("/customer")
async def customer_analytics(current: CurrentUser = Depends(require_roles("customer", "admin"))):
    return {"success": True, "data": {"user_id": str(current.id), "bookings": 0, "favorites": 0}}


@router.get("/owner")
async def owner_analytics(current: CurrentUser = Depends(require_roles("owner", "admin"))):
    return {"success": True, "data": {"owner_id": str(current.id), "revenue_inr": 0, "bookings": 0}}


@router.get("/admin")
async def admin_analytics(_: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": {"users": 0, "spaces": 0, "bookings": 0, "fraud_alerts": 0}}

