import pytest

from semana2.sensor_registry import SensorNotFoundError, SensorRegistry


def test_get_unknown_sensor_raises() -> None:
    registry = SensorRegistry()

    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")

def test_register_and_get_sensor() -> None:
    registry = SensorRegistry()

    registry.register("SENSOR-01")

    assert registry.get("SENSOR-01") == "SENSOR-01"