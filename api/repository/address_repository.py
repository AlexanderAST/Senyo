from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.addresses_model import AddressesModel
from api.dto.address_dto import AddressCreateDTO, UpdateAddressDTO


class AddressesRepository:
    @classmethod
    async def create_address(cls, db:AsyncSession, address_data: AddressCreateDTO):
        new_address = AddressesModel(
            address= address_data.address,
            id_client= address_data.id_client
        )
        
        db.add(new_address)
        await db.commit()
        await db.refresh(new_address)
        return new_address
    
    @classmethod
    async def delete_address(cls, db:AsyncSession, id:int):
        address = await db.get(AddressesModel, id)
        
        if not address:
            return None
        
        await db.delete(address)
        await db.commit()
        
        return id
    
    @classmethod
    async def update_address(cls, db:AsyncSession, address: UpdateAddressDTO):
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
    
    @classmethod
    async def get_by_client_id(cls, db: AsyncSession, client_id: int) -> list[AddressesModel]:
        result = await db.execute(
            select(AddressesModel).where(AddressesModel.id_client == client_id)
        )
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, address_id: int) -> AddressesModel | None:
        return await db.get(AddressesModel, address_id)