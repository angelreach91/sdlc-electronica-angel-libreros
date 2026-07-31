from pydantic import BaseModel, ConfigDict, Field

from app.sensor_types import SensorType, SensorUnit


class SensorCreate(BaseModel):
    """Datos necesarios para registrar un sensor."""

    id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    sensor_type: SensorType
    unit: SensorUnit


class SensorUpdate(BaseModel):
    """Datos que pueden modificarse en un sensor."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    sensor_type: SensorType | None = None
    unit: SensorUnit | None = None
    is_active: bool | None = None


class SensorResponse(BaseModel):
    """Representación de un sensor devuelto por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    sensor_type: SensorType
    unit: SensorUnit
    is_active: bool