from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from semana2.sensor_registry import SensorRegistry


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