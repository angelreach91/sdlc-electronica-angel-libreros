from typing import Protocol

from app.models.alert import Alert


class AlertQueryRepository(Protocol):
    """Define las operaciones requeridas para consultar alertas."""

    def list_by_sensor(self, sensor_id: str) -> list[Alert]:
        """Consulta las alertas de un sensor."""
        ...


class AlertService:
    """Consulta las alertas generadas para los sensores."""

    def __init__(self, repository: AlertQueryRepository) -> None:
        self._repository = repository

    def list_by_sensor(self, sensor_id: str) -> list[Alert]:
        """Devuelve las alertas obtenidas del repositorio."""

        return self._repository.list_by_sensor(sensor_id)
