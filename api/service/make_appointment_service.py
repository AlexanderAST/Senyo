from api.domain.make_appointment_model import MakeAppointmentModel
from api.repository.address_repository import AddressesRepository
from api.repository.client_balance_repository import ClientBalanceRepository
from api.repository.client_repository import ClientRepository
from api.repository.gender_repository import GenderRepository
from api.repository.place_type_repository import PlaceTypeRepository
from api.repository.services_repository import ServiceRepository
from api.repository.status_repository import StatusTypeRepository
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.make_appointment_repository import AppointemntRepository
from api.dto.make_appointment_dto import CreateAppointment, RequestAppointment, UpdateAppointment, AppointmentUI
from sqlalchemy import select

class AppointmentService:

    async def cancel_appointment(self, db: AsyncSession, appointment_id: int):
        # Находим запись по ID (без проверки на клиента)
        query = select(MakeAppointmentModel).where(MakeAppointmentModel.id == appointment_id)
        result = await db.execute(query)
        appointment = result.scalar_one_or_none()
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # Только если активная (статус 1 или 2), иначе ошибка
        if appointment.id_status_type not in (1, 2):
            raise HTTPException(status_code=400, detail="Only active appointments can be cancelled")
        
        # Меняем статус на 4 (отменена)
        update_data = UpdateAppointment(id=appointment_id, id_status_type=4)
        updated_appointment = await AppointemntRepository.update_appointment(db, update_data)
        
        if not updated_appointment:
            raise HTTPException(status_code=500, detail="Failed to update appointment")
        
        return updated_appointment
    
    async def create_appointment(self, db:AsyncSession, appointment_data:RequestAppointment,user_agent:str):
        new_appointment = CreateAppointment(
            id_client = appointment_data.id_client,
            id_address = appointment_data.id_address,
            date = appointment_data.date,
            id_status_type = 2 if user_agent == "Admin" else 1,
            final_sum = appointment_data.final_sum,
            id_services = appointment_data.id_services,
            id_place_type = appointment_data.id_place_type
        )
        
        return await AppointemntRepository.create_appointment(db,new_appointment)

    async def get_appointment_client(self, db:AsyncSession, client_id:int):
        appointments = await AppointemntRepository.get_appointment_client(db, client_id)
        if not appointments:
            raise HTTPException(status_code=404, detail="Appointment not found")

        client = await ClientRepository.get_client(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        gender = await GenderRepository.get_gender_by_id(db, client.id_gender)
        balance = await ClientBalanceRepository.get_by_client_id(db, client.id)

        result = []

        for a in appointments:
            service = await ServiceRepository.get_service(db, a.id_services)
            status = await StatusTypeRepository.get_status_by_id(db, a.id_status_type)
            place = await PlaceTypeRepository.get_place_type(db, a.id_place_type)

            result.append(AppointmentUI(
                id=a.id,
                client_name=f"{client.name} {client.surname}",
                client_phone=client.phone,
                client_gender=gender.title if gender else None,
                client_points=(balance.permanent_points + balance.temporary_points) if balance else 0.0,
                service_price=service.price,
                service_name=service.title,
                place=place.title,
                status=status.title,
                date=a.date,
                final_sum=a.final_sum,
                used_points=service.price - a.final_sum
            ))

        return result
    
    async def get_appointments(self, db:AsyncSession):
        appointments = await AppointemntRepository.get_appointments(db)
        if appointments is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )
        
        return appointments

    async def update_appointment(self, db:AsyncSession, appointment:UpdateAppointment):
        new_appointment = await AppointemntRepository.update_appointment(db, appointment)
        if new_appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        return new_appointment
    
    async def get_ui_appointments(self, db:AsyncSession) -> list[AppointmentUI]:
        appointments = await AppointemntRepository.get_appointments(db)
        appointments = [a for a in appointments if a.id_status_type in (1, 2)]
        result =[]

        for a in appointments:
            client = await ClientRepository.get_client(db, a.id_client)
            service = await ServiceRepository.get_service(db, a.id_services)
            status = await StatusTypeRepository.get_status_by_id(db, a.id_status_type)
            gender = await GenderRepository.get_gender_by_id(db, client.id_gender)
            place = await PlaceTypeRepository.get_place_type(db, a.id_place_type)
            balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
            place_title = place.title  # по умолчанию — офис

            if a.id_place_type == 2 and a.id_address is not None:
                 address = await AddressesRepository.get_by_id(db, a.id_address)
                 if address:
                     place_title = address.address
            result.append(AppointmentUI(
                id=a.id,
                client_name=f"{client.name} {client.surname}",
                client_phone=client.phone,
                client_gender=gender.title,
                client_points=balance.permanent_points+balance.temporary_points,
                service_price=service.price,
                service_name=service.title,
                place=place_title,
                status=status.title,
                date=a.date,
                final_sum=a.final_sum,
                used_points=service.price - a.final_sum
            ))

        return result
    
    async def get_ui_archived_appointments(self, db: AsyncSession) -> list[AppointmentUI]:
        appointments = await AppointemntRepository.get_appointments(db)

        appointments = [a for a in appointments if a.id_status_type in (3, 4)]

        result = []
        for a in appointments:
            client = await ClientRepository.get_client(db, a.id_client)
            service = await ServiceRepository.get_service(db, a.id_services)
            status = await StatusTypeRepository.get_status_by_id(db, a.id_status_type)
            gender = await GenderRepository.get_gender_by_id(db, client.id_gender)
            place = await PlaceTypeRepository.get_place_type(db, a.id_place_type)
            balance = await ClientBalanceRepository.get_by_client_id(db, client.id)

            place_title = place.title
            if a.id_place_type == 2 and a.id_address is not None:
                address = await AddressesRepository.get_by_id(db, a.id_address)
                if address:
                    place_title = address.address

            result.append(AppointmentUI(
                id=a.id,
                client_name=f"{client.name} {client.surname}",
                client_phone=client.phone,
                client_gender=gender.title,
                client_points=balance.permanent_points + balance.temporary_points,
                service_price=service.price,
                service_name=service.title,
                place=place_title,
                status=status.title,
                date=a.date,
                final_sum=a.final_sum,
                used_points=service.price - a.final_sum
            ))
    
        return result
    
    