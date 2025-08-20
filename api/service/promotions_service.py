from api.repository.client_balance_repository import ClientBalanceRepository
from api.repository.client_repository import ClientRepository
from api.repository.gender_repository import GenderRepository
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.promotions_dto import PromotionsCreate, PromotionsUI
from api.repository.promotions_repository import PromotionsRepository, PromotionsUpdate
from sqlalchemy import func, and_
from api.domain.make_appointment_model import MakeAppointmentModel  # Для query
from api.repository.point_type_repository import PointTypeRepository
from api.repository.direction_repository import DirectionRepository
from api.repository.type_accrual_repository import TypeAccrualRepository
from api.service.point_logs_service import PointLogsService
from api.dto.point_logs_dto import PointLogsCreateDTO


point_logs_service = PointLogsService()


class PromotionsService:

        
    async def create_promotion(self, db:AsyncSession, new_promotion:PromotionsCreate):
        return await PromotionsRepository.create_promotions(db, new_promotion)
    
    async def delete_promotiom(self, db:AsyncSession, id:int):
        id = await PromotionsRepository.delete_promotion(db, id)
        return {"status":"success", "id":id}
    
    async def get_promotions(self, db:AsyncSession) -> list[PromotionsUI]:
        promotions = await PromotionsRepository.get_promotions(db)
        result =[]

        for a in promotions:
            gender = await GenderRepository.get_gender_by_id(db, a.id_gender)
            
            result.append(PromotionsUI(
                id = a.id,
                title = a.title,
                description = a.description,
                added_points = a.added_points,
                gender =  gender.title,
                start_date = a.start_date,
                expiration_date = a.expiration_date,
            ))
        
        today = date.today()
        result = sorted(result, key=lambda x: abs(x.start_date - today))
        return result

    async def update_promotions(self, db:AsyncSession, promotion:PromotionsUpdate):
        new_promotion = await PromotionsRepository.update_promptions(db, promotion)
        
        return new_promotion
    
    async def daily_promo_check(self, db: AsyncSession):
        today = date.today()

        # Начисление для start_date == today
        starting_promos = await PromotionsRepository.get_by_start_date(db, today)  # Добавь метод в repo: select where start_date == today
        for promo in starting_promos:
            clients = await ClientRepository.get_clients_by_gender(db, promo.id_gender)  # Добавь метод в ClientRepository: select where id_gender == id_gender
            for client in clients:
                await ClientBalanceRepository.update_balance(db, client.id, temporary_delta=promo.added_points)
                
                # Лог
                accrual_type = await TypeAccrualRepository.get_by_title(db, 'promo')
                direction = await DirectionRepository.get_by_title(db, 'accrual')
                point_type = await PointTypeRepository.get_by_title(db, 'temporary')
                log_dto = PointLogsCreateDTO(
                    id_client=client.id,
                    id_point_type=point_type.id,
                    points=promo.added_points,
                    id_direction=direction.id,
                    id_type_accural=accrual_type.id,
                    expiration_date=promo.expiration_date
                )
                await point_logs_service.create_log(db, log_dto)

        # Списание для expiration_date == today
        ending_promos = await PromotionsRepository.get_by_expiration_date(db, today)  # Добавь метод
        for promo in ending_promos:
            clients = await ClientRepository.get_clients_by_gender(db, promo.id_gender)
            for client in clients:
                balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
                to_deduct = min(promo.added_points, balance.temporary_points)  # Max до начисленного
                await ClientBalanceRepository.update_balance(db, client.id, temporary_delta=-to_deduct)
                
                # Лог
                direction_ded = await DirectionRepository.get_by_title(db, 'deduction')
                log_dto = PointLogsCreateDTO(
                    id_client=client.id,
                    id_point_type=point_type.id,
                    points=to_deduct,
                    id_direction=direction_ded.id,
                    id_type_accural=accrual_type.id,
                    expiration_date=promo.expiration_date
                )
                await point_logs_service.create_log(db, log_dto)    