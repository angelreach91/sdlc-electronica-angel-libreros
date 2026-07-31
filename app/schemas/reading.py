from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.sensor_types import SensorUnit


class ReadingCreate(BaseModel):
    """Datos necesarios para registrar una lectura."""

    value: float
    unit: SensorUnit


class ReadingUpdate(BaseModel):
    """Datos que pueden modificarse en una lectura."""

    value: float | None = None
    unit: SensorUnit | None = None


class ReadingResponse(BaseModel):
    """Representación de una lectura devuelta por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: str
    value: float
    unit: SensorUnit
    received_at: datetime