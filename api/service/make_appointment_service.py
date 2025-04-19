from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.make_appointment_repository import AppointemntRepository
from api.dto.make_appointment_dto import CreateAppointment, RequestAppointment

class AppointmentService:
    def __init__(self, appointment_repository:AppointemntRepository):
        self.appointment_repository = appointment_repository
    
    async def create_appointment(self, db:AsyncSession, appointment_data:RequestAppointment,user_agent:str):
        new_appointment = CreateAppointment(
            id_client = appointment_data.id_client,
            id_address = appointment_data.id_address,
            date = appointment_data.date,
            title = appointment_data.title,
            id_status_type = 2 if user_agent == "Admin" else 1,
            final_sum = appointment_data.final_sum,
            id_services = appointment_data.id_services,
            id_place_type = appointment_data.id_place_type
        )
        
        return await self.appointment_repository.create_appointment(db,new_appointment)

    async def get_appointment_client(self, db:AsyncSession, client_id:int):
        appointment = await self.appointment_repository.get_appointment_client(db, client_id)
        
        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )
        
        return appointment
    
    async def get_appointments(self, db:AsyncSession):
        appointments = await self.appointment_repository.get_appointments(db)
        if appointments is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )
        
        return appointments