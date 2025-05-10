from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.referral_dto import ReferralDTO, CreateReferralRequestDTO, UpdateReferralDTO
from api.repository.refferal_repository import ReferralsRepository


class ReferralsService:
    
    async def create_referral(self, db:AsyncSession, new_referrals_data:CreateReferralRequestDTO):
        
        referrals_data = ReferralDTO(
            id_client=new_referrals_data.id_client,
            refferal_phone=new_referrals_data.refferal_phone,
            is_active=False
        )
        
        return await ReferralsRepository.create_referral(db, referrals_data)
    
    
    async def get_referrals(self, db:AsyncSession, client_id:int) -> list[ReferralDTO]:
        referrals = await ReferralsRepository.get_referrals(db, client_id)
        result =[]
        for a in referrals:
            result.append(ReferralDTO(
                id = a.id,
                id_client = a.id_client,
                refferal_phone = a.referral_phone,
                is_active = a.is_active
            ))

        if referrals is None:
            raise HTTPException(
                status_code=404,
                detail="Referrals not found"
            )
        
        return result
    
    async def update_referrals(self, db:AsyncSession, referrals_data:UpdateReferralDTO):
        referral = await ReferralsRepository.update_referral(db, referrals_data)
        
        if referral is None:
            raise HTTPException(status_code=404, detail="Referral not found")
        
        return referral
    
    async def update_referrals_phone(self, db:AsyncSession, referrals_data:UpdateReferralDTO):
        referral = await ReferralsRepository.update_referral(db, referrals_data)
        
        return referral
        
    async def get_referrals_phone(self, db:AsyncSession, phone:str):
        referrals = await ReferralsRepository.get_referrals_phone(db, phone)
        
        if referrals is None:
            return None
        
        return referrals.id