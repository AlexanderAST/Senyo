from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base
from .gender_model import GenderModel

class PromotionModel(Base):
    __tablename__ = "promotions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    added_points = Column(Float)
    id_gender = Column(Integer, ForeignKey(GenderModel.id))
    start_date = Column(Date)
    expiration_date = Column(Date)
    
    gender = relationship(GenderModel, foreign_keys=[id_gender])