from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Reading(Base):
    """Representa una lectura almacenada de temperatura y humedad."""

    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    humidity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            "Reading("
            f"id={self.id!r}, "
            f"sensor_id={self.sensor_id!r}, "
            f"temperature={self.temperature!r}, "
            f"humidity={self.humidity!r}, "
            f"received_at={self.received_at!r}"
            ")"
        )