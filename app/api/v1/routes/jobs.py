from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.job import JobCreate, JobRead
from app.services.job_service import create_job, list_jobs, get_job
from app.services.matching_service import auto_assign_job

router = APIRouter()


@router.post("/jobs", response_model=JobRead)
async def create_job_endpoint(job_data: JobCreate, db: AsyncSession = Depends(get_db)):
    return await create_job(db, job_data)


@router.get("/jobs", response_model=list[JobRead])
async def list_jobs_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_jobs(db)


@router.get("/jobs/{job_id}", response_model=JobRead)
async def get_job_endpoint(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs/{job_id}/assign", response_model=JobRead)
async def assign_job_endpoint(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await get_job(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    assigned_job = await auto_assign_job(db, job)
    if assigned_job is None:
        raise HTTPException(status_code=409, detail="No available technician found")

    return assigned_job
