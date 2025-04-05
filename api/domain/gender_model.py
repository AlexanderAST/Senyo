from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from api.database import Base

class GenderModel(Base):
    __tablename__ = "gender"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    client = relationship('client', backref='gender')
    promotions = relationship('promotions', backref='gender')