from api.database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.referrals_service import ReferralsService
from api.repository.refferal_repository import ReferralsRepository
from api.dto.referral_dto import CreateReferralRequestDTO, ReferralsDTO

router = APIRouter()
referrals_service = ReferralsService(ReferralsRepository())


@router.post("/referrals", response_model=ReferralsDTO)
async def create_referrals(referrals:CreateReferralRequestDTO, db:AsyncSession=Depends(get_db)):  
    try:
        new_referrals = await referrals_service.create_referral(db, referrals)
        return ReferralsDTO(
            id = new_referrals.id,
            id_client=new_referrals.id_client, 
            refferal_phone=new_referrals.referral_phone,
            is_active=new_referrals.is_active,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/referrals/{client_id}")
async def get_referrals(client_id:int, db:AsyncSession= Depends(get_db)):
    try:
        referrals_data = await referrals_service.get_referrals(db, client_id)
        return referrals_data
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))