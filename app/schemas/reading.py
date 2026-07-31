from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReadingCreate(BaseModel):
    """Datos necesarios para registrar una lectura."""

    temperature: float
    humidity: float = Field(ge=0.0, le=100.0)


class ReadingUpdate(BaseModel):
    """Datos que pueden modificarse en una lectura."""

    temperature: float | None = None
    humidity: float | None = Field(default=None, ge=0.0, le=100.0)


class ReadingResponse(BaseModel):
    """Representación de una lectura devuelta por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: str
    temperature: float
    humidity: float
    received_at: datetime