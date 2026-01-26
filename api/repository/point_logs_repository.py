from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.point_logs_model import PointLogsModel
from datetime import datetime

class PointLogsRepository:

    @classmethod
    async def create_log(cls, db: AsyncSession, log: PointLogsModel) -> PointLogsModel:
        log.created_at = datetime.utcnow()  # Автоматически устанавливаем время создания
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log

    @classmethod
    async def get_logs_by_client_id(cls, db: AsyncSession, client_id: int) -> list[PointLogsModel]:
        query = select(PointLogsModel).where(PointLogsModel.id_client == client_id)
        result = await db.execute(query)
        return result.scalars().all()