from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.db import Base
from app.models.alert import Alert
from app.models.reading import Reading
from app.models.sensor import Sensor
from app.repositories.alert_repository import SQLAlchemyAlertRepository


def create_test_engine(database_path: Path) -> Engine:
    """Crea un motor conectado a una base SQLite temporal."""

    return create_engine(
        f"sqlite+pysqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )


def add_sensor_and_reading(
    session: Session,
    sensor_id: str,
    *,
    value: float,
) -> Reading:
    """Registra las entidades necesarias para relacionar una alerta."""

    session.add(
        Sensor(
            id=sensor_id,
            name=f"Sensor {sensor_id}",
            sensor_type="temperature",
            unit="C",
            is_active=True,
            threshold=30.0,
        )
    )
    session.commit()

    reading = Reading(
        sensor_id=sensor_id,
        value=value,
        unit="C",
        received_at=datetime(2026, 8, 14, 10, 0),
    )
    session.add(reading)
    session.commit()
    session.refresh(reading)

    return reading


def make_alert(reading: Reading, *, threshold: float = 30.0) -> Alert:
    """Construye una alerta vinculada a una lectura almacenada."""

    return Alert(
        sensor_id=reading.sensor_id,
        reading_id=reading.id,
        value=reading.value,
        threshold=threshold,
        created_at=datetime(2026, 8, 14, 10, 1),
    )


def test_alert_repository_persists_and_recovers_alert_between_sessions(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "alerts.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            reading = add_sensor_and_reading(
                session,
                "TEMP-01",
                value=31.5,
            )
            reading_id = reading.id
            repository = SQLAlchemyAlertRepository(session)
            saved = repository.add(make_alert(reading))
            saved_id = saved.id

        with Session(engine) as session:
            repository = SQLAlchemyAlertRepository(session)
            stored_alerts = repository.list_by_sensor("TEMP-01")

            assert len(stored_alerts) == 1

            stored = stored_alerts[0]
            assert stored.id == saved_id
            assert stored.sensor_id == "TEMP-01"
            assert stored.reading_id == reading_id
            assert stored.value == 31.5
            assert stored.threshold == 30.0
            assert stored.created_at == datetime(2026, 8, 14, 10, 1)
    finally:
        engine.dispose()


def test_list_by_sensor_returns_only_requested_sensor_alerts(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "alerts.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            first_reading = add_sensor_and_reading(
                session,
                "TEMP-01",
                value=31.5,
            )
            second_reading = add_sensor_and_reading(
                session,
                "TEMP-02",
                value=35.0,
            )
            repository = SQLAlchemyAlertRepository(session)
            expected = repository.add(make_alert(first_reading))
            repository.add(make_alert(second_reading))

            result = repository.list_by_sensor("TEMP-01")

            assert result == [expected]
            assert all(
                alert.sensor_id == "TEMP-01" for alert in result
            )
    finally:
        engine.dispose()
