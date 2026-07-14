from datetime import datetime
import enum

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[JobStatus] = mapped_column( SQLAlchemyEnum(JobStatus, values_callable=lambda enum_cls: [e.value for e in enum_cls]),default=JobStatus.PENDING)
    pickup_address: Mapped[str] = mapped_column(String(255))
    dropoff_address: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
