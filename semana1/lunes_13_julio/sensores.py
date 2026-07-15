from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


class SensorType(Enum):
    """Tipos de sensores soportados por el ejercicio."""

    TEMPERATURE = auto()
    HUMIDITY = auto()


@dataclass(frozen=True)
class Reading:
    """Lectura inmutable de un sensor."""

    sensor_id: str
    value: float
    sensor_type: SensorType


class Transport(Protocol):
    """Contrato para un transporte de lecturas."""

    def send(self, payload: bytes) -> None:
        """Envía un payload de bytes a un destino externo."""
        ...


def celsius_to_fahrenheit(reading: Reading) -> float:
    """Convierte una lectura de temperatura de Celsius a Fahrenheit."""

    if reading.sensor_type is not SensorType.TEMPERATURE:
        raise ValueError("La lectura no es de temperatura")

    return reading.value * 9 / 5 + 32


def exceeds_threshold(reading: Reading, threshold: float) -> bool:
    """Determina si una lectura excede un umbral dado."""

    return reading.value > threshold


def to_frame(reading: Reading) -> bytes:
    """Serializa una lectura en formato de bytes."""

    frame = (
        f"{reading.sensor_id}:"
        f"{reading.value:.2f}:"
        f"{reading.sensor_type.name}"
    )

    return frame.encode()


def classify_reading(
    reading: Reading,
    low_limit: float,
    high_limit: float,
) -> str:
    """Clasifica una lectura como baja, normal o alta."""

    if reading.value < low_limit:
        return "LOW"

    if reading.value > high_limit:
        return "HIGH"

    return "NORMAL"


def scale_reading(reading: Reading, factor: float) -> Reading:
    """Devuelve una nueva lectura con el valor escalado."""

    return Reading(
        sensor_id=reading.sensor_id,
        value=reading.value * factor,
        sensor_type=reading.sensor_type,
    )