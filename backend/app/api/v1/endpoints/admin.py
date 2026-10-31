from fastapi import APIRouter, Depends

from app.dependencies.auth import CurrentUser
from app.permissions import require_roles

router = APIRouter()


@router.get("/dashboard")
async def dashboard(_: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": {"status": "ready"}}


@router.get("/spaces/pending")
async def pending_spaces(_: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": []}


@router.patch("/spaces/{space_id}/approve")
async def approve_space(space_id: str, _: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": {"space_id": space_id, "status": "approved"}}


@router.patch("/spaces/{space_id}/reject")
async def reject_space(space_id: str, payload: dict, _: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": {"space_id": space_id, "status": "rejected", "payload": payload}}


@router.get("/reports")
async def list_reports(_: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": []}


@router.post("/reports")
async def create_report(payload: dict, _: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": {"status": "queued", "payload": payload}}


@router.get("/fraud/assessments")
async def fraud_assessments(_: CurrentUser = Depends(require_roles("admin"))):
    return {"success": True, "data": []}

