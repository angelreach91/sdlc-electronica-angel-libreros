from enum import StrEnum


class SensorType(StrEnum):
    """Tipos de sensor aceptados por SensorHub."""

    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"


class SensorUnit(StrEnum):
    """Unidades de medición aceptadas por SensorHub."""

    CELSIUS = "C"
    PERCENT = "%"


EXPECTED_UNIT_BY_TYPE: dict[SensorType, SensorUnit] = {
    SensorType.TEMPERATURE: SensorUnit.CELSIUS,
    SensorType.HUMIDITY: SensorUnit.PERCENT,
}