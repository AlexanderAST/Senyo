from datetime import date
from sqlalchemy import select,delete
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.applied_promotion_model import AppliedPromotionModel

class AppliedPromotionRepository: 
    
    @classmethod
    async def create_applied(cls, db:AsyncSession, id_client:int, id_promotion:int, applied_date:date) -> AppliedPromotionModel:
        new_applied = AppliedPromotionModel(
            id_client = id_client,
            id_promotion = id_promotion,
            applied_date = applied_date
        )
        db.add(new_applied)
        await db.commit()
        await db.refresh(new_applied)
        return new_applied
    
    @classmethod
    async def get_by_client_and_promo(cls, db:AsyncSession, id_client:int, id_promotion:int)-> AppliedPromotionModel | None:
        query = select(AppliedPromotionModel).where(
            AppliedPromotionModel.id_client == id_client,
            AppliedPromotionModel.id_promotion ==id_promotion
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    @classmethod
    async def get_all_by_promotion(cls, db: AsyncSession, promo_id: int) -> list[AppliedPromotionModel]:
        query = select(AppliedPromotionModel).where(AppliedPromotionModel.id_promotion == promo_id)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def delete_all_by_promotion(cls, db: AsyncSession, promo_id: int):
        stmt = delete(AppliedPromotionModel).where(AppliedPromotionModel.id_promotion == promo_id)
        await db.execute(stmt)
        await db.commit()