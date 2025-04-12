from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.client_service import ClientService
from api.dto.client_dto import ClientCreateDTO, ClientCreateResponseDTO, ClientUpdateDTO
from api.database import get_db
from api.repository.client_repository import ClientRepository

router= APIRouter()
client_service = ClientService(ClientRepository())

@router.post("/client", response_model=ClientCreateResponseDTO)
async def sing_up(client:ClientCreateDTO, db:AsyncSession = Depends(get_db)):
    try:
        created_client = await client_service.create_client(db, client)
        return ClientCreateResponseDTO(
            id = created_client.id,
            telegram_id = created_client.telegram_id,
            status = "success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/client")
async def update_info(client: ClientUpdateDTO, db:AsyncSession = Depends(get_db)):
    try:
        await client_service.update_client(db, client)
        return {"status":"updated success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/client/{client_id}")
async def info(client_id:int, db:AsyncSession = Depends(get_db)):
    try:
        client_data = await client_service.get_info(db, client_id)
        
        return client_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/admin-get-clients")
async def get_clients(db:AsyncSession= Depends(get_db)):
    try:
        clients = await client_service.get_clients(db)
        
        return {"clients": clients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))