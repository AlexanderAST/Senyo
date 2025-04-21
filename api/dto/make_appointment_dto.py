from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class CreateAppointment(BaseModel):
    id_client:int
    id_address:int
    date:datetime
    title:str
    id_status_type:int
    final_sum:float
    id_services:int
    id_place_type:int
    @field_validator("date")
    def convert_to_naive(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value
    


class RequestAppointment(BaseModel):
    id_client:int
    id_address:int
    date:datetime
    title:str
    final_sum:float
    id_services:int
    id_place_type:int
    
    

class UpdateAppointment(BaseModel):
    id:int
    id_client:Optional[int]= None
    id_address:Optional[int] = None
    date:Optional[datetime] = None
    title:Optional[str] = None
    id_status_type:Optional[int] = None
    final_sum:Optional[float] = None
    id_services:Optional[int] = None
    id_place_type:Optional[int] = None
    @field_validator("date")
    def convert_to_naive(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value