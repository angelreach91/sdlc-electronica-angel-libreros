from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_alert_service
from app.schemas.alert import AlertResponse, AlertStatusUpdate
from app.services.alert_service import AlertService

AlertServiceDependency = Annotated[
    AlertService,
    Depends(get_alert_service),
]

router = APIRouter(tags=["alerts"])


def _bad_request(error: ValueError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )


def _not_found(alert_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe la alerta con id {alert_id}",
    )


@router.get(
    "/sensors/{sensor_id}/alerts",
    response_model=list[AlertResponse],
)
def list_sensor_alerts(
    sensor_id: str,
    service: AlertServiceDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    from_date: Annotated[
        datetime | None,
        Query(alias="from"),
    ] = None,
    to_date: Annotated[
        datetime | None,
        Query(alias="to"),
    ] = None,
) -> list[AlertResponse]:
    """Consulta alertas almacenadas aplicando filtros y paginación."""

    try:
        alerts = service.list_by_sensor(
            sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )
    except ValueError as error:
        raise _bad_request(error) from error

    return [
        AlertResponse.model_validate(alert)
        for alert in alerts
    ]


@router.get(
    "/alerts/active",
    response_model=list[AlertResponse],
)
def list_active_alerts(
    service: AlertServiceDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[AlertResponse]:
    """Consulta las alertas abiertas o reconocidas."""

    try:
        alerts = service.list_active(limit=limit, offset=offset)
    except ValueError as error:
        raise _bad_request(error) from error

    return [AlertResponse.model_validate(alert) for alert in alerts]


@router.patch(
    "/alerts/{alert_id}/status",
    response_model=AlertResponse,
)
def update_alert_status(
    alert_id: int,
    alert_data: AlertStatusUpdate,
    service: AlertServiceDependency,
) -> AlertResponse:
    """Actualiza el estado de una alerta mediante una transición válida."""

    try:
        alert = service.update_status(alert_id, alert_data.status)
    except ValueError as error:
        raise _bad_request(error) from error

    if alert is None:
        raise _not_found(alert_id)

    return AlertResponse.model_validate(alert)
