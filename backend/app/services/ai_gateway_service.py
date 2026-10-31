from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import AiJob, AiJobStatus


class AiGatewayService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def enqueue(self, service_name: str, payload: dict, entity_type: str | None = None, entity_id: UUID | None = None) -> AiJob:
        job = AiJob(
            service_name=service_name,
            entity_type=entity_type,
            entity_id=entity_id,
            input_payload=payload,
            status=AiJobStatus.queued,
        )
        self.session.add(job)
        await self.session.commit()
        await self.session.refresh(job)
        return job
