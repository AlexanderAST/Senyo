from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from api.domain.make_appointment_model import MakeAppointmentModel
from api.dto.make_appointment_dto import CreateAppointment, UpdateAppointment


class AppointemntRepository:

    @classmethod
    async def create_appointment(cls, db:AsyncSession, appiontment:CreateAppointment):
        new_appointment = MakeAppointmentModel(
            id_client = appiontment.id_client,
            id_address = appiontment.id_address,
            date = appiontment.date,
            id_status_type = appiontment.id_status_type,
            final_sum = appiontment.final_sum,
            id_services = appiontment.id_services,
            id_place_type = appiontment.id_place_type
        )
        
        db.add(new_appointment)
        await db.commit()
        await db.refresh(new_appointment)
        
        return new_appointment
    
    @classmethod
    async def get_appointment_client(cls, db:AsyncSession, client_id:int):
        query = select(MakeAppointmentModel).where(MakeAppointmentModel.id_client == client_id)
        result = await db.execute(query)
        
        return result.scalars().all()
    
    @classmethod
    async def get_appointments(cls, db:AsyncSession):
        query = select(MakeAppointmentModel)
        result = await db.execute(query)
        
        return result.scalars().all()

    @classmethod
    async def update_appointment(cls, db:AsyncSession, appointment:UpdateAppointment):
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
        
    @classmethod
    async def nullify_address_references(cls, db: AsyncSession, address_id: int):
        stmt = (
            update(MakeAppointmentModel)
            .where(MakeAppointmentModel.id_address == address_id)
            .values(id_address=None)
        )
        await db.execute(stmt)
        await db.commit()