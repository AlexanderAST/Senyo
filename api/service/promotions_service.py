from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.promotions_dto import PromotionsCreate
from api.repository.promotions_repository import PromotionsRepository

class PromotionsService:
    def __init__(self, promotions_repository:PromotionsRepository):
        self.promotions_repository = promotions_repository
        
    async def create_promotion(self, db:AsyncSession, new_promotion:PromotionsCreate):
        return await self.promotions_repository.create_promotions(db, new_promotion)
    
    async def delete_promotiom(self, db:AsyncSession, id:int):
        id = await self.promotions_repository.delete_promotion(db, id)
        return {"status":"success", "id":id}
    
    async def get_promotions(self, db:AsyncSession):
        promotions = await self.promotions_repository.get_promotions(db)
        
        if promotions is None:
            raise HTTPException(
                status_code=404,
                detail="Clients not found"
            )
        
        return promotions