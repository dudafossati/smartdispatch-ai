from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.schemas.job import JobCreate


async def create_job(db: AsyncSession, job_data: JobCreate) -> Job:
    new_job = Job(
        pickup_address=job_data.pickup_address,
        dropoff_address=job_data.dropoff_address
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job