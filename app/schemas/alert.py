from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.alert_status import AlertStatus


class AlertStatusUpdate(BaseModel):
    """Estado solicitado para actualizar una alerta."""

    model_config = ConfigDict(extra="forbid")

    status: AlertStatus


class AlertResponse(BaseModel):
    """Representación de una alerta devuelta por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: str
    reading_id: int
    value: float
    threshold: float
    status: AlertStatus
    created_at: datetime
