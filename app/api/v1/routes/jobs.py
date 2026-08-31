from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.job import JobCreate, JobRead
from app.services.job_service import create_job, list_jobs

router = APIRouter()


@router.post("/jobs", response_model=JobRead)
async def create_job_endpoint(job_data: JobCreate, db: AsyncSession = Depends(get_db)):
    return await create_job(db, job_data)


@router.get("/jobs", response_model=list[JobRead])
async def list_jobs_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_jobs(db)
