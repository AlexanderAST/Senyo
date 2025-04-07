from sqlalchemy import Column, Integer, Float, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base
from .client_model import ClientModel
from .point_type_model import PointTypeModel
from .direction_model import DirectionModel
from .type_accrual_model import TypeAccrualModel




class PointLogsModel(Base):
    __tablename__ = "point_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    id_client = Column(Integer, ForeignKey(ClientModel.id))
    client = relationship(ClientModel, foreign_keys=[id_client])
    id_point_type = Column(Integer, ForeignKey(PointTypeModel.id))
    point_type = relationship(PointTypeModel, foreign_keys=[id_point_type])
    points = Column(Float)
    id_direction = Column(Integer, ForeignKey(DirectionModel.id))
    direction = relationship(DirectionModel, foreign_keys=[id_direction])
    id_type_accural = Column(Integer, ForeignKey(TypeAccrualModel.id))
    type_accrual = relationship(TypeAccrualModel, foreign_keys=[id_type_accural])
    expiration_date = Column(Date)
    created_at = Column(TIMESTAMP)