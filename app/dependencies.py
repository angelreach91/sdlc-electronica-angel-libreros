from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.reading_repository import SQLAlchemyReadingRepository
from app.repositories.sensor_repository import SQLAlchemySensorRepository
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService


def get_session() -> Generator[Session, None, None]:
    """Proporciona una sesión de SQLAlchemy durante una petición."""

    with SessionLocal() as session:
        yield session


def get_reading_service(
    session: Annotated[Session, Depends(get_session)],
) -> ReadingService:
    """Construye el servicio de lecturas."""

    reading_repository = SQLAlchemyReadingRepository(session)
    sensor_repository = SQLAlchemySensorRepository(session)

    return ReadingService(
        reading_repository=reading_repository,
        sensor_repository=sensor_repository,
    )


def get_sensor_service(
    session: Annotated[Session, Depends(get_session)],
) -> SensorService:
    """Construye el servicio de sensores."""

    repository = SQLAlchemySensorRepository(session)
    return SensorService(repository)