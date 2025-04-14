from pydantic import BaseModel
from datetime import date

class PromotionsCreate(BaseModel):
    title:str
    description:str
    added_points:int
    id_gender:int
    start_date:date
    expiration_date:date