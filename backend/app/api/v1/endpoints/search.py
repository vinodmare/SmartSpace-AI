from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.space import SpaceRead, SpaceSearchParams
from app.services.space_service import SpaceService

router = APIRouter()


@router.get("/spaces", response_model=list[SpaceRead])
async def search_spaces(
    query: str | None = None,
    city: str | None = None,
    capacity: int | None = None,
    budget_inr: int | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    params = SpaceSearchParams(query=query, city=city, capacity=capacity, budget_inr=budget_inr)
    return await SpaceService(db).search_spaces(params, page, page_size)


@router.post("/ai")
async def ai_search(payload: dict, db: AsyncSession = Depends(get_db)):
    from app.services.ai_gateway_service import AiGatewayService

    job = await AiGatewayService(db).enqueue("ai_search", payload)
    return {"success": True, "data": {"job_id": str(job.id), "status": job.status.value}}

