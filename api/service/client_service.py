from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.client_repository import ClientRepository
from api.dto.client_dto import ClientCreateDTO, ClientUpdateDTO


class ClientService:
    def __init__(self, client_repository:ClientRepository):
        self.client_repository = client_repository
        
    
    async def create_client(self, db:AsyncSession, client_data:ClientCreateDTO):        
        return await self.client_repository.create_client(db, client_data)
    
    async def update_client(self, db:AsyncSession, client_data: ClientUpdateDTO):
        
        client = await self.client_repository.update_client(db, client_data)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return client
    
    async def get_info(self, db:AsyncSession, client_id: int):
        client_data = await self.client_repository.get_client(db, client_id)
        if client_data is None:
            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        
        return{"id":client_data.id,"surname":client_data.surname,"name":client_data.name, "phone":client_data.phone, "id_gender":client_data.id_gender, "telegram_id": client_data.telegram_id}
    
    
    async def get_clients(self, db:AsyncSession):
        clients = await self.client_repository.get_clients(db)
        
        if clients is None:
            raise HTTPException(
                status_code=404,
                detail="Clients not found"
            )
        
        return clients