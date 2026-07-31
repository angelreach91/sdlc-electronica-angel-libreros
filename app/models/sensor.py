from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Sensor(Base):
    """Representa un sensor registrado en SensorHub."""

    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    sensor_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    unit: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    def __repr__(self) -> str:
        return (
            "Sensor("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"sensor_type={self.sensor_type!r}, "
            f"unit={self.unit!r}, "
            f"is_active={self.is_active!r}"
            ")"
        )