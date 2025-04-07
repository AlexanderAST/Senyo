from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.client_service import ClientService
from api.dto.client_dto import ClientCreateDTO, ClientCreateResponseDTO, ClientUpdateDTO
from api.database import get_db
from api.repository.client_repository import ClientRepository

router= APIRouter()
client_service = ClientService(ClientRepository())

@router.post("/sign-up", response_model=ClientCreateResponseDTO)
async def sing_up(client:ClientCreateDTO, db:AsyncSession = Depends(get_db)):
    try:
        created_client = await client_service.create_client(db, client)
        return ClientCreateResponseDTO(
            id = created_client.id,
            telegram_id = created_client.telegram_id,
            status = "success"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/update-info")
async def update_info(client: ClientUpdateDTO, db:AsyncSession = Depends(get_db)):
    try:
        await client_service.update_client(db, client)
        return {"status":"updated success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))