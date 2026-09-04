from datetime import datetime
from typing import TYPE_CHECKING
import enum

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.technician import Technician


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[JobStatus] = mapped_column(
        SQLAlchemyEnum(JobStatus, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=JobStatus.PENDING,
    )
    site_address: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    technician_id: Mapped[int | None] = mapped_column(ForeignKey("technicians.id"), nullable=True)
    technician: Mapped["Technician | None"] = relationship("Technician", back_populates="jobs")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
