from pydantic import BaseModel, ConfigDict

class StationCreate(BaseModel):
    name: str
    location: tuple[str, str]
    option: int

class Station(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(arbitrary_types_allowed=True)

class nearstationresponse(BaseModel):
    stations: list[Station] 
    distance: float