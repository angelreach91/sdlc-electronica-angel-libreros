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

def test_register_duplicate_sensor_raises() -> None:
    registry = SensorRegistry()
    registry.register("SENSOR-01")

    with pytest.raises(ValueError, match="ya está registrado."):
        registry.register("SENSOR-01")

def test_register_empty_sensor_id_raises() -> None:
    registry = SensorRegistry()

    with pytest.raises(ValueError, match="no puede estar vacío."):
        registry.register("")