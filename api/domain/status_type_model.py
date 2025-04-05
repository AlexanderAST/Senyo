from sqlalchemy import Integer, Column, String
from api.database import Base

class StatusTypeModel(Base):
    __tablename__ = "status_type"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)