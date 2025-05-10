from api.dto.address_dto import AddressDTO
from api.repository.address_repository import AddressesRepository
from api.repository.client_balance_repository import ClientBalanceRepository
from api.repository.gender_repository import GenderRepository
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.client_repository import ClientRepository
from api.dto.client_dto import ClientCreateDTO, ClientUI, ClientUpdateDTO
from api.dto.referral_dto import UpdateReferralDTO
from api.service.referrals_service import ReferralsService
from api.repository.refferal_repository import ReferralsRepository
from api.dto.referral_dto import UpdateReferralDTO

referrals_service = ReferralsService()

class ClientService:
            
    async def create_client(self, db: AsyncSession, client_data: ClientCreateDTO):
        client = await ClientRepository.create_client(db, client_data)

        await ClientBalanceRepository.create_balance(
            db=db,
            client_id=client.id,
            permanent=0.0,
            temporary=0.0
        )

        return client
    
    async def update_client(self, db:AsyncSession, client_data: ClientUpdateDTO):       
        client = await ClientRepository.update_client(db, client_data)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
                
        if client_data.phone is not None:
            referrals = await referrals_service.get_referrals_phone(db, client_data.phone)
            
            if referrals is not None:
                referral_data = UpdateReferralDTO(id=referrals, is_active=True)
                await referrals_service.update_referrals_phone(db,referral_data)
                
        
        return client
    
    async def get_info(self, db: AsyncSession, client_id: int) -> ClientUI:
        client = await ClientRepository.get_client(db, client_id)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
        addresses = await AddressesRepository.get_by_client_id(db, client.id)
        gender = await GenderRepository.get_gender_by_id(db, client.id_gender)

        address_dtos = [AddressDTO(
            id=a.id,
            address=a.address,
            id_client=a.id_client,
            status=a.status
        ) for a in addresses]

        return ClientUI(
            id=client.id,
            surname=client.surname,
            name=client.name,
            phone=client.phone,
            gender=gender.title if gender else None,
            permanent_points=balance.permanent_points if balance else 0.0,
            temporary_point=balance.temporary_points if balance else 0.0,
            addresses=address_dtos
        )

    async def get_clients(self, db: AsyncSession) -> list[ClientUI]:
        clients = await ClientRepository.get_clients(db)
        if not clients:
            raise HTTPException(status_code=404, detail="Clients not found")

        result = []

        for client in clients:
            balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
            addresses = await AddressesRepository.get_by_client_id(db, client.id)
            gender = await GenderRepository.get_gender_by_id(db, client.id_gender)

            address_dtos = [AddressDTO(
                id=a.id,
                address=a.address,
                id_client=a.id_client,
            ) for a in addresses]

            result.append(ClientUI(
                id=client.id,
                surname=client.surname,
                name=client.name,
                phone=client.phone,
                gender=gender.title if gender else None,
                permanent_points=balance.permanent_points if balance else 0.0,
                temporary_point=balance.temporary_points if balance else 0.0,
                addresses=address_dtos
            ))

        return result