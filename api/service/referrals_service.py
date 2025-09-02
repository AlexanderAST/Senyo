from http.client import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.referral_dto import ReferralDTO, CreateReferralRequestDTO, UpdateReferralDTO
from api.repository.refferal_repository import ReferralsRepository
from api.repository.client_balance_repository import ClientBalanceRepository
from api.repository.client_repository import ClientRepository
from api.repository.point_type_repository import PointTypeRepository
from api.repository.direction_repository import DirectionRepository
from api.repository.type_accrual_repository import TypeAccrualRepository
from api.service.point_logs_service import PointLogsService
from api.dto.point_logs_dto import PointLogsCreateDTO

point_logs_service = PointLogsService()

class ReferralsService:
    
    async def create_referral(self, db:AsyncSession, new_referrals_data:CreateReferralRequestDTO):
        client = await ClientRepository.get_client(db, new_referrals_data.id_client)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
    
        if new_referrals_data.refferal_phone == client.phone:  # Предполагаю, что у ClientModel есть поле phone
            raise HTTPException(status_code=400, detail="Cannot refer yourself")
    
        existing_referral = await ReferralsRepository.get_referrals_phone(db, new_referrals_data.refferal_phone)
        if existing_referral:
            raise HTTPException(status_code=400, detail="Referral phone already exists")
    
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
        return result
    
    async def update_referrals(self, db:AsyncSession, referrals_data:UpdateReferralDTO):
        referral = await ReferralsRepository.update_referral(db, referrals_data)
        
        if referral is None:
            raise HTTPException(status_code=404, detail="Referral not found")
        
        return referral
    
    async def update_referrals_phone(self, db:AsyncSession, referrals_data:UpdateReferralDTO):
        referral = await ReferralsRepository.update_referral(db, referrals_data)
        
        if referral.is_active:
            referral_phone = referral.referral_phone

            client = await ClientRepository.get_by_phone(db, referral_phone)
            if client:
                await ClientBalanceRepository.update_balance(db, client.id, permanent_delta=500)
                
                accrual_type = await TypeAccrualRepository.get_by_title(db, 'referral')
                direction = await DirectionRepository.get_by_title(db, 'accrual')
                point_type = await PointTypeRepository.get_by_title(db, 'permanent')
                log_dto = PointLogsCreateDTO(
                    id_client=client.id,
                    id_point_type=point_type.id,
                    points=500,
                    id_direction=direction.id,
                    id_type_accural=accrual_type.id,
                    expiration_date=None
                )
                await point_logs_service.create_log(db, log_dto)
        
        return referral
        
    async def get_referrals_phone(self, db:AsyncSession, phone:str):
        referrals = await ReferralsRepository.get_referrals_phone(db, phone)
        
        if referrals is None:
            return None
        
        return referrals.id