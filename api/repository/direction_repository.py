from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.direction_model import DirectionModel

class DirectionRepository:
    @classmethod
    async def get_by_title(cls, db: AsyncSession, title: str) -> DirectionModel | None:
        query = select(DirectionModel).where(DirectionModel.title == title)
        result = await db.execute(query)
        return result.scalars().first()