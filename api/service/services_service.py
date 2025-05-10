from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.services_repository import ServiceRepository
from api.dto.services_dto import CreateService


class ServicesService:
    
    async def create_service(self, db:AsyncSession, service = CreateService):
        return await ServiceRepository.create_service(db, service)