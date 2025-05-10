from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.domain.client_balance import ClientBalanceModel

class ClientBalanceRepository:

    @classmethod
    async def get_by_client_id(cls, db: AsyncSession, client_id: int) -> ClientBalanceModel | None:
        query = select(ClientBalanceModel).where(ClientBalanceModel.id_client == client_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def update_balance(cls, db: AsyncSession, client_id: int, permanent_delta: float = 0.0, temporary_delta: float = 0.0) -> ClientBalanceModel | None:
        balance = await cls.get_by_client_id(db, client_id)
        if not balance:
            return None

        balance.permanent_points += permanent_delta
        balance.temporary_points += temporary_delta

        await db.commit()
        await db.refresh(balance)
        return balance

    @classmethod
    async def create_balance(cls, db: AsyncSession, client_id: int, permanent: float = 0.0, temporary: float = 0.0) -> ClientBalanceModel:
        new_balance = ClientBalanceModel(
            id_client=client_id,
            permanent_points=permanent,
            temporary_points=temporary
        )
        db.add(new_balance)
        await db.commit()
        await db.refresh(new_balance)
        return new_balance
