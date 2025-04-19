from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.services_model import ServicesModel
from api.dto.services_dto import CreateService


class ServiceRepository:
    async def create_service(self,db:AsyncSession, service_data = CreateService):
        new_service = ServicesModel(
            price = service_data.price,
            duration = service_data.duration,
            title = service_data.title,
            subtitle = service_data.subtitle
        )
        
        db.add(new_service)
        await db.commit()
        await db.refresh(new_service)
        return new_service