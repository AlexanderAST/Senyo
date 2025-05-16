from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.address_repository import AddressesRepository
from api.repository.make_appointment_repository import AppointemntRepository
from api.dto.address_dto import AddressCreateDTO, UpdateAddressDTO


class AddressService:
   
    
    async def create_address(self, db:AsyncSession, address_data:AddressCreateDTO):
        
        return await AddressesRepository.create_address(db,address_data)
        
    
    async def delete_address(self, db:AsyncSession, id:int):

        await AppointemntRepository.nullify_address_references(db, id)
        id = await AddressesRepository.delete_address(db, id)
        
        return {"status":"success", "id":id}
    
    async def update_address(self, db:AsyncSession, address:UpdateAddressDTO):
        new_address = await AddressesRepository.update_address(db, address)
        if new_address is None:
            raise HTTPException(status_code=404,detail="Address not found")
        
        return new_address
    
    