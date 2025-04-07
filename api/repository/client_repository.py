from sqlalchemy import update
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.client_model import ClientModel
from api.dto.client_dto import ClientCreateDTO, ClientUpdateDTO
from api.domain.client_model import ClientModel

class ClientRepository:
    async def create_client(self, db:AsyncSession, client_data: ClientCreateDTO):
        new_client = ClientModel(
            telegram_id = client_data.telegram_id
        )
        
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        return new_client
    
    async def update_client(self, db:AsyncSession, client_data: ClientUpdateDTO):
        client = await db.get(ClientModel, client_data.id)
        
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        update_data = client_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if key != "id":
                setattr(client, key, value)
        
        await db.commit()
        await db.refresh(client)

        return client