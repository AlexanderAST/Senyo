from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.place_type_dto import CreatePlaceType
from api.repository.place_type_repository import PlaceTypeRepository

class PlaceTypeService:
    
    async def create_place_type(self, db:AsyncSession, place_type:CreatePlaceType):
        return await PlaceTypeRepository.create_place_type(db,place_type)