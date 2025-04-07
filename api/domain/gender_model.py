from sqlalchemy import Column, Integer, String
from api.database import Base

class GenderModel(Base):
    __tablename__ = "gender"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)