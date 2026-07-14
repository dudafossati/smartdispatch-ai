from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.job import JobStatus


class JobCreate(BaseModel):
    pickup_address: str
    dropoff_address: str


class JobRead(BaseModel):
    id: int
    status: JobStatus
    pickup_address: str
    dropoff_address: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
