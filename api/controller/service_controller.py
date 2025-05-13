from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.services_service import ServicesService
from api.dto.services_dto import CreateService, GetService

router = APIRouter()

service_service = ServicesService()


@router.post("/admin/service")
async def create_service(service_data:CreateService, db:AsyncSession= Depends(get_db)):
    try:
        return await service_service.create_service(db,service_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/services", response_model= list[GetService])
async def get_services(db:AsyncSession= Depends(get_db)):
    try:
        return await service_service.get_services(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))