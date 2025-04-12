from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.repository.address_repository import AddressesRepository
from api.dto.address_dto import AddressCreateDTO, UpdateAddressDTO


class AddressService:
    def __init__(self, address_repository:AddressesRepository):
        self.address_repository = address_repository
        
    
    async def create_address(self, db:AsyncSession, address_data:AddressCreateDTO):
        
        return await self.address_repository.create_address(db,address_data)
        
    
    async def delete_address(self, db:AsyncSession, id:int):
        
        id = await self.address_repository.delete_address(db, id)
        
        return {"status":"success", "id":id}
    
    async def update_address(self, db:AsyncSession, address:UpdateAddressDTO):
        new_address = await self.address_repository.update_address(db, address)
        if new_address is None:
            raise HTTPException(status_code=404,detail="Address not found")
        
        return new_address