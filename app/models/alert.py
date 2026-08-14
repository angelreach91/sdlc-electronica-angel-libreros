from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Alert(Base):
    """Representa una alerta generada por una lectura anómala."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("sensors.id"),
        nullable=False,
    )
    reading_id: Mapped[int] = mapped_column(
        ForeignKey("readings.id"),
        nullable=False,
    )
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    threshold: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
