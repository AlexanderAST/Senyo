from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base
from .client_model import ClientModel


class AddressesModel(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    id_client = Column(Integer, ForeignKey(ClientModel.id))

    client = relationship(ClientModel, foreign_keys=[id_client])