from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.client_service import ClientService
from api.dto.client_dto import ClientAddPointsDTO, ClientCreateDTO, ClientUI, ClientUpdateDTO
from api.database import get_db

router= APIRouter()
client_service = ClientService()

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
    

@router.get("/client/{client_id}", response_model = ClientUI)
async def info(client_id:int, db:AsyncSession = Depends(get_db)):
    try:
        return await client_service.get_info(db, client_id) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/admin/get-clients", response_model = list[ClientUI])
async def get_clients(db:AsyncSession= Depends(get_db)):
    try:
        return await client_service.get_clients(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/admin/client/add-points")
async def add_points(
    dto: ClientAddPointsDTO,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await client_service.add_points_to_client(
            db=db,
            client_id=dto.client_id,
            permanent_delta=dto.permanent_delta,
            temporary_delta=dto.temporary_delta
        )
        return {"status": "success", "balance": {
            "permanent": result.permanent_points,
            "temporary": result.temporary_points
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))