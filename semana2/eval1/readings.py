from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from semana2.sensor_registry import SensorRegistry


class InvalidReadingError(ValueError):
    """Indica que una lectura contiene datos inválidos."""


@dataclass(frozen=True)
class SensorReading:
    """Representa una lectura ambiental recibida desde un sensor."""

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

    @staticmethod
    def _validate_values(temperature: object, humidity: object) -> None:
        if (
            isinstance(temperature, bool)
            or not isinstance(temperature, (int, float))
            or isinstance(humidity, bool)
            or not isinstance(humidity, (int, float))
        ):
            raise InvalidReadingError(
                "La temperatura y la humedad deben ser valores numéricos."
            )

        if not 0.0 <= humidity <= 100.0:
            raise InvalidReadingError(
                "La humedad debe encontrarse entre 0 y 100."
            )
