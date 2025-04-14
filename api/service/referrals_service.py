from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.referral_dto import CreateReferralDTO, CreateReferralRequestDTO
from api.repository.refferal_repository import ReferralsRepository


class ReferralsService:
    def __init__(self, referrals_repository:ReferralsRepository):
        self.referrals_repository = referrals_repository
        
    
    async def create_referral(self, db:AsyncSession, new_referrals_data:CreateReferralRequestDTO):
        
        referrals_data = CreateReferralDTO(
            id_client=new_referrals_data.id_client,
            refferal_phone=new_referrals_data.refferal_phone,
            is_active=False
        )
        
        return await self.referrals_repository.create_referral(db, referrals_data)
    
    
    async def get_referrals(self, db:AsyncSession, client_id:int):
        referrals = await self.referrals_repository.get_referrals(db, client_id)
        
        if referrals is None:
            raise HTTPException(
                status_code=404,
                detail="Referrals not found"
            )
        
        return referrals