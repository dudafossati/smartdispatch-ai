from pydantic import BaseModel, ConfigDict

from app.models.technician import TechnicianStatus


class TechnicianCreate(BaseModel):
    name: str
    skills: list[str]
    latitude: float
    longitude: float


class TechnicianRead(BaseModel):
    id: int
    name: str
    status: TechnicianStatus
    skills: list[str]
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)
