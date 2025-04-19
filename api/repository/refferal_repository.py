from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.referrals_model import ReferralsModel
from api.dto.referral_dto import ReferralDTO, UpdateReferralDTO

class ReferralsRepository:
    async def create_referral(self, db:AsyncSession, referrals_data:ReferralDTO):
        new_referral= ReferralsModel(
            id_client=referrals_data.id_client,
            referral_phone = referrals_data.refferal_phone,
            is_active = referrals_data.is_active
        )
        
        db.add(new_referral)
        await db.commit()
        await db.refresh(new_referral)
        return new_referral
    
    async def get_referrals(self, db:AsyncSession, client_id:int):
        query = select(ReferralsModel).where(ReferralsModel.id_client == client_id)
        result = await db.execute(query)
        
        return result.scalars().all()
    
    async def update_referral(self, db:AsyncSession, referrals_data:UpdateReferralDTO):
        referral = await db.get(ReferralsModel, referrals_data.id)
        
        if not referral:
            return None
        
        update_referral = referrals_data.model_dump(exclude_unset=True)
        
        for key, value in update_referral.items():
            if key != "id":
                setattr(referral, key, value)
        
        await db.commit()
        await db.refresh(referral)

        return referral
    
    async def get_referrals_phone(self, db:AsyncSession, phone:str):
        query = select(ReferralsModel).where(ReferralsModel.referral_phone == phone)
        result = await db.execute(query)
        
        return result.scalars().first()