from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.technician import Technician
from app.schemas.technician import TechnicianCreate


async def create_technician(db: AsyncSession, technician_data: TechnicianCreate) -> Technician:
    new_technician = Technician(
        name=technician_data.name,
        skills=technician_data.skills,
        latitude=technician_data.latitude,
        longitude=technician_data.longitude,
    )
    db.add(new_technician)
    await db.commit()
    await db.refresh(new_technician)
    return new_technician


async def list_technicians(db: AsyncSession) -> list[Technician]:
    result = await db.execute(select(Technician))
    return list(result.scalars().all())
