from collections.abc import Callable
from datetime import datetime, timezone

from app.models.reading import Reading
from app.repositories.reading_repository import ReadingRepository


def utc_now() -> datetime:
    """Devuelve la fecha y hora actual en UTC."""
    return datetime.now(timezone.utc)


class ReadingService:
    """Gestiona las reglas de negocio relacionadas con las lecturas."""

    def __init__(
        self,
        repository: ReadingRepository,
        clock: Callable[[], datetime] = utc_now,
    ) -> None:
        self._repository = repository
        self._clock = clock

    def create_reading(
        self,
        sensor_id: str,
        temperature: float,
        humidity: float,
    ) -> Reading:
        """Valida y registra una nueva lectura."""

        normalized_sensor_id = self._normalize_sensor_id(sensor_id)
        self._validate_temperature(temperature)
        self._validate_humidity(humidity)

        reading = Reading(
            sensor_id=normalized_sensor_id,
            temperature=temperature,
            humidity=humidity,
            received_at=self._clock(),
        )

        return self._repository.add(reading)

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

        if not 1 <= limit <= 100:
            raise ValueError("limit debe estar entre 1 y 100")

        if offset < 0:
            raise ValueError("offset no puede ser negativo")

        if (
            from_date is not None
            and to_date is not None
            and from_date > to_date
        ):
            raise ValueError("from_date no puede ser posterior a to_date")

        return self._repository.list_by_sensor(
            normalized_sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )

    def get_by_id(self, reading_id: int) -> Reading | None:
        """Busca una lectura mediante su identificador."""

        self._validate_reading_id(reading_id)
        return self._repository.get_by_id(reading_id)

    def update_reading(
        self,
        reading_id: int,
        *,
        temperature: float | None = None,
        humidity: float | None = None,
    ) -> Reading | None:
        """Actualiza los valores proporcionados de una lectura."""

        self._validate_reading_id(reading_id)

        if temperature is None and humidity is None:
            raise ValueError("debe proporcionar al menos un valor para actualizar")

        if temperature is not None:
            self._validate_temperature(temperature)

        if humidity is not None:
            self._validate_humidity(humidity)

        reading = self._repository.get_by_id(reading_id)

        if reading is None:
            return None

        if temperature is not None:
            reading.temperature = temperature

        if humidity is not None:
            reading.humidity = humidity

        return self._repository.update(reading)

    def delete_reading(self, reading_id: int) -> bool:
        """Elimina una lectura e indica si fue encontrada."""

        self._validate_reading_id(reading_id)
        reading = self._repository.get_by_id(reading_id)

        if reading is None:
            return False

        self._repository.delete(reading)
        return True

    @staticmethod
    def _normalize_sensor_id(sensor_id: str) -> str:
        normalized_sensor_id = sensor_id.strip()

        if not normalized_sensor_id:
            raise ValueError("sensor_id no puede estar vacío")

        return normalized_sensor_id

    @staticmethod
    def _validate_temperature(temperature: float) -> None:
        if temperature < -273.15:
            raise ValueError("temperature no puede ser menor que -273.15 °C")

    @staticmethod
    def _validate_humidity(humidity: float) -> None:
        if not 0.0 <= humidity <= 100.0:
            raise ValueError("humidity debe estar entre 0 y 100")

    @staticmethod
    def _validate_reading_id(reading_id: int) -> None:
        if reading_id <= 0:
            raise ValueError("reading_id debe ser mayor que cero")