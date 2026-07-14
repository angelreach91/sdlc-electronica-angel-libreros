from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class SensorType(Enum):
    """Tipos de sensores soportados por el ejercicio."""

    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"


@dataclass(frozen=True, slots=True)
class Reading:
    """Lectura inmutable de un sensor."""

    sensor: SensorType
    value: float
    unit: str


class Transport(Protocol):
    """Contrato para un transporte de lecturas."""

    def send(self, payload: str) -> None:
        """Envía un mensaje serializado."""


def convert_temperature(value: float, source_unit: str, target_unit: str) -> float:
    """Convierte una temperatura entre unidades compatibles."""

    if source_unit == target_unit:
        return value
    if source_unit == "C" and target_unit == "F":
        return value * 9 / 5 + 32
    if source_unit == "F" and target_unit == "C":
        return (value - 32) * 5 / 9
    raise ValueError(f"Unidades no compatibles: {source_unit} -> {target_unit}")


def compare_thresholds(value: float, threshold: float, *, operator: str = "gte") -> bool:
    """Compara un valor con un umbral usando un operador explícito."""

    if operator == "gte":
        return value >= threshold
    if operator == "gt":
        return value > threshold
    if operator == "lte":
        return value <= threshold
    if operator == "lt":
        return value < threshold
    if operator == "eq":
        return value == threshold
    raise ValueError(f"Operador no soportado: {operator}")


def serialize_reading(reading: Reading) -> str:
    """Serializa una lectura en una cadena estable."""

    return f"{reading.sensor.value}:{reading.value:.2f}:{reading.unit}"


def classify(reading: Reading, *, warning_threshold: float, critical_threshold: float) -> str:
    """Clasifica una lectura según el tipo de sensor y los umbrales dados."""

    if reading.sensor is SensorType.TEMPERATURE:
        if reading.value >= critical_threshold:
            return "critical"
        if reading.value >= warning_threshold:
            return "warning"
        return "normal"

    if reading.sensor is SensorType.HUMIDITY:
        if reading.value <= critical_threshold:
            return "critical"
        if reading.value <= warning_threshold:
            return "warning"
        return "normal"

    raise ValueError(f"Sensor no soportado: {reading.sensor}")


def scale_value(value: float, *, min_value: float, max_value: float) -> float:
    """Escala un valor al rango [0, 1] sin modificar el valor original."""

    if max_value <= min_value:
        raise ValueError("max_value debe ser mayor que min_value")
    return (value - min_value) / (max_value - min_value)
