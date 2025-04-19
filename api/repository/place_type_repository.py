from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.place_type_dto import CreatePlaceType
from api.domain.place_type_model import PlaceTypeModel

class PlaceTypeRepository:
    async def create_place_type(self,db:AsyncSession, place_type:CreatePlaceType):
        place = PlaceTypeModel(title=place_type.title)
        
        db.add(place)
        await db.commit()
        await db.refresh(place)
        return place