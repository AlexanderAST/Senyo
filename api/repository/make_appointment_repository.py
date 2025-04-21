from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.make_appointment_model import MakeAppointmentModel
from api.dto.make_appointment_dto import CreateAppointment, UpdateAppointment


class AppointemntRepository:
    async def create_appointment(self, db:AsyncSession, appiontment:CreateAppointment):
        new_appointment = MakeAppointmentModel(
            id_client = appiontment.id_client,
            id_address = appiontment.id_address,
            date = appiontment.date,
            title = appiontment.title,
            id_status_type = appiontment.id_status_type,
            final_sum = appiontment.final_sum,
            id_services = appiontment.id_services,
            id_place_type = appiontment.id_place_type
        )
        
        db.add(new_appointment)
        await db.commit()
        await db.refresh(new_appointment)
        
        return new_appointment
    
    async def get_appointment_client(self, db:AsyncSession, client_id:int):
        query = select(MakeAppointmentModel).where(MakeAppointmentModel.id_client == client_id)
        result = await db.execute(query)
        
        return result.scalars().all()
    
    async def get_appointments(self, db:AsyncSession):
        query = select(MakeAppointmentModel)
        result = await db.execute(query)
        
        return result.scalars().all()

    async def update_appointment(self, db:AsyncSession, appointment:UpdateAppointment):
        new_appointment = await db.get(MakeAppointmentModel, appointment.id)
        
        if not new_appointment:
            return None
        
        update_appointment = appointment.model_dump(exclude_unset=True)
        
        for key, value in update_appointment.items():
            if key != "id":
                setattr(new_appointment, key, value)
            
        
        await db.commit()
        await db.refresh(new_appointment)
        
        return new_appointment
        