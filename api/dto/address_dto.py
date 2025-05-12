from typing import Optional
from pydantic import BaseModel

class AddressCreateDTO(BaseModel):
    address: str
    id_client: int
    


class AddressDTO(BaseModel):
    id: int
    address: str
    id_client: int
    status: Optional[str] = None
    


class UpdateAddressDTO(BaseModel):
    id: int
    address: str