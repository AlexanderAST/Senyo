from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from api.database import Base
from sqlalchemy.orm import relationship
from .client_model import ClientModel

class ReferralsModel(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey(ClientModel.id))
    client = relationship(ClientModel, foreign_keys=[id_client])
    referral_phone = Column(String,unique=True)
    is_active = Column(Boolean)