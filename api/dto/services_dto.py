from pydantic import BaseModel
from datetime import time


class CreateService(BaseModel):
    price: int
    duration:time
    title:str
    subtitle:str