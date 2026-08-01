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
from app.exceptions import SensorAlreadyExistsError
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


def _bad_request(error: ValueError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )


def _conflict(error: SensorAlreadyExistsError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(error),
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

    try:
        sensor = service.create_sensor(
            sensor_id=sensor_data.id,
            name=sensor_data.name,
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
        )
    except SensorAlreadyExistsError as error:
        raise _conflict(error) from error
    except ValueError as error:
        raise _bad_request(error) from error

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

    try:
        sensors = service.list_sensors(
            limit=limit,
            offset=offset,
        )
    except ValueError as error:
        raise _bad_request(error) from error

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

    try:
        sensor = service.get_by_id(sensor_id)
    except ValueError as error:
        raise _bad_request(error) from error

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

    try:
        sensor = service.update_sensor(
            sensor_id,
            name=sensor_data.name,
            is_active=sensor_data.is_active,
        )
    except ValueError as error:
        raise _bad_request(error) from error

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

    try:
        deactivated = service.deactivate_sensor(sensor_id)
    except ValueError as error:
        raise _bad_request(error) from error

    if not deactivated:
        raise _sensor_not_found(sensor_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
