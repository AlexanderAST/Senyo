from sqlalchemy import Integer, Column, String
from api.database import Base

class PointTypeModel(Base):
    __tablename__ = "point_type"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)