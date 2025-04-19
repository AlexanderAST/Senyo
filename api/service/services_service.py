from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.services_repository import ServiceRepository
from api.dto.services_dto import CreateService


class ServicesService:
    def __init__(self, service_repository:ServiceRepository):
        self.service_repository = service_repository
        
    
    async def create_service(self, db:AsyncSession, service = CreateService):
        return await self.service_repository.create_service(db, service)