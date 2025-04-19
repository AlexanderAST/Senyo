from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.client_repository import ClientRepository
from api.dto.client_dto import ClientCreateDTO, ClientUpdateDTO
from api.dto.referral_dto import UpdateReferralDTO
from api.service.referrals_service import ReferralsService
from api.repository.refferal_repository import ReferralsRepository
from api.dto.referral_dto import UpdateReferralDTO

referrals_service = ReferralsService(ReferralsRepository())

class ClientService:
    def __init__(self, client_repository:ClientRepository):
        self.client_repository = client_repository
        
    
    async def create_client(self, db:AsyncSession, client_data:ClientCreateDTO):        
        return await self.client_repository.create_client(db, client_data)
    
    async def update_client(self, db:AsyncSession, client_data: ClientUpdateDTO):       
        client = await self.client_repository.update_client(db, client_data)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
                
        if client_data.phone is not None:
            referrals = await referrals_service.get_referrals_phone(db, client_data.phone)
            
            if referrals is not None:
                referral_data = UpdateReferralDTO(id=referrals, is_active=True)
                await referrals_service.update_referrals(db,referral_data)
                
        
        return client
    
    async def get_info(self, db:AsyncSession, client_id: int):
        client_data = await self.client_repository.get_client(db, client_id)
        if client_data is None:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        
        return client_data
    
    
    async def get_clients(self, db:AsyncSession):
        clients = await self.client_repository.get_clients(db)
        
        if clients is None:
            raise HTTPException(
                status_code=404,
                detail="Clients not found"
            )
        
        return clients