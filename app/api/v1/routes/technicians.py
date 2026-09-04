from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.technician import TechnicianCreate, TechnicianRead
from app.services.technician_service import create_technician, list_technicians

router = APIRouter()


@router.post("/technicians", response_model=TechnicianRead)
async def create_technician_endpoint(technician_data: TechnicianCreate, db: AsyncSession = Depends(get_db)):
    return await create_technician(db, technician_data)


@router.get("/technicians", response_model=list[TechnicianRead])
async def list_technicians_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_technicians(db)
