from pydantic import BaseModel
from typing import Optional

class CreateReferralRequestDTO(BaseModel):
    id_client:int
    refferal_phone:str

class ReferralDTO(BaseModel):
    id_client:int
    refferal_phone:str
    is_active:bool

class UpdateReferralDTO(BaseModel):
    id:int
    id_client:Optional[int] = None
    refferal_phone:Optional[str] = None
    is_active:Optional[bool] = None
    