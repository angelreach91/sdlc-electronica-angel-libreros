from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)

from app.dependencies import get_reading_service
from app.schemas.reading import (
    ReadingCreate,
    ReadingResponse,
    ReadingUpdate,
)
from app.services.reading_service import ReadingService

ReadingServiceDependency = Annotated[
    ReadingService,
    Depends(get_reading_service),
]

router = APIRouter()


def bad_request(error: ValueError) -> HTTPException:
    """Convierte un error de negocio en una respuesta HTTP 400."""

    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    )


def reading_not_found(reading_id: int) -> HTTPException:
    """Construye la respuesta HTTP para una lectura inexistente."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe la lectura con id {reading_id}",
    )


@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    sensor_id: str,
    reading_data: ReadingCreate,
    service: ReadingServiceDependency,
) -> ReadingResponse:
    """Registra una lectura para el sensor indicado."""

    try:
        reading = service.create_reading(
            sensor_id=sensor_id,
            temperature=reading_data.temperature,
            humidity=reading_data.humidity,
        )
    except ValueError as error:
        raise bad_request(error) from error

    return ReadingResponse.model_validate(reading)


@router.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[ReadingResponse],
)
def list_readings(
    sensor_id: str,
    service: ReadingServiceDependency,
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
) -> list[ReadingResponse]:
    """Consulta las lecturas registradas para un sensor."""

    try:
        readings = service.list_by_sensor(
            sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )
    except ValueError as error:
        raise bad_request(error) from error

    return [
        ReadingResponse.model_validate(reading)
        for reading in readings
    ]


@router.get(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
)
def get_reading(
    reading_id: int,
    service: ReadingServiceDependency,
) -> ReadingResponse:
    """Devuelve una lectura mediante su identificador."""

    try:
        reading = service.get_by_id(reading_id)
    except ValueError as error:
        raise bad_request(error) from error

    if reading is None:
        raise reading_not_found(reading_id)

    return ReadingResponse.model_validate(reading)


@router.patch(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
)
def update_reading(
    reading_id: int,
    reading_data: ReadingUpdate,
    service: ReadingServiceDependency,
) -> ReadingResponse:
    """Actualiza parcialmente una lectura existente."""

    try:
        reading = service.update_reading(
            reading_id,
            temperature=reading_data.temperature,
            humidity=reading_data.humidity,
        )
    except ValueError as error:
        raise bad_request(error) from error

    if reading is None:
        raise reading_not_found(reading_id)

    return ReadingResponse.model_validate(reading)


@router.delete(
    "/readings/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reading(
    reading_id: int,
    service: ReadingServiceDependency,
) -> Response:
    """Elimina una lectura mediante su identificador."""

    try:
        deleted = service.delete_reading(reading_id)
    except ValueError as error:
        raise bad_request(error) from error

    if not deleted:
        raise reading_not_found(reading_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)