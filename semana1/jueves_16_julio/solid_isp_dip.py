from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SensorReading:
    """Lectura inmutable producida por un sensor."""

    sensor_id: str
    value: float


# ---------- I: Interface Segregation Principle ----------


class Readable(Protocol):
    """Capacidad de producir lecturas."""

    def read(self) -> SensorReading:
        ...


class Writable(Protocol):
    """Capacidad de recibir un valor para escribirlo."""

    def write(self, value: float) -> None:
        ...


class Calibratable(Protocol):
    """Capacidad de calibrarse y restablecerse."""

    def calibrate(self) -> None:
        ...

    def reset(self) -> None:
        ...


# ---------- D: Dependency Inversion Principle ----------


class DataRepository(Protocol):
    """Abstracción para almacenar y consultar lecturas."""

    def save(self, reading: SensorReading) -> None:
        ...

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        ...


class DataProcessor:
    """Procesa lecturas de sensores y las almacena en un repositorio."""

    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository

    def process(self, reading: SensorReading) -> None:
        self._repo.save(reading)

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._repo.get_latest(sensor_id)


class InMemoryRepository:
    """Repositorio en memoria para almacenar lecturas de sensores."""

    def __init__(self) -> None:
        self._storage: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self._storage[reading.sensor_id] = reading

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._storage.get(sensor_id)
