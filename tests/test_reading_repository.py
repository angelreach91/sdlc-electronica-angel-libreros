from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.db import Base
from app.models.reading import Reading
from app.repositories.reading_repository import SQLAlchemyReadingRepository


def create_test_engine(database_path: Path) -> Engine:
    """Crea un motor conectado a una base SQLite temporal."""
    return create_engine(
        f"sqlite+pysqlite:///{database_path}",
        connect_args={"check_same_thread": False},
    )


def test_add_persists_reading(tmp_path: Path) -> None:
    engine = create_test_engine(tmp_path / "repository.db")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        repository = SQLAlchemyReadingRepository(session)

        reading = Reading(
            sensor_id="sensor-01",
            temperature=24.5,
            humidity=60.0,
            received_at=datetime(
                2026,
                7,
                29,
                18,
                0,
                tzinfo=timezone.utc,
            ),
        )

        saved_reading = repository.add(reading)
        saved_id = saved_reading.id

        assert saved_id is not None

    with Session(engine) as session:
        persisted_reading = session.get(Reading, saved_id)

        assert persisted_reading is not None
        assert persisted_reading.sensor_id == "sensor-01"
        assert persisted_reading.temperature == 24.5
        assert persisted_reading.humidity == 60.0

    engine.dispose()


def test_list_by_sensor_filters_and_orders_readings(
    tmp_path: Path,
) -> None:
    engine = create_test_engine(tmp_path / "repository.db")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        repository = SQLAlchemyReadingRepository(session)

        repository.add(
            Reading(
                sensor_id="sensor-01",
                temperature=26.0,
                humidity=65.0,
                received_at=datetime(
                    2026,
                    7,
                    29,
                    19,
                    0,
                    tzinfo=timezone.utc,
                ),
            )
        )
        repository.add(
            Reading(
                sensor_id="sensor-02",
                temperature=30.0,
                humidity=70.0,
                received_at=datetime(
                    2026,
                    7,
                    29,
                    17,
                    0,
                    tzinfo=timezone.utc,
                ),
            )
        )
        repository.add(
            Reading(
                sensor_id="sensor-01",
                temperature=24.0,
                humidity=55.0,
                received_at=datetime(
                    2026,
                    7,
                    29,
                    18,
                    0,
                    tzinfo=timezone.utc,
                ),
            )
        )

        result = repository.list_by_sensor("sensor-01")

        assert len(result) == 2
        assert [reading.sensor_id for reading in result] == [
            "sensor-01",
            "sensor-01",
        ]
        assert [reading.temperature for reading in result] == [
            24.0,
            26.0,
        ]

    engine.dispose()