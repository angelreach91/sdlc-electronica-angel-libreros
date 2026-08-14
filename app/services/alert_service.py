from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository


class AlertService:
    """Consulta las alertas generadas para los sensores."""

    def __init__(self, repository: AlertRepository) -> None:
        self._repository = repository

    def list_by_sensor(self, sensor_id: str) -> list[Alert]:
        """Devuelve las alertas obtenidas del repositorio."""

        return self._repository.list_by_sensor(sensor_id)
