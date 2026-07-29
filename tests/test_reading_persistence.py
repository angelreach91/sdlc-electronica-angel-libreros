from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models import Reading


def test_reading_is_persisted_and_retrieved(tmp_path: Path) -> None:
    """Comprueba que una lectura permanece almacenada en SQLite."""
    database_path = tmp_path / "test_sensorhub.db"
    test_engine = create_engine(f"sqlite:///{database_path}")

    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Reading.metadata.create_all(bind=test_engine)

    received_at = datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc)

    try:
        with TestingSessionLocal() as session:
            reading = Reading(
                sensor_id="sensor-01",
                temperature=28.5,
                humidity=65.0,
                received_at=received_at,
            )

            session.add(reading)
            session.commit()

            reading_id = reading.id

        with TestingSessionLocal() as session:
            stored_reading = session.scalar(
                select(Reading).where(Reading.id == reading_id)
            )

            assert stored_reading is not None
            assert stored_reading.sensor_id == "sensor-01"
            assert stored_reading.temperature == 28.5
            assert stored_reading.humidity == 65.0
            assert stored_reading.received_at == received_at.replace(tzinfo=None)
    finally:
        test_engine.dispose()