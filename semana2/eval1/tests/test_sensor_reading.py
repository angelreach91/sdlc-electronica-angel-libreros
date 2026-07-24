from datetime import datetime, timezone
from typing import cast

import pytest

from semana2.eval1.readings import (
    InvalidReadingError,
    ReadingRecorder,
    SensorReading,
)
from semana2.sensor_registry import (
    SensorNotFoundError,
    SensorRegistry,
)


def test_record_reading_associates_sensor_and_reception_time() -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    reading = recorder.record(
        sensor_id="SENSOR-01",
        temperature=24.5,
        humidity=60.0,
    )

    assert reading == SensorReading(
        sensor_id="SENSOR-01",
        temperature=24.5,
        humidity=60.0,
        received_at=reception_time,
    )


def test_record_reading_preserves_previous_readings() -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    first_reading = recorder.record("SENSOR-01", 24.5, 60.0)
    second_reading = recorder.record("SENSOR-01", 25.0, 61.5)

    assert recorder.get_all() == (first_reading, second_reading)


def test_record_reading_from_unknown_sensor_raises() -> None:
    registry = SensorRegistry()
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    with pytest.raises(SensorNotFoundError):
        recorder.record("SENSOR-99", 24.5, 60.0)

    assert recorder.get_all() == ()

@pytest.mark.parametrize(
    ("temperature", "humidity"),
    [
        (None, 60.0),
        (24.5, None),
    ],
)
def test_record_reading_rejects_incomplete_data(
    temperature: object,
    humidity: object,
) -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    with pytest.raises(InvalidReadingError):
        recorder.record(
            "SENSOR-01",
            cast(float, temperature),
            cast(float, humidity),
        )

    assert recorder.get_all() == ()


@pytest.mark.parametrize(
    ("temperature", "humidity"),
    [
        ("temperatura-invalida", 60.0),
        (24.5, "humedad-invalida"),
    ],
)
def test_record_reading_rejects_non_numeric_data(
    temperature: object,
    humidity: object,
) -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    with pytest.raises(InvalidReadingError):
        recorder.record(
            "SENSOR-01",
            cast(float, temperature),
            cast(float, humidity),
        )

    assert recorder.get_all() == ()


@pytest.mark.parametrize("humidity", [-0.1, 100.1])
def test_record_reading_rejects_humidity_outside_valid_range(
    humidity: float,
) -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    with pytest.raises(InvalidReadingError):
        recorder.record("SENSOR-01", 24.5, humidity)

    assert recorder.get_all() == ()


def test_record_reading_accepts_humidity_range_boundaries() -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")
    reception_time = datetime(2026, 7, 23, 20, 30, tzinfo=timezone.utc)
    recorder = ReadingRecorder(registry, clock=lambda: reception_time)

    first_reading = recorder.record("SENSOR-01", 24.5, 0.0)
    second_reading = recorder.record("SENSOR-01", 24.5, 100.0)

    assert recorder.get_all() == (first_reading, second_reading)