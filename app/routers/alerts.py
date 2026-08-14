from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_alert_service
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService

AlertServiceDependency = Annotated[
    AlertService,
    Depends(get_alert_service),
]

router = APIRouter(tags=["alerts"])


@router.get(
    "/sensors/{sensor_id}/alerts",
    response_model=list[AlertResponse],
)
def list_sensor_alerts(
    sensor_id: str,
    service: AlertServiceDependency,
) -> list[AlertResponse]:
    """Consulta las alertas almacenadas para un sensor."""

    alerts = service.list_by_sensor(sensor_id)
    return [
        AlertResponse.model_validate(alert)
        for alert in alerts
    ]
