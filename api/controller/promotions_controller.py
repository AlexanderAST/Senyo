from api.database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.promotions_service import PromotionsService
from api.repository.promotions_repository import PromotionsRepository
from api.dto.promotions_dto import PromotionsCreate

router = APIRouter()
promotions_service = PromotionsService(PromotionsRepository())


@router.post("/promotions")
async def create_promotion(promotion:PromotionsCreate, db:AsyncSession = Depends(get_db)):
    try:
        new_promotion = await promotions_service.create_promotion(db, promotion)
        return new_promotion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/promotions")
async def delete_promotion(id:int, db:AsyncSession= Depends(get_db)):
    try:
        result = await promotions_service.delete_promotiom(db, id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))