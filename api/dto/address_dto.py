from pydantic import BaseModel

class AddressCreateDTO(BaseModel):
    address: str
    id_client: int
    


class AddressDTO(BaseModel):
    id: int
    address: str
    id_client: int
    status: str
    


class UpdateAddressDTO(BaseModel):
    id: int
    address: str