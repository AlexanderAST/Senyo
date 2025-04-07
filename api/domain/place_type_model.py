from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base

class PlaceTypeModel(Base):
    __tablename__ = "place_type"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)