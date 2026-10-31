from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.ai_gateway_service import AiGatewayService

router = APIRouter()


async def enqueue(service_name: str, payload: dict, db: AsyncSession):
    job = await AiGatewayService(db).enqueue(service_name, payload)
    return {"success": True, "data": {"job_id": str(job.id), "service": service_name, "status": job.status.value}}


@router.post("/price-prediction")
async def price_prediction(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("price_prediction", payload, db)


@router.post("/fraud-risk")
async def fraud_risk(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("fraud_detection", payload, db)


@router.post("/recommendations")
async def recommendations(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("recommendation_engine", payload, db)


@router.post("/demand-forecast")
async def demand_forecast(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("demand_forecast", payload, db)


@router.post("/review-sentiment")
async def review_sentiment(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("review_sentiment", payload, db)


@router.post("/chat")
async def ai_chat(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("ai_chat", payload, db)


@router.post("/image-quality")
async def image_quality(payload: dict, db: AsyncSession = Depends(get_db)):
    return await enqueue("image_quality_detection", payload, db)
