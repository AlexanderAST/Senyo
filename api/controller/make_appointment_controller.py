from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.make_appointment_service import AppointmentService
from api.repository.make_appointment_repository import AppointemntRepository
from api.dto.make_appointment_dto import RequestAppointment, UpdateAppointment

router = APIRouter()
appointment_service = AppointmentService(AppointemntRepository())

@router.post("/appointment")
async def create_appointment(appointment_data:RequestAppointment, user_agent:str, db:AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.create_appointment(db, appointment_data, user_agent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/appointment/{client_id}")
async def get_appointment(client_id:int, db:AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.get_appointment_client(db, client_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin/appointment")
async def get_appointments(db:AsyncSession = Depends(get_db)):
    try:
        return await appointment_service.get_appointments(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/admin/appointment")
async def update_appointments(appointment:UpdateAppointment, db:AsyncSession=Depends(get_db)):
    try:
        await appointment_service.update_appointment(db, appointment)
        return {"status":"updated success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))