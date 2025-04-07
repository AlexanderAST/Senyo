from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.client_repository import ClientRepository
from api.dto.client_dto import ClientCreateDTO, ClientUpdateDTO


class ClientService:
    def __init__(self, client_repository:ClientRepository):
        self.client_repository = client_repository
        
    
    async def create_client(self, db:AsyncSession, client_data:ClientCreateDTO):
        
        new_client = ClientCreateDTO(
            telegram_id=client_data.telegram_id
        )
        
        return await self.client_repository.create_client(db, new_client)
    
    async def update_client(self, db:AsyncSession, client_data: ClientUpdateDTO):
        updated_client = ClientUpdateDTO(
                id = client_data.id,
                surname = client_data.surname,
                name = client_data.name,
                phone = client_data.phone,
                id_gender = client_data.id_gender
        )
        
        return await self.client_repository.update_client(db, updated_client)