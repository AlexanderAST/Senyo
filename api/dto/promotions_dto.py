from pydantic import BaseModel
from datetime import date
from typing import Optional

class PromotionsCreate(BaseModel):
    title:str
    description:str
    added_points:int
    id_gender:int
    start_date:date
    expiration_date:date


class PromotionsUpdate(BaseModel):
    id: int
    title:Optional[str] = None
    description:Optional[str] = None
    added_points:Optional[int] = None
    id_gender:Optional[int] = None
    start_date:Optional[date] = None
    expiration_date:Optional[date] = None