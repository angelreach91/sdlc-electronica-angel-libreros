from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.sensor_types import SensorUnit


class ReadingCreate(BaseModel):
    """Datos necesarios para registrar una lectura."""

    value: float
    unit: SensorUnit


class ReadingUpdate(BaseModel):
    """Datos que pueden modificarse en una lectura."""

    value: float | None = None
    unit: SensorUnit | None = None

    @field_validator("value", "unit", mode="before")
    @classmethod
    def reject_explicit_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("el campo no puede ser null")

        return value


class ReadingResponse(BaseModel):
    """Representación de una lectura devuelta por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: str
    value: float
    unit: SensorUnit
    received_at: datetime
