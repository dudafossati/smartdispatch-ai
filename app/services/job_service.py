from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.schemas.job import JobCreate


async def create_job(db: AsyncSession, job_data: JobCreate) -> Job:
    new_job = Job(
        site_address=job_data.site_address,
        description=job_data.description,
    )
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job


async def list_jobs(db: AsyncSession) -> list[Job]:
    result = await db.execute(select(Job))
    return list(result.scalars().all())


async def get_job(db: AsyncSession, job_id: int) -> Job | None:
    result = await db.execute(select(Job).where(Job.id == job_id))
    return result.scalar_one_or_none()






        
