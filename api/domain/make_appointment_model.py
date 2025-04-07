from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Float, String
from sqlalchemy.orm import relationship
from api.database import Base
from .client_model import ClientModel
from .addresses_model import AddressesModel
from .status_type_model import StatusTypeModel
from .services_model import ServicesModel
from .place_type_model import PlaceTypeModel

class MakeAppointmentModel(Base):
    __tablename__ = "make_appointment"
    
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey(ClientModel.id))
    client = relationship(ClientModel, foreign_keys=[id_client])
    id_address = Column(Integer, ForeignKey(AddressesModel.id))
    address = relationship(AddressesModel, foreign_keys=[id_address])
    date = Column(TIMESTAMP)
    title = Column(String)
    id_status_type = Column(Integer, ForeignKey(StatusTypeModel.id))
    status_type = relationship(StatusTypeModel, foreign_keys=[id_status_type])
    final_sum = Column(Float)
    id_services = Column(Integer, ForeignKey(ServicesModel.id))
    service = relationship(ServicesModel, foreign_keys=[id_services])
    id_place_type = Column(Integer, ForeignKey(PlaceTypeModel.id))
    place_type = relationship(PlaceTypeModel, foreign_keys=[id_place_type])