from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.services_model import ServicesModel
from api.dto.services_dto import CreateService

class ServiceRepository:

    @classmethod
    async def create_service(cls, db: AsyncSession, service_data: CreateService) -> ServicesModel:
        new_service = ServicesModel(
            price=service_data.price,
            duration=service_data.duration,
            title=service_data.title,
            subtitle=service_data.subtitle
        )
        db.add(new_service)
        await db.commit()
        await db.refresh(new_service)
        return new_service

    @classmethod
    async def get_service(cls, db: AsyncSession, service_id: int) -> ServicesModel | None:
        return await db.get(ServicesModel, service_id)

    @classmethod
    async def get_all_services(cls, db: AsyncSession) -> list[ServicesModel]:
        result = await db.execute(select(ServicesModel))
        return result.scalars().all()

    @classmethod
    async def delete_service(cls, db: AsyncSession, service_id: int) -> bool:
        service = await db.get(ServicesModel, service_id)
        if not service:
            return False
        await db.delete(service)
        await db.commit()
        return True
