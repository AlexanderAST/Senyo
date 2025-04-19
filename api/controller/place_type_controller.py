from api.database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.place_type_service import PlaceTypeService
from api.repository.place_type_repository import PlaceTypeRepository
from api.dto.place_type_dto import CreatePlaceType

router = APIRouter()

place_type_service = PlaceTypeService(PlaceTypeRepository())


@router.post("/admin/place-type")
async def create_place_type(place_type:CreatePlaceType, db:AsyncSession=Depends(get_db)):
    try:
        return await place_type_service.create_place_type(db, place_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))