from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from typing import Optional

class CreateAppointment(BaseModel):
    id_client:int
    id_address: Optional[int] = None
    date:datetime
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
    id_address:Optional[int]= None
    date:datetime
    final_sum:float
    id_services:int
    id_place_type:int
    @model_validator(mode='after')
    def validate_address(self) -> 'RequestAppointment':
        if self.id_place_type == 2 and self.id_address is None:
            raise ValueError("Поле 'id_address' обязательно при выборе визита 'на дому' (id_place_type = 2)")
        return self
    
    

class UpdateAppointment(BaseModel):
    id:int
    id_client:Optional[int]= None
    id_address:Optional[int] = None
    date:Optional[datetime] = None
    id_status_type:Optional[int] = None
    final_sum:Optional[float] = None
    id_services:Optional[int] = None
    id_place_type:Optional[int] = None
    @field_validator("date")
    def convert_to_naive(cls, value: datetime) -> datetime:
        if value.tzinfo is not None:
            return value.replace(tzinfo=None)
        return value

class AppointmentUI(BaseModel):
    id:int
    client_name:str
    client_phone:str
    client_gender:str
    client_points:float
    service_price:float
    service_name:str
    place:str
    status:str
    date:datetime
    final_sum:float
    used_points: Optional[int] = None