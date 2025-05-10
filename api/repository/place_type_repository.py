from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.dto.place_type_dto import CreatePlaceType
from api.domain.place_type_model import PlaceTypeModel

class PlaceTypeRepository:

    @classmethod
    async def create_place_type(cls, db: AsyncSession, place_type: CreatePlaceType):
        place = PlaceTypeModel(title=place_type.title)
        db.add(place)
        await db.commit()
        await db.refresh(place)
        return place

    @classmethod
    async def get_place_type(cls, db: AsyncSession, place_type_id: int) -> PlaceTypeModel | None:
        return await db.get(PlaceTypeModel, place_type_id)

    @classmethod
    async def get_all_place_types(cls, db: AsyncSession) -> list[PlaceTypeModel]:
        result = await db.execute(select(PlaceTypeModel))
        return result.scalars().all()
