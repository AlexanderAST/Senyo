from api.database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.referrals_service import ReferralsService
from api.dto.referral_dto import CreateReferralRequestDTO, ReferralDTO, UpdateReferralDTO

router = APIRouter()
referrals_service = ReferralsService()


@router.post("/referrals")
async def create_referrals(referrals:CreateReferralRequestDTO, db:AsyncSession=Depends(get_db)):  
    try:
       
        return await referrals_service.create_referral(db, referrals)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/referrals/{client_id}", response_model =list[ReferralDTO])
async def get_referrals(client_id:int, db:AsyncSession= Depends(get_db)):
    try:
        return await referrals_service.get_referrals(db, client_id)
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.put("/referrals")
async def update_referrals(referrals:UpdateReferralDTO, db:AsyncSession=Depends(get_db)):
    try:
        await referrals_service.update_referrals(db,referrals)
        return {"status":"updated success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))