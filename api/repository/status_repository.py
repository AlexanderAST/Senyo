from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.status_type_model import StatusTypeModel

class StatusTypeRepository:

    @classmethod
    async def get_status_by_id(self, db:AsyncSession, status_id: int)-> StatusTypeModel | None:
        return await db.get(StatusTypeModel, status_id)
    
    @classmethod
    async def get_all_statuses(self, db:AsyncSession ) -> list[StatusTypeModel]:
        result = await db.execute(select(StatusTypeModel))
        return result.scalars().all()
    
    @classmethod
    async def create_status(self, db:AsyncSession, title:str) -> StatusTypeModel:
        new_status = StatusTypeModel(title = title)
        db.add(new_status)
        await db.commit()
        await db.refresh(new_status)
        return new_status
    
    @classmethod
    async def delete_status(self,db:AsyncSession, status_id:int) -> bool:
        status = await db.get(StatusTypeModel, status_id)
        if not status:
            return False
        await db.delete(status)
        await db.commit()
        return True