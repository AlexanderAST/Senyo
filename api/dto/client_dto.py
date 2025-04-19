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

