from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from semana2.sensor_registry import SensorRegistry


class InvalidReadingError(ValueError):
    """Indica que una lectura contiene datos inválidos."""


@dataclass(frozen=True)
class SensorReading:
    """Representa una lectura recibida desde un sensor."""

    sensor_id: str
    temperature: float
    humidity: float
    received_at: datetime


class ReadingRecorder:
    """Registra y conserva las lecturas de sensores existentes."""

    def __init__(
        self,
        registry: SensorRegistry,
        clock: Callable[[], datetime],
    ) -> None:
        self._registry = registry
        self._clock = clock
        self._readings: list[SensorReading] = []

    @staticmethod
    def _require_numeric(value: object) -> int | float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidReadingError(
                "La temperatura y la humedad deben ser valores numéricos."
            )

        return value

    @classmethod
    def _validate_values(
        cls,
        temperature: object,
        humidity: object,
    ) -> None:
        cls._require_numeric(temperature)
        numeric_humidity = cls._require_numeric(humidity)

        if not 0.0 <= numeric_humidity <= 100.0:
            raise InvalidReadingError(
                "La humedad debe encontrarse entre 0 y 100."
            )

    def record(
        self,
        sensor_id: str,
        temperature: float,
        humidity: float,
    ) -> SensorReading:
        self._registry.get(sensor_id)
        self._validate_values(temperature, humidity)

        reading = SensorReading(
            sensor_id=sensor_id,
            temperature=temperature,
            humidity=humidity,
            received_at=self._clock(),
        )
        self._readings.append(reading)

        return reading

    def get_all(self) -> tuple[SensorReading, ...]:
        return tuple(self._readings)