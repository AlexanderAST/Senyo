from http.client import HTTPException
from api.domain.make_appointment_model import MakeAppointmentModel
from api.repository.address_repository import AddressesRepository
from api.repository.client_balance_repository import ClientBalanceRepository
from api.repository.client_repository import ClientRepository
from api.repository.gender_repository import GenderRepository
from api.repository.place_type_repository import PlaceTypeRepository
from api.repository.refferal_repository import ReferralsRepository
from api.repository.services_repository import ServiceRepository
from api.repository.status_repository import StatusTypeRepository
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.make_appointment_repository import AppointemntRepository
from api.dto.make_appointment_dto import CreateAppointment, RequestAppointment, UpdateAppointment, AppointmentUI
from sqlalchemy import select
from sqlalchemy import func, and_
from api.domain.make_appointment_model import MakeAppointmentModel  # Для query
from api.repository.point_type_repository import PointTypeRepository
from api.repository.direction_repository import DirectionRepository
from api.repository.type_accrual_repository import TypeAccrualRepository
from api.service.point_logs_service import PointLogsService
from api.dto.point_logs_dto import PointLogsCreateDTO


point_logs_service = PointLogsService()

class AppointmentService:

    async def create_appointment(self, db:AsyncSession, appointment_data:RequestAppointment, user_agent:str):
        service = await ServiceRepository.get_service(db, appointment_data.id_services)
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")

        final_sum = appointment_data.final_sum
        if final_sum > service.price:
            raise HTTPException(status_code=400, detail="Final sum exceeds service price")

        used_points = service.price - final_sum  # Рассчитываем на лету

        if used_points > 0:
            balance = await ClientBalanceRepository.get_by_client_id(db, appointment_data.id_client)
            if not balance:
                raise HTTPException(status_code=404, detail="Balance not found")

            # Сумма used_points в активных appointments (рассчитываем на лету)
            active_appointments = await AppointemntRepository.get_appointment_client(db, appointment_data.id_client)
            active_used_sum = 0.0
            for appt in [a for a in active_appointments if a.id_status_type in (1, 2)]:
                appt_service = await ServiceRepository.get_service(db, appt.id_services)
                active_used_sum += appt_service.price - appt.final_sum

            available_points = balance.permanent_points + balance.temporary_points - active_used_sum

            if used_points > available_points:
                raise HTTPException(status_code=400, detail="Not enough available points")

            # Списание с приоритетом temporary
            deduction = used_points
            temp_deduct = min(deduction, balance.temporary_points)
            perm_deduct = deduction - temp_deduct

            await ClientBalanceRepository.update_balance(
                db, appointment_data.id_client, permanent_delta=-perm_deduct, temporary_delta=-temp_deduct
            )

            accrual_type = await TypeAccrualRepository.get_by_title(db, 'appointment')
            direction = await DirectionRepository.get_by_title(db, 'deduction')

            if temp_deduct > 0:
                point_type = await PointTypeRepository.get_by_title(db, 'temporary')
                log_dto = PointLogsCreateDTO(
                    id_client=appointment_data.id_client,
                    id_point_type=point_type.id,
                    points=temp_deduct,
                    id_direction=direction.id,
                    id_type_accrual=accrual_type.id,
                    expiration_date=None
                )
                await point_logs_service.create_log(db, log_dto)

            if perm_deduct > 0:
                point_type = await PointTypeRepository.get_by_title(db, 'permanent')
                log_dto = PointLogsCreateDTO(
                    id_client=appointment_data.id_client,
                    id_point_type=point_type.id,
                    points=perm_deduct,
                    id_direction=direction.id,
                    id_type_accrual=accrual_type.id,
                    expiration_date=None
                )
                await point_logs_service.create_log(db, log_dto)

        new_appointment = CreateAppointment(
            id_client=appointment_data.id_client,
            id_address=appointment_data.id_address,
            date=appointment_data.date,
            id_status_type=2 if user_agent == "Admin" else 1,
            final_sum=final_sum,
            id_services=appointment_data.id_services,
            id_place_type=appointment_data.id_place_type
        )
        
        return await AppointemntRepository.create_appointment(db, new_appointment)

    async def close_appointment(self, db: AsyncSession, appointment_id: int):
        query = select(MakeAppointmentModel).where(MakeAppointmentModel.id == appointment_id)
        result = await db.execute(query)
        appointment = result.scalar_one_or_none()
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        if appointment.id_status_type not in (1, 2):
            raise HTTPException(status_code=400, detail="Only active appointments can be closed")
        
        update_data = UpdateAppointment(id=appointment_id, id_status_type=3)
        updated_appointment = await AppointemntRepository.update_appointment(db, update_data)
        
        if not updated_appointment:
            raise HTTPException(status_code=500, detail="Failed to update appointment")
        
        points_to_add = appointment.final_sum * 0.07
        await ClientBalanceRepository.update_balance(db, appointment.id_client, permanent_delta=points_to_add)
        
        accrual_type = await TypeAccrualRepository.get_by_title(db, 'appointment')
        direction = await DirectionRepository.get_by_title(db, 'accrual')
        point_type = await PointTypeRepository.get_by_title(db, 'permanent')
        log_dto = PointLogsCreateDTO(
            id_client=appointment.id_client,
            id_point_type=point_type.id,
            points=points_to_add,
            id_direction=direction.id,
            id_type_accrual=accrual_type.id,
            expiration_date=None
        )
        await point_logs_service.create_log(db, log_dto)
        
        closed_count_query = select(func.count(MakeAppointmentModel.id)).where(
            and_(
                MakeAppointmentModel.id_client == appointment.id_client,
                MakeAppointmentModel.id_status_type == 3
            )
        )
        closed_count = (await db.execute(closed_count_query)).scalar() or 0
        
        if closed_count == 1:
            client = await ClientRepository.get_client(db, appointment.id_client)
            referral = await ReferralsRepository.get_referrals_phone(db, client.phone)
            if referral:
                inviter_id = referral.id_client
                await ClientBalanceRepository.update_balance(db, inviter_id, permanent_delta=500)
                
                accrual_type_ref = await TypeAccrualRepository.get_by_title(db, 'referral')
                log_dto_inv = PointLogsCreateDTO(
                    id_client=inviter_id,
                    id_point_type=point_type.id,
                    points=500,
                    id_direction=direction.id,
                    id_type_accrual=accrual_type_ref.id,
                    expiration_date=None
                )
                await point_logs_service.create_log(db, log_dto_inv)
        
        return updated_appointment

    async def cancel_appointment(self, db: AsyncSession, appointment_id: int):
        query = select(MakeAppointmentModel).where(MakeAppointmentModel.id == appointment_id)
        result = await db.execute(query)
        appointment = result.scalar_one_or_none()
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        if appointment.id_status_type not in (1, 2):
            raise HTTPException(status_code=400, detail="Only active appointments can be cancelled")
        
        update_data = UpdateAppointment(id=appointment_id, id_status_type=4)
        updated_appointment = await AppointemntRepository.update_appointment(db, update_data)
        
        if not updated_appointment:
            raise HTTPException(status_code=500, detail="Failed to update appointment")
        
        service = await ServiceRepository.get_service(db, appointment.id_services)
        used_points = service.price - appointment.final_sum  # Рассчитываем на лету
        
        if used_points > 0:
            # Возврат только permanent (temporary не возвращаем)
            await ClientBalanceRepository.update_balance(db, appointment.id_client, permanent_delta=used_points)
            
            accrual_type = await TypeAccrualRepository.get_by_title(db, 'appointment')  # Или 'cancel', если есть
            direction = await DirectionRepository.get_by_title(db, 'accrual')
            point_type = await PointTypeRepository.get_by_title(db, 'permanent')
            log_dto = PointLogsCreateDTO(
                id_client=appointment.id_client,
                id_point_type=point_type.id,
                points=used_points,
                id_direction=direction.id,
                id_type_accrual=accrual_type.id,
                expiration_date=None
            )
            await point_logs_service.create_log(db, log_dto)
        
        return updated_appointment

    async def get_appointment_client(self, db:AsyncSession, client_id:int):
        appointments = await AppointemntRepository.get_appointment_client(db, client_id)

        client = await ClientRepository.get_client(db, client_id)
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
        now = datetime.now()
        result = sorted(result, key=lambda x: abs(x.date - now))
        return result
    
    async def get_appointments(self, db:AsyncSession):
        appointments = await AppointemntRepository.get_appointments(db)
        
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
        now = datetime.now()
        result = sorted(result, key=lambda x: abs(x.date - now))
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
        now = datetime.now()
        result = sorted(result, key=lambda x: abs(x.date - now))
        return result
