from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.client_model import ClientModel
from api.dto.client_dto import ClientCreateDTO, ClientUpdateDTO

class ClientRepository:
    @classmethod
    async def create_client(cls, db:AsyncSession, client_data: ClientCreateDTO):
        new_client = ClientModel(
            telegram_id = client_data.telegram_id
        )
        
        db.add(new_client)
        await db.commit()
        await db.refresh(new_client)
        return new_client
    
    @classmethod
    async def update_client(cls, db:AsyncSession, client_data: ClientUpdateDTO):
        client = await db.get(ClientModel, client_data.id)
        
        if not client:
            return None
        
        update_data = client_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if key != "id":
                setattr(client, key, value)
        
        await db.commit()
        await db.refresh(client)

        return client
    
    @classmethod
    async def get_client(cls, db:AsyncSession, id:int):
        query = select(ClientModel).where(ClientModel.id == id)
        result = await db.execute(query)

        return result.scalars().first()
    
    @classmethod
    async def get_clients(cls, db:AsyncSession):
        query = select(ClientModel)
        result = await db.execute(query)
        
        return result.scalars().all()