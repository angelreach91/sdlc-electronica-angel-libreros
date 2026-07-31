from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.db import Base
from app.models.sensor import Sensor
from app.repositories.sensor_repository import (
    SQLAlchemySensorRepository,
)


def create_test_engine(database_path: Path) -> Engine:
    """Crea un motor conectado a una base SQLite temporal."""

    return create_engine(
        f"sqlite+pysqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )


def make_sensor(
    sensor_id: str,
    *,
    name: str = "Sensor de prueba",
) -> Sensor:
    """Construye un sensor válido para las pruebas."""

    return Sensor(
        id=sensor_id,
        name=name,
        sensor_type="temperature",
        unit="C",
        is_active=True,
    )


def test_sensor_repository_persists_and_gets_sensor(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "sensors.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            repository = SQLAlchemySensorRepository(session)
            repository.add(make_sensor("TEMP-01"))

        with Session(engine) as session:
            repository = SQLAlchemySensorRepository(session)
            stored = repository.get_by_id("TEMP-01")

            assert stored is not None
            assert stored.id == "TEMP-01"
            assert stored.name == "Sensor de prueba"
            assert stored.sensor_type == "temperature"
            assert stored.unit == "C"
            assert stored.is_active is True
    finally:
        engine.dispose()


def test_sensor_repository_lists_with_pagination(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "sensors.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            repository = SQLAlchemySensorRepository(session)
            repository.add(make_sensor("TEMP-02"))
            repository.add(make_sensor("HUM-01"))
            repository.add(make_sensor("TEMP-01"))

            result = repository.list_all(
                limit=1,
                offset=1,
            )

            assert len(result) == 1
            assert result[0].id == "TEMP-01"
    finally:
        engine.dispose()


def test_sensor_repository_persists_update(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "sensors.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            repository = SQLAlchemySensorRepository(session)
            sensor = repository.add(make_sensor("TEMP-01"))

            sensor.name = "Sensor actualizado"
            sensor.is_active = False
            repository.update(sensor)

        with Session(engine) as session:
            repository = SQLAlchemySensorRepository(session)
            stored = repository.get_by_id("TEMP-01")

            assert stored is not None
            assert stored.name == "Sensor actualizado"
            assert stored.is_active is False
    finally:
        engine.dispose()