from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.place_type_dto import CreatePlaceType,PlaceTypeResponse
from api.repository.place_type_repository import PlaceTypeRepository  

class PlaceTypeService:
    
    async def create_place_type(self, db:AsyncSession, place_type:CreatePlaceType):
        return await PlaceTypeRepository.create_place_type(db,place_type)
    
    async def get_all_place_types(self, db: AsyncSession) -> list[PlaceTypeResponse]:
        place_types = await PlaceTypeRepository.get_all_place_types(db)
        return [PlaceTypeResponse(id=pt.id, title=pt.title) for pt in place_types]