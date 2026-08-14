from collections.abc import Callable
from datetime import datetime, timezone
from math import isfinite
from typing import Protocol

from app.models.reading import Reading
from app.models.sensor import Sensor
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorLookupRepository
from app.sensor_types import (
    EXPECTED_UNIT_BY_TYPE,
    SensorType,
    SensorUnit,
)


def utc_now() -> datetime:
    """Devuelve la fecha y hora actual en UTC."""

    return datetime.now(timezone.utc)


class AnomalyEvaluator(Protocol):
    """Contrato mínimo para evaluar anomalías en una lectura."""

    def evaluate(self, reading: Reading) -> object | None:
        """Evalúa una lectura persistida."""
        ...


class ReadingService:
    """Gestiona las reglas de negocio relacionadas con las lecturas."""

    def __init__(
        self,
        reading_repository: ReadingRepository,
        sensor_repository: SensorLookupRepository,
        clock: Callable[[], datetime] = utc_now,
        anomaly_evaluator: AnomalyEvaluator | None = None,
    ) -> None:
        self._reading_repository = reading_repository
        self._sensor_repository = sensor_repository
        self._clock = clock
        self._anomaly_evaluator = anomaly_evaluator

    def create_reading(
        self,
        sensor_id: str,
        value: float,
        unit: SensorUnit,
    ) -> Reading:
        """Valida y registra una nueva lectura."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)
        sensor = self._get_sensor_or_raise(normalized_sensor_id)

        if not sensor.is_active:
            raise ValueError(
                f"el sensor {normalized_sensor_id} está desactivado"
            )

        self._validate_measurement(
            sensor=sensor,
            value=value,
            unit=unit,
        )

        reading = Reading(
            sensor_id=normalized_sensor_id,
            value=value,
            unit=unit.value,
            received_at=self._clock(),
        )
        saved_reading = self._reading_repository.add(reading)

        if self._anomaly_evaluator is not None:
            self._anomaly_evaluator.evaluate(saved_reading)

        return saved_reading

    def list_by_sensor(
        self,
        sensor_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[Reading]:
        """Consulta lecturas aplicando filtros y paginación."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)
        self._get_sensor_or_raise(normalized_sensor_id)

        if not 1 <= limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100")

        if offset < 0:
            raise ValueError("offset no puede ser negativo")

        if from_date is not None and to_date is not None:
            from_date_is_aware = from_date.utcoffset() is not None
            to_date_is_aware = to_date.utcoffset() is not None

            if from_date_is_aware != to_date_is_aware:
                raise ValueError(
                    "from_date y to_date deben tener la misma "
                    "conciencia de zona horaria"
                )

            if from_date > to_date:
                raise ValueError(
                    "from_date no puede ser posterior a to_date"
                )

        return self._reading_repository.list_by_sensor(
            normalized_sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )

    def get_by_id(self, reading_id: int) -> Reading | None:
        """Busca una lectura mediante su identificador."""

        self._validate_reading_id(reading_id)
        return self._reading_repository.get_by_id(reading_id)

    def update_reading(
        self,
        reading_id: int,
        *,
        value: float | None = None,
        unit: SensorUnit | None = None,
    ) -> Reading | None:
        """Actualiza los valores proporcionados de una lectura."""

        self._validate_reading_id(reading_id)

        if value is None and unit is None:
            raise ValueError(
                "debe proporcionar al menos un valor para actualizar"
            )

        reading = self._reading_repository.get_by_id(reading_id)

        if reading is None:
            return None

        sensor = self._get_sensor_or_raise(reading.sensor_id)

        final_value = reading.value if value is None else value
        final_unit = (
            SensorUnit(reading.unit)
            if unit is None
            else unit
        )

        self._validate_measurement(
            sensor=sensor,
            value=final_value,
            unit=final_unit,
        )

        reading.value = final_value
        reading.unit = final_unit.value

        return self._reading_repository.update(reading)

    def delete_reading(self, reading_id: int) -> bool:
        """Elimina una lectura e indica si fue encontrada."""

        self._validate_reading_id(reading_id)
        reading = self._reading_repository.get_by_id(reading_id)

        if reading is None:
            return False

        self._reading_repository.delete(reading)
        return True

    def _get_sensor_or_raise(self, sensor_id: str) -> Sensor:
        sensor = self._sensor_repository.get_by_id(sensor_id)

        if sensor is None:
            raise LookupError(
                f"No existe el sensor con id {sensor_id}"
            )

        return sensor

    @staticmethod
    def _validate_measurement(
        sensor: Sensor,
        value: float,
        unit: SensorUnit,
    ) -> None:
        sensor_type = SensorType(sensor.sensor_type)
        expected_unit = EXPECTED_UNIT_BY_TYPE[sensor_type]

        if unit != expected_unit:
            raise ValueError(
                f"la unidad {unit.value} no corresponde "
                f"al sensor {sensor.id}"
            )

        if not isfinite(value):
            raise ValueError("el valor de medición debe ser finito")

        if (
            sensor_type == SensorType.TEMPERATURE
            and value < -273.15
        ):
            raise ValueError(
                "la temperatura no puede ser menor que -273.15 °C"
            )

        if (
            sensor_type == SensorType.HUMIDITY
            and not 0.0 <= value <= 100.0
        ):
            raise ValueError(
                "la humedad debe estar entre 0 y 100"
            )

    @staticmethod
    def _normalize_sensor_id(sensor_id: str) -> str:
        normalized_sensor_id = sensor_id.strip()

        if not normalized_sensor_id:
            raise ValueError("sensor_id no puede estar vacío")

        return normalized_sensor_id

    @staticmethod
    def _validate_reading_id(reading_id: int) -> None:
        if reading_id <= 0:
            raise ValueError(
                "reading_id debe ser mayor que cero"
            )
