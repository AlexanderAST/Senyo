from pydantic import BaseModel

class CreateReferralRequestDTO(BaseModel):
    id_client:int
    refferal_phone:str

class CreateReferralDTO(BaseModel):
    id_client:int
    refferal_phone:str
    is_active:bool
    


class ReferralsDTO(BaseModel):
    id:int
    id_client:int
    refferal_phone:str
    is_active:bool
    status:str