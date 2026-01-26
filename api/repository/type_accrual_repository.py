from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.type_accrual_model import TypeAccrualModel

class TypeAccrualRepository:
    @classmethod
    async def get_by_title(cls, db: AsyncSession, title: str) -> TypeAccrualModel | None:
        query = select(TypeAccrualModel).where(TypeAccrualModel.title == title)
        result = await db.execute(query)
        return result.scalars().first()