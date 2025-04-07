from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.database import Base

class StatusTypeModel(Base):
    __tablename__ = "status_type"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)