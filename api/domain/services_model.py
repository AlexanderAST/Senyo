from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from api.database import Base

class ServicesModel(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer)
    duration = Column(TIMESTAMP)
    title = Column(String)
    subtitle = Column(String)