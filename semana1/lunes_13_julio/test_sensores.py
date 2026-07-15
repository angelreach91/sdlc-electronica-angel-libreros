import pytest

from sensores import (
    Reading,
    SensorType,
    celsius_to_fahrenheit,
    classify_reading,
    exceeds_threshold,
)


def test_celsius_to_fahrenheit_converts_temperature() -> None:
    reading = Reading(
        sensor_id="temp-1",
        value=0.0,
        sensor_type=SensorType.TEMPERATURE,
    )

    result = celsius_to_fahrenheit(reading)

    assert result == 32.0


def test_celsius_to_fahrenheit_raises_for_humidity() -> None:
    reading = Reading(
        sensor_id="hum-1",
        value=50.0,
        sensor_type=SensorType.HUMIDITY,
    )

    with pytest.raises(ValueError):
        celsius_to_fahrenheit(reading)


def test_exceeds_threshold_returns_true() -> None:
    reading = Reading(
        sensor_id="temp-2",
        value=25.0,
        sensor_type=SensorType.TEMPERATURE,
    )

    assert exceeds_threshold(reading, 20.0) is True


def test_classify_reading_returns_high() -> None:
    reading = Reading(
        sensor_id="temp-3",
        value=35.0,
        sensor_type=SensorType.TEMPERATURE,
    )

    assert classify_reading(reading, 10.0, 30.0) == "HIGH"