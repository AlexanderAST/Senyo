from api.dto.address_dto import AddressDTO
from pydantic import BaseModel
from typing import Optional

class ClientCreateDTO(BaseModel):
    telegram_id: int

class ClientUpdateDTO(BaseModel):
    id: int
    surname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    id_gender: Optional[int] = None

class ClientUI(BaseModel):
    id: int
    surname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    gender:Optional[str] = None
    permanent_points:float
    temporary_point:float
    addresses: list[AddressDTO]
