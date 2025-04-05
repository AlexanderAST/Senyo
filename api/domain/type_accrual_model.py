from sqlalchemy import Integer, Column, String
from api.database import Base

class TypeAccrualModel(Base):
    __tablename__ = "type_accrual"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)