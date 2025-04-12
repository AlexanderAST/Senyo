from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.referrals_model import ReferralsModel
from api.dto.referral_dto import CreateReferralDTO

class ReferralsRepository:
    async def create_referral(self, db:AsyncSession, referrals_data:CreateReferralDTO):
        new_referral= ReferralsModel(
            id_client=referrals_data.id_client,
            referral_phone = referrals_data.refferal_phone,
            is_active = referrals_data.is_active
        )
        
        db.add(new_referral)
        await db.commit()
        await db.refresh(new_referral)
        return new_referral