from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from api.database import Base

class ReferralsModel(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey('client.id'))
    referral_phone = Column(String)
    is_active = Column(Boolean)