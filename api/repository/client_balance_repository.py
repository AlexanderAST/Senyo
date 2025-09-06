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
    async def update_balance(
        cls, 
        db: AsyncSession, 
        client_id: int, 
        permanent_delta: float = 0.0, 
        temporary_delta: float = 0.0,
        deduct_temporary_first: bool = True
    ) -> ClientBalanceModel | None:
        balance = await cls.get_by_client_id(db, client_id)
        if not balance:
            return None
    
        total_delta = permanent_delta + temporary_delta
        if total_delta < 0:
            deduction = abs(total_delta)
            if deduct_temporary_first:
                temp_deduct = min(deduction, balance.temporary_points)
                balance.temporary_points -= temp_deduct
                remaining_deduct = deduction - temp_deduct
                balance.permanent_points -= remaining_deduct
            else:
                perm_deduct = min(deduction, balance.permanent_points)
                balance.permanent_points -= perm_deduct
                remaining_deduct = deduction - perm_deduct
                balance.temporary_points -= remaining_deduct
        else:
            # Начисление: добавляем как указано
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
