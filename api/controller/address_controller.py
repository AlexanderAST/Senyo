from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.service.address_service import AddressService
from api.repository.address_repository import AddressesRepository
from api.dto.address_dto import AddressCreateDTO, AddressDTO, UpdateAddressDTO

router = APIRouter()
address_service = AddressService(AddressesRepository())

@router.post("/address", response_model=AddressDTO)
async def create_address(address:AddressCreateDTO, db:AsyncSession=Depends(get_db)):
    try:
        address = await address_service.create_address(db, address)
        return AddressDTO(
            id=address.id,
            address= address.address,
            id_client=address.id_client,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/address")
async def delete_address(id:int, db:AsyncSession = Depends(get_db)):
    try:
        result = await address_service.delete_address(db, id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/address")
async def update_address(address:UpdateAddressDTO, db:AsyncSession = Depends(get_db)):
    try:
        await address_service.update_address(db, address)
        return {"status":"updated success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))