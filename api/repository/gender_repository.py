from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.gender_model import GenderModel

class GenderRepository:

    @classmethod
    async def get_gender_by_id(cls, db: AsyncSession, gender_id: int) -> GenderModel | None:
        return await db.get(GenderModel, gender_id)

    @classmethod
    async def get_all_genders(cls, db: AsyncSession) -> list[GenderModel]:
        result = await db.execute(select(GenderModel))
        return result.scalars().all()

    @classmethod
    async def create_gender(cls, db: AsyncSession, title: str) -> GenderModel:
        gender = GenderModel(title=title)
        db.add(gender)
        await db.commit()
        await db.refresh(gender)
        return gender

    @classmethod
    async def delete_gender(cls, db: AsyncSession, gender_id: int) -> bool:
        gender = await db.get(GenderModel, gender_id)
        if not gender:
            return False
        await db.delete(gender)
        await db.commit()
        return True
