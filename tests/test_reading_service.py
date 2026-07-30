from datetime import datetime, timezone

import pytest

from app.models.reading import Reading
from app.services.reading_service import ReadingService

FIXED_TIME = datetime(2026, 7, 29, 18, 0, tzinfo=timezone.utc)


class FakeReadingRepository:
    """Repositorio en memoria utilizado únicamente durante las pruebas."""

    def __init__(self) -> None:
        self.readings: list[Reading] = []

    def add(self, reading: Reading) -> Reading:
        self.readings.append(reading)
        return reading

    def list_by_sensor(self, sensor_id: str) -> list[Reading]:
        return [
            reading
            for reading in self.readings
            if reading.sensor_id == sensor_id
        ]


def fixed_clock() -> datetime:
    """Devuelve una fecha fija para obtener pruebas deterministas."""
    return FIXED_TIME


def test_create_reading_stores_valid_reading() -> None:
    repository = FakeReadingRepository()
    service = ReadingService(repository, clock=fixed_clock)

    reading = service.create_reading(
        sensor_id=" sensor-01 ",
        temperature=24.5,
        humidity=60.0,
    )

    assert reading.sensor_id == "sensor-01"
    assert reading.temperature == 24.5
    assert reading.humidity == 60.0
    assert reading.received_at == FIXED_TIME
    assert repository.readings == [reading]


def test_create_reading_rejects_empty_sensor_id() -> None:
    repository = FakeReadingRepository()
    service = ReadingService(repository, clock=fixed_clock)

    with pytest.raises(ValueError, match="sensor_id no puede estar vacío"):
        service.create_reading(
            sensor_id="   ",
            temperature=24.5,
            humidity=60.0,
        )

    assert repository.readings == []


def test_create_reading_rejects_temperature_below_absolute_zero() -> None:
    repository = FakeReadingRepository()
    service = ReadingService(repository, clock=fixed_clock)

    with pytest.raises(
        ValueError,
        match="temperature no puede ser menor",
    ):
        service.create_reading(
            sensor_id="sensor-01",
            temperature=-273.16,
            humidity=60.0,
        )

    assert repository.readings == []


@pytest.mark.parametrize("humidity", [-0.1, 100.1])
def test_create_reading_rejects_invalid_humidity(humidity: float) -> None:
    repository = FakeReadingRepository()
    service = ReadingService(repository, clock=fixed_clock)

    with pytest.raises(
        ValueError,
        match="humidity debe estar entre 0 y 100",
    ):
        service.create_reading(
            sensor_id="sensor-01",
            temperature=24.5,
            humidity=humidity,
        )

    assert repository.readings == []


def test_list_by_sensor_returns_only_requested_readings() -> None:
    repository = FakeReadingRepository()
    service = ReadingService(repository, clock=fixed_clock)

    first_reading = service.create_reading(
        sensor_id="sensor-01",
        temperature=24.5,
        humidity=60.0,
    )
    service.create_reading(
        sensor_id="sensor-02",
        temperature=26.0,
        humidity=65.0,
    )

    result = service.list_by_sensor(" sensor-01 ")

    assert result == [first_reading]