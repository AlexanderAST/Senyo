from sqlalchemy import Column, Integer, Float, TIMESTAMP, ForeignKey
from api.database import Base
from sqlalchemy.orm import relationship
from .client_model import ClientModel

class ClientBalanceModel(Base):
    __tablename__ = "client_balances"
    
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey(ClientModel.id))
    client = relationship(ClientModel, foreign_keys=[id_client])
    permanent_points = Column(Float)
    temporary_points = Column(Float)
    updated_at = Column(TIMESTAMP)
    
    