from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.alert_repository import SQLAlchemyAlertRepository
from app.repositories.reading_repository import SQLAlchemyReadingRepository
from app.repositories.sensor_repository import SQLAlchemySensorRepository
from app.services.alert_service import AlertService
from app.services.anomaly_service import (
    AnomalyService,
    LoggingNotificationStrategy,
)
from app.services.reading_service import ReadingService, utc_now
from app.services.sensor_service import SensorService


def get_session() -> Generator[Session, None, None]:
    """Proporciona una sesión de SQLAlchemy durante una petición."""

    with SessionLocal() as session:
        yield session


def get_alert_service(
    session: Annotated[Session, Depends(get_session)],
) -> AlertService:
    """Construye el servicio de alertas."""

    repository = SQLAlchemyAlertRepository(session)
    return AlertService(repository)


def get_reading_service(
    session: Annotated[Session, Depends(get_session)],
) -> ReadingService:
    """Construye el servicio de lecturas."""

    reading_repository = SQLAlchemyReadingRepository(session)
    sensor_repository = SQLAlchemySensorRepository(session)
    alert_repository = SQLAlchemyAlertRepository(session)
    notification_strategy = LoggingNotificationStrategy()
    anomaly_evaluator = AnomalyService(
        sensor_repository=sensor_repository,
        alert_repository=alert_repository,
        notification_strategy=notification_strategy,
        clock=utc_now,
    )

    return ReadingService(
        reading_repository=reading_repository,
        sensor_repository=sensor_repository,
        anomaly_evaluator=anomaly_evaluator,
    )


def get_sensor_service(
    session: Annotated[Session, Depends(get_session)],
) -> SensorService:
    """Construye el servicio de sensores."""

    repository = SQLAlchemySensorRepository(session)
    return SensorService(repository)
