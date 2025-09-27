from http.client import HTTPException
from api.dto.address_dto import AddressDTO
from api.repository.address_repository import AddressesRepository
from api.repository.client_balance_repository import ClientBalanceRepository
from api.repository.gender_repository import GenderRepository
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.client_repository import ClientRepository
from api.dto.client_dto import ClientCreateDTO, ClientUI, ClientUpdateDTO
from api.dto.referral_dto import UpdateReferralDTO
from api.service.referrals_service import ReferralsService
from api.repository.refferal_repository import ReferralsRepository
from api.dto.referral_dto import UpdateReferralDTO
from api.repository.point_type_repository import PointTypeRepository
from api.repository.direction_repository import DirectionRepository
from api.repository.type_accrual_repository import TypeAccrualRepository
from api.service.point_logs_service import PointLogsService
from api.dto.point_logs_dto import PointLogsCreateDTO
from datetime import date
from api.repository.promotions_repository import PromotionsRepository
from api.repository.applied_promotion_repository import AppliedPromotionRepository
import logging

logger = logging.getLogger(__name__)
referrals_service = ReferralsService()
point_logs_service = PointLogsService()
class ClientService:
            
    async def create_client(self, db: AsyncSession, client_data: ClientCreateDTO):
        try:
            client = await ClientRepository.create_client(db, client_data)
            logger.info(f"Client created: ID {client.id}")  # Лог: успех создания клиента
        except Exception as e:
            logger.error(f"Error in ClientRepository.create_client: {str(e)}")  # Лог: ошибка на создании клиента
            raise  # Поднимаем, чтобы router поймал

        try:
            await ClientBalanceRepository.create_balance(
                db=db,
                client_id=client.id,
                permanent=0.0,
                temporary=0.0
            )
            logger.info(f"Balance created for client {client.id}")
        except Exception as e:
            logger.error(f"Error in create_balance: {str(e)}")
            raise

        try:
            await self.apply_active_promotions(db, client.id)
            logger.info(f"Promotions applied for client {client.id}")
        except Exception as e:
            logger.error(f"Error in apply_active_promotions: {str(e)}")
            raise

        return client
    
    async def apply_active_promotions(self, db:AsyncSession, client_id : int):
        today = date.today()
        client = await ClientRepository.get_client(db,client_id)
        if not client:
            return
        
        active_promos = await PromotionsRepository.get_active_for_gender(db,client.id_gender, today)
        
        for promo in active_promos:
            applied = await AppliedPromotionRepository.get_by_client_and_promo(db,client_id,promo.id)
            if applied:
                continue
            
            await ClientBalanceRepository.update_balance(db,client_id,temporary_delta=promo.added_points)
            
            accrual_type = await TypeAccrualRepository.get_by_title(db, 'promo')
            direction = await DirectionRepository.get_by_title(db, 'accrual')
            point_type = await PointTypeRepository.get_by_title(db, 'temporary')
            log_dto = PointLogsCreateDTO(
                id_client=client_id,
                id_point_type=point_type.id,
                points=promo.added_points,
                id_direction=direction.id,
                id_type_accural=accrual_type.id,
                expiration_date=promo.expiration_date
            )
            await point_logs_service.create_log(db,log_dto)
            
            await AppliedPromotionRepository.create_applied(db,client_id, promo.id, today)
    
    async def update_client(self, db:AsyncSession, client_data: ClientUpdateDTO):       
        client = await ClientRepository.update_client(db, client_data)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
                
        if client_data.phone is not None:
            referrals = await referrals_service.get_referrals_phone(db, client_data.phone)
            
            if referrals is not None:
                referral_data = UpdateReferralDTO(id=referrals, is_active=True)
                await referrals_service.update_referrals_phone(db,referral_data)
                
                # Начислить 500 permanent рефералу (новому клиенту)
                await ClientBalanceRepository.update_balance(db, client.id, permanent_delta=500.0)
                
                # Лог для начисления
                accrual_type = await TypeAccrualRepository.get_by_title(db, 'referral')
                direction = await DirectionRepository.get_by_title(db, 'accrual')
                point_type = await PointTypeRepository.get_by_title(db, 'permanent')
                log_dto = PointLogsCreateDTO(
                    id_client=client.id,
                    id_point_type=point_type.id,
                    points=500.0,
                    id_direction=direction.id,
                    id_type_accural=accrual_type.id,
                    expiration_date=None
                )
                await point_logs_service.create_log(db, log_dto)
                
        
        return client
    
    async def get_info(self, db: AsyncSession, client_id: int) -> ClientUI:
        client = await ClientRepository.get_client(db, client_id)
        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
        addresses = await AddressesRepository.get_by_client_id(db, client.id)
        gender = await GenderRepository.get_gender_by_id(db, client.id_gender)

        address_dtos = [AddressDTO(
            id=a.id,
            address=a.address,
            id_client=a.id_client,
        ) for a in addresses]

        return ClientUI(
            id=client.id,
            surname=client.surname,
            name=client.name,
            phone=client.phone,
            gender=gender.title if gender else None,
            permanent_points=balance.permanent_points if balance else 0.0,
            temporary_point=balance.temporary_points if balance else 0.0,
            addresses=address_dtos,
            telegram_id = client.telegram_id
        )
    
    async def get_by_telegram_id(self, db: AsyncSession, telegram_id: int) -> ClientUI:
        client = await ClientRepository.get_by_telegram_id(db, telegram_id)

        balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
        addresses = await AddressesRepository.get_by_client_id(db, client.id)
        gender = await GenderRepository.get_gender_by_id(db, client.id_gender)

        address_dtos = [AddressDTO(
            id=a.id,
            address=a.address,
            id_client=a.id_client,
        ) for a in addresses]

        return ClientUI(
            id=client.id,
            surname=client.surname,
            name=client.name,
            phone=client.phone,
            gender=gender.title if gender else None,
            permanent_points=balance.permanent_points if balance else 0.0,
            temporary_point=balance.temporary_points if balance else 0.0,
            addresses=address_dtos,
            telegram_id=client.telegram_id
        )
    
    async def get_clients(self, db: AsyncSession) -> list[ClientUI]:
        clients = await ClientRepository.get_clients(db)

        result = []

        for client in clients:
            balance = await ClientBalanceRepository.get_by_client_id(db, client.id)
            addresses = await AddressesRepository.get_by_client_id(db, client.id)
            gender = await GenderRepository.get_gender_by_id(db, client.id_gender)

            address_dtos = [AddressDTO(
                id=a.id,
                address=a.address,
                id_client=a.id_client,
            ) for a in addresses]

            result.append(ClientUI(
                id=client.id,
                surname=client.surname,
                name=client.name,
                phone=client.phone,
                gender=gender.title if gender else None,
                permanent_points=balance.permanent_points if balance else 0.0,
                temporary_point=balance.temporary_points if balance else 0.0,
                addresses=address_dtos,
                telegram_id = client.telegram_id
            ))

        return result
    
    async def add_points_to_client(
     self,
     db: AsyncSession,
     client_id: int,
     permanent_delta: float = 0.0,
     temporary_delta: float = 0.0,
     deduct_temporary_first: bool = True
    ):  
     updated_balance = await ClientBalanceRepository.update_balance(
         db=db,
         client_id=client_id,
         permanent_delta=permanent_delta,
         temporary_delta=temporary_delta,
         deduct_temporary_first=deduct_temporary_first
     )

     accrual_type = await TypeAccrualRepository.get_by_title(db, 'manual')

     # Лог для permanent
     if permanent_delta != 0:
         direction_title = 'accrual' if permanent_delta > 0 else 'deduction'
         direction = await DirectionRepository.get_by_title(db, direction_title)
         point_type = await PointTypeRepository.get_by_title(db, 'permanent')
         log_dto = PointLogsCreateDTO(
             id_client=client_id,
             id_point_type=point_type.id,
             points=abs(permanent_delta),
             id_direction=direction.id,
             id_type_accural=accrual_type.id,
             expiration_date=None  # Для permanent нет expiration
         )
         await point_logs_service.create_log(db, log_dto)

     # Лог для temporary
     if temporary_delta != 0:
         direction_title = 'accrual' if temporary_delta > 0 else 'deduction'
         direction = await DirectionRepository.get_by_title(db, direction_title)
         point_type = await PointTypeRepository.get_by_title(db, 'temporary')
         log_dto = PointLogsCreateDTO(
             id_client=client_id,
             id_point_type=point_type.id,
             points=abs(temporary_delta),
             id_direction=direction.id,
             id_type_accural=accrual_type.id,
             expiration_date=None  # Укажи, если есть логика для expiration
         )
         await point_logs_service.create_log(db, log_dto)

     return updated_balance