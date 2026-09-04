from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.job import JobStatus


class JobCreate(BaseModel):
    site_address: str
    description: str
    latitude: float
    longitude: float


class JobRead(BaseModel):
    id: int
    status: JobStatus
    site_address: str
    description: str
    latitude: float
    longitude: float
    technician_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
