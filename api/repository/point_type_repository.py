from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.point_type_model import PointTypeModel

class PointTypeRepository:
    @classmethod
    async def get_by_title(cls, db: AsyncSession, title: str) -> PointTypeModel | None:
        query = select(PointTypeModel).where(PointTypeModel.title == title)
        result = await db.execute(query)
        return result.scalars().first()