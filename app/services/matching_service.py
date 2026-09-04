import math

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job, JobStatus
from app.models.technician import Technician, TechnicianStatus


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance in km between two lat/long points."""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = ((math.sin(delta_lat/2))**2) + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


async def find_closest_available_technician(db: AsyncSession, job: Job) -> Technician | None:
    result = await db.execute(
        select(Technician).where(Technician.status == TechnicianStatus.AVAILABLE)
    )
    available_technicians = result.scalars().all()
    if not available_technicians:
        return None
    closest = min(
        available_technicians,
        key=lambda tech: haversine_distance(job.latitude, job.longitude, tech.latitude, tech.longitude),
    )
    return closest


async def auto_assign_job(db: AsyncSession, job: Job) -> Job | None:
    technician = await find_closest_available_technician(db, job)
    if technician is None:
        return None

    job.technician_id = technician.id
    job.status = JobStatus.ASSIGNED
    technician.status = TechnicianStatus.BUSY

    await db.commit()
    await db.refresh(job)
    return job
