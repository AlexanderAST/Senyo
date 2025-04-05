from sqlalchemy import Integer, Column, String
from api.database import Base

class DirectionModel(Base):
    __tablename__ = "direction"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)