from api.repository.gender_repository import GenderRepository
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.promotions_dto import PromotionsCreate, PromotionsUI
from api.repository.promotions_repository import PromotionsRepository, PromotionsUpdate

class PromotionsService:

        
    async def create_promotion(self, db:AsyncSession, new_promotion:PromotionsCreate):
        return await PromotionsRepository.create_promotions(db, new_promotion)
    
    async def delete_promotiom(self, db:AsyncSession, id:int):
        id = await PromotionsRepository.delete_promotion(db, id)
        return {"status":"success", "id":id}
    
    async def get_promotions(self, db:AsyncSession) -> list[PromotionsUI]:
        promotions = await PromotionsRepository.get_promotions(db)
        result =[]

        for a in promotions:
            gender = await GenderRepository.get_gender_by_id(db, a.id_gender)
            
            result.append(PromotionsUI(
                id = a.id,
                title = a.title,
                description = a.description,
                added_points = a.added_points,
                gender =  gender.title,
                start_date = a.start_date,
                expiration_date = a.expiration_date,
            ))
        if promotions is None:
            raise HTTPException(
                status_code=404,
                detail="Clients not found"
            )
        
        
        return result

    async def update_promotions(self, db:AsyncSession, promotion:PromotionsUpdate):
        new_promotion = await PromotionsRepository.update_promptions(db, promotion)
        
        if new_promotion is None:
            raise HTTPException(status_code=404,detail="Promotion not found")
        
        return new_promotion