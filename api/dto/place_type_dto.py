from pydantic import BaseModel


class CreatePlaceType(BaseModel):
    title:str

class PlaceTypeResponse(BaseModel):
    id: int
    title: str