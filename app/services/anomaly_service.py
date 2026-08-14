import logging
from datetime import datetime
from typing import Protocol

from app.models.alert import Alert
from app.models.reading import Reading

logger = logging.getLogger(__name__)


class ThresholdSensor(Protocol):
    """Contrato mínimo de un sensor con threshold configurable."""

    id: str
    threshold: float | None


class SensorThresholdRepository(Protocol):
    """Contrato para consultar sensores con threshold."""

    def get_by_id(self, sensor_id: str) -> ThresholdSensor | None:
        """Busca un sensor mediante su identificador."""
        ...


class AlertRepository(Protocol):
    """Contrato para guardar alertas."""

    def add(self, alert: Alert) -> Alert:
        """Guarda y devuelve una alerta."""
        ...


class NotificationStrategy(Protocol):
    """Contrato sustituible para notificar alertas."""

    def notify(self, alert: Alert) -> None:
        """Notifica una alerta."""
        ...


class LoggingNotificationStrategy:
    """Notifica alertas mediante el sistema estándar de logging."""

    def notify(self, alert: Alert) -> None:
        """Registra los datos que identifican la alerta."""

        logger.info(
            "Anomaly alert sensor_id=%s reading_id=%s value=%s threshold=%s",
            alert.sensor_id,
            alert.reading_id,
            alert.value,
            alert.threshold,
        )


class Clock(Protocol):
    """Contrato para obtener la fecha actual."""

    def __call__(self) -> datetime:
        """Devuelve la fecha actual."""
        ...


class AnomalyService:
    """Evalúa lecturas almacenadas y genera alertas por threshold."""

    def __init__(
        self,
        sensor_repository: SensorThresholdRepository,
        alert_repository: AlertRepository,
        notification_strategy: NotificationStrategy,
        clock: Clock,
    ) -> None:
        self._sensor_repository = sensor_repository
        self._alert_repository = alert_repository
        self._notification_strategy = notification_strategy
        self._clock = clock

    def evaluate(self, reading: Reading) -> Alert | None:
        """Genera una alerta cuando la lectura supera el threshold."""

        sensor = self._sensor_repository.get_by_id(reading.sensor_id)

        if sensor is None or sensor.threshold is None:
            return None

        threshold = sensor.threshold

        if reading.value <= threshold:
            return None

        alert = Alert(
            sensor_id=reading.sensor_id,
            reading_id=reading.id,
            value=reading.value,
            threshold=threshold,
            created_at=self._clock(),
        )
        saved_alert = self._alert_repository.add(alert)
        self._notification_strategy.notify(saved_alert)

        return saved_alert
