from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.db import Base
from app.models.reading import Reading
from app.models.sensor import Sensor
from app.repositories.reading_repository import (
    SQLAlchemyReadingRepository,
)


def create_test_engine(database_path: Path) -> Engine:
    """Crea un motor conectado a una base SQLite temporal."""

    return create_engine(
        f"sqlite+pysqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )


def add_sensor(
    session: Session,
    sensor_id: str,
    *,
    sensor_type: str = "temperature",
    unit: str = "C",
) -> None:
    """Registra un sensor necesario para relacionar sus lecturas."""

    session.add(
        Sensor(
            id=sensor_id,
            name=f"Sensor {sensor_id}",
            location="Laboratorio",
            sensor_type=sensor_type,
            unit=unit,
            is_active=True,
        )
    )
    session.commit()


def make_reading(
    sensor_id: str,
    *,
    value: float,
    day: int,
) -> Reading:
    """Construye una lectura para las pruebas del repositorio."""

    return Reading(
        sensor_id=sensor_id,
        value=value,
        unit="C",
        received_at=datetime(2026, 7, day),
    )


def test_add_persists_reading(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "readings.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            add_sensor(session, "TEMP-01")
            repository = SQLAlchemyReadingRepository(session)

            saved = repository.add(
                make_reading(
                    "TEMP-01",
                    value=24.5,
                    day=28,
                )
            )
            saved_id = saved.id

        with Session(engine) as session:
            repository = SQLAlchemyReadingRepository(session)
            stored = repository.get_by_id(saved_id)

            assert stored is not None
            assert stored.sensor_id == "TEMP-01"
            assert stored.value == 24.5
            assert stored.unit == "C"
            assert stored.received_at == datetime(2026, 7, 28)
    finally:
        engine.dispose()


def test_list_by_sensor_applies_date_filters(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "readings.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            add_sensor(session, "TEMP-01")
            add_sensor(session, "TEMP-02")
            repository = SQLAlchemyReadingRepository(session)

            repository.add(
                make_reading("TEMP-01", value=21.0, day=27)
            )
            repository.add(
                make_reading("TEMP-01", value=22.0, day=28)
            )
            repository.add(
                make_reading("TEMP-02", value=30.0, day=28)
            )
            repository.add(
                make_reading("TEMP-01", value=23.0, day=29)
            )
            repository.add(
                make_reading("TEMP-01", value=24.0, day=30)
            )

            result = repository.list_by_sensor(
                "TEMP-01",
                from_date=datetime(2026, 7, 28),
                to_date=datetime(2026, 7, 29),
            )

            assert [reading.value for reading in result] == [
                22.0,
                23.0,
            ]
    finally:
        engine.dispose()


def test_list_by_sensor_applies_pagination(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "readings.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            add_sensor(session, "TEMP-01")
            repository = SQLAlchemyReadingRepository(session)

            repository.add(
                make_reading("TEMP-01", value=21.0, day=27)
            )
            repository.add(
                make_reading("TEMP-01", value=22.0, day=28)
            )
            repository.add(
                make_reading("TEMP-01", value=23.0, day=29)
            )

            result = repository.list_by_sensor(
                "TEMP-01",
                limit=1,
                offset=1,
            )

            assert len(result) == 1
            assert result[0].value == 22.0
    finally:
        engine.dispose()


def test_get_statistics_by_sensor_aggregates_requested_period(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "readings.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            add_sensor(session, "TEMP-01")
            add_sensor(session, "TEMP-02")
            repository = SQLAlchemyReadingRepository(session)

            repository.add(
                make_reading("TEMP-01", value=-100.0, day=27)
            )
            repository.add(
                make_reading("TEMP-01", value=20.0, day=28)
            )
            repository.add(
                make_reading("TEMP-01", value=25.0, day=29)
            )
            repository.add(
                make_reading("TEMP-01", value=30.0, day=30)
            )
            repository.add(
                make_reading("TEMP-01", value=100.0, day=31)
            )
            repository.add(
                make_reading("TEMP-02", value=1000.0, day=29)
            )

            result = repository.get_statistics_by_sensor(
                "TEMP-01",
                from_date=datetime(2026, 7, 28),
                to_date=datetime(2026, 7, 30),
            )

            assert result == (20.0, 30.0, 25.0)
    finally:
        engine.dispose()


def test_get_statistics_by_sensor_returns_none_without_readings(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "readings.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            add_sensor(session, "TEMP-01")
            repository = SQLAlchemyReadingRepository(session)

            result = repository.get_statistics_by_sensor(
                "TEMP-01",
                from_date=datetime(2026, 8, 1),
                to_date=datetime(2026, 8, 2),
            )

            assert result is None
    finally:
        engine.dispose()


def test_get_update_and_delete_reading_between_sessions(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "readings.db")

    try:
        Base.metadata.create_all(bind=engine)

        with Session(engine) as session:
            add_sensor(session, "TEMP-01")
            repository = SQLAlchemyReadingRepository(session)

            reading = repository.add(
                make_reading(
                    "TEMP-01",
                    value=24.5,
                    day=28,
                )
            )
            reading_id = reading.id

        with Session(engine) as session:
            repository = SQLAlchemyReadingRepository(session)
            stored = repository.get_by_id(reading_id)

            assert stored is not None

            stored.value = 27.0
            repository.update(stored)

        with Session(engine) as session:
            repository = SQLAlchemyReadingRepository(session)
            updated = repository.get_by_id(reading_id)

            assert updated is not None
            assert updated.value == 27.0

            repository.delete(updated)

        with Session(engine) as session:
            repository = SQLAlchemyReadingRepository(session)

            assert repository.get_by_id(reading_id) is None
    finally:
        engine.dispose()
