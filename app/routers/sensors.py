from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)

from app.dependencies import get_sensor_service
from app.schemas.sensor import (
    SensorCreate,
    SensorResponse,
    SensorUpdate,
)
from app.services.sensor_service import SensorService

SensorServiceDependency = Annotated[
    SensorService,
    Depends(get_sensor_service),
]

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


def _sensor_not_found(sensor_id: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el sensor con id {sensor_id}",
    )


@router.post(
    "",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sensor(
    sensor_data: SensorCreate,
    service: SensorServiceDependency,
) -> SensorResponse:
    """Registra un sensor."""

    sensor = service.create_sensor(
        sensor_id=sensor_data.id,
        name=sensor_data.name,
        sensor_type=sensor_data.sensor_type,
        unit=sensor_data.unit,
        location=sensor_data.location,
        threshold=sensor_data.threshold,
    )

    return SensorResponse.model_validate(sensor)


@router.get(
    "",
    response_model=list[SensorResponse],
)
def list_sensors(
    service: SensorServiceDependency,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[SensorResponse]:
    """Consulta los sensores registrados."""

    sensors = service.list_sensors(
        limit=limit,
        offset=offset,
    )

    return [
        SensorResponse.model_validate(sensor)
        for sensor in sensors
    ]


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
)
def get_sensor(
    sensor_id: str,
    service: SensorServiceDependency,
) -> SensorResponse:
    """Devuelve un sensor mediante su identificador."""

    sensor = service.get_by_id(sensor_id)

    if sensor is None:
        raise _sensor_not_found(sensor_id)

    return SensorResponse.model_validate(sensor)


@router.patch(
    "/{sensor_id}",
    response_model=SensorResponse,
)
def update_sensor(
    sensor_id: str,
    sensor_data: SensorUpdate,
    service: SensorServiceDependency,
) -> SensorResponse:
    """Actualiza parcialmente un sensor."""

    sensor = service.update_sensor(
        sensor_id,
        name=sensor_data.name,
        location=sensor_data.location,
        is_active=sensor_data.is_active,
        threshold=sensor_data.threshold,
    )

    if sensor is None:
        raise _sensor_not_found(sensor_id)

    return SensorResponse.model_validate(sensor)


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deactivate_sensor(
    sensor_id: str,
    service: SensorServiceDependency,
) -> Response:
    """Desactiva un sensor mediante su identificador."""

    deactivated = service.deactivate_sensor(sensor_id)

    if not deactivated:
        raise _sensor_not_found(sensor_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
