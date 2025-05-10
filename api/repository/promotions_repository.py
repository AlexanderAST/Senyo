from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.promotions_dto import PromotionsCreate, PromotionsUpdate
from api.domain.promotion_model import PromotionModel

class PromotionsRepository:

    @classmethod
    async def create_promotions(cls, db:AsyncSession, promotion_data:PromotionsCreate):
        new_promotion = PromotionModel(
            title = promotion_data.title,
            description = promotion_data.description,
            added_points = promotion_data.added_points,
            id_gender = promotion_data.id_gender,
            start_date = promotion_data.start_date,
            expiration_date = promotion_data.expiration_date
        )
        
        db.add(new_promotion)
        await db.commit()
        await db.refresh(new_promotion)
        return new_promotion
    
    @classmethod
    async def delete_promotion(cls, db:AsyncSession, id:int):
        promotion = await db.get(PromotionModel, id)
        
        if not promotion:
            return None
        
        await db.delete(promotion)
        await db.commit()
        
        return id

    @classmethod
    async def get_promotions(cls, db:AsyncSession):
        query = select(PromotionModel)
        result = await db.execute(query)
        
        return result.scalars().all()
    
    @classmethod
    async def update_promptions(cls, db:AsyncSession, promotion:PromotionsUpdate):
        new_promotions = await db.get(PromotionModel, promotion.id)
        
        if not new_promotions:
            return None
        
        update_promotion = promotion.model_dump(exclude_unset=True)
        
        for key, value in update_promotion.items():
            if key != "id":
                setattr(new_promotions, key, value)
            
        
        await db.commit()
        await db.refresh(new_promotions)
        
        return new_promotions