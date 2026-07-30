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

        normalized_sensor_id = sensor_id.strip()

        if not normalized_sensor_id:
            raise ValueError("sensor_id no puede estar vacío")

        if temperature < -273.15:
            raise ValueError("temperature no puede ser menor que -273.15 °C")

        if not 0.0 <= humidity <= 100.0:
            raise ValueError("humidity debe estar entre 0 y 100")

        reading = Reading(
            sensor_id=normalized_sensor_id,
            temperature=temperature,
            humidity=humidity,
            received_at=self._clock(),
        )

        return self._repository.add(reading)

    def list_by_sensor(self, sensor_id: str) -> list[Reading]:
        """Obtiene las lecturas registradas para un sensor."""

        normalized_sensor_id = sensor_id.strip()

        if not normalized_sensor_id:
            raise ValueError("sensor_id no puede estar vacío")

        return self._repository.list_by_sensor(normalized_sensor_id)