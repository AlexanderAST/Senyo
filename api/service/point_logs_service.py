from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.point_logs_repository import PointLogsRepository
from api.domain.point_logs_model import PointLogsModel
from api.dto.point_logs_dto import PointLogsCreateDTO, PointLogsUI

class PointLogsService:
    
    async def create_log(self, db: AsyncSession, log_data: PointLogsCreateDTO) -> PointLogsModel:
        new_log = PointLogsModel(
            id_client=log_data.id_client,
            id_point_type=log_data.id_point_type,
            points=log_data.points,
            id_direction=log_data.id_direction,
            id_type_accural=log_data.id_type_accural,  # Опечатка сохранена
            expiration_date=log_data.expiration_date
        )
        return await PointLogsRepository.create_log(db, new_log)

    async def get_logs_by_client(self, db: AsyncSession, client_id: int) -> list[PointLogsUI]:
        logs = await PointLogsRepository.get_logs_by_client_id(db, client_id)
        return [PointLogsUI(
            id=log.id,
            point_type_title=log.point_type.title if log.point_type else None,
            points=log.points,
            direction_title=log.direction.title if log.direction else None,
            type_accrual_title=log.type_accrual.title if log.type_accrual else None,
            expiration_date=log.expiration_date,
            created_at=log.created_at
        ) for log in logs]