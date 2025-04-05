from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

class ClientModel(Base):
    __tablename__= "client"
    
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    id_gender = Column(Integer, ForeignKey('gender.id'))
    telegram_id = Column(Integer),
    
    referrals = relationship('refferals', backref='client')