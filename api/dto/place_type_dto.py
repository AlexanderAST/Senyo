from pydantic import BaseModel


class CreatePlaceType(BaseModel):
    title:str