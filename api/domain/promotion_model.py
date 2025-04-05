from sqlalchemy import Column, String, Date, Integer, ForeignKey, Float
from api.database import Base

class PromotionModel(Base):
    __tablename__ = "promotion"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    added_points = Column(Float)
    id_gender = Column(Integer, ForeignKey('gender.id'))
    start_date = Column(Date)
    expiration_date = Column(Date)