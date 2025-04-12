from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.addresses_model import AddressesModel
from api.dto.address_dto import AddressCreateDTO, UpdateAddressDTO


class AddressesRepository:
    async def create_address(self, db:AsyncSession, address_data: AddressCreateDTO):
        new_address = AddressesModel(
            address= address_data.address,
            id_client= address_data.id_client
        )
        
        db.add(new_address)
        await db.commit()
        await db.refresh(new_address)
        return new_address
    
    async def delete_address(self, db:AsyncSession, id:int):
        address = await db.get(AddressesModel, id)
        
        if not address:
            return None
        
        await db.delete(address)
        await db.commit()
        
        return id
    
    async def update_address(self, db:AsyncSession, address: UpdateAddressDTO):
        new_address = await db.get(AddressesModel, address.id)
        
        if not new_address:
            return None
        
        update_data = address.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if key != "id":
                setattr(new_address, key, value)
        
        await db.commit()
        await db.refresh(new_address)
        
        return new_address
        