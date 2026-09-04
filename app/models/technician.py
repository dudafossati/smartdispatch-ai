from datetime import datetime
from typing import TYPE_CHECKING
import enum

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.job import Job


class TechnicianStatus(str, enum.Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFF_DUTY = "off_duty"


class Technician(Base):
    __tablename__ = "technicians"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[TechnicianStatus] = mapped_column(
        SQLAlchemyEnum(TechnicianStatus, values_callable=lambda e: [x.value for x in e]),
        default=TechnicianStatus.AVAILABLE,
    )
    skills: Mapped[list[str]] = mapped_column(ARRAY(String))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    jobs: Mapped[list["Job"]] = relationship("Job", back_populates="technician")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
