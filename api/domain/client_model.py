from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base
from .gender_model import GenderModel

class ClientModel(Base):
    __tablename__ = "client"
    
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    phone = Column(String)
    id_gender = Column(Integer, ForeignKey(GenderModel.id))
    telegram_id = Column(Integer)
    
    gender = relationship(GenderModel, foreign_keys=[id_gender])