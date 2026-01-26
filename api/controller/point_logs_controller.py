from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.point_logs_service import PointLogsService
from api.dto.point_logs_dto import PointLogsCreateDTO, PointLogsUI
from api.database import get_db

router = APIRouter(prefix="/point-logs")
point_logs_service = PointLogsService()

@router.post("/")
async def create_log(log: PointLogsCreateDTO, db: AsyncSession = Depends(get_db)):
    try:
        return await point_logs_service.create_log(db, log)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/client/{client_id}", response_model=list[PointLogsUI])
async def get_logs(client_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await point_logs_service.get_logs_by_client(db, client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))