from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PointLogsCreateDTO(BaseModel):
    id_client: int
    id_point_type: int
    points: float
    id_direction: int
    id_type_accrual: int  # Учёл опечатку из модели (accural вместо accrual)
    expiration_date: Optional[date] = None

class PointLogsUI(BaseModel):
    id: int
    point_type_title: str  # title из point_type
    points: float
    direction_title: str  # title из direction
    type_accrual_title: str  # title из type_accrual
    expiration_date: Optional[date]
    created_at: datetime