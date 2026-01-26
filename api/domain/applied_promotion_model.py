from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base
from .client_model import ClientModel
from .promotion_model import PromotionModel

class AppliedPromotionModel(Base):
    __tablename__ = "applied_promotions"
    
    id = Column(Integer,primary_key = True, index = True)
    id_client = Column(Integer, ForeignKey(ClientModel.id))
    id_promotion = Column(Integer,ForeignKey(PromotionModel.id))
    applied_date = Column(Date)
    
    client = relationship(ClientModel, foreign_keys =[id_client])
    promotion = relationship(PromotionModel,foreign_keys = [id_promotion])