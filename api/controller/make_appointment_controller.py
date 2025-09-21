from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.make_appointment_service import AppointmentService
from api.dto.make_appointment_dto import RequestAppointment, UpdateAppointment, AppointmentUI
from fastapi import Query
from datetime import datetime

router = APIRouter()
appointment_service = AppointmentService()

@router.post("/appointment")
async def create_appointment(appointment_data:RequestAppointment, user_agent:str, db:AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.create_appointment(db, appointment_data, user_agent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/appointment/{client_id}", response_model = list[AppointmentUI])
async def get_appointment(client_id:int, db:AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.get_appointment_client(db, client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/appointment", response_model = list[AppointmentUI])
async def get_appointments(db:AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.get_ui_appointments(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/admin/appointment")
async def update_appointments(appointment:UpdateAppointment, db:AsyncSession=Depends(get_db)):
    try:
        await appointment_service.update_appointment(db, appointment)
        return {"status":"updated success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/admin/appointment/archive", response_model=list[AppointmentUI])
async def get_archived_appointments(db: AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.get_ui_archived_appointments(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/appointment/cancel/{appointment_id}")
async def cancel_client_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.cancel_appointment(db, appointment_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/admin/appointment/close/{appointment_id}")
async def close_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.close_appointment(db, appointment_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/available-times")
async def get_available_times(
    date: datetime = Query(..., description="Дата в формате YYYY-MM-DD"),
    id_services: int = Query(..., description="ID услуги"),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Конвертируем date в naive datetime без timezone
        naive_date = date.replace(tzinfo=None)
        return await appointment_service.get_available_times(db, naive_date, id_services)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))