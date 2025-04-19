from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.client_service import ClientService
from api.dto.client_dto import ClientCreateDTO, ClientUpdateDTO
from api.database import get_db
from api.repository.client_repository import ClientRepository

router= APIRouter()
client_service = ClientService(ClientRepository())

@router.post("/client")
async def sing_up(client:ClientCreateDTO, db:AsyncSession = Depends(get_db)):
    try:
        return await client_service.create_client(db, client)
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
        return await client_service.get_info(db, client_id) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/admin/get-clients")
async def get_clients(db:AsyncSession= Depends(get_db)):
    try:
        return await client_service.get_clients(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))